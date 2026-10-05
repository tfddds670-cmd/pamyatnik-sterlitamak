# -*- coding: utf-8 -*-
"""
Генератор SVG-заглушек для сайта ритуальной мастерской.
Изображения стилизованные (не фото) — их легко заменить на реальные снимки,
сохранив те же имена файлов.
"""
import os
import math
import random

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "img")
os.makedirs(OUT, exist_ok=True)

W, H = 900, 675
random.seed(20240517)

PALETTES = {
    "gabbro": ("#4d545c", "#2a3037", "#14171b", "Габбро-диабаз"),
    "grey": ("#9aa1a8", "#6d747c", "#3d434a", "Серый гранит"),
    "marble": ("#fbf9f4", "#e3ded2", "#bdb6a6", "Мрамор"),
    "red": ("#8a4a3f", "#5d2c25", "#301512", "Красный гранит"),
    "green": ("#5b7367", "#33463d", "#182420", "Зелёный гранит"),
    "dymovsky": ("#7d7f86", "#4f5259", "#282a2f", "Дымовский гранит"),
}

DEFS_COMMON = """
  <defs>
    <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#eef1f5"/>
      <stop offset="0.55" stop-color="#e2e6ea"/>
      <stop offset="1" stop-color="#d5dade"/>
    </linearGradient>
    <linearGradient id="ground" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#9aa694"/>
      <stop offset="1" stop-color="#77836f"/>
    </linearGradient>
    <radialGradient id="vignette" cx="0.5" cy="0.5" r="0.78">
      <stop offset="0.35" stop-color="#000" stop-opacity="0"/>
      <stop offset="1" stop-color="#000" stop-opacity="0.16"/>
    </radialGradient>
    <linearGradient id="sheen" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#fff" stop-opacity="0.26"/>
      <stop offset="0.42" stop-color="#fff" stop-opacity="0.05"/>
      <stop offset="1" stop-color="#fff" stop-opacity="0"/>
    </linearGradient>
    <filter id="speckle" x="-5%" y="-5%" width="110%" height="110%">
      <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="3" seed="7" result="n"/>
      <feColorMatrix in="n" type="saturate" values="0" result="g"/>
      <feComponentTransfer in="g" result="g2">
        <feFuncA type="linear" slope="0.5" intercept="0"/>
      </feComponentTransfer>
      <feComposite in="g2" in2="SourceGraphic" operator="in"/>
    </filter>
    <filter id="soft" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="16"/>
    </filter>
    <filter id="soft8" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="8"/>
    </filter>
  </defs>
"""


def scene(bg_extra=""):
    return (
        '<rect width="%d" height="%d" fill="url(#sky)"/>' % (W, H)
        + bg_extra
        + '<ellipse cx="90" cy="500" rx="200" ry="120" fill="#5d6d57" opacity="0.55" filter="url(#soft8)"/>'
        + '<ellipse cx="820" cy="496" rx="220" ry="130" fill="#54644f" opacity="0.5" filter="url(#soft8)"/>'
        + '<ellipse cx="450" cy="470" rx="300" ry="90" fill="#8fa08a" opacity="0.45" filter="url(#soft)"/>'
        + '<rect y="520" width="%d" height="%d" fill="url(#ground)"/>' % (W, H - 520)
        + '<path d="M0 520 Q225 502 450 519 T900 514 L900 545 L0 545 Z" fill="#8d9a83" opacity="0.6"/>'
    )


def granite_defs(key):
    light, mid, dark, _ = PALETTES[key]
    return """
    <linearGradient id="granite" x1="0.05" y1="0" x2="0.95" y2="1">
      <stop offset="0" stop-color="%s"/>
      <stop offset="0.45" stop-color="%s"/>
      <stop offset="1" stop-color="%s"/>
    </linearGradient>
    <linearGradient id="graniteDark" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="%s"/>
      <stop offset="1" stop-color="%s"/>
    </linearGradient>
    """ % (light, mid, dark, mid, dark)


def speckle_layer(x, y, w, h, r=6):
    return (
        '<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="#000" opacity="0.20" filter="url(#speckle)"/>'
        % (x, y, w, h, r)
    )


def shadow(cx, cy, rx, ry):
    return '<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="#1b2118" opacity="0.30" filter="url(#soft8)"/>' % (
        cx, cy, rx, ry)


def base_block(cx, top, w, h, key, rx=4):
    x = cx - w / 2.0
    return (
        '<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="url(#graniteDark)"/>' % (x, top, w, h, rx)
        + speckle_layer(x, top, w, h, rx)
        + '<rect x="%s" y="%s" width="%s" height="6" fill="#fff" opacity="0.10"/>' % (x, top, w)
    )


