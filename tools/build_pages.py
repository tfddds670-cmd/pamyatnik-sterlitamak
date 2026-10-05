# -*- coding: utf-8 -*-
"""
Сборка статических страниц сайта «Вечная память» (Стерлитамак).

Шапка, подвал, модальное окно и служебная разметка описаны здесь один раз,
поэтому правки в них достаточно делать в одном месте. На выходе — обычные
HTML-файлы, которые можно открыть без сервера и править руками.

Запуск:  python3 tools/build_pages.py
"""
import os
import json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# --------------------------------------------------------------------------
# Контакты и реквизиты  (ЗАМЕНИТЕ на реальные)
# --------------------------------------------------------------------------
SITE = {
    "name": "Вечная память",
    "legal": "Ритуальная мастерская «Вечная память»",
    "tagline": "Ритуальная мастерская",
    "city": "Стерлитамак",
    "phone": "+7 (3473) 00-00-00",
    "phone_href": "tel:+73473000000",
    "phone2": "+7 (917) 000-00-00",
    "phone2_href": "tel:+79170000000",
    "hours": "Ежедневно 8:00–20:00",
    "email": "zakaz@vechnaya-pamyat.ru",
    "address": "г. Стерлитамак, ул. Строителей, 00, офис 1",
    "address_short": "ул. Строителей, 00",
    "map_link": "https://yandex.ru/maps/?text=Стерлитамак%20ул.%20Строителей",
    "vk": "https://vk.com/",
    "tg": "https://t.me/",
    "wa": "https://wa.me/79170000000",
    "inn": "ИНН 000000000000 · ОГРНИП 000000000000000",
}

NAV = [
    ("index.html", "Главная"),
    ("catalog.html", "Каталог"),
    ("uslugi.html", "Услуги"),
    ("tovary.html", "Венки"),
    ("raboty.html", "Работы"),
    ("ceny.html", "Цены"),
    ("kontakty.html", "Контакты"),
]

# --------------------------------------------------------------------------
# Иконки (инлайновые SVG, обводка)
# --------------------------------------------------------------------------
def ic(path, box="0 0 24 24"):
    return '<svg class="i" viewBox="%s" aria-hidden="true">%s</svg>' % (box, path)


I = {
    "phone": ic('<path d="M6.5 3h3l1.5 4-2 1.5a12 12 0 0 0 6 6L16.5 12l4 1.5v3a2 2 0 0 1-2.2 2A17 17 0 0 1 4.5 5.2 2 2 0 0 1 6.5 3Z"/>'),
    "clock": ic('<circle cx="12" cy="12" r="9"/><path d="M12 7v5.2l3.2 2"/>'),
    "pin": ic('<path d="M12 21.5s7-6.6 7-11.5a7 7 0 1 0-14 0c0 4.9 7 11.5 7 11.5Z"/><circle cx="12" cy="10" r="2.6"/>'),
    "mail": ic('<rect x="3" y="5" width="18" height="14" rx="2.5"/><path d="m3.8 7.2 8.2 6 8.2-6"/>'),
    "shield": ic('<path d="M12 3l7.5 3v6.2c0 4.6-3.2 7.9-7.5 9.3-4.3-1.4-7.5-4.7-7.5-9.3V6L12 3Z"/><path d="m8.8 12.2 2.2 2.2 4.4-4.6"/>'),
    "percent": ic('<path d="M19 5 5 19"/><circle cx="7.6" cy="7.6" r="2.6"/><circle cx="16.4" cy="16.4" r="2.6"/>'),
    "factory": ic('<path d="M4 20V10l5 3V10l5 3V6l6 3v11H4Z"/><path d="M7.5 20v-3.5h3V20"/>'),
    "ruler": ic('<rect x="2.5" y="8" width="19" height="8" rx="2"/><path d="M7 8v3.2M11 8v4.4M15 8v3.2M19 8v4.4"/>'),
    "truck": ic('<path d="M3 6.5h11v10H3z"/><path d="M14 10h3.6l3.4 3.4v3.1h-7z"/><circle cx="7" cy="18.4" r="1.9"/><circle cx="17" cy="18.4" r="1.9"/>'),
    "doc": ic('<path d="M14 3.2H7.5a2 2 0 0 0-2 2v13.6a2 2 0 0 0 2 2h9a2 2 0 0 0 2-2V8.2l-4.5-5Z"/><path d="M14 3.2v5h4.5"/><path d="M9 13h6M9 16.5h4"/>'),
    "chat": ic('<path d="M20.5 11.8a7.8 7.8 0 0 1-11.3 7L4 20.5l1.8-5.2a7.8 7.8 0 1 1 14.7-3.5Z"/>'),
    "star": ic('<path d="m12 3.4 2.6 5.5 6 .8-4.4 4.2 1.1 6-5.3-2.9-5.3 2.9 1.1-6L3.4 9.7l6-.8L12 3.4Z"/>'),
    "leaf": ic('<path d="M20 4c-8 0-13 3.4-13 9a5 5 0 0 0 1.6 3.7C11 13.4 14.6 11 19 10c-2.6 2-4.8 4.3-6.2 7.4A5.6 5.6 0 0 0 16 18c4 0 6-3.6 6-9 0-2-.7-3.8-2-5Z"/>'),
    "tools": ic('<path d="M4.5 20.5 12 13"/><path d="M14.2 3.6 20.4 9.8l-3.6 3.6-6.2-6.2 3.6-3.6Z"/><path d="m4.5 15.5 4 4"/>'),
    "check": ic('<path d="m5 12.5 4.5 4.5L19 7.5"/>'),
    "arrow": ic('<path d="M5 12h13.5"/><path d="m13.5 6.5 5.5 5.5-5.5 5.5"/>'),
    "calc": ic('<rect x="4.5" y="2.8" width="15" height="18.4" rx="2.5"/><path d="M8 7h8M8 11.5h3M8 15.5h3M13 11.5h3M13 15.5h3"/>'),
    "cash": ic('<rect x="2.5" y="6" width="19" height="12" rx="2.5"/><circle cx="12" cy="12" r="2.6"/><path d="M6 9.5v5M18 9.5v5"/>'),
    "user": ic('<circle cx="12" cy="8.4" r="3.9"/><path d="M4.8 20.2a7.4 7.4 0 0 1 14.4 0"/>'),
}

SOCIALS = {
    "vk": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12.9 17.1c-6 0-9.4-4.1-9.5-11h3c.1 5.1 2.3 7.3 4.1 7.7V6.1h2.8v4.4c1.7-.2 3.5-2.2 4.1-4.4h2.8c-.5 2.7-2.4 4.7-3.8 5.5 1.4.7 3.6 2.4 4.4 5.5h-3.1c-.6-2-2.2-3.5-4.4-3.8v3.8h-.4Z"/></svg>',
    "tg": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M21.6 4.3 2.9 11.5c-.9.4-.9 1.6.1 1.9l4.4 1.4 1.7 5.2c.3.9 1.4 1.1 2 .4l2.4-2.5 4.5 3.3c.7.5 1.7.1 1.9-.8l3-14.4c.2-1-.8-1.9-1.7-1.7ZM9.4 14.3l8-5.2-6.5 6.2-.3 3.2-1.2-4.2Z"/></svg>',
    "wa": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2.2A9.7 9.7 0 0 0 3.6 16.8L2.2 21.8l5.1-1.3A9.7 9.7 0 1 0 12 2.2Zm5 13.6c-.2.6-1.2 1.2-1.7 1.3-.5.1-1 .1-1.7-.1-.4-.1-1-.3-1.7-.6-2.9-1.3-4.8-4.3-5-4.5-.2-.2-1.2-1.6-1.2-3s.7-2.1 1-2.4c.3-.3.6-.4.8-.4h.6c.2 0 .4 0 .7.5l.9 2.1c.1.2.1.4 0 .5l-.4.5c-.1.2-.3.3-.1.6.2.3.7 1.1 1.4 1.8 1 .9 1.8 1.2 2.1 1.3.3.1.4.1.6-.1l.7-.8c.2-.2.4-.2.6-.1l2 1c.3.1.4.2.5.3.1.2.1.8-.1 1.4Z"/></svg>',
}

# --------------------------------------------------------------------------
# Карточки каталога
# --------------------------------------------------------------------------
CATEGORIES = [
    ("all", "Все"),
    ("granit", "Гранитные"),
    ("kompleks", "Комплексы"),
    ("mramor", "Мраморные"),
    ("dvojnoj", "Двойные"),
    ("detskij", "Детские"),
    ("musulmanskij", "Мусульманские"),
    ("pravoslav", "Православные"),
    ("svo", "Участникам СВО"),
]

