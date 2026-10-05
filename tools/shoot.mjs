/**
 * Скриншоты и проверка интерактива через Chrome DevTools Protocol.
 *
 * Примеры:
 *   node tools/shoot.mjs --page index.html --name index --width 1440
 *   node tools/shoot.mjs --page index.html --name mobile --mobile
 *   node tools/shoot.mjs --page catalog.html --name catalog-filter \
 *        --eval "document.querySelector('[data-filter=kompleks]').click()"
 *
 * Полноэкранный PNG кладётся в .tmp/shots/<name>.png
 */
import { spawn } from 'node:child_process';
import { mkdirSync, rmSync, writeFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const SHOTS = path.join(ROOT, '.tmp', 'shots');
mkdirSync(SHOTS, { recursive: true });

function arg(name, def = null) {
  const i = process.argv.indexOf('--' + name);
  if (i === -1) return def;
  const next = process.argv[i + 1];
  if (next === undefined || next.startsWith('--')) return true;
  return next;
}

const page = arg('page', 'index.html');
const name = arg('name', page.replace('.html', ''));
const width = parseInt(arg('width', '1440'), 10);
const height = parseInt(arg('height', '1000'), 10);
const mobile = !!arg('mobile', false);
const evalJs = arg('eval', null);
const wait = parseInt(arg('wait', '700'), 10);

class CDP {
  constructor(ws) {
    this.ws = ws;
    this.id = 0;
    this.pending = new Map();
    this.handlers = new Set();
    ws.addEventListener('message', (ev) => {
      const msg = JSON.parse(ev.data);
      if (msg.id && this.pending.has(msg.id)) {
        const { resolve, reject } = this.pending.get(msg.id);
        this.pending.delete(msg.id);
        msg.error ? reject(new Error(JSON.stringify(msg.error))) : resolve(msg.result);
      } else if (msg.method) {
        this.handlers.forEach((h) => h(msg));
      }
    });
  }
  send(method, params = {}, sessionId) {
    const id = ++this.id;
    this.ws.send(JSON.stringify({ id, method, params, sessionId }));
    return new Promise((resolve, reject) => this.pending.set(id, { resolve, reject }));
  }
  once(method) {
    return new Promise((resolve) => {
      const handler = (msg) => {
        if (msg.method === method) {
          this.handlers.delete(handler);
          resolve(msg);
        }
      };
      this.handlers.add(handler);
    });
  }
}

const profile = path.join(ROOT, '.tmp', 'cdp-' + name);
rmSync(profile, { recursive: true, force: true });
const home = path.join(ROOT, '.tmp', 'home-cdp');
mkdirSync(home, { recursive: true });

const chrome = spawn(CHROME, [
  '--headless=old', '--no-sandbox', '--disable-gpu',
  '--disable-crash-reporter', '--disable-breakpad', '--no-first-run',
  '--hide-scrollbars', '--remote-debugging-port=0',
  '--user-data-dir=' + profile, 'about:blank',
], { env: { ...process.env, HOME: home }, stdio: ['ignore', 'pipe', 'pipe'] });

const wsUrl = await new Promise((resolve, reject) => {
  let buffer = '';
  const timer = setTimeout(() => reject(new Error('не дождались DevTools-порта')), 30000);
  chrome.stderr.on('data', (chunk) => {
    buffer += chunk.toString();
    const m = buffer.match(/DevTools listening on (ws:\/\/\S+)/);
    if (m) { clearTimeout(timer); resolve(m[1]); }
  });
});

let failed = false;
try {
  const ws = new WebSocket(wsUrl);
  await new Promise((res, rej) => {
    ws.addEventListener('open', res, { once: true });
    ws.addEventListener('error', rej, { once: true });
  });
  const cdp = new CDP(ws);
  const target = await cdp.send('Target.createTarget', { url: 'about:blank' });
  const { sessionId } = await cdp.send('Target.attachToTarget', { targetId: target.targetId, flatten: true });

  await cdp.send('Page.enable', {}, sessionId);
  await cdp.send('Runtime.enable', {}, sessionId);
  const pageErrors = [];
  cdp.handlers.add((msg) => {
    if (msg.method === 'Runtime.exceptionThrown') {
      const d = msg.params.exceptionDetails;
      pageErrors.push((d.exception && d.exception.description) || d.text);
    }
  });
  await cdp.send('Emulation.setDeviceMetricsOverride', {
    width, height, deviceScaleFactor: mobile ? 2 : 1, mobile: !!mobile,
  }, sessionId);

  const loaded = cdp.once('Page.loadEventFired');
  const pageUrl = /^https?:\/\//.test(page) ? page : 'file://' + path.join(ROOT, page);
  await cdp.send('Page.navigate', { url: pageUrl }, sessionId);
  await loaded;
  await new Promise((r) => setTimeout(r, wait));

  if (evalJs) {
    const result = await cdp.send('Runtime.evaluate', {
      expression: evalJs, returnByValue: true, awaitPromise: true,
    }, sessionId);
    if (result.exceptionDetails) {
      console.error('eval ✗', (result.exceptionDetails.exception || {}).description || result.exceptionDetails.text);
    } else {
      const value = result.result && result.result.value;
      console.log('eval →', typeof value === 'object' ? JSON.stringify(value) : value);
    }
    await new Promise((r) => setTimeout(r, 500));
  }

  // разворачиваем вьюпорт на всю высоту страницы: так срабатывают resize/scroll
  // и становятся видимыми блоки с анимацией появления
  let metrics = await cdp.send('Page.getLayoutMetrics', {}, sessionId);
  const fullHeight = Math.min(Math.ceil(metrics.cssContentSize.height) + 40, 30000);
  await cdp.send('Emulation.setDeviceMetricsOverride', {
    width, height: fullHeight, deviceScaleFactor: mobile ? 2 : 1, mobile: !!mobile,
  }, sessionId);
  await cdp.send('Runtime.evaluate', {
    expression: 'window.dispatchEvent(new Event("resize")); window.dispatchEvent(new Event("scroll"));',
  }, sessionId);
  await new Promise((r) => setTimeout(r, 900));

  metrics = await cdp.send('Page.getLayoutMetrics', {}, sessionId);
  const shot = await cdp.send('Page.captureScreenshot', {
    format: 'png', captureBeyondViewport: true, fromSurface: true,
  }, sessionId);
  if (pageErrors.length) console.error('ошибки страницы:\n  ' + pageErrors.join('\n  '));
  const out = path.join(SHOTS, name + '.png');
  writeFileSync(out, Buffer.from(shot.data, 'base64'));
  console.log('%s → %dx%d (страница %dx%d)',
    path.relative(ROOT, out), width, height,
    Math.round(metrics.cssContentSize.width), Math.round(metrics.cssContentSize.height));
} catch (err) {
  failed = true;
  console.error('Ошибка:', err.message);
} finally {
  chrome.kill('SIGKILL');
  rmSync(profile, { recursive: true, force: true });
}
process.exit(failed ? 1 : 0);