def stele(cx, top, w, h, key, kind="classic", grad="granite"):
    """kind: classic | arch | wave | cross | crescent | heart | angel | flat"""
    x = cx - w / 2.0
    bottom = top + h
    if kind in ("classic", "cross", "angel"):
        r = w * 0.16
        path = (
            "M{x} {b} L{x} {t1} Q{x} {t} {x1} {t} L{x2} {t} Q{x3} {t} {x3} {t1} L{x3} {b} Z"
        ).format(x=x, b=bottom, t=top, t1=top + r, x1=x + r, x2=x + w - r, x3=x + w)
    elif kind == "arch":
        path = "M{x} {b} L{x} {t1} A{r} {r} 0 0 1 {x3} {t1} L{x3} {b} Z".format(
            x=x, b=bottom, t1=top + w / 2.0, r=w / 2.0, x3=x + w)
    elif kind == "wave":
        path = (
            "M{x} {b} L{x} {t} C {x1} {t2} {x2} {t3} {x3} {t} L{x3} {b} Z"
        ).format(x=x, b=bottom, t=top, x1=x + w * 0.25, x2=x + w * 0.75, x3=x + w,
                 t2=top - 34, t3=top + 54)
    elif kind == "crescent":
        path = "M{x} {b} L{x} {t1} Q{x} {t} {cx} {t} Q{x3} {t} {x3} {t1} L{x3} {b} Z".format(
            x=x, b=bottom, t=top - 26, t1=top + 40, cx=cx, x3=x + w)
    elif kind == "heart":
        path = (
            "M{x} {b} L{x} {t2} C {x} {t} {cx} {t} {cx} {tm} C {cx} {t} {x3} {t} {x3} {t2} L{x3} {b} Z"
        ).format(x=x, b=bottom, t=top, t2=top + 54, cx=cx, x3=x + w, tm=top + 86)
    else:  # flat
        path = "M{x} {b} L{x} {t} L{x3} {t} L{x3} {b} Z".format(x=x, b=bottom, t=top, x3=x + w)

    out = '<path d="%s" fill="url(#%s)"/>' % (path, grad)
    out += '<path d="%s" fill="none" stroke="#000" stroke-opacity="0.28" stroke-width="2"/>' % path
    if kind == "flat":
        out += speckle_layer(x, top, w, h, 2)
    else:
        out += (
            '<clipPath id="clipStele"><path d="%s"/></clipPath>'
            '<g clip-path="url(#clipStele)">'
            '<rect x="%s" y="%s" width="%s" height="%s" fill="#000" opacity="0.20" filter="url(#speckle)"/>'
            '<rect x="%s" y="%s" width="%s" height="%s" fill="url(#sheen)"/>'
            "</g>" % (path, x, top, w, h, x, top, w, h)
        )
    return out


def engraving_cross(cx, cy, s=1.0):
    """Православный крест: верхняя короткая, средняя длинная и нижняя косая перекладины."""
    w1, w2, w3 = 34 * s, 92 * s, 58 * s
    sw = round(7 * s, 2)
    return (
        '<g opacity="0.9" fill="#e9e4d8">'
        '<rect x="{vx}" y="{vy}" width="{sw}" height="{vh}" rx="{r}"/>'
        '<rect x="{x1}" y="{y1}" width="{w1}" height="{sw}" rx="{r}"/>'
        '<rect x="{x2}" y="{y2}" width="{w2}" height="{sw}" rx="{r}"/>'
        '<rect x="{x3}" y="{y3}" width="{w3}" height="{sw}" rx="{r}" transform="rotate(-16 {rx} {ry})"/>'
        "</g>"
    ).format(
        vx=round(cx - sw / 2, 1), vy=round(cy - 74 * s, 1), vh=round(150 * s, 1), sw=sw,
        r=round(sw / 2, 1),
        x1=round(cx - w1 / 2, 1), y1=round(cy - 50 * s, 1), w1=round(w1, 1),
        x2=round(cx - w2 / 2, 1), y2=round(cy - 12 * s, 1), w2=round(w2, 1),
        x3=round(cx - w3 / 2, 1), y3=round(cy + 44 * s, 1), w3=round(w3, 1),
        rx=cx, ry=round(cy + 44 * s + sw / 2, 1))