CATALOG = [
    dict(name="Памятник «Классика»", cats=["granit"], price=34900, img="pamyatnik-klassika.svg",
         tag="Хит продаж", meta="Габбро-диабаз · стела 100×50×8 см",
         specs=["Стела из габбро-диабаза 100×50×8 см", "Тумба 60×20×15 см, цветник 90×50 см",
                "Портрет и текст — по желанию"]),
    dict(name="Памятник «Волна» фигурный", cats=["granit"], price=39500, img="pamyatnik-volna.svg",
         tag="", meta="Серый гранит · стела 110×50×8 см",
         specs=["Фигурная стела с волнообразным верхом", "Гранит «Мансуровский» серый",
                "Полировка всех сторон"]),
    dict(name="Памятник «Православный» с крестом", cats=["granit", "pravoslav"], price=36000,
         img="pamyatnik-krest.svg", tag="", meta="Габбро-диабаз · стела 100×50×8 см",
         specs=["Православный крест с Голгофой", "Стела, тумба, цветник", "Возможна эпитафия и даты"]),
    dict(name="Памятник «Мусульманский»", cats=["granit", "musulmanskij"], price=31000,
         img="pamyatnik-musulmanskij.svg", tag="", meta="Зелёный гранит · стела 100×50×8 см",
         specs=["Полумесяц и звезда в гравировке", "Арабская вязь по желанию", "Тумба и цветник"]),
    dict(name="Детский памятник «Сердце»", cats=["detskij"], price=24500, img="pamyatnik-detskij.svg",
         tag="", meta="Серый гранит · стела 80×40×7 см",
         specs=["Форма сердца, деликатная гравировка", "Небольшие размеры 80×40 см",
                "Ангел или голубь — на выбор"]),
    dict(name="Памятник «Ангел» резной", cats=["granit"], price=58000, img="pamyatnik-angel.svg",
         tag="Эксклюзив", meta="Габбро-диабаз · стела 120×60×8 см",
         specs=["Ручная объёмная резка фигуры ангела", "Индивидуальный эскиз и 3D-макет",
                "Срок изготовления 14–21 день"]),
    dict(name="Памятник «Семейный» двойной", cats=["dvojnoj", "granit"], price=62000,
         img="pamyatnik-dvojnoj.svg", tag="", meta="Дымовский гранит · 2 стелы 100×50 см",
         specs=["Две стелы на общем основании", "Ширина комплекта 160 см", "Два портрета и текста"]),
    dict(name="Мраморный памятник «Арка»", cats=["mramor"], price=27000, img="pamyatnik-mramor.svg",
         tag="", meta="Мрамор · стела 100×50×8 см",
         specs=["Белый мрамор с арочным верхом", "Классическая форма", "Лёгкий и бюджетный вариант"]),
    dict(name="Памятник из красного гранита", cats=["granit"], price=44000, img="pamyatnik-krasnyj.svg",
         tag="", meta="Красный гранит · стела 110×50×8 см",
         specs=["Гранит «Лезниковский» красный", "Насыщенный цвет не выгорает", "Тумба и цветник в комплекте"]),
    dict(name="Памятник горизонтальный (плита)", cats=["granit"], price=42000,
         img="pamyatnik-gorizontalnyj.svg", tag="", meta="Габбро-диабаз · плита 120×60×8 см",
         specs=["Лежачая плита на основании", "Традиция для мусульманских захоронений",
                "Гравировка сверху"]),
    dict(name="Мемориальный комплекс «Православный»", cats=["kompleks", "pravoslav"], price=96000,
         img="kompleks-pravoslavnyj.svg", tag="Под ключ", meta="Стела 120×60, плитка 2×1,5 м",
         specs=["Стела, тумба, крест, оградка", "Облицовка плиткой 2×1,5 м",
                "Установка, отсыпка, уборка — включены"]),
    dict(name="Мемориальный комплекс «Семейный»", cats=["kompleks", "dvojnoj"], price=132000,
         img="kompleks-semejnyj.svg", tag="", meta="Две стелы, плитка 2×2 м, оградка",
         specs=["Двойной комплекс с облицовкой 2×2 м", "Кованая оградка 2×2 м",
                "Стол и скамья — по желанию"]),
    dict(name="Мемориальный комплекс «Элитный»", cats=["kompleks"], price=185000,
         img="kompleks-elitnyj.svg", tag="Премиум", meta="Стела 140×70, скульптура, плитка 2,5×2 м",
         specs=["Скульптура ангела, резной декор", "Гранитная плитка и цоколь по периметру",
                "Индивидуальный проект"]),
    dict(name="Памятник участнику СВО", cats=["svo", "granit", "pravoslav"], price=48000,
         img="pamyatnik-svo.svg", tag="Льготы", meta="Габбро-диабаз · стела 110×55×8 см",
         specs=["Крест, лампадка, изображение награды", "Помощь в оформлении документов на льготу",
                "Скидка семьям участников СВО — 10%"]),
]

SERVICES = [
    dict(name="Установка памятника", price="от 5 500 ₽", img="usluga-ustanovka.svg",
         text="Монтаж на бетонное основание, армирование, выставление по уровню. Работаем круглый год.",
         specs=["Бетонное основание под памятник", "Гарантия на установку 10 лет", "Выезд мастера — бесплатно"]),
    dict(name="Благоустройство захоронения", price="от 32 000 ₽", img="usluga-plitka.svg",
         text="Облицовка плиткой, цоколь, бордюр, отсыпка цветника, дренаж и подготовка основания.",
         specs=["Гранитная плитка 2×1,5 м — от 32 000 ₽", "Цоколь и бордюр по периметру",
                "Отсыпка камушками, дренаж"]),
    dict(name="Оградки: кованые и сварные", price="от 9 500 ₽", img="usluga-ogradka-kovanaya.svg",
         text="Изготовим оградку по размеру участка: художественная ковка, сварные секции, покраска.",
         specs=["Сварная оградка 2×1 м — от 9 500 ₽", "Кованая оградка — от 18 000 ₽",
                "Стол и скамья в комплект"]),
    dict(name="Гравировка и портреты", price="от 2 500 ₽", img="usluga-gravirovka.svg",
         text="Портрет на металлокерамике или фотокерамике, художественная гравировка, эпитафии.",
         specs=["Портрет 13×18 — от 2 500 ₽", "Художественная гравировка — от 4 500 ₽",
                "Текст: 1 знак — от 40 ₽"]),
    dict(name="Реставрация памятника", price="от 6 000 ₽", img="pamyatnik-klassika.svg",
         text="Выравнивание просевшего основания, чистка гранита, обновление гравировки и покраска.",
         specs=["Выравнивание и подливка основания", "Чистка и полировка стелы",
                "Обновление букв, креста, портрета"]),
    dict(name="Демонтаж и вывоз старого памятника", price="от 4 500 ₽", img="pamyatnik-gorizontalnyj.svg",
         text="Аккуратно демонтируем старый памятник, вывезем и утилизируем по договорённости.",
         specs=["Демонтаж стелы и основания", "Погрузка и вывоз", "Работа с согласованием смотрителя"]),
    dict(name="Уход за захоронением", price="от 1 500 ₽", img="usluga-plitka.svg",
         text="Разовая уборка или годовой абонемент: уборка, уход за гравировкой, посадка, полив.",
         specs=["Разовая уборка — от 1 500 ₽", "Абонемент на год (4 выезда) — от 5 400 ₽",
                "Фотоотчёт после каждого выезда"]),
    dict(name="Замена и ремонт оград", price="от 7 000 ₽", img="usluga-ogradka-svarnaya.svg",
         text="Демонтаж старой оградки, изготовление и установка новой, сварка и покраска секций.",
         specs=["Демонтаж старой оградки", "Изготовление новой по размеру",
                "Покраска и антикоррозийная обработка"]),
]

PRODUCTS = [
    dict(name="Венок «Скорбь»", cats=["venok"], price=1900, img="venok-skorbi.svg", tag="Хит",
         meta="Диаметр 60 см · хвоя и искусственные цветы",
         specs=["Диаметр 60 см", "Двухцветная лента с надписью", "Доставка по городу — 2 часа"]),
    dict(name="Венок «Любимой маме»", cats=["venok"], price=2900, img="venok-mame.svg", tag="",
         meta="Диаметр 80 см · белые и кремовые цветы",
         specs=["Диаметр 80 см", "Лента с индивидуальной надписью", "Устойчивые ножки"]),
    dict(name="Венок «От всех скорбящих»", cats=["venok"], price=2400, img="venok-ot-vseh.svg", tag="",
         meta="Диаметр 70 см · классическая форма",
         specs=["Диаметр 70 см", "Надпись на ленте по желанию", "Подходит для прощания"]),
    dict(name="Венок дубовый", cats=["venok"], price=2100, img="venok-dubovyj.svg", tag="",
         meta="Диаметр 65 см · зелень и хвоя",
         specs=["Дубовые листья и хвоя", "Долго сохраняет вид", "Без надписи или с лентой"]),
    dict(name="Корзина «Печаль»", cats=["korzina"], price=3600, img="korzina-pechal.svg", tag="",
         meta="Высота 60 см · траурная композиция",
         specs=["Плетёная корзина, живые или искусственные цветы", "Лента с надписью",
                "Устанавливается на постамент"]),
    dict(name="Крест деревянный православный", cats=["tovar"], price=1500, img="tovar-krest.svg", tag="",
         meta="Сосна, 120×70 см · с табличкой",
         specs=["Высота 120 см", "Влагостойкая пропитка", "Табличка с именем и датами"]),
    dict(name="Гроб (сосна, обивка)", cats=["tovar"], price=8900, img="tovar-grob.svg", tag="",
         meta="Стандарт / евро · 4 варианта обивки",
         specs=["Лакированная сосна", "Обивка: атлас, бархат, ситец", "Ручки, крест, покрывало в комплекте"]),
    dict(name="Траурная лента с надписью", cats=["tovar"], price=350, img="venok-ot-vseh.svg", tag="",
         meta="Печать золотом по чёрной ленте",
         specs=["Длина 2 м, ширина 12 см", "Печать золотом или серебром", "Изготовление 20 минут"]),
]

# --------------------------------------------------------------------------
# Хелперы разметки
# --------------------------------------------------------------------------
def card(item, tag_class="card"):
    specs = "".join("<li>%s</li>" % s for s in item.get("specs", []))
    specs_html = '<ul class="card__specs">%s</ul>' % specs if specs else ""
    tag = '<span class="card__tag">%s</span>' % item["tag"] if item.get("tag") else ""
    cats = " ".join(item.get("cats", []))
    price = '<div class="price"><span>Цена</span><b>от %s ₽</b></div>' % fnum(item["price"])
    return f'''<article class="{tag_class}" data-item data-category="{cats}">
          <div class="card__media">{tag}<img src="assets/img/{item["img"]}" alt="{item["name"]}" loading="lazy" width="900" height="675"></div>
          <div class="card__body">
            <h3 class="card__title">{item["name"]}</h3>
            <p class="card__meta">{item["meta"]}</p>
            {specs_html}
            <div class="card__foot">
              {price}
              <button class="btn btn--sm" type="button" data-open-modal="{item["name"]}">Заказать</button>
            </div>
          </div>
        </article>'''


def service_card(item):
    specs = "".join("<li>%s</li>" % s for s in item.get("specs", []))
    return f'''<article class="card card--service" data-item>
          <div class="card__media"><img src="assets/img/{item["img"]}" alt="{item["name"]}" loading="lazy" width="900" height="675"></div>
          <div class="card__body">
            <h3 class="card__title">{item["name"]}</h3>
            <p class="card__meta">{item["text"]}</p>
            <ul class="card__specs">{specs}</ul>
            <div class="card__foot">
              <div class="price"><span>Стоимость</span><b>{item["price"]}</b></div>
              <button class="btn btn--sm" type="button" data-open-modal="{item["name"]}">Узнать цену</button>
            </div>
          </div>
        </article>'''


def fnum(n):
    return "{:,}".format(int(n)).replace(",", " ")


def feature(icon, title, text):
    return f'''<article class="feature reveal">
          <div class="feature__icon">{I[icon]}</div>
          <h3>{title}</h3>
          <p>{text}</p>
        </article>'''


def step(title, text):
    return f'''<div class="step reveal"><h3>{title}</h3><p>{text}</p></div>'''


