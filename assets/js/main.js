/* ==========================================================================
   «Вечная память» — интерактив сайта
   Без внешних зависимостей. Формы работают как демо: данные никуда не уходят,
   точки подключения к бэкенду помечены комментарием BACKEND.
   ========================================================================== */
(function () {
  'use strict';

  /* Адрес обработчика заявок. Укажите свой, например:
     '/send.php'  или  'https://formspree.io/f/xxxxxxx'.
     Пока строка пустая — формы работают в демонстрационном режиме:
     данные никуда не отправляются, а только пишутся в консоль. */
  var LEAD_ENDPOINT = '';

  var $  = function (sel, ctx) { return (ctx || document).querySelector(sel); };
  var $$ = function (sel, ctx) { return Array.prototype.slice.call((ctx || document).querySelectorAll(sel)); };

  /* ------------------------------- шапка ---------------------------------- */
  var header = $('.header');
  var toTop  = $('.fab__top');

  // страховка: любая неожиданная ошибка не должна ломать остальной интерактив
  window.addEventListener('error', function (e) { console.warn('[site] ошибка:', e.message); });

  function onScroll() {
    var y = window.pageYOffset || document.documentElement.scrollTop;
    if (header) header.classList.toggle('is-stuck', y > 8);
    if (toTop) toTop.classList.toggle('is-visible', y > 700);
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  if (toTop) {
    toTop.addEventListener('click', function () {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  /* --------------------------- мобильное меню ----------------------------- */
  var burger = $('.burger');
  var mobileNav = $('.mobile-nav');
  var overlay = $('.overlay');

  function setMenu(open) {
    if (!mobileNav) return;
    mobileNav.classList.toggle('is-open', open);
    if (overlay) overlay.classList.toggle('is-open', open);
    if (burger) burger.classList.toggle('is-open', open);
    document.body.classList.toggle('is-locked', open);
  }

  if (burger) burger.addEventListener('click', function () { setMenu(!mobileNav.classList.contains('is-open')); });
  if (overlay) overlay.addEventListener('click', function () { setMenu(false); });
  var closeBtn = $('.mobile-nav__close');
  if (closeBtn) closeBtn.addEventListener('click', function () { setMenu(false); });
  $$('.mobile-nav__list a').forEach(function (a) { a.addEventListener('click', function () { setMenu(false); }); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') { setMenu(false); closeModal(); closeLightbox(); } });

  /* --------------------------------- FAQ ---------------------------------- */
  $$('.faq__item').forEach(function (item) {
    var q = $('.faq__q', item);
    var a = $('.faq__a', item);
    if (!q || !a) return;
    q.addEventListener('click', function () {
      var isOpen = item.classList.contains('is-open');
      $$('.faq__item.is-open').forEach(function (other) {
        if (other !== item) {
          other.classList.remove('is-open');
          $('.faq__a', other).style.maxHeight = '';
          $('.faq__q', other).setAttribute('aria-expanded', 'false');
        }
      });
      item.classList.toggle('is-open', !isOpen);
      a.style.maxHeight = isOpen ? '' : a.scrollHeight + 'px';
      q.setAttribute('aria-expanded', String(!isOpen));
    });
  });

  /* ------------------------------ фильтры --------------------------------- */
  var filterBar = $('[data-filters]');
  if (filterBar) {
    var chips = $$('.chip[data-filter]', filterBar);
    var search = $('[data-search]', filterBar);
    var counter = $('[data-count]', filterBar);
    var items = $$('[data-item]');
    var empty = $('.empty-state');
    var active = 'all';

    function applyFilters() {
      var q = (search && search.value || '').trim().toLowerCase();
      var shown = 0;
      items.forEach(function (item) {
        var cats = (item.getAttribute('data-category') || '').split(/\s+/);
        var okCat = active === 'all' || cats.indexOf(active) !== -1;
        var okText = !q || (item.textContent || '').toLowerCase().indexOf(q) !== -1;
        var show = okCat && okText;
        item.style.display = show ? '' : 'none';
        if (show) shown++;
      });
      if (counter) counter.textContent = 'Показано: ' + shown;
      if (empty) empty.style.display = shown ? 'none' : '';
    }

    chips.forEach(function (chip) {
      chip.addEventListener('click', function () {
        chips.forEach(function (c) { c.classList.remove('is-checked'); });
        chip.classList.add('is-checked');
        active = chip.getAttribute('data-filter');
        applyFilters();
      });
    });
    if (search) search.addEventListener('input', applyFilters);
    applyFilters();
  }

  /* ---------------------------- калькулятор ------------------------------- */
  var calc = $('[data-calc]');
  if (calc) {
    var BASE = 34900;
    var outSum = $('[data-calc-sum]', calc);
    var outList = $('[data-calc-list]', calc);

    function fmt(n) { return String(Math.round(n / 100) * 100).replace(/\B(?=(\d{3})+(?!\d))/g, ' '); }

    function groupValue(group) {
      var inputs = $$('[data-calc-group="' + group + '"]', calc);
      return inputs.filter(function (i) { return i.checked || i.selected; });
    }

    // подсветка выбранных вариантов: и радиогруппы (тип, материал, размер),
    // и группы с множественным выбором (оформление, благоустройство)
    function syncChips() {
      $$('.chip', calc).forEach(function (chip) {
        var input = $('input', chip);
        if (input) chip.classList.toggle('is-checked', !!input.checked);
      });
    }

    function recalc() {
      var mult = 1, add = 0;
      var lines = ['Базовый памятник (стела 100×50, габбро-диабаз)', ''];

      syncChips();

      ['type', 'material', 'size'].forEach(function (group) {
        var picked = groupValue(group)[0];
        if (!picked) return;
        var m = parseFloat(picked.getAttribute('data-mult') || '1');
        mult *= m;
        lines[0] = group === 'type' ? (picked.getAttribute('data-title') || lines[0]) : lines[0];
        if (group === 'material') lines[0] += ', ' + (picked.getAttribute('data-title') || '');
        var d = picked.getAttribute('data-delta');
        if (d) lines.push(d);
      });

      var total = BASE * mult;

      $$('[data-calc-group="extra"], [data-calc-group="blago"]', calc).forEach(function (input) {
        if (input.checked) {
          var price = parseFloat(input.getAttribute('data-add') || '0');
          add += price;
          lines.push((input.getAttribute('data-title') || 'Опция') + ' — ' + fmt(price) + ' ₽');
        }
      });

      total += add;

      if (outSum) outSum.innerHTML = 'от ' + fmt(total) + ' <span style="font-size:.6em">₽</span>';
      if (outList) {
        outList.innerHTML = lines.filter(Boolean).map(function (line, i) {
          return '<li>' + line + (i === 0 ? '<b>' + fmt(BASE * mult) + ' ₽</b>' : '') + '</li>';
        }).join('') + '<li style="border-top:1px solid rgba(255,255,255,.12);margin-top:8px;padding-top:10px">' +
          'Установка и доставка по Стерлитамаку<b>бесплатно</b></li>';
      }
      var hidden = $('[data-calc-input]', calc);
      if (hidden) hidden.value = 'Предварительный расчёт: от ' + fmt(total) + ' ₽';
    }

    calc.addEventListener('change', recalc);
    calc.addEventListener('input', recalc);
    $$('.chip', calc).forEach(function (chip) {
      var input = $('input', chip);
      if (!input) return;
      chip.addEventListener('click', function () { setTimeout(recalc, 0); });
      chip.classList.toggle('is-checked', !!input.checked);
    });
    recalc();
  }

  /* ------------------------------- галерея -------------------------------- */
  var lb = $('.lightbox');
  if (lb) {
    var lbImg = $('img', lb);
    var lbCap = $('.lightbox__caption', lb);
    var shots = $$('.gallery__item');
    var index = 0;

    function show(i) {
      if (!shots.length) return;
      index = (i + shots.length) % shots.length;
      var shot = shots[index];
      var img = $('img', shot);
      lbImg.src = shot.getAttribute('data-full') || (img && img.src) || '';
      lbImg.alt = (img && img.alt) || '';
      lbCap.textContent = shot.getAttribute('data-caption') || '';
      lb.classList.add('is-open');
      document.body.classList.add('is-locked');
    }

    shots.forEach(function (shot, i) {
      shot.addEventListener('click', function () { show(i); });
    });
    var nextBtn = $('.lightbox__nav--next', lb);
    var prevBtn = $('.lightbox__nav--prev', lb);
    var closeLb = $('.lightbox__close', lb);
    if (nextBtn) nextBtn.addEventListener('click', function (e) { e.stopPropagation(); show(index + 1); });
    if (prevBtn) prevBtn.addEventListener('click', function (e) { e.stopPropagation(); show(index - 1); });
    if (closeLb) closeLb.addEventListener('click', closeLightbox);
    lb.addEventListener('click', function (e) { if (e.target === lb) closeLightbox(); });
    document.addEventListener('keydown', function (e) {
      if (!lb.classList.contains('is-open')) return;
      if (e.key === 'ArrowRight') show(index + 1);
      if (e.key === 'ArrowLeft') show(index - 1);
    });
  }

  function closeLightbox() {
    if (!lb) return;
    lb.classList.remove('is-open');
    document.body.classList.remove('is-locked');
  }

  /* ------------------------------- модалка -------------------------------- */
  var modal = $('.modal');

  function openModal(source) {
    if (!modal) return;
    if (source) {
      var topic = $('[data-modal-topic]', modal);
      if (topic) topic.value = source;
      var title = $('[data-modal-title]', modal);
      if (title && source) title.textContent = 'Заявка: ' + source;
    }
    modal.classList.add('is-open');
    document.body.classList.add('is-locked');
    var first = $('input[name="name"]', modal);
    if (first) setTimeout(function () { first.focus(); }, 60);
  }

  function closeModal() {
    if (!modal) return;
    modal.classList.remove('is-open');
    document.body.classList.remove('is-locked');
  }

  $$('[data-open-modal]').forEach(function (btn) {
    btn.addEventListener('click', function (e) {
      e.preventDefault();
      openModal(btn.getAttribute('data-open-modal') || '');
    });
  });
  var mc = $('.modal__close');
  if (mc) mc.addEventListener('click', closeModal);
  if (modal) modal.addEventListener('click', function (e) { if (e.target === modal) closeModal(); });

  /* ------------------------------ формы/маска ----------------------------- */
  function maskPhone(input) {
    input.addEventListener('input', function () {
      var digits = input.value.replace(/\D/g, '');
      if (digits[0] === '8') digits = '7' + digits.slice(1);
      if (digits[0] !== '7') digits = '7' + digits;
      digits = digits.slice(0, 11);
      var out = '+7';
      if (digits.length > 1) out += ' (' + digits.slice(1, 4);
      if (digits.length >= 4) out += ') ' + digits.slice(4, 7);
      if (digits.length >= 7) out += '-' + digits.slice(7, 9);
      if (digits.length >= 9) out += '-' + digits.slice(9, 11);
      input.value = out;
    });
  }
  $$('input[type="tel"]').forEach(maskPhone);

  function toast(message) {
    var el = $('.toast');
    if (!el) return;
    el.textContent = message;
    el.classList.add('is-visible');
    clearTimeout(el._t);
    el._t = setTimeout(function () { el.classList.remove('is-visible'); }, 4200);
  }

  $$('form[data-lead]').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var ok = true;
      $$('[required]', form).forEach(function (input) {
        var bad = input.type === 'checkbox' ? !input.checked : !input.value.trim();
        if (input.type === 'tel') bad = input.value.replace(/\D/g, '').length < 11;
        input.classList.toggle('is-error', bad);
        if (bad) ok = false;
      });
      if (!ok) { toast('Проверьте, пожалуйста, выделенные поля'); return; }

      var data = {};
      new FormData(form).forEach(function (v, k) { data[k] = v; });
      data.page = window.location.pathname;
      data.sentAt = new Date().toISOString();

      if (LEAD_ENDPOINT) {
        // отправляем заявку на сервер; ответ не блокирует интерфейс
        fetch(LEAD_ENDPOINT, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(data),
        }).catch(function (err) { console.warn('[site] заявку не удалось отправить:', err); });
      } else {
        console.log('[демо] заявка (обработчик не подключён):', data);
      }

      form.reset();
      $$('.chip', form).forEach(function (c) { c.classList.remove('is-checked'); });
      closeModal();
      toast('Заявка принята. Перезвоним в течение 15 минут.');
    });
  });

  /* ------------------------------- анимации ------------------------------- */
  var revealEls = $$('.reveal');
  if (revealEls.length) {
    var revealCheck = function () {
      var limit = window.innerHeight * 0.94;
      revealEls.forEach(function (el) {
        if (el.classList.contains('is-in')) return;
        var box = el.getBoundingClientRect();
        if (box.top < limit && box.bottom > -160) el.classList.add('is-in');
      });
    };

    if ('IntersectionObserver' in window) {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-in');
            io.unobserve(entry.target);
          }
        });
      }, { rootMargin: '0px 0px -8% 0px', threshold: 0.05 });
      revealEls.forEach(function (el) { io.observe(el); });
    }

    // страховка: показываем блоки, которые уже в зоне видимости
    revealCheck();
    window.addEventListener('load', revealCheck);
    window.addEventListener('scroll', revealCheck, { passive: true });
    window.addEventListener('resize', revealCheck);
    setTimeout(revealCheck, 250);
    setTimeout(revealCheck, 900);
  }

  /* --------------------------- год в подвале ------------------------------ */
  $$('[data-year]').forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();