def engraving_portrait(cx, cy, r=30):
    return (
        '<g opacity="0.55" fill="none" stroke="#e9e4d8" stroke-width="2.4">'
        '<ellipse cx="%s" cy="%s" rx="%s" ry="%s"/>'
        '<circle cx="%s" cy="%s" r="%s"/>'
        '<path d="M%s %s Q %s %s %s %s"/></g>'
        % (cx, cy, r * 1.15, r * 1.35, cx, cy - r * 0.28, r * 0.42,
           cx - r * 0.62, cy + r * 0.95, cx, cy + r * 0.42, cx + r * 0.62, cy + r * 0.95)
    )


def engraving_lines(cx, cy, n=3, w=90):
    out = '<g opacity="0.5" fill="#e9e4d8">'
    for i in range(n):
        ww = w if i < n - 1 else w * 0.62
        out += '<rect x="%s" y="%s" width="%s" height="5" rx="2.5"/>' % (cx - ww / 2.0, cy + i * 20, ww)
    return out + "</g>"


def engraving_crescent(cx, cy, r=30):
    """Полумесяц: круг минус смещённый круг (через маску)."""
    return (
        '<mask id="mCrescent">'
        '<rect x="0" y="0" width="{w}" height="{h}" fill="#fff"/>'
        '<circle cx="{ox}" cy="{oy}" r="{ir}" fill="#000"/>'
        "</mask>"
        '<circle cx="{cx}" cy="{cy}" r="{r}" fill="#e9e4d8" opacity="0.92" mask="url(#mCrescent)"/>'
        '<path d="M {sx} {sy} l 5 11 l 12 1.6 l -9 8.4 l 2.4 11.8 l -10.4 -5.8 l -10.4 5.8 l 2.4 -11.8 l -9 -8.4 l 12 -1.6 Z" '
        'fill="#e9e4d8" opacity="0.92"/>'
    ).format(w=W, h=H, cx=cx, cy=cy, r=r,
             ox=round(cx + r * 0.42, 1), oy=round(cy - r * 0.16, 1), ir=round(r * 0.94, 1),
             sx=round(cx - r * 1.62, 1), sy=round(cy - r * 0.72, 1))


def angel_silhouette(cx, cy, s=1.0):
    return (
        '<g opacity="0.7" fill="#e9e4d8" transform="translate(%s,%s) scale(%s)">'
        '<path d="M0 -46 C 8 -46 12 -38 12 -30 L 12 26 L -12 26 L -12 -30 C -12 -38 -8 -46 0 -46 Z"/>'
        '<path d="M-12 -22 C -40 -30 -52 -12 -46 6 C -36 -8 -22 -12 -12 -6 Z" opacity="0.85"/>'
        '<path d="M12 -22 C 40 -30 52 -12 46 6 C 36 -8 22 -12 12 -6 Z" opacity="0.85"/>'
        '<circle cx="0" cy="-56" r="11"/></g>' % (cx, cy, s)
    )


