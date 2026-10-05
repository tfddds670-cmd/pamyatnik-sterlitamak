# -*- coding: utf-8 -*-
"""
Скриншоты страниц для визуальной проверки.

Запуск:  python3 tools/shoot.py index.html [--height 9000] [--slice 1500]
Кладёт PNG в .tmp/shots/ и нарезает длинную страницу на части.
Chrome запускается в режиме --headless=old и с --no-sandbox: так он работает
внутри файловой песочницы DSH.
"""
import os
import shutil
import subprocess
import sys

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
TMP = os.path.join(ROOT, ".tmp")
SHOTS = os.path.join(TMP, "shots")
os.makedirs(SHOTS, exist_ok=True)


def capture(page, height=9000, width=1440, name=None, budget=2500):
    name = name or page.replace(".html", "")
    out = os.path.join(SHOTS, name + ".png")
    url = "file://" + os.path.join(ROOT, page)
    profile = os.path.join(TMP, "prof-" + name)
    home = os.path.join(TMP, "home-" + name)
    shutil.rmtree(profile, ignore_errors=True)
    os.makedirs(home, exist_ok=True)
    cmd = [
        CHROME, "--headless=old", "--no-sandbox", "--disable-gpu",
        "--disable-crash-reporter", "--disable-breakpad", "--no-first-run",
        "--hide-scrollbars", "--force-device-scale-factor=1",
        "--force-prefers-reduced-motion",
        "--user-data-dir=" + profile, "--virtual-time-budget=%d" % budget,
        "--screenshot=" + out, "--window-size=%d,%d" % (width, height), url,
    ]
    proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                            env=dict(os.environ, HOME=home))
    try:
        proc.wait(timeout=60)
    except subprocess.TimeoutExpired:
        proc.kill()
    shutil.rmtree(profile, ignore_errors=True)
    if not os.path.exists(out):
        raise SystemExit("Chrome не сделал скриншот: " + page)
    return out


def cut(png, slice_h=1500, keep=99):
    im = Image.open(png).convert("RGB")
    w, h = im.size
    n = min(keep, max(1, (h + slice_h - 1) // slice_h))
    base = png[:-4]
    paths = []
    for i in range(n):
        top = i * slice_h
        box = (0, top, w, min(top + slice_h, h))
        part = im.crop(box)
        path = "%s-%02d.png" % (base, i + 1)
        part.save(path)
        paths.append(path)
    print("%s: %dx%d → %d частей" % (os.path.basename(png), w, h, len(paths)))
    for p in paths:
        print("  ", os.path.relpath(p, ROOT))
    return paths


if __name__ == "__main__":
    def arg(flag, default, cast=int):
        return cast(sys.argv[sys.argv.index(flag) + 1]) if flag in sys.argv else default

    page = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else "index.html"
    name = sys.argv[sys.argv.index("--name") + 1] if "--name" in sys.argv else None
    cut(capture(page, height=arg("--height", 9000), width=arg("--width", 1440), name=name),
        slice_h=arg("--slice", 1500), keep=arg("--keep", 99))