def review(name, meta, text, letter):
    return f'''<article class="review reveal">
          <div class="review__stars" aria-label="Оценка 5 из 5">★★★★★</div>
          <p class="review__text">«{text}»</p>
          <div class="review__author">
            <div class="review__avatar" aria-hidden="true">{letter}</div>
            <div>
              <div class="review__name">{name}</div>
              <div class="review__meta">{meta}</div>
            </div>
          </div>
        </article>'''


def faq_item(q, a, num):
    return f'''<div class="faq__item">
          <button class="faq__q" type="button" aria-expanded="false" aria-controls="faq-a-{num}">{q}<span class="faq__icon" aria-hidden="true">+</span></button>
          <div class="faq__a" id="faq-a-{num}"><div>{a}</div></div>
        </div>'''


def lead_form(prefix, submit="Отправить заявку", note=True, topic=""):
    note_html = ('<p class="form-note">Перезвоним в течение 15 минут. Выезд замерщика по Стерлитамаку — '
                 'бесплатно.</p>') if note else ''
    return f'''<form data-lead novalidate>
          <input type="hidden" name="topic" value="{topic}">
          <div class="field">
            <label for="{prefix}-name">Как вас зовут</label>
            <input class="input" id="{prefix}-name" name="name" type="text" placeholder="Имя" required>
          </div>
          <div class="field">
            <label for="{prefix}-phone">Телефон</label>
            <input class="input" id="{prefix}-phone" name="phone" type="tel" placeholder="+7 (___) ___-__-__" required>
          </div>
          <div class="field">
            <label for="{prefix}-comment">Комментарий <span class="hint">(не обязательно)</span></label>
            <textarea class="textarea" id="{prefix}-comment" name="comment" placeholder="Что нужно: памятник, благоустройство, венки…"></textarea>
          </div>
          <label class="checkbox">
            <input type="checkbox" name="consent" required>
            <span>Согласен(на) на обработку персональных данных согласно <a href="politika.html">политике конфиденциальности</a></span>
          </label>
          <button class="btn btn--block" type="submit" style="margin-top:16px">{submit}</button>
          {note_html}
        </form>'''


# --------------------------------------------------------------------------
# Каркас страницы
# --------------------------------------------------------------------------
def nav_html(active, cls="nav__link"):
    out = []
    for href, title in NAV:
        klass = cls + (" is-active" if href == active else "")
        out.append('<li><a class="%s" href="%s">%s</a></li>' % (klass, href, title))
    return "\n            ".join(out)


def header_html(active):
    return f'''<div class="topbar">
      <div class="container topbar__inner">
        <span class="topbar__item">{I["pin"]} {SITE["city"]}, {SITE["address_short"]}</span>
        <span class="topbar__item">{I["clock"]} {SITE["hours"]}</span>
        <span class="topbar__item topbar__spacer">{I["truck"]} Доставка по Стерлитамаку, Салавату и Ишимбаю</span>
        <a class="topbar__item" href="mailto:{SITE["email"]}">{I["mail"]} {SITE["email"]}</a>
      </div>
    </div>

    <header class="header">
      <div class="container header__inner">
        <a class="logo" href="index.html">
          <span class="logo__mark" aria-hidden="true">
            <svg viewBox="0 0 24 24"><rect x="6.4" y="2.6" width="11.2" height="13.4" rx="1.6" fill="#c8a24a"/><rect x="3.6" y="17.2" width="16.8" height="3.4" rx="1" fill="#e0c377"/><rect x="5.6" y="21" width="12.8" height="1.6" rx="0.8" fill="#8d6f26"/></svg>
          </span>
          <span class="logo__text">
            <span class="logo__name">{SITE["name"]}</span>
            <span class="logo__tag">{SITE["tagline"]} · {SITE["city"]}</span>
          </span>
        </a>

        <nav class="nav" aria-label="Основное меню">
          <ul class="nav__list">
            {nav_html(active)}
          </ul>
        </nav>

        <div class="header__actions">
          <a class="header__phone" href="{SITE["phone_href"]}">
            <b>{SITE["phone"]}</b>
            <span>{SITE["hours"]}</span>
          </a>
          <button class="btn btn--callback" type="button" data-open-modal="Обратный звонок">Заказать звонок</button>
          <button class="burger" type="button" aria-label="Меню" aria-expanded="false"><span></span></button>
        </div>
      </div>
    </header>

    <aside class="mobile-nav" aria-label="Мобильное меню">
      <div class="mobile-nav__head">
        <span class="logo__name">{SITE["name"]}</span>
        <button class="mobile-nav__close" type="button" aria-label="Закрыть">×</button>
      </div>
      <ul class="mobile-nav__list">
        {nav_html(active, "mobile-nav__link")}
      </ul>
      <a class="btn btn--block" href="{SITE["phone_href"]}">{SITE["phone"]}</a>
      <p class="small muted" style="margin-top:14px">{SITE["hours"]}<br>{SITE["address"]}</p>
    </aside>
    <div class="overlay"></div>'''


def footer_html():
    cat_links = "".join('<li><a href="catalog.html">%s</a></li>' % t for _, t in CATEGORIES[1:6])
    return f'''<footer class="footer">
      <div class="container">
        <div class="footer__grid">
          <div>
            <a class="logo" href="index.html">
              <span class="logo__mark" aria-hidden="true">
                <svg viewBox="0 0 24 24"><rect x="6.4" y="2.6" width="11.2" height="13.4" rx="1.6" fill="#c8a24a"/><rect x="3.6" y="17.2" width="16.8" height="3.4" rx="1" fill="#e0c377"/><rect x="5.6" y="21" width="12.8" height="1.6" rx="0.8" fill="#8d6f26"/></svg>
              </span>
              <span class="logo__text">
                <span class="logo__name">{SITE["name"]}</span>
                <span class="logo__tag">{SITE["tagline"]}</span>
              </span>
            </a>
            <p class="footer__about">Изготовление, установка и благоустройство памятников в Стерлитамаке
              и районах Башкортостана. Собственная мастерская, гранит и мрамор, гарантия 10 лет.</p>
            <div class="socials">
              <a href="{SITE["vk"]}" aria-label="ВКонтакте" rel="noopener" target="_blank">{SOCIALS["vk"]}</a>
              <a href="{SITE["tg"]}" aria-label="Telegram" rel="noopener" target="_blank">{SOCIALS["tg"]}</a>
              <a href="{SITE["wa"]}" aria-label="WhatsApp" rel="noopener" target="_blank">{SOCIALS["wa"]}</a>
            </div>
          </div>
          <div>
            <h4>Каталог</h4>
            <ul>{cat_links}<li><a href="catalog.html">Мемориальные комплексы</a></li></ul>
          </div>
          <div>
            <h4>Услуги</h4>
            <ul>
              <li><a href="uslugi.html">Установка памятников</a></li>
              <li><a href="uslugi.html">Благоустройство могил</a></li>
              <li><a href="uslugi.html">Оградки и ограждения</a></li>
              <li><a href="uslugi.html">Гравировка и портреты</a></li>
              <li><a href="uslugi.html">Реставрация памятников</a></li>
              <li><a href="tovary.html">Венки и ритуальные товары</a></li>
            </ul>
          </div>
          <div>
            <h4>Контакты</h4>
            <ul>
              <li><a href="{SITE["phone_href"]}"><b style="color:#fff;font-size:17px">{SITE["phone"]}</b></a></li>
              <li><a href="{SITE["phone2_href"]}">{SITE["phone2"]}</a></li>
              <li><a href="mailto:{SITE["email"]}">{SITE["email"]}</a></li>
              <li>{SITE["address"]}</li>
              <li>{SITE["hours"]}</li>
            </ul>
            <button class="btn btn--sm" type="button" data-open-modal="Обратный звонок" style="margin-top:6px">Заказать звонок</button>
          </div>
        </div>

        <div class="footer__bottom">
          <span>© <span data-year>2025</span> {SITE["legal"]}</span>
          <span>{SITE["inn"]}</span>
          <span class="spacer"></span>
          <a href="politika.html">Политика конфиденциальности</a>
          <a href="oferta.html">Публичная оферта</a>
        </div>
        <p class="disclaimer">Информация на сайте носит справочный характер и не является публичной офертой.
          Точная стоимость определяется после выбора модели, материала и замеров. Изображения изделий —
          демонстрационные макеты; фактический вид может отличаться.</p>
      </div>
    </footer>'''


def floating_html():
    return f'''<div class="fab">
      <button class="fab__btn" type="button" data-open-modal="Обратный звонок">
        {I["phone"]}<span>Заказать звонок</span>
      </button>
      <button class="fab__top" type="button" aria-label="Наверх">↑</button>
    </div>

    <div class="modal" role="dialog" aria-modal="true" aria-labelledby="modal-title">
      <div class="modal__dialog">
        <button class="modal__close" type="button" aria-label="Закрыть">×</button>
        <h3 id="modal-title" data-modal-title>Заявка</h3>
        <p>Оставьте телефон — перезвоним в течение 15 минут, подскажем по цене и срокам.</p>
        <form data-lead novalidate>
          <input type="hidden" name="topic" data-modal-topic value="">
          <div class="field">
            <label for="m-name">Имя</label>
            <input class="input" id="m-name" name="name" type="text" placeholder="Имя" required>
          </div>
          <div class="field">
            <label for="m-phone">Телефон</label>
            <input class="input" id="m-phone" name="phone" type="tel" placeholder="+7 (___) ___-__-__" required>
          </div>
          <label class="checkbox">
            <input type="checkbox" name="consent" required>
            <span>Согласен(на) на обработку персональных данных</span>
          </label>
          <button class="btn btn--block" type="submit" style="margin-top:16px">Жду звонка</button>
        </form>
      </div>
    </div>

    <div class="lightbox" role="dialog" aria-modal="true">
      <button class="lightbox__close" type="button" aria-label="Закрыть">×</button>
      <button class="lightbox__nav lightbox__nav--prev" type="button" aria-label="Предыдущее">‹</button>
      <img src="" alt="">
      <button class="lightbox__nav lightbox__nav--next" type="button" aria-label="Следующее">›</button>
      <div class="lightbox__caption"></div>
    </div>

    <div class="toast" role="status" aria-live="polite"></div>'''


FAVICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E"
           "%3Crect width='32' height='32' rx='7' fill='%2312161b'/%3E"
           "%3Crect x='10' y='6' width='12' height='15' rx='2' fill='%23c8a24a'/%3E"
           "%3Crect x='7' y='22' width='18' height='4' rx='1' fill='%23e0c377'/%3E%3C/svg%3E")