def wreath(name, ring_r, flowers, palette, ribbon_text=None, legs=True, cy=None):
    w, h = 900, 675
    cx = w / 2.0
    cy = 300.0 if cy is None else cy
    out = ['<rect width="%d" height="%d" fill="url(#sky)"/>' % (w, h)]
    out.append('<ellipse cx="90" cy="520" rx="220" ry="110" fill="#5d6d57" opacity="0.5" filter="url(#soft8)"/>')
    out.append('<ellipse cx="820" cy="516" rx="230" ry="120" fill="#54644f" opacity="0.45" filter="url(#soft8)"/>')
    out.append('<rect y="520" width="%d" height="%d" fill="url(#ground)"/>' % (w, h - 520))
    out.append('<path d="M0 520 Q225 504 450 519 T900 514 L900 545 L0 545 Z" fill="#8d9a83" opacity="0.6"/>')
    out.append('<ellipse cx="%s" cy="%s" rx="%s" ry="22" fill="#1b2118" opacity="0.22" filter="url(#soft8)"/>'
               % (cx, cy + ring_r + 60, round(ring_r * 0.95, 1)))
    thickness = ring_r * 0.34
    out.append('<circle cx="%s" cy="%s" r="%s" fill="none" stroke="#2b4527" stroke-width="%s"/>'
               % (cx, cy, ring_r, thickness))
    out.append('<circle cx="%s" cy="%s" r="%s" fill="none" stroke="#3d5c37" stroke-width="%s" opacity="0.95"/>'
               % (cx, cy, ring_r, thickness * 0.7))
    # листья в два ряда
    for i in range(flowers * 4):
        a = 2 * math.pi * i / (flowers * 4.0)
        for k, off in enumerate((-0.34, 0.34)):
            rr = ring_r + thickness * off
            x = cx + rr * math.cos(a)
            y = cy + rr * math.sin(a)
            rot = math.degrees(a) + 90 + (18 if k else -18)
            out.append('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="%s" opacity="0.95" transform="rotate(%s %s %s)"/>'
                       % (round(x, 1), round(y, 1), round(thickness * 0.36, 1), round(thickness * 0.17, 1),
                          "#4a7040" if k else "#3e6038", round(rot, 1), round(x, 1), round(y, 1)))
    # цветы
    colors = palette
    for i in range(flowers):
        a = 2 * math.pi * i / flowers + 0.12
        x = cx + ring_r * math.cos(a)
        y = cy + ring_r * math.sin(a)
        c = colors[i % len(colors)]
        r = thickness * 0.52
        out.append('<g transform="translate(%s,%s)">' % (round(x, 1), round(y, 1)))
        for k in range(6):
            ang = 60 * k
            out.append('<ellipse cx="0" cy="%s" rx="%s" ry="%s" fill="%s" opacity="0.98" transform="rotate(%s)"/>'
                       % (round(-r * 0.60, 1), round(r * 0.46, 1), round(r * 0.82, 1), c, ang))
        out.append('<circle cx="0" cy="0" r="%s" fill="#e8c65c"/></g>' % round(r * 0.38, 1))
    if ribbon_text:
        out.append('<g transform="translate(%s,%s)">' % (cx, cy + ring_r * 0.58))
        out.append('<rect x="-140" y="-36" width="280" height="72" rx="6" fill="#1b1f24" opacity="0.95"/>')
        out.append('<rect x="-140" y="-36" width="280" height="72" rx="6" fill="none" stroke="#c8a24a" stroke-width="2" opacity="0.85"/>')
        fs = min(28, int(250.0 / max(6, len(ribbon_text)) * 1.6))
        out.append('<text x="0" y="%s" text-anchor="middle" font-family="Georgia,serif" font-size="%s" fill="#e6d6ac">%s</text>'
                   % (round(fs * 0.32, 1), fs, ribbon_text))
        out.append("</g>")
    if legs:
        out.append('<g stroke="#2b4527" stroke-width="16" fill="none" opacity="0.95">'
                   '<path d="M%s %s L%s %s"/><path d="M%s %s L%s %s"/></g>'
                   % (cx - ring_r * 0.55, cy + ring_r * 0.85, cx - ring_r * 0.62, 618,
                      cx + ring_r * 0.55, cy + ring_r * 0.85, cx + ring_r * 0.62, 618))
    out.append('<rect width="%d" height="%d" fill="url(#vignette)"/>' % (w, h))
    write(name, wrap("\n".join(out)))


def wrap(body, defs=DEFS_COMMON):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" role="img">'
            % (W, H, W, H)) + defs + body + "</svg>"


def write(name, content):
    p = os.path.join(OUT, name)
    with open(p, "w", encoding="utf-8") as f:
        f.write(content)
    print("ok", name)


# ---------------------------------------------------------------- памятники
def monument(name, key, kind, *, w=250, h=390, base_w=300, base_h=58, extras=None,
             portrait=True, lines=True, top_y=150):
    body = [scene(), granite_defs(key)]
    cx = W / 2.0
    body.append(shadow(cx, top_y + h + base_h + 6, base_w * 0.78, 26))
    if extras == "platform":
        body.append('<rect x="%s" y="%s" width="360" height="14" rx="4" fill="#cdc7b8" opacity="0.95"/>'
                    % (cx - 180, top_y + h + base_h + 2))
        body.append('<rect x="%s" y="%s" width="360" height="70" fill="#b9b3a4" opacity="0.9"/>'
                    % (cx - 180, top_y + h + base_h + 16))
        for i in range(3):
            body.append('<rect x="%s" y="%s" width="360" height="2" fill="#8f8a7d" opacity="0.6"/>'
                        % (cx - 180, top_y + h + base_h + 34 + i * 16))
    if extras == "double":
        body.append(stele(cx - w * 0.56, top_y + 26, w * 0.9, h - 26, key, kind))
        body.append(stele(cx + w * 0.56, top_y + 26, w * 0.9, h - 26, key, kind))
        body.append(base_block(cx, top_y + h + 6, base_w * 1.35, base_h, key))
    else:
        body.append(stele(cx, top_y, w, h, key, kind))
        body.append(base_block(cx, top_y + h + 6, base_w, base_h, key))
    if extras == "fence":
        fy = top_y + h + base_h + 24
        body.append('<g stroke="#3b3f45" stroke-width="4" fill="none" opacity="0.95">'
                    '<path d="M%s %s L%s %s"/></g>' % (cx - 220, fy, cx + 220, fy))
    if portrait:
        body.append(engraving_portrait(cx, top_y + h * 0.27, max(22, w * 0.155)))
    if kind == "cross" or extras == "cross":
        body.append(engraving_cross(cx, top_y + h * 0.44, max(0.7, w / 230.0)))
    if kind == "crescent":
        body.append(engraving_crescent(cx, top_y + h * 0.27, w * 0.15))
    if kind == "angel":
        body.append(angel_silhouette(cx, top_y + h * 0.5, max(0.9, w / 190.0)))
    if kind == "heart":
        body.append('<path d="M{cx} {y2} C {a} {b} {a2} {c} {cx} {d} C {a3} {c} {a4} {b} {cx} {y2} Z" '
                    'fill="none" stroke="#e9e4d8" stroke-width="{sw}" opacity="0.8"/>'.format(
                        cx=cx, y2=top_y + h * 0.22, a=cx - w * 0.22, a2=cx - w * 0.34,
                        a3=cx + w * 0.34, a4=cx + w * 0.22,
                        b=top_y + h * 0.13, c=top_y + h * 0.38, d=top_y + h * 0.47,
                        sw=round(max(4, w * 0.03), 1)))
    if lines:
        body.append(engraving_lines(cx, top_y + h * 0.72, 3, w * 0.6))
    body.append('<rect width="%d" height="%d" fill="url(#vignette)"/>' % (W, H))
    write(name, wrap("\n".join(body)))


