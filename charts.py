from __future__ import annotations

import os

from PIL import Image, ImageDraw, ImageFont, ImageTk

SS = 4

FONT_DIR = os.path.expanduser("~/.local/share/fonts/poppins")
_FONT_CACHE: dict = {}

PALETTE = ["#22C55E", "#3B82F6", "#F59E0B",
           "#EC4899", "#8B5CF6", "#14B8A6"]

# helpers -------------------------------------------------------------
def _mix(h1: str, h2: str, t: float) -> str:
    a, b = _rgb(h1), _rgb(h2)
    return "#%02X%02X%02X" % tuple(
        int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def _tint(hex_color: str, t: float = 0.85) -> str:
    """Blend a color toward white."""
    return _mix(hex_color, "#FFFFFF", t)


def _vgrad_round(w: int, h: int, top: str, bottom: str, radius: int):
    """Rounded rect filled with a vertical gradient (pre-scaled coords)."""
    grad = Image.new("RGBA", (w, h))
    px = grad.load()
    tr, br = _rgb(top), _rgb(bottom)
    for y in range(h):
        t = y / max(h - 1, 1)
        row = tuple(int(tr[i] + (br[i] - tr[i]) * t) for i in range(3)) \
            + (255,)
        for x in range(w):
            px[x, y] = row
    mask = Image.new("L", (w, h), 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle([0, 0, w - 1, h - 1], radius=radius, fill=255)
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    out.paste(grad, (0, 0), mask)
    return out


def _font(size: int, bold: bool = False):
    key = (size, bold)
    if key in _FONT_CACHE:
        return _FONT_CACHE[key]
    name = "SemiBold" if bold else "Regular"
    path = os.path.join(FONT_DIR, f"Poppins-{name}.ttf")
    try:
        fnt = ImageFont.truetype(path, size * SS)
    except OSError:
        fnt = ImageFont.load_default()
    _FONT_CACHE[key] = fnt
    return fnt


def _finish(im: Image.Image, w: int, h: int):
    im = im.resize((w, h), Image.LANCZOS)
    return ImageTk.PhotoImage(im)


def _text(d, xy, txt, size, fill, bold=False, anchor="la"):
    d.text((xy[0] * SS, xy[1] * SS), txt, font=_font(size, bold),
           fill=fill, anchor=anchor)


def _rrect(d, box, radius, fill):
    d.rounded_rectangle([v * SS for v in box], radius=radius * SS, fill=fill)


def track_color(card_bg: str) -> str:
    dark_cards = {"#1a222e"}
    light_cards = {"#f7faf5", "#ffffff"}
    bg = card_bg.lower()
    if bg in dark_cards:
        return "#2E2A27"
    return "#EAF4EC"


# --------------------------------------------------------------- charts --
def draw_hbars(w, h, data, colors_cfg):
    """Modern pill bars: slim rounded fill on soft track, value chip."""
    text, muted, card = (colors_cfg[k] for k in
                         ("text", "muted", "card"))
    im = Image.new("RGBA", (w * SS, h * SS), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    rows = [r for r in data[:5]]
    n = len(rows)
    top, bottom = 6, h - 6
    row_h = (bottom - top) / max(n, 1)
    bar_x, bar_w_max = 96, w - 96 - 30
    vmax = max((v for _, v in rows), default=1) or 1
    for i, (label, v) in enumerate(rows):
        y = top + i * row_h + row_h / 2
        color = PALETTE[i % len(PALETTE)]
        label = str(label)
        while label and _font(9, False).getlength(label) > bar_x - 10:
            label = label[:-1]
        if label != str(rows[i][0]):
            label = label.rstrip() + "\u2026"
        _text(d, (2, y - 11), label, 8, muted)
        # track
        _rrect(d, (bar_x, y - 5, bar_x + bar_w_max, y + 5), 5,
               _tint(color, 0.82))
        # gradient fill
        fill_w = max(int(bar_w_max * v / vmax), 12)
        grad = _vgrad_round(fill_w * SS, 10 * SS,
                            _mix(color, "#FFFFFF", 0.18), color, 5 * SS)
        im.paste(grad, (int(bar_x * SS), int((y - 5) * SS)), grad)
        # value
        _text(d, (bar_x + bar_w_max + 6, y - 7), str(v), 10, text,
              bold=True)
    return _finish(im, w, h)


def draw_columns(w, h, data, colors_cfg):
    """Floating gradient columns, value bubbles, minimal baseline."""
    text, muted, card = (colors_cfg[k] for k in
                         ("text", "muted", "card"))
    im = Image.new("RGBA", (w * SS, h * SS), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    n = max(len(data), 1)
    col_w = min(34, int((w - 40) / n - 14))
    base_y = h - 24
    top_y = 22
    vmax = max((v for _, v in data), default=1) or 1
    # dotted baseline
    x0, x1 = 12 * SS, (w - 12) * SS
    seg, gap = 3 * SS, 4 * SS
    xx = x0
    while xx < x1:
        d.line([(xx, base_y * SS), (min(xx + seg, x1), base_y * SS)],
               fill=(*_rgb(_tint(text, 0.72)), 255), width=SS)
        xx += seg + gap
    for i, (label, v) in enumerate(data):
        cx = (w / n) * (i + 0.5)
        color = PALETTE[i % len(PALETTE)]
        bh = int(max((base_y - top_y) * v / vmax, 8)) if v else 4
        if v:
            grad = _vgrad_round(col_w * SS, bh * SS,
                                _mix(color, "#FFFFFF", 0.35), color,
                                min(col_w // 2, 9) * SS)
            im.paste(grad, (int((cx - col_w / 2) * SS),
                            int((base_y - bh) * SS)), grad)
        else:
            _rrect(d, (cx - col_w / 2, base_y - 4, cx + col_w / 2, base_y),
                   2, _tint(color, 0.82))
        # bubble
        bw = 10 * SS * len(str(v)) + 8 * SS
        by = base_y - bh - 15
        d.rounded_rectangle([(cx - bw / 2), (by - 9) * SS,
                             (cx + bw / 2), (by + 2) * SS],
                            radius=5 * SS, fill=_tint(color, 0.78))
        _text(d, (cx, by - 8), str(v), 8, text, bold=True, anchor="ma")
        lab = str(label)[:11]
        _text(d, (cx, base_y + 6), lab, 8, muted, anchor="ma")
    return _finish(im, w, h)


def draw_pie(w, h, data, colors_cfg):
    """Classic solid pie with crisp slice separators + side legend."""
    import i18n
    text, muted, card = (colors_cfg[k] for k in ("text", "muted", "card"))
    im = Image.new("RGBA", (w * SS, h * SS), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    segs = [x for x in data if x[1] > 0]
    total = sum(v for _, v in segs) or 1
    dia = min(h - 16, w - 140)
    cx, cy, r = 12 + dia / 2, h / 2, dia / 2
    box = [cx - r, cy - r, cx + r, cy + r]
    start = -90.0
    for i, (_, v) in enumerate(segs):
        ext = 360.0 * v / total
        color = PALETTE[i % len(PALETTE)]
        sweep = ext - (1.4 if len(segs) > 1 else 0)
        if sweep > 0:
            d.pieslice([b * SS for b in box], start, start + sweep,
                       fill=_rgb(color), outline=_rgb(card), width=SS)
        start += ext
    ly = cy - len(data) * 11 + 2
    for i, (label, v) in enumerate(data[:6]):
        y = ly + i * 22
        color = PALETTE[i % len(PALETTE)]
        d.rounded_rectangle([(w - 128) * SS, (y - 3) * SS,
                             (w - 116) * SS, (y + 9) * SS],
                            radius=6 * SS, fill=_rgb(color))
        pct = f"{v * 100 // total}%"
        _text(d, (w - 108, y - 7), str(label)[:11], 9, text)
        _text(d, (w - 8, y - 7), f"{v} \u00B7 {pct}", 8, muted,
              bold=True, anchor="ra")
    return _finish(im, w, h)


MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug",
          "Sep", "Oct", "Nov", "Dec"]


def draw_area(w, h, labels, values, colors_cfg):
    """Smooth spline with soft gradient fill; no grid clutter."""
    text, muted, accent, card = (colors_cfg[k] for k in
                                 ("text", "muted", "accent", "card"))
    c2 = PALETTE[1]                     # second hue for the gradient
    im = Image.new("RGBA", (w * SS, h * SS), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    n = max(len(values), 2)
    pad_l, pad_r, pad_t, pad_b = 12, 12, 14, 24
    plot_w, plot_h = w - pad_l - pad_r, h - pad_t - pad_b
    vmax = max(values, default=1) or 1
    pts = []
    for i, v in enumerate(values):
        x = pad_l + plot_w * (i / (n - 1)) if n > 1 else pad_l + plot_w / 2
        y = pad_t + plot_h * (1 - (v / vmax))
        pts.append((x, y))
    # catmull-rom smoothing
    smooth = []
    for i in range(len(pts) - 1):
        p0 = pts[max(i - 1, 0)]
        p1, p2 = pts[i], pts[i + 1]
        p3 = pts[min(i + 2, len(pts) - 1)]
        for t in range(8):
            tt = t / 8
            tt2, tt3 = tt * tt, tt * tt * tt
            x = 0.5 * ((2 * p1[0]) + (-p0[0] + p2[0]) * tt +
                       (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * tt2 +
                       (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * tt3)
            y = 0.5 * ((2 * p1[1]) + (-p0[1] + p2[1]) * tt +
                       (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * tt2 +
                       (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * tt3)
            smooth.append((x, y))
    smooth.append(pts[-1])
    base = pad_t + plot_h
    poly = [(pad_l, base)] + smooth + [(pad_l + plot_w, base)]
    # gradient fill via mask paste
    gh = int(base - pad_t) * SS
    gw = int(plot_w) * SS
    grad = Image.new("RGBA", (gw, gh))
    gp = grad.load()
    ca, cb = (*_rgb(accent), 95), (*_rgb(c2), 8)
    for yy in range(gh):
        t = yy / max(gh - 1, 1)
        row = tuple(int(ca[k] + (cb[k] - ca[k]) * t) for k in range(4))
        for xx in range(gw):
            gp[xx, yy] = row
    mask = Image.new("L", (gw, gh), 0)
    md = ImageDraw.Draw(mask)
    local = [(x - pad_l, y - pad_t) for x, y in poly]
    md.polygon([(x * SS, y * SS) for x, y in local], fill=255)
    im.paste(grad, (int(pad_l * SS), int(pad_t * SS)), mask)
    # line
    line_im = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ld = ImageDraw.Draw(line_im)
    ld.line([(x * SS, y * SS) for x, y in smooth],
            fill=(*_rgb(accent), 255), width=int(1.6 * SS), joint="curve")
    im = Image.alpha_composite(im, line_im)
    d = ImageDraw.Draw(im)
    # endpoint halo dot
    ex, ey = smooth[-1]
    rr = 4 * SS
    d.ellipse([ex * SS - rr * 2, ey * SS - rr * 2,
               ex * SS + rr * 2, ey * SS + rr * 2],
              fill=(*_rgb(accent), 40))
    d.ellipse([ex * SS - rr, ey * SS - rr, ex * SS + rr, ey * SS + rr],
              fill=_rgb("#FFFFFF"), outline=_rgb(accent), width=SS)
    for i, lab in enumerate(labels):
        x = pad_l + plot_w * (i / (n - 1)) if n > 1 else pad_l + plot_w / 2
        _text(d, (x, h - 16), str(lab)[:6], 8, muted, bold=True, anchor="ma")
    return _finish(im, w, h)


def _rgb(hex_color: str):
    h = hex_color.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def render(key: str, w: int, h: int, payload, colors_cfg):
    if key == "owners":
        return draw_hbars(w, h, payload, colors_cfg)
    if key == "appointments":
        return draw_columns(w, h, payload, colors_cfg)
    if key == "pets":
        return draw_pie(w, h, payload, colors_cfg)
    return draw_area(w, h, payload[0], payload[1], colors_cfg)