SHELL = """<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{TITLE}}</title>
<meta name="description" content="{{DESC}}">
<meta name="theme-color" content="#12161b">
<meta property="og:title" content="{{TITLE}}">
<meta property="og:description" content="{{DESC}}">
<meta property="og:type" content="website">
<meta property="og:locale" content="ru_RU">
<link rel="icon" href="{{FAVICON}}">
<script>document.documentElement.classList.add("js");</script>
<!-- Счётчик аналитики: вставьте код Яндекс.Метрики или Google Analytics здесь -->
<!-- <script src="https://mc.yandex.ru/metrika/tag.js" async></script> -->
<link rel="stylesheet" href="assets/css/style.css">
{{JSONLD}}
</head>
<body>

{{HEADER}}

<main>
{{BODY}}
</main>

{{FOOTER}}
{{FLOATING}}

<script src="assets/js/main.js" defer></script>
</body>
</html>
"""


def render(filename, title, desc, active, body, jsonld=""):
    html = (SHELL
            .replace("{{TITLE}}", title)
            .replace("{{DESC}}", desc)
            .replace("{{FAVICON}}", FAVICON)
            .replace("{{JSONLD}}", jsonld)
            .replace("{{HEADER}}", header_html(active))
            .replace("{{BODY}}", body)
            .replace("{{FOOTER}}", footer_html())
            .replace("{{FLOATING}}", floating_html()))
    path = os.path.join(ROOT, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print("ok", filename, "%.1f КБ" % (len(html) / 1024))


def page_head(h1, text, crumbs, active_title):
    crumbs_html = '<a href="index.html">Главная</a><span>/</span>' + active_title
    return f'''<section class="page-head">
      <div class="container">
        <nav class="breadcrumbs" aria-label="Хлебные крошки">{crumbs_html}</nav>
        <h1>{h1}</h1>
        <p>{text}</p>
      </div>
    </section>'''


JSONLD = json.dumps({
    "@context": "https://schema.org",
    "@type": "LocalBusiness",
    "name": SITE["legal"],
    "description": "Изготовление и установка памятников из гранита и мрамора, благоустройство захоронений, венки и ритуальные товары в Стерлитамаке.",
    "telephone": SITE["phone"],
    "email": SITE["email"],
    "address": {"@type": "PostalAddress", "addressLocality": "Стерлитамак",
                "addressRegion": "Республика Башкортостан", "streetAddress": "ул. Строителей, 00",
                "addressCountry": "RU"},
    "openingHours": "Mo-Su 08:00-20:00",
    "priceRange": "от 1 500 ₽",
    "areaServed": ["Стерлитамак", "Салават", "Ишимбай", "Кумертау"],
}, ensure_ascii=False, indent=2)

JSONLD_TAG = '<script type="application/ld+json">\n%s\n</script>' % JSONLD

# ==========================================================================
# ГЛАВНАЯ
# ==========================================================================
MARQUEE_ITEMS = ["Памятники из гранита", "Мемориальные комплексы", "Облицовка плиткой",
                 "Оградки и ограждения", "Гравировка портретов", "Реставрация памятников",
                 "Венки и корзины", "Уход за захоронениями", "Доставка по району"]

marquee = '<section class="marquee"><div class="marquee__track">%s</div></section>' % (
    "".join('<span class="marquee__item">%s</span>' % t for t in MARQUEE_ITEMS * 2))

hero = f'''<section class="hero">
      <div class="container hero__inner">
        <div>
          <span class="badge badge--dark">{I["shield"]} Собственная мастерская · 4 200+ установленных памятников</span>
          <h1 style="margin-top:18px">Памятники из гранита в Стерлитамаке <em>с установкой под ключ</em></h1>
          <p class="hero__lead">Изготовим памятник, подготовим основание, облицуем плиткой и установим.
            Фиксируем цену в договоре, даём гарантию 10 лет и работаем на всех кладбищах города и района.</p>
          <div class="hero__actions">
            <a class="btn btn--lg" href="#calc">Рассчитать стоимость</a>
            <a class="btn btn--lg btn--light" href="catalog.html">Смотреть каталог</a>
          </div>
          <div class="hero__facts">
            <div class="hero__fact"><b>18 лет</b><span>на рынке Стерлитамака</span></div>
            <div class="hero__fact"><b>4 200+</b><span>установленных памятников</span></div>
            <div class="hero__fact"><b>10 лет</b><span>гарантия на установку</span></div>
          </div>
        </div>
        <div class="hero__card">
          <h3>Бесплатный выезд замерщика</h3>
          <p>Приедем на кладбище или к вам, замерим участок, покажем образцы гранита и посчитаем стоимость на месте.</p>
          {lead_form("hero", "Записаться на замер")}
        </div>
      </div>
    </section>
    {marquee}'''

features = f'''<section class="section section--paper">
      <div class="container">
        <div class="section-head section-head--center reveal">
          <span class="kicker">Почему нас выбирают</span>
          <h2>Делаем так, чтобы к этому вопросу не пришлось возвращаться</h2>
          <p>Мы не посредники: пилим, гравируем, бетонируем и устанавливаем сами. Поэтому отвечаем за сроки,
            цену и качество на каждом этапе.</p>
        </div>
        <div class="grid grid--3">
          {feature("factory", "Собственная мастерская", "Гранит и мрамор в наличии, резка и гравировка на месте — без наценок посредников и лишних ожиданий.")}
          {feature("ruler", "Бесплатный выезд замерщика", "Замерим участок, покажем образцы камня, посчитаем смету и нарисуем эскиз будущего памятника.")}
          {feature("doc", "Фиксируем цену в договоре", "Стоимость из сметы не меняется в процессе. Аванс 30%, остаток — после установки.")}
          {feature("shield", "Гарантия 10 лет", "Гарантия на конструкцию и установку — 10 лет, на гравировку и фотокерамику — 5 лет.")}
          {feature("percent", "Рассрочка 0%", "До 6 месяцев без процентов и переплат. Первый взнос — от 30% стоимости.")}
          {feature("truck", "Работаем по району", "Стерлитамак, Салават, Ишимбай, Кумертау, Стерлибашево, Гафурийский и Аургазинский районы.")}
        </div>
      </div>
    </section>'''

catalog_preview = f'''<section class="section section--white">
      <div class="container">
        <div class="section-head reveal" style="display:flex;flex-wrap:wrap;gap:20px;align-items:flex-end;justify-content:space-between;max-width:none">
          <div style="max-width:620px">
            <span class="kicker">Каталог</span>
            <h2>Популярные памятники</h2>
            <p>Более 200 моделей из габбро-диабаза, дымовского, красного и зелёного гранита, мрамора.
              Любую модель адаптируем под ваш размер и оформление.</p>
          </div>
          <a class="btn btn--outline" href="catalog.html">Весь каталог {I["arrow"]}</a>
        </div>
        <div class="cards">{"".join(card(c) for c in CATALOG[:4])}</div>
      </div>
    </section>'''

calc_section = f'''<section class="section section--paper2" id="calc">
      <div class="container">
        <div class="section-head section-head--center reveal">
          <span class="kicker">Калькулятор</span>
          <h2>Соберите памятник и узнайте цену за 30 секунд</h2>
          <p>Выберите тип, материал и оформление — калькулятор покажет ориентировочную стоимость
            с установкой. Точную смету менеджер подтвердит после замера.</p>
        </div>

        <div class="calc" data-calc>
          <div>
            <div class="calc__row">
              <span class="calc__label">1. Тип памятника</span>
              <div class="chips">
                <label class="chip"><input type="radio" name="calcType" data-calc-group="type" data-mult="1" data-title="Одинарный вертикальный памятник" checked><span>Одинарный</span><small>100×50 см</small></label>
                <label class="chip"><input type="radio" name="calcType" data-calc-group="type" data-mult="1.2" data-title="Горизонтальный памятник (плита)"><span>Горизонтальный</span><small>плита</small></label>
                <label class="chip"><input type="radio" name="calcType" data-calc-group="type" data-mult="1.75" data-title="Двойной (семейный) памятник"><span>Двойной</span><small>2 стелы</small></label>
                <label class="chip"><input type="radio" name="calcType" data-calc-group="type" data-mult="2.6" data-title="Мемориальный комплекс"><span>Комплекс</span><small>с плиткой</small></label>
                <label class="chip"><input type="radio" name="calcType" data-calc-group="type" data-mult="0.72" data-title="Детский памятник"><span>Детский</span><small>80×40 см</small></label>
              </div>
            </div>

            <div class="calc__row">
              <span class="calc__label">2. Материал</span>
              <div class="chips">
                <label class="chip"><input type="radio" name="calcMaterial" data-calc-group="material" data-mult="1" data-title="габбро-диабаз" checked><span>Габбро-диабаз</span><small>чёрный</small></label>
                <label class="chip"><input type="radio" name="calcMaterial" data-calc-group="material" data-mult="1.12" data-title="дымовский гранит"><span>Дымовский</span><small>серый</small></label>
                <label class="chip"><input type="radio" name="calcMaterial" data-calc-group="material" data-mult="0.82" data-title="мрамор"><span>Мрамор</span><small>светлый</small></label>
                <label class="chip"><input type="radio" name="calcMaterial" data-calc-group="material" data-mult="1.18" data-title="красный гранит"><span>Красный гранит</span><small>Лезники</small></label>
                <label class="chip"><input type="radio" name="calcMaterial" data-calc-group="material" data-mult="1.08" data-title="зелёный гранит"><span>Зелёный гранит</span><small>Башкирия</small></label>
              </div>
            </div>

            <div class="calc__row">
              <span class="calc__label">3. Размер стелы</span>
              <div class="chips">
                <label class="chip"><input type="radio" name="calcSize" data-calc-group="size" data-mult="1" data-title="100×50×8 см" checked><span>100×50×8 см</span><small>стандарт</small></label>
                <label class="chip"><input type="radio" name="calcSize" data-calc-group="size" data-mult="1.16" data-title="120×60×8 см"><span>120×60×8 см</span><small>+16%</small></label>
                <label class="chip"><input type="radio" name="calcSize" data-calc-group="size" data-mult="1.34" data-title="140×70×8 см"><span>140×70×8 см</span><small>+34%</small></label>
              </div>
            </div>

            <div class="calc__row">
              <span class="calc__label">4. Оформление</span>
              <div class="chips">
                <label class="chip"><input type="checkbox" name="calcExtra" data-calc-group="extra" data-add="3000" data-title="Портрет на металлокерамике"><span>Портрет 13×18</span><small>+3 000 ₽</small></label>
                <label class="chip"><input type="checkbox" name="calcExtra" data-calc-group="extra" data-add="1500" data-title="Эпитафия и даты"><span>Текст и даты</span><small>+1 500 ₽</small></label>
                <label class="chip"><input type="checkbox" name="calcExtra" data-calc-group="extra" data-add="1200" data-title="Символ веры (крест, полумесяц)"><span>Крест / символ</span><small>+1 200 ₽</small></label>
                <label class="chip"><input type="checkbox" name="calcExtra" data-calc-group="extra" data-add="4500" data-title="Художественная гравировка"><span>Художественная гравировка</span><small>+4 500 ₽</small></label>
                <label class="chip"><input type="checkbox" name="calcExtra" data-calc-group="extra" data-add="2500" data-title="Фотокерамика на стекле"><span>Фотокерамика</span><small>+2 500 ₽</small></label>
              </div>
            </div>

            <div class="calc__row" style="margin-bottom:0">
              <span class="calc__label">5. Благоустройство</span>
              <div class="chips">
                <label class="chip"><input type="checkbox" name="calcBlago" data-calc-group="blago" data-add="32000" data-title="Облицовка плиткой 2×1,5 м"><span>Плитка 2×1,5 м</span><small>+32 000 ₽</small></label>
                <label class="chip"><input type="checkbox" name="calcBlago" data-calc-group="blago" data-add="9000" data-title="Цоколь по периметру"><span>Цоколь</span><small>+9 000 ₽</small></label>
                <label class="chip"><input type="checkbox" name="calcBlago" data-calc-group="blago" data-add="9500" data-title="Оградка сварная 2×1 м"><span>Оградка сварная</span><small>+9 500 ₽</small></label>
                <label class="chip"><input type="checkbox" name="calcBlago" data-calc-group="blago" data-add="24000" data-title="Кованая оградка 2×2 м"><span>Оградка кованая</span><small>+24 000 ₽</small></label>
                <label class="chip"><input type="checkbox" name="calcBlago" data-calc-group="blago" data-add="4000" data-title="Отсыпка цветника камушками"><span>Отсыпка цветника</span><small>+4 000 ₽</small></label>
              </div>
            </div>
          </div>

          <div class="calc__result">
            <span class="badge badge--dark">{I["calc"]} Предварительный расчёт</span>
            <div class="calc__sum" data-calc-sum>от 34 900 ₽</div>
            <p class="tiny" style="color:rgba(238,240,243,.66);margin:0">Установка, доставка и бетонное основание включены</p>
            <ul class="calc__breakdown" data-calc-list></ul>
            <input type="hidden" data-calc-input value="">
            <button class="btn btn--block" type="button" data-open-modal="Расчёт стоимости">Отправить расчёт менеджеру</button>
            <p class="calc__hint">Расчёт предварительный: точная цена зависит от состояния участка и выбранного камня.
              Менеджер бесплатно проверит смету после замера.</p>
          </div>
        </div>
      </div>
    </section>'''

services_preview = f'''<section class="section section--white">
      <div class="container">
        <div class="section-head reveal" style="display:flex;flex-wrap:wrap;gap:20px;align-items:flex-end;justify-content:space-between;max-width:none">
          <div style="max-width:620px">
            <span class="kicker">Услуги</span>
            <h2>Полный цикл: от эскиза до благоустроенного захоронения</h2>
            <p>Можем изготовить только памятник, а можем взять на себя всё: основание, плитку, оградку,
              отсыпку и дальнейший уход.</p>
          </div>
          <a class="btn btn--outline" href="uslugi.html">Все услуги и цены {I["arrow"]}</a>
        </div>
        <div class="cards">{"".join(service_card(s) for s in SERVICES[:4])}</div>
      </div>
    </section>'''

steps_section = f'''<section class="section section--dark">
      <div class="container">
        <div class="section-head section-head--center reveal">
          <span class="kicker">Как мы работаем</span>
          <h2>Пять шагов без лишних хлопот</h2>
          <p>Вам не нужно ездить по мастерским и сравнивать десятки подрядчиков — всё сделаем сами и покажем фотоотчётом.</p>
        </div>
        <div class="steps">
          {step("Заявка и консультация", "Позвоните или оставьте заявку. Уточним пожелания, подскажем бюджет и сроки.")}
          {step("Замер и эскиз", "Бесплатно выезжаем на участок, замеряем, показываем образцы камня и рисуем эскиз.")}
          {step("Договор и аванс", "Фиксируем цену, материал и сроки в договоре. Аванс — 30%.")}
          {step("Изготовление", "Режем, полируем, гравируем портрет и текст. Срок — от 7 до 21 дня.")}
          {step("Установка", "Бетонируем основание, монтируем, убираем мусор. Остаток оплаты — по факту.")}
        </div>
      </div>
    </section>'''

RABOTY = [
    ("kompleks-pravoslavnyj.svg", "Комплекс «Православный» с облицовкой 2×1,5 м", "Стерлитамак"),
    ("pamyatnik-klassika.svg", "Памятник «Классика», габбро-диабаз", "Стерлитамак"),
    ("pamyatnik-angel.svg", "Резной памятник с ангелом, ручная работа", "Стерлитамак"),
    ("kompleks-semejnyj.svg", "Двойной комплекс для семьи, дымовский гранит", "Салават"),
    ("pamyatnik-krest.svg", "Православный памятник с крестом и лампадкой", "Ишимбай"),
    ("pamyatnik-musulmanskij.svg", "Мусульманский памятник с полумесяцем", "Стерлитамак"),
    ("usluga-plitka.svg", "Облицовка плиткой и цоколь по периметру", "Стерлитамак"),
    ("usluga-ogradka-kovanaya.svg", "Кованая оградка со столом и скамьёй", "Стерлитамак"),
    ("pamyatnik-mramor.svg", "Мраморный памятник с арочным верхом", "Кумертау"),
    ("usluga-gravirovka.svg", "Портрет на металлокерамике и эпитафия", "Стерлитамак"),
    ("kompleks-elitnyj.svg", "Комплекс «Элитный» со скульптурой, 2,5×2 м", "Стерлитамак"),
    ("pamyatnik-dvojnoj.svg", "Двойной памятник на общем основании", "Стерлитамак"),
]


def gallery_item(img, caption, place, wide=False):
    return f'''<figure class="gallery__item reveal" role="button" tabindex="0" data-full="assets/img/{img}" data-caption="{caption} · {place}">
          <img src="assets/img/{img}" alt="{caption}" loading="lazy" width="900" height="675">
          <figcaption>{caption} · <span class="muted" style="color:rgba(255,255,255,.6)">{place}</span></figcaption>
        </figure>'''


gallery_preview = f'''<section class="section section--paper">
      <div class="container">
        <div class="section-head reveal" style="display:flex;flex-wrap:wrap;gap:20px;align-items:flex-end;justify-content:space-between;max-width:none">
          <div style="max-width:620px">
            <span class="kicker">Наши работы</span>
            <h2>Фотографии установленных памятников</h2>
            <p>Показываем реальные работы: комплексы, одиночные и двойные памятники, облицовку, оградки.
              Фото — с согласия заказчиков.</p>
          </div>
          <a class="btn btn--outline" href="raboty.html">Все работы {I["arrow"]}</a>
        </div>
        <div class="gallery">
          {"".join(gallery_item(*item) for item in RABOTY[:6])}
        </div>
      </div>
    </section>'''

REVIEWS = [
    ("Елена", "Стерлитамак · памятник «Классика»", "Обратились после похорон отца — было тяжело и ничего не понятно. Приехали на кладбище в тот же день, всё замерили, показали образцы гранита. Через две недели памятник стоял, участок обложен плиткой. Цену не меняли ни разу."),
    ("Ильдар", "Стерлитамак · мусульманский памятник", "Сделали по всем нашим обычаям, полумесяц и арабскую вязь выполнили аккуратно. Отдельное спасибо за то, что помогли с документами и не торопили с выбором."),
    ("Ольга и Сергей", "Салават · двойной комплекс", "Заказывали двойной памятник родителям. Понравилось, что показали 3D-макет заранее и цена в договоре не изменилась. Установили быстро, мусор увезли, плитку выложили ровно."),
]

reviews_section = f'''<section class="section section--white">
      <div class="container">
        <div class="section-head section-head--center reveal">
          <span class="kicker">Отзывы</span>
          <h2>Что говорят наши заказчики</h2>
          <p>Мы работаем на репутацию: большинство клиентов приходят по рекомендации родных и соседей.</p>
        </div>
        <div class="grid grid--3">
          {"".join(review(n, m, t, n[0]) for n, m, t in REVIEWS)}
        </div>
      </div>
    </section>'''

products_preview = f'''<section class="section section--paper2">
      <div class="container">
        <div class="section-head reveal" style="display:flex;flex-wrap:wrap;gap:20px;align-items:flex-end;justify-content:space-between;max-width:none">
          <div style="max-width:620px">
            <span class="kicker">Ритуальные товары</span>
            <h2>Венки, корзины и принадлежности с доставкой за 2 часа</h2>
            <p>Работаем круглосуточно по договорённости: привезём венок, ленту с надписью, крест или
              полный набор в морг, дом или прямо к кладбищу.</p>
          </div>
          <a class="btn btn--outline" href="tovary.html">Смотреть товары {I["arrow"]}</a>
        </div>
        <div class="cards">{"".join(card(p) for p in PRODUCTS[:4])}</div>
      </div>
    </section>'''

FAQ = [
    ("Сколько стоит памятник под ключ в Стерлитамаке?",
     "Базовый одинарный памятник из габбро-диабаза с установкой — от 34 900 ₽. Итоговая цена зависит от размера стелы, породы камня, оформления и благоустройства (плитка, цоколь, оградка). Точную смету считаем бесплатно после замера и фиксируем в договоре."),
    ("Сколько времени занимает изготовление?",
     "Стандартный памятник с портретом и текстом — 7–14 дней. Резные и эксклюзивные работы — до 21 дня. Установка занимает один день; бетонному основанию нужно около 3–5 дней до монтажа стелы."),
    ("Можно ли устанавливать памятник зимой?",
     "Да. Мы работаем круглый год: используем противоморозные добавки в бетон и прогрев основания. Если грунт промёрз настолько, что монтаж может повредить участок, предложим установить памятник позже без изменения цены."),
    ("Есть ли рассрочка?",
     "Да, рассрочка 0% на срок до 6 месяцев без банка и переплат. Первый взнос — от 30% стоимости. Также принимаем оплату картой, наличными и по счёту."),
    ("Какая гарантия на памятник и установку?",
     "10 лет — на конструкцию и установку (просадка, перекос, крепление). 5 лет — на гравировку и портрет на металлокерамике: изображение не выгорает и не отслаивается."),
    ("Вы работаете за пределами Стерлитамака?",
     "Да. Работаем в Стерлитамаке, Салавате, Ишимбае, Кумертау, Стерлибашево, Гафурийском и Аургазинском районах. Доставка до 60 км — бесплатно при заказе от 30 000 ₽."),
    ("Можно ли сделать памятник по своему эскизу?",
     "Конечно. Пришлите фотографию или рисунок — художник подготовит эскиз и 3D-макет, покажем, как это будет выглядеть на камне, до начала работ."),
    ("Как заказать и какие документы нужны?",
     "Достаточно паспорта заказчика и данных об умершем: ФИО, даты рождения и смерти, фотография для портрета. Если памятник устанавливается не вами, понадобится согласование со смотрителем кладбища — поможем оформить."),
]

faq_section = f'''<section class="section section--paper" id="faq">
      <div class="container">
        <div class="section-head section-head--center reveal">
          <span class="kicker">Вопросы и ответы</span>
          <h2>Отвечаем на частые вопросы</h2>
          <p>Если чего-то не нашли — позвоните, подскажем без навязчивых продаж.</p>
        </div>
        <div class="faq">
          {"".join(faq_item(q, a, i) for i, (q, a) in enumerate(FAQ))}
        </div>
      </div>
    </section>'''

cta_section = f'''<section class="section section--white">
      <div class="container">
        <div class="cta reveal">
          <div>
            <span class="kicker">Бесплатно и без обязательств</span>
            <h2>Выезд замерщика с образцами гранита</h2>
            <p>Приедем в удобное время — на кладбище, домой или в морг. Замерим участок,
              покажем каталог и посчитаем стоимость на месте. Решение принимать вам.</p>
            <ul class="card__specs" style="color:rgba(238,240,243,.8);margin-top:20px">
              <li>Работаем ежедневно с 8:00 до 20:00</li>
              <li>Перезваниваем в течение 15 минут</li>
              <li>Никаких навязчивых звонков после консультации</li>
            </ul>
          </div>
          <div class="cta__form">{lead_form("cta", "Записаться на выезд")}</div>
        </div>
      </div>
    </section>'''

index_body = "\n".join([hero, features, catalog_preview, calc_section, services_preview,
                        steps_section, gallery_preview, reviews_section, products_preview,
                        faq_section, cta_section])

render("index.html",
       "Памятники в Стерлитамаке — изготовление и установка под ключ | %s" % SITE["name"],
       "Изготовление памятников из гранита и мрамора в Стерлитамаке: каталог, цены, установка под ключ, "
       "благоустройство захоронений, венки и ритуальные товары. Гарантия 10 лет, рассрочка 0%.",
       "index.html", index_body, JSONLD_TAG)

# ==========================================================================
# КАТАЛОГ
# ==========================================================================
filters = '''<div class="filters" data-filters>
          <div class="chips">
            %s
          </div>
          <div class="filters__search">
            <input class="input" type="search" placeholder="Поиск по каталогу: «ангел», «двойной»…" data-search>
          </div>
          <span class="filters__count" data-count></span>
        </div>''' % "".join(
    '<button class="chip%s" type="button" data-filter="%s">%s</button>' % (" is-checked" if key == "all" else "", key, title)
    for key, title in CATEGORIES)

catalog_body = "\n".join([
    page_head("Каталог памятников", "Более 200 моделей памятников и мемориальных комплексов из гранита и мрамора. "
              "Любую модель адаптируем под ваши размеры, добавим гравировку, портрет и благоустройство. "
              "Цены указаны с установкой по Стерлитамаку.", None, "Каталог"),
    f'''<section class="section section--paper">
      <div class="container">
        {filters}
        <div class="cards">{"".join(card(c) for c in CATALOG)}</div>
        <div class="empty-state" style="display:none">По вашему запросу ничего не нашлось. Позвоните нам —
          подберём модель из готовых решений или изготовим по индивидуальному эскизу.</div>
      </div>
    </section>''',
    f'''<section class="section section--white">
      <div class="container">
        <div class="section-head section-head--center reveal">
          <span class="kicker">Что входит в стоимость</span>
          <h2>Памятник под ключ — это не только стела</h2>
        </div>
        <div class="grid grid--4">
          {feature("ruler", "Замер участка", "Выезд замерщика по Стерлитамаку и району бесплатно.")}
          {feature("tools", "Основание из бетона", "Армированная подушка под памятник — чтобы не просел.")}
          {feature("truck", "Доставка и монтаж", "Привезём, установим по уровню, уберём мусор.")}
          {feature("doc", "Договор и гарантия", "Цена фиксируется, гарантия 10 лет на установку.")}
        </div>
      </div>
    </section>''',
    cta_section,
])

render("catalog.html",
       "Каталог памятников из гранита и мрамора в Стерлитамаке — цены с установкой | %s" % SITE["name"],
       "Каталог памятников в Стерлитамаке: одинарные, двойные, детские, мусульманские, православные, "
       "мемориальные комплексы. Цены от 24 500 ₽ с установкой.",
       "catalog.html", catalog_body)

# ==========================================================================
# УСЛУГИ
# ==========================================================================
uslugi_body = "\n".join([
    page_head("Услуги мастерской", "Изготавливаем и устанавливаем памятники, благоустраиваем захоронения, "
              "делаем оградки, гравировку и реставрацию. Все работы выполняем своими мастерами и даём "
              "гарантию 10 лет.", None, "Услуги"),
    f'''<section class="section section--paper">
      <div class="container">
        <div class="cards">{"".join(service_card(s) for s in SERVICES)}</div>
      </div>
    </section>''',
    steps_section,
    f'''<section class="section section--white">
      <div class="container">
        <div class="section-head section-head--center reveal">
          <span class="kicker">Частые вопросы по работам</span>
          <h2>Что уточняют перед заказом</h2>
        </div>
        <div class="faq">
          {faq_item("Сколько стоит благоустройство могилы под ключ?", "Облицовка плиткой 2×1,5 м с бордюром и отсыпкой — от 32 000 ₽. Комплекс «памятник + плитка + оградка» — от 96 000 ₽. Точная сумма зависит от площади участка и выбранной плитки. Замер и смета — бесплатно.", 0)}
          {faq_item("Можно ли заказать только гравировку, если памятник уже стоит?", "Да. Выедем на кладбище, сделаем портрет на металлокерамике, обновим надпись или добавим даты. Работаем и с чужими памятниками — аккуратно, без демонтажа стелы.", 1)}
          {faq_item("Вы демонтируете старый памятник?", "Да, демонтаж, погрузка и вывоз — от 4 500 ₽. Утилизируем или поможем оформить вывоз на полигон. При заказе нового памятника демонтаж делаем со скидкой.", 2)}
          {faq_item("Кто отвечает за согласование с администрацией кладбища?", "Мы. Подскажем, какие документы нужны, и при необходимости согласуем установку со смотрителем кладбища — это входит в стоимость работ.", 3)}
        </div>
      </div>
    </section>''',
    cta_section,
])

render("uslugi.html",
       "Услуги: установка памятников, благоустройство могил, оградки, гравировка в Стерлитамаке | %s" % SITE["name"],
       "Услуги ритуальной мастерской в Стерлитамаке: установка памятников от 5 500 ₽, благоустройство "
       "захоронений от 32 000 ₽, оградки, гравировка портретов, реставрация, уход за могилой.",
       "uslugi.html", uslugi_body)

# ==========================================================================
# ВЕНКИ И ТОВАРЫ
# ==========================================================================
PROD_CATEGORIES = [("all", "Все"), ("venok", "Венки"), ("korzina", "Корзины"), ("tovar", "Гробы, кресты, ленты")]

prod_filters = '''<div class="filters" data-filters>
          <div class="chips">
            %s
          </div>
          <div class="filters__search">
            <input class="input" type="search" placeholder="Поиск: «венок 80», «лента», «крест»…" data-search>
          </div>
          <span class="filters__count" data-count></span>
        </div>''' % "".join(
    '<button class="chip%s" type="button" data-filter="%s">%s</button>' % (" is-checked" if key == "all" else "", key, title)
    for key, title in PROD_CATEGORIES)

tovary_body = "\n".join([
    page_head("Венки и ритуальные товары", "Траурные венки, корзины, кресты, гробы и принадлежности. "
              "Доставим по Стерлитамаку за 2 часа, по району — в день заказа. Работаем круглосуточно "
              "по договорённости.", None, "Венки и товары"),
    f'''<section class="section section--paper">
      <div class="container">
        {prod_filters}
        <div class="cards">{"".join(card(p) for p in PRODUCTS)}</div>
        <div class="empty-state" style="display:none">Ничего не нашлось. Позвоните — подберём венок или
          соберём композицию под заказ в течение часа.</div>
      </div>
    </section>''',
    f'''<section class="section section--white">
      <div class="container">
        <div class="grid grid--2" style="align-items:center;gap:44px">
          <div class="reveal">
            <span class="kicker">Организация похорон</span>
            <h2>Возьмём на себя всю организацию</h2>
            <p>Если беда случилась ночью или в выходные — звоните, поможем сразу. Подскажем порядок действий,
              оформим документы, привезём всё необходимое и будем рядом до конца.</p>
            <ul class="card__specs" style="font-size:15px">
              <li>Круглосуточная помощь и консультация по телефону</li>
              <li>Оформление документов и справок</li>
              <li>Венки, корзины, ленты с надписью — изготовление от 20 минут</li>
              <li>Доставка в морг, дом или к кладбищу</li>
              <li>Копка могилы, отпевание, поминальный обед — по договорённости</li>
            </ul>
            <div style="display:flex;gap:14px;flex-wrap:wrap;margin-top:22px">
              <a class="btn btn--lg" href="{SITE["phone_href"]}">{I["phone"]} {SITE["phone"]}</a>
              <button class="btn btn--lg btn--outline" type="button" data-open-modal="Организация похорон">Оставить заявку</button>
            </div>
          </div>
          <div class="reveal">
            <img src="assets/img/venok-mame.svg" alt="Траурный венок 80 см" style="border-radius:24px;box-shadow:0 26px 60px rgba(18,22,27,.16)" loading="lazy" width="900" height="675">
          </div>
        </div>
      </div>
    </section>''',
    f'''<section class="section section--paper2">
      <div class="container">
        <div class="section-head section-head--center reveal">
          <span class="kicker">Доставка и оплата</span>
          <h2>Быстро, аккуратно и без лишних вопросов</h2>
        </div>
        <div class="grid grid--3">
          {feature("truck", "Доставка за 2 часа", "По Стерлитамаку — в течение 2 часов, по Салавату, Ишимбаю и району — в день заказа. Привезём на дом, в морг или к кладбищу.")}
          {feature("cash", "Удобная оплата", "Наличные, перевод или карта. Для похорон в кредит — рассрочка 0% до 6 месяцев.")}
          {feature("chat", "Круглосуточная связь", "Телефон доступен 24/7. Подскажем, что нужно в конкретной ситуации, и не будем навязывать лишнее.")}
        </div>
      </div>
    </section>''',
    cta_section,
])

render("tovary.html",
       "Траурные венки, корзины, кресты и гробы с доставкой в Стерлитамаке | %s" % SITE["name"],
       "Ритуальные товары в Стерлитамаке: траурные венки от 1 900 ₽, корзины, кресты, гробы, ленты с "
       "надписью. Доставка по городу за 2 часа, работаем круглосуточно.",
       "tovary.html", tovary_body)

# ==========================================================================
# НАШИ РАБОТЫ
# ==========================================================================
raboty_body = "\n".join([
    page_head("Наши работы", "Более 4 200 установленных памятников и благоустроенных захоронений "
              "в Стерлитамаке, Салавате, Ишимбае и Кумертау. Публикуем фотографии с согласия заказчиков — "
              "нажмите на фото, чтобы увеличить.", None, "Наши работы"),
    f'''<section class="section section--paper">
      <div class="container">
        <div class="gallery">
          {"".join(gallery_item(img, cap, place) for img, cap, place in RABOTY)}
        </div>
      </div>
    </section>''',
    reviews_section,
    cta_section,
])

render("raboty.html",
       "Наши работы — установленные памятники в Стерлитамаке, фото | %s" % SITE["name"],
       "Фотографии наших работ: памятники из гранита и мрамора, мемориальные комплексы, облицовка плиткой, "
       "оградки в Стерлитамаке, Салавате и Ишимбае.",
       "raboty.html", raboty_body)

# ==========================================================================
# ЦЕНЫ
# ==========================================================================
def price_table(groups):
    rows = []
    for group_name, items in groups:
        rows.append('<tr class="price-table__group"><td colspan="3">%s</td></tr>' % group_name)
        for name, note, price in items:
            rows.append('<tr><td>%s</td><td class="muted small">%s</td><td><b>%s</b></td></tr>' % (name, note, price))
    return ('<table class="price-table"><thead><tr><th>Позиция</th><th>Что входит</th><th>Цена</th></tr></thead>'
            '<tbody>%s</tbody></table>' % "".join(rows))


ceny_body = "\n".join([
    page_head("Цены на памятники и услуги", "Актуальный прайс на 2025 год. Цены указаны с установкой "
              "по Стерлитамаку и району. Итоговая стоимость фиксируется в договоре после замера — "
              "доплат «по ходу работ» не бывает.", None, "Цены"),
    f'''<section class="section section--paper">
      <div class="container">
        <div class="section-head reveal">
          <span class="kicker">Памятники</span>
          <h2>Гранит и мрамор — с установкой</h2>
          <p>В комплект входит стела, тумба, цветник и бетонное основание. Портрет и текст считаются отдельно.</p>
        </div>
        {price_table([
          ("Гранитные памятники", [
            ("Памятник «Классика», габбро-диабаз", "стела 100×50×8, тумба, цветник", "от 34 900 ₽"),
            ("Памятник «Волна» фигурный", "серый гранит, стела 110×50×8", "от 39 500 ₽"),
            ("Православный памятник с крестом", "стела 100×50×8, крест, лампадка", "от 36 000 ₽"),
            ("Мусульманский памятник", "зелёный гранит, полумесяц и звезда", "от 31 000 ₽"),
            ("Памятник из красного гранита", "стела 110×50×8, тумба, цветник", "от 44 000 ₽"),
            ("Памятник «Ангел» резной", "ручная резка, стела 120×60×8", "от 58 000 ₽"),
            ("Горизонтальный памятник (плита)", "плита 120×60×8 на основании", "от 42 000 ₽"),
            ("Памятник участнику СВО", "стела 110×55×8, помощь с льготами", "от 48 000 ₽"),
          ]),
          ("Мрамор и двойные", [
            ("Мраморный памятник «Арка»", "стела 100×50×8, белый мрамор", "от 27 000 ₽"),
            ("Двойной памятник «Семейный»", "две стелы на общем основании, 160 см", "от 62 000 ₽"),
            ("Детский памятник «Сердце»", "стела 80×40×7, деликатная гравировка", "от 24 500 ₽"),
          ]),
          ("Мемориальные комплексы", [
            ("Комплекс «Православный»", "стела, плитка 2×1,5 м, оградка, установка", "от 96 000 ₽"),
            ("Комплекс «Семейный»", "две стелы, плитка 2×2 м, кованая оградка", "от 132 000 ₽"),
            ("Комплекс «Элитный»", "скульптура, декор, плитка 2,5×2 м", "от 185 000 ₽"),
          ]),
        ])}
      </div>
    </section>''',
    f'''<section class="section section--white">
      <div class="container">
        <div class="section-head reveal">
          <span class="kicker">Работы и услуги</span>
          <h2>Установка, благоустройство, гравировка</h2>
        </div>
        {price_table([
          ("Установка и благоустройство", [
            ("Установка памятника", "бетонное основание, армирование, уровень", "от 5 500 ₽"),
            ("Облицовка плиткой 2×1,5 м", "гранитная плитка, бордюр, отсыпка", "от 32 000 ₽"),
            ("Цоколь по периметру", "гранитный цоколь, затирка швов", "от 9 000 ₽"),
            ("Сварная оградка 2×1 м", "изготовление, покраска, монтаж", "от 9 500 ₽"),
            ("Кованая оградка 2×2 м", "художественная ковка, стол и скамья", "от 24 000 ₽"),
            ("Демонтаж и вывоз старого памятника", "демонтаж, погрузка, утилизация", "от 4 500 ₽"),
          ]),
          ("Гравировка и оформление", [
            ("Портрет на металлокерамике 13×18", "по фотографии, не выгорает", "от 3 000 ₽"),
            ("Фотокерамика на стекле", "стойкая печать по фото", "от 2 500 ₽"),
            ("Текст и даты (до 60 знаков)", "гравировка, закраска золотом", "от 1 500 ₽"),
            ("Художественная гравировка", "пейзаж, храм, цветы, портрет на камне", "от 4 500 ₽"),
            ("Символ веры (крест, полумесяц)", "гравировка и закраска", "от 1 200 ₽"),
          ]),
          ("Уход и реставрация", [
            ("Реставрация памятника", "выравнивание основания, чистка, обновление", "от 6 000 ₽"),
            ("Разовая уборка захоронения", "уборка, уход за гравировкой, фотоотчёт", "от 1 500 ₽"),
            ("Абонемент на год (4 выезда)", "уборка, посадка, полив, фотоотчёт", "от 5 400 ₽"),
            ("Замена и ремонт оградки", "демонтаж, изготовление, покраска", "от 7 000 ₽"),
          ]),
        ])}
      </div>
    </section>''',
    f'''<section class="section section--paper2">
      <div class="container">
        <div class="section-head reveal">
          <span class="kicker">Ритуальные товары</span>
          <h2>Венки, корзины и принадлежности</h2>
        </div>
        {price_table([
          ("Венки и корзины", [
            ("Венок «Скорбь» 60 см", "хвоя и искусственные цветы, лента", "от 1 900 ₽"),
            ("Венок «От всех скорбящих» 70 см", "классическая форма, лента", "от 2 400 ₽"),
            ("Венок «Любимой маме» 80 см", "белые и кремовые цветы, лента", "от 2 900 ₽"),
            ("Венок из живых цветов", "под заказ, по сезону", "от 4 500 ₽"),
            ("Корзина «Печаль»", "высота 60 см, лента с надписью", "от 3 600 ₽"),
          ]),
          ("Принадлежности", [
            ("Крест деревянный 120 см", "сосна, пропитка, табличка", "от 1 500 ₽"),
            ("Гроб (сосна, обивка)", "лак, атлас/бархат, ручки, покрывало", "от 8 900 ₽"),
            ("Траурная лента с надписью", "печать золотом, 2 м", "от 350 ₽"),
            ("Табличка на крест или памятник", "гравировка, крепление", "от 700 ₽"),
          ]),
        ])}
        <p class="small muted" style="margin-top:18px">Цены являются ориентировочными и не являются публичной офертой.
          Актуальную стоимость уточняйте по телефону {SITE["phone"]}.</p>
      </div>
    </section>''',
    f'''<section class="section section--white">
      <div class="container">
        <div class="grid grid--3">
          {feature("percent", "Рассрочка 0%", "До 6 месяцев без процентов и справок. Первый взнос — от 30%.")}
          {feature("cash", "Оплата по факту", "Аванс 30%, остаток — после установки и вашей приёмки.")}
          {feature("doc", "Договор и смета", "Все позиции прописаны, цена не меняется в процессе работ.")}
        </div>
      </div>
    </section>''',
    cta_section,
])

render("ceny.html",
       "Цены на памятники, установку и ритуальные товары в Стерлитамаке 2025 | %s" % SITE["name"],
       "Прайс-лист ритуальной мастерской в Стерлитамаке: памятники от 24 500 ₽, установка от 5 500 ₽, "
       "благоустройство от 32 000 ₽, венки от 1 900 ₽. Рассрочка 0%, гарантия 10 лет.",
       "ceny.html", ceny_body)

# ==========================================================================
# КОНТАКТЫ
# ==========================================================================
MAP_NOTE = """<!-- Чтобы поставить настоящую карту, удалите этот блок и вставьте
           iframe конструктора Яндекс.Карт:
           <iframe src="https://yandex.ru/map-widget/v1/?text=..." width="100%" height="380"
                   frameborder="0" style="border:0"></iframe> -->"""

kontakty_body = "\n".join([
    page_head("Контакты", "Позвоните, напишите в мессенджер или оставьте заявку — ответим в течение "
              "15 минут и бесплатно проконсультируем. Выезд замерщика по Стерлитамаку и району бесплатный.",
              None, "Контакты"),
    f'''<section class="section section--paper">
      <div class="container">
        <div class="grid grid--4">
          <div class="info-card reveal">
            <div class="info-card__icon">{I["phone"]}</div>
            <h3>Телефоны</h3>
            <p><a href="{SITE["phone_href"]}"><b>{SITE["phone"]}</b></a><br>
               <a href="{SITE["phone2_href"]}">{SITE["phone2"]}</a><br>
               <span class="small muted">Круглосуточно при срочном заказе</span></p>
          </div>
          <div class="info-card reveal">
            <div class="info-card__icon">{I["pin"]}</div>
            <h3>Адрес мастерской</h3>
            <p>{SITE["address"]}<br>
              <span class="small muted">Приём заказов и образцы камня — ежедневно</span></p>
          </div>
          <div class="info-card reveal">
            <div class="info-card__icon">{I["clock"]}</div>
            <h3>Режим работы</h3>
            <p>{SITE["hours"]}<br>
              <span class="small muted">Установка на кладбище — по договорённости</span></p>
          </div>
          <div class="info-card reveal">
            <div class="info-card__icon">{I["mail"]}</div>
            <h3>Почта и мессенджеры</h3>
            <p><a href="mailto:{SITE["email"]}">{SITE["email"]}</a><br>
              <a href="{SITE["wa"]}" target="_blank" rel="noopener">WhatsApp</a> ·
              <a href="{SITE["tg"]}" target="_blank" rel="noopener">Telegram</a></p>
          </div>
        </div>

        <div class="grid grid--2" style="margin-top:34px;gap:34px;align-items:start">
          <div class="info-card reveal" style="padding:clamp(22px,2.6vw,34px)">
            <span class="kicker">Заявка</span>
            <h2 style="margin-bottom:10px">Оставьте заявку</h2>
            <p class="muted" style="margin-bottom:20px">Перезвоним в течение 15 минут, ответим на вопросы
              и при необходимости запишем на бесплатный выезд замерщика.</p>
            {lead_form("contacts", "Отправить заявку")}
          </div>
          <div>
            <div class="map reveal">
              <div class="map__placeholder">
                {I["pin"]}
                <strong>Мастерская в Стерлитамаке</strong>
                <p>{SITE["address"]}</p>
                <p class="small muted">Здесь будет интерактивная карта. Пока — кнопка, которая откроет
                  адрес в Яндекс.Картах.</p>
                <a class="btn" href="{SITE["map_link"]}" target="_blank" rel="noopener">Открыть в Яндекс.Картах</a>
              </div>
              {MAP_NOTE}
            </div>
            <div class="info-card reveal" style="margin-top:22px">
              <h3>Куда мы выезжаем</h3>
              <p>Стерлитамак, Салават, Ишимбай, Кумертау, Стерлибашево, а также Гафурийский и
                Аургазинский районы. Работаем на всех кладбищах Стерлитамака и окрестностей.
                Доставка до 60 км — бесплатно при заказе от 30 000 ₽.</p>
            </div>
          </div>
        </div>
      </div>
    </section>''',
    f'''<section class="section section--dark">
      <div class="container">
        <div class="section-head section-head--center reveal">
          <span class="kicker">Если беда случилась сейчас</span>
          <h2>Позвоните — подскажем, что делать</h2>
          <p>Мы работаем с 2007 года и знаем, что в такой момент важно не ошибиться и не переплатить.
            Консультация бесплатная, без навязывания услуг.</p>
        </div>
        <div style="display:flex;gap:16px;justify-content:center;flex-wrap:wrap">
          <a class="btn btn--lg" href="{SITE["phone_href"]}">{I["phone"]} {SITE["phone"]}</a>
          <a class="btn btn--lg btn--light" href="{SITE["phone2_href"]}">{SITE["phone2"]}</a>
        </div>
      </div>
    </section>''',
])

render("kontakty.html",
       "Контакты ритуальной мастерской в Стерлитамаке — адрес, телефон, режим работы | %s" % SITE["name"],
       "Контакты ритуальной мастерской «Вечная память» в Стерлитамаке: телефон +7 (3473) 00-00-00, "
       "адрес мастерской, режим работы, бесплатный выезд замерщика.",
       "kontakty.html", kontakty_body)

# ==========================================================================
# ЮРИДИЧЕСКИЕ СТРАНИЦЫ (шаблоны — проверьте у юриста перед публикацией)
# ==========================================================================
politika_body = "\n".join([
    page_head("Политика конфиденциальности",
              "Как мы обрабатываем и защищаем персональные данные посетителей сайта и заказчиков.",
              None, "Политика конфиденциальности"),
    f'''<section class="section section--paper">
      <div class="container">
        <div class="prose">
          <p>Настоящая политика определяет порядок обработки персональных данных и меры по обеспечению их
            безопасности, применяемые {SITE["legal"]} (далее — Оператор).</p>

          <div class="note">Это типовой шаблон. Перед публикацией подставьте свои реквизиты
            ({SITE["inn"]}), проверьте формулировки у юриста и разместите документ по постоянному адресу.</div>

          <h2>1. Общие положения</h2>
          <p>Политика разработана в соответствии с Федеральным законом от 27.07.2006 № 152-ФЗ
            «О персональных данных». Используя сайт и отправляя заявку через формы, вы подтверждаете
            согласие с условиями настоящей политики.</p>

          <h2>2. Какие данные мы обрабатываем</h2>
          <ul>
            <li>имя, указанное в форме заявки;</li>
            <li>номер телефона, адрес электронной почты;</li>
            <li>сведения, которые вы добровольно указываете в комментарии к заявке;</li>
            <li>обезличенные данные о посещении сайта (cookies, статистика).</li>
          </ul>
          <p>Оператор не обрабатывает специальные категории персональных данных и не собирает данные
            несовершеннолетних.</p>

          <h2>3. Цели обработки</h2>
          <ul>
            <li>обратная связь по заявке, консультация, расчёт стоимости;</li>
            <li>заключение и исполнение договора на изготовление и установку изделий;</li>
            <li>информирование о статусе заказа.</li>
          </ul>

          <h2>4. Правовые основания</h2>
          <p>Обработка осуществляется на основании согласия субъекта персональных данных, выраженного
            путём отметки в соответствующем поле формы, а также в целях исполнения договора.</p>

          <h2>5. Порядок и сроки обработки</h2>
          <p>Данные обрабатываются с использованием средств автоматизации и без них, хранятся не дольше,
            чем этого требуют цели обработки, либо до отзыва согласия. Передача третьим лицам возможна
            только в объёме, необходимом для исполнения заказа, или по требованию закона.</p>

          <h2>6. Права субъекта персональных данных</h2>
          <p>Вы вправе запросить сведения об обработке своих данных, потребовать их уточнения, блокирования
            или уничтожения, а также отозвать согласие. Для этого направьте обращение на
            <a href="mailto:{SITE["email"]}">{SITE["email"]}</a> или позвоните по телефону
            <a href="{SITE["phone_href"]}">{SITE["phone"]}</a>.</p>

          <h2>7. Меры защиты</h2>
          <p>Оператор принимает необходимые правовые, организационные и технические меры для защиты
            персональных данных от неправомерного доступа, уничтожения, изменения и распространения.</p>

          <h2>8. Изменения политики</h2>
          <p>Оператор вправе изменять настоящую политику. Новая редакция вступает в силу с момента
            размещения на сайте.</p>

          <h2>Контакты оператора</h2>
          <p>{SITE["legal"]}<br>{SITE["address"]}<br>{SITE["inn"]}<br>
            Телефон: <a href="{SITE["phone_href"]}">{SITE["phone"]}</a><br>
            E-mail: <a href="mailto:{SITE["email"]}">{SITE["email"]}</a></p>
        </div>
      </div>
    </section>''',
])

render("politika.html",
       "Политика конфиденциальности — %s" % SITE["name"],
       "Политика обработки персональных данных ритуальной мастерской «Вечная память», Стерлитамак.",
       "politika.html", politika_body)

oferta_body = "\n".join([
    page_head("Публичная оферта",
              "Условия оказания услуг по изготовлению, установке и благоустройству памятников.",
              None, "Публичная оферта"),
    f'''<section class="section section--paper">
      <div class="container">
        <div class="prose">
          <div class="note">Типовой шаблон. Перед публикацией подставьте реквизиты, сроки и условия,
            которые используете на практике, и проверьте документ у юриста.</div>

          <h2>1. Предмет договора</h2>
          <p>Исполнитель изготавливает, доставляет и устанавливает памятники, элементы благоустройства
            захоронений, а также изготавливает ритуальные товары, а Заказчик принимает и оплачивает
            результат работ на условиях настоящей оферты.</p>

          <h2>2. Оформление заказа</h2>
          <ul>
            <li>Заказ оформляется после консультации, замера участка и согласования эскиза;</li>
            <li>существенные условия (модель, материал, размеры, оформление, срок) фиксируются в договоре
              и приложении к нему;</li>
            <li>изображения и описания на сайте носят справочный характер, точная цена определяется сметой.</li>
          </ul>

          <h2>3. Цена и порядок оплаты</h2>
          <ul>
            <li>стоимость определяется сметой и фиксируется в договоре;</li>
            <li>аванс — 30% от стоимости, остаток — после установки и приёмки работ;</li>
            <li>возможна рассрочка 0% на условиях, согласованных сторонами.</li>
          </ul>

          <h2>4. Сроки</h2>
          <p>Стандартный срок изготовления — от 7 до 21 дня с момента согласования эскиза и внесения аванса.
            Сроки могут увеличиваться при индивидуальной резке и при погодных условиях,
            препятствующих монтажу.</p>

          <h2>5. Гарантия</h2>
          <p>Гарантия на конструкцию и установку — 10 лет, на гравировку и фотокерамику — 5 лет, при условии
            соблюдения правил эксплуатации и отсутствия внешнего воздействия. Гарантия не распространяется
            на повреждения, возникшие по вине третьих лиц.</p>

          <h2>6. Ответственность сторон</h2>
          <p>Стороны несут ответственность в соответствии с законодательством РФ. Исполнитель не отвечает
            за решения, принятые Заказчиком на основании справочной информации сайта без согласования
            с менеджером.</p>

          <h2>7. Реквизиты исполнителя</h2>
          <p>{SITE["legal"]}<br>{SITE["address"]}<br>{SITE["inn"]}<br>
            Телефон: <a href="{SITE["phone_href"]}">{SITE["phone"]}</a><br>
            E-mail: <a href="mailto:{SITE["email"]}">{SITE["email"]}</a></p>
        </div>
      </div>
    </section>''',
])

render("oferta.html",
       "Публичная оферта — %s" % SITE["name"],
       "Условия оказания услуг ритуальной мастерской «Вечная память» в Стерлитамаке: заказ, оплата, сроки, гарантия.",
       "oferta.html", oferta_body)

print("Сборка страниц завершена.")