monument("pamyatnik-klassika.svg", "gabbro", "classic")
monument("pamyatnik-volna.svg", "grey", "wave")
monument("pamyatnik-krest.svg", "gabbro", "classic", extras="cross", portrait=False)
monument("pamyatnik-musulmanskij.svg", "green", "crescent", portrait=False, lines=True)
monument("pamyatnik-detskij.svg", "grey", "heart", w=210, h=310, base_w=250, top_y=210, portrait=False)
monument("pamyatnik-angel.svg", "gabbro", "angel", w=270, h=400, base_w=320, portrait=False, lines=False)
monument("pamyatnik-dvojnoj.svg", "dymovsky", "classic", extras="double", w=210, h=350, base_w=330)
monument("pamyatnik-mramor.svg", "marble", "arch", w=225, h=360)
monument("pamyatnik-krasnyj.svg", "red", "arch", w=235, h=380)
monument("pamyatnik-gorizontalnyj.svg", "gabbro", "flat", w=400, h=190, base_w=420, base_h=48, top_y=300)
monument("kompleks-pravoslavnyj.svg", "gabbro", "classic", w=270, h=390, base_w=330,
         extras="platform", portrait=True)
monument("kompleks-semejnyj.svg", "dymovsky", "arch", extras="double", w=215, h=360, base_w=340)
monument("kompleks-elitnyj.svg", "gabbro", "angel", w=300, h=410, base_w=350,
         extras="platform", portrait=False, lines=False)
monument("pamyatnik-svo.svg", "gabbro", "classic", w=265, h=395, extras="cross", portrait=True)

# ---------------------------------------------------------------- услуги
def service_ogradka(name, style):
    body = [scene()]
    cx, cy = W / 2.0, 430
    rail = "#2f3338" if style == "kovka" else "#484d54"
    body.append('<rect x="%s" y="%s" width="520" height="80" fill="#b7b1a2" opacity="0.85"/>' % (cx - 260, 470))
    body.append('<g stroke="%s" stroke-width="7" fill="none">' % rail)
    body.append('<path d="M%s 470 L%s 470"/><path d="M%s 350 L%s 350"/><path d="M%s 430 L%s 430"/>'
                % (cx - 260, cx + 260, cx - 260, cx + 260, cx - 260, cx + 260))
    for i in range(9):
        x = cx - 240 + i * 60
        body.append('<path d="M%s 470 L%s 300"/>' % (x, x))
    body.append("</g>")
    if style == "kovka":
        body.append('<g stroke="%s" stroke-width="4" fill="none" opacity="0.95">' % rail)
        for i in range(8):
            x = cx - 210 + i * 60
            body.append('<path d="M%s 400 q 30 -34 60 0"/>' % x)
        body.append("</g>")
    body.append('<rect width="%d" height="%d" fill="url(#vignette)"/>' % (W, H))
    write(name, wrap("\n".join(body)))


def service_plitka(name):
    """Облицованная плиткой площадка вокруг памятника (в перспективе)."""
    body = [scene(), granite_defs("gabbro")]
    cx = W / 2.0
    top_y, top_w = 430.0, 430.0
    bot_y, bot_w = 615.0, 600.0
    vpx, vpy = cx, 250.0

    def edge_w(y):
        t = (y - top_y) / (bot_y - top_y)
        return top_w + (bot_w - top_w) * t

    def edge_x(y, side):
        return cx + side * edge_w(y) / 2.0

    # плитка площадки
    body.append('<path d="M%s %s L%s %s L%s %s L%s %s Z" fill="#d5cfc1"/>'
                % (edge_x(top_y, -1), top_y, edge_x(top_y, 1), top_y, edge_x(bot_y, 1), bot_y, edge_x(bot_y, -1), bot_y))
    body.append('<g stroke="#aaa392" stroke-width="2.5" opacity="0.9">')
    for y in [462, 496, 532, 572]:
        body.append('<path d="M%s %s L%s %s"/>' % (edge_x(y, -1), y, edge_x(y, 1), y))
    for i in [-0.62, -0.24, 0.24, 0.62]:
        x1 = cx + i * edge_w(top_y) / 2.0
        x2 = cx + i * edge_w(bot_y) / 2.0
        body.append('<path d="M%s %s L%s %s"/>' % (x1, top_y, x2, bot_y))
    body.append("</g>")
    # бордюр
    body.append('<path d="M%s %s L%s %s L%s %s L%s %s Z" fill="#c3bcab"/>'
                % (edge_x(bot_y, -1) - 10, bot_y, edge_x(bot_y, 1) + 10, bot_y,
                   edge_x(bot_y, 1) + 4, bot_y + 16, edge_x(bot_y, -1) - 4, bot_y + 16))
    # памятник
    body.append(shadow(cx, top_y + 6, 160, 18))
    body.append(stele(cx, 195, 200, 190, "gabbro", "classic"))
    body.append(base_block(cx, 385, 235, 48, "gabbro"))
    body.append(engraving_lines(cx, 300, 3, 120))
    # ваза
    body.append('<path d="M%s %s L%s %s L%s %s L%s %s Z" fill="#b9b2a1" opacity="0.95"/>'
                % (cx + 140, 520, cx + 190, 520, cx + 182, 566, cx + 148, 566))
    body.append('<rect width="%d" height="%d" fill="url(#vignette)"/>' % (W, H))
    write(name, wrap("\n".join(body)))


def service_gravirovka(name):
    body = ['<rect width="%d" height="%d" fill="#20242a"/>' % (W, H), granite_defs("gabbro")]
    body.append('<rect x="60" y="40" width="%s" height="%s" rx="10" fill="url(#granite)"/>' % (W - 120, H - 80))
    body.append(speckle_layer(60, 40, W - 120, H - 80, 10))
    cx, cy = W / 2.0, H / 2.0
    body.append(engraving_portrait(cx - 210, cy - 30, 96))
    body.append('<g opacity="0.92" fill="#e9e4d8" font-family="Georgia,serif" text-anchor="middle">'
                '<text x="%s" y="%s" font-size="46">ИВАНОВ</text>'
                '<text x="%s" y="%s" font-size="38">Пётр Сергеевич</text>'
                '<text x="%s" y="%s" font-size="28" opacity="0.8">1949 — 2024</text>'
                '<text x="%s" y="%s" font-size="24" opacity="0.65" font-style="italic">Помним. Любим. Скорбим.</text></g>'
                % (cx + 130, cy - 90, cx + 130, cy - 24, cx + 130, cy + 26, cx + 130, cy + 96))
    body.append(engraving_cross(cx + 330, cy + 10, 1.1))
    body.append('<rect width="%d" height="%d" fill="url(#vignette)"/>' % (W, H))
    write(name, wrap("\n".join(body)))


def service_ustanovka(name):
    """Монтаж памятника: стропы, крюк и уровень."""
    body = [scene(), granite_defs("gabbro"),
            '<linearGradient id="granite2" x1="0" y1="0" x2="1" y2="1">'
            '<stop offset="0" stop-color="#9aa1a8"/><stop offset="1" stop-color="#3d434a"/></linearGradient>']
    cx = W / 2.0
    body.append(shadow(cx - 150, 640, 190, 24))
    body.append(shadow(cx + 150, 640, 180, 24))
    # стропы (второй памятник уже опущен)
    body.append('<g stroke="#d9b24a" stroke-width="9" stroke-linecap="round" fill="none" opacity="0.95">'
                '<path d="M%s %s L%s %s"/><path d="M%s %s L%s %s"/></g>'
                % (cx - 190, 210, cx - 155, 30, cx - 110, 210, cx - 120, 30))
    body.append('<circle cx="%s" cy="24" r="15" fill="none" stroke="#c8a24a" stroke-width="8" opacity="0.95"/>' % (cx - 138))
    # памятник на стропах
    body.append(stele(cx - 150, 190, 200, 330, "gabbro", "classic"))
    body.append(base_block(cx - 150, 526, 235, 48, "gabbro"))
    body.append(engraving_lines(cx - 150, 400, 3, 118))
    # установленный памятник
    body.append(stele(cx + 150, 300, 175, 226, "grey", "arch", grad="granite2"))
    body.append(base_block(cx + 150, 532, 215, 46, "grey"))
    # уровень на основании
    body.append('<g transform="translate(%s,%s)">'
                '<rect x="-70" y="-14" width="140" height="28" rx="6" fill="#e0b64c"/>'
                '<rect x="-8" y="-8" width="16" height="16" rx="8" fill="#f6f0dc"/>'
                '<rect x="-56" y="-5" width="30" height="10" rx="5" fill="#b98f2e" opacity="0.8"/>'
                '<rect x="26" y="-5" width="30" height="10" rx="5" fill="#b98f2e" opacity="0.8"/></g>'
                % (cx + 150, 512))
    body.append('<rect width="%d" height="%d" fill="url(#vignette)"/>' % (W, H))
    write(name, wrap("\n".join(body)))


def background_crane():
    return ""


service_ogradka("usluga-ogradka-kovanaya.svg", "kovka")
service_ogradka("usluga-ogradka-svarnaya.svg", "svarka")
service_plitka("usluga-plitka.svg")
service_gravirovka("usluga-gravirovka.svg")
service_ustanovka("usluga-ustanovka.svg")

# ---------------------------------------------------------------- венки и товары
wreath("venok-skorbi.svg", 175, 18, ["#f3f0e8", "#e7e2d6", "#f7f5ef"], "СКОРБИМ")
wreath("venok-mame.svg", 215, 24, ["#f6f4ee", "#dcd8cc", "#efece2"], "ЛЮБИМОЙ МАМЕ")
wreath("venok-ot-vseh.svg", 195, 20, ["#efece2", "#c9b98a", "#f6f4ee"], "ОТ ВСЕХ СКОРБЯЩИХ")
wreath("venok-dubovyj.svg", 185, 16, ["#5f7a4a", "#8fa86a", "#4d6639"], None)


def basket(name):
    body = ['<rect width="%d" height="%d" fill="url(#sky)"/>' % (W, H),
            '<rect y="520" width="%d" height="%d" fill="url(#ground)"/>' % (W, H - 520)]
    cx, cy = W / 2.0, 420
    body.append('<ellipse cx="%s" cy="%s" rx="200" ry="24" fill="#1b2118" opacity="0.25" filter="url(#soft8)"/>' % (cx, cy + 90))
    body.append('<path d="M%s %s L%s %s L%s %s L%s %s Z" fill="#8b6a45"/>' % (
        cx - 130, cy - 60, cx + 130, cy - 60, cx + 95, cy + 80, cx - 95, cy + 80))
    body.append('<g stroke="#6d5233" stroke-width="3" opacity="0.8">')
    for i in range(1, 5):
        body.append('<path d="M%s %s L%s %s"/>' % (cx - 130 + i * 26, cy - 60, cx - 130 + i * 20, cy + 80))
    for i in range(1, 4):
        body.append('<path d="M%s %s L%s %s"/>' % (cx - 128 + i * 4, cy - 60 + i * 35, cx + 128 - i * 4, cy - 60 + i * 35))
    body.append("</g>")
    random.seed(3)
    for i in range(30):
        x = cx + random.uniform(-120, 120)
        y = cy - 70 + random.uniform(-40, 30) - abs(x - cx) * 0.12
        r = random.uniform(12, 20)
        c = ["#f6f4ee", "#e6e1d3", "#cfc7b3", "#e8dcc0"][i % 4]
        body.append('<circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (round(x, 1), round(y, 1), round(r, 1), c))
    body.append('<rect x="%s" y="%s" width="240" height="56" rx="6" fill="#1b1f24" opacity="0.94"/>' % (cx - 120, cy + 86))
    body.append('<rect x="%s" y="%s" width="240" height="56" rx="6" fill="none" stroke="#c8a24a" stroke-width="2" opacity="0.8"/>' % (cx - 120, cy + 86))
    body.append('<text x="%s" y="%s" text-anchor="middle" font-family="Georgia,serif" font-size="24" fill="#e6d6ac">ПЕЧАЛЬ</text>' % (cx, cy + 122))
    body.append('<rect width="%d" height="%d" fill="url(#vignette)"/>' % (W, H))
    write(name, wrap("\n".join(body)))


basket("korzina-pechal.svg")


def wooden(name, kind):
    body = ['<rect width="%d" height="%d" fill="#23272d"/>' % (W, H)]
    body.append('<radialGradient id="glow" cx="0.5" cy="0.45" r="0.6">'
                '<stop offset="0" stop-color="#3d434b"/><stop offset="1" stop-color="#1a1d22"/></radialGradient>')
    body.append('<rect width="%d" height="%d" fill="url(#glow)"/>' % (W, H))
    cx, cy = W / 2.0, H / 2.0
    wood = "linearGradient"
    body.append('<linearGradient id="wood" x1="0" y1="0" x2="1" y2="1">'
                '<stop offset="0" stop-color="#b08a5a"/><stop offset="1" stop-color="#7a5b34"/></linearGradient>')
    if kind == "cross":
        body.append('<g fill="url(#wood)">'
                    '<rect x="%s" y="%s" width="52" height="420" rx="8"/>'
                    '<rect x="%s" y="%s" width="260" height="52" rx="8"/>'
                    '<rect x="%s" y="%s" width="180" height="46" rx="8"/></g>'
                    % (cx - 26, cy - 190, cx - 130, cy - 130, cx - 90, cy - 40))
        body.append('<path d="M%s %s L%s %s" stroke="#c8a24a" stroke-width="4" opacity="0.7"/>' % (cx - 90, cy - 210, cx + 60, cy - 210))
    else:
        body.append('<g fill="url(#wood)">'
                    '<path d="M%s %s L%s %s L%s %s L%s %s Z"/>'
                    '<path d="M%s %s L%s %s L%s %s L%s %s Z" opacity="0.92"/></g>'
                    % (cx - 150, cy - 120, cx + 110, cy - 120, cx + 150, cy + 120, cx - 110, cy + 120,
                       cx - 150, cy - 120, cx - 110, cy + 120, cx - 118, cy + 132, cx - 158, cy - 128))
        body.append('<g stroke="#6d5233" stroke-width="3" opacity="0.55">')
        for i in range(1, 6):
            body.append('<path d="M%s %s L%s %s"/>' % (cx - 150 + i * 45, cy - 120, cx - 110 + i * 45, cy + 120))
        body.append("</g>")
    body.append('<rect width="%d" height="%d" fill="url(#vignette)"/>' % (W, H))
    write(name, wrap("\n".join(body)))


wooden("tovar-krest.svg", "cross")
wooden("tovar-grob.svg", "grob")

# ---------------------------------------------------------------- текстуры и баннеры
def hero_bg(name):
    body = ['<rect width="%d" height="%d" fill="#14181d"/>' % (W, H)]
    body.append('<radialGradient id="g1" cx="0.22" cy="0.28" r="0.8">'
                '<stop offset="0" stop-color="#39414b"/><stop offset="1" stop-color="#14181d"/></radialGradient>')
    body.append('<rect width="%d" height="%d" fill="url(#g1)"/>' % (W, H))
    body.append('<rect width="%d" height="%d" fill="#000" opacity="0.35" filter="url(#speckle)"/>' % (W, H))
    body.append('<ellipse cx="700" cy="120" rx="320" ry="220" fill="#c8a24a" opacity="0.16" filter="url(#soft)"/>')
    body.append('<ellipse cx="120" cy="620" rx="300" ry="180" fill="#c8a24a" opacity="0.08" filter="url(#soft)"/>')
    write(name, wrap("\n".join(body)))


def pattern_stone(name):
    body = ['<rect width="120" height="120" fill="#181c21"/>']
    random.seed(11)
    for i in range(120):
        body.append('<circle cx="%s" cy="%s" r="%s" fill="#%s" opacity="%s"/>'
                    % (round(random.uniform(0, 120), 1), round(random.uniform(0, 120), 1),
                       round(random.uniform(0.4, 1.6), 2),
                       random.choice(["ffffff", "9aa1a8", "c8a24a", "5b636c"]),
                       round(random.uniform(0.05, 0.28), 2)))
    write(name, ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120" width="120" height="120">'
                 + "\n".join(body) + "</svg>"))


hero_bg("hero-bg.svg")
pattern_stone("pattern-stone.svg")

print("\nГотово:", len(os.listdir(OUT)), "файлов в", OUT)
