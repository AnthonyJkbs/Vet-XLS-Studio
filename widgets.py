from __future__ import annotations

import os
import tkinter as tk
from tkinter import font as tkfont

FONT = "Poppins"

ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
try:
    import paths
    ASSETS = paths.resource("assets")
except ImportError:
    pass
LOGO_PATH = os.path.join(ASSETS, "logo.png")

_ICON_CACHE: dict[int, object] = {}
_AA_CACHE: dict[tuple, object] = {}


def load_logo(size: int):
    """Return a PhotoImage of the app logo at the requested pixel size."""
    if size in _ICON_CACHE:
        return _ICON_CACHE[size]
    try:
        from PIL import Image, ImageTk
        img = Image.open(LOGO_PATH).convert("RGBA")
        img = img.resize((size, size), Image.LANCZOS)
        photo = ImageTk.PhotoImage(img)
    except Exception:
        photo = None
    _ICON_CACHE[size] = photo
    return photo


def reset_logo_cache():
    """Drop cached images (they belong to a specific Tk interpreter)."""
    _ICON_CACHE.clear()
    _AA_CACHE.clear()


def _aa_round_photo(pill: bool, w: int, h: int, color: str):
    """Pre-render an anti-aliased button background (4x supersampled)."""
    if w < 4 or h < 4:
        return None
    key = ("pill" if pill else "circ", w, h, color)
    cached = _AA_CACHE.get(key)
    if cached is not None:
        return cached
    try:
        from PIL import Image, ImageDraw, ImageTk
        ss = 4
        im = Image.new("RGBA", (w * ss, h * ss), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        box = [ss - 1, ss - 1, w * ss - ss, h * ss - ss]
        if pill:
            d.rounded_rectangle(box, radius=h * ss // 2 - 1, fill=color)
        else:
            d.ellipse(box, fill=color)
        im = im.resize((w, h), Image.LANCZOS)
        photo = ImageTk.PhotoImage(im)
    except Exception:
        return None
    _AA_CACHE[key] = photo
    return photo

THEMES = {
    "light": {
        "bg": "#ECEFE9", "card": "#FFFFFF", "accent": "#16A34A",
        "accent_dark": "#15803D", "accent_soft": "#DFF2E4",
        "text": "#26312B", "muted": "#7E8B82", "danger": "#C9503C",
        "border": "#DFE6DE", "zebra": "#F5FAF5", "input": "#F2F7F1",
        "neutral": "#87938A", "shell_text": "#26312B",
        "shell_muted": "#79857C",
    },
    "dark": {
        "bg": "#1E211F", "card": "#F7FAF5", "accent": "#22B45A",
        "accent_dark": "#15803D", "accent_soft": "#DCF2E2",
        "text": "#26312B", "muted": "#83907F", "danger": "#C9503C",
        "border": "#E0E8DE", "zebra": "#EFF7EE", "input": "#EDF4EA",
        "neutral": "#8B9689", "shell_text": "#EFF5EB",
        "shell_muted": "#AEBBA9",
    },
}

COLORS = dict(THEMES["light"])


def get_theme() -> str:
    import settings
    theme = settings.load().get("theme")
    return theme if theme in THEMES else "dark"


def set_theme(name: str) -> None:
    import settings
    if name not in THEMES:
        return
    COLORS.clear()
    COLORS.update(THEMES[name])
    settings.save("theme", name)


def init_theme() -> str:
    name = get_theme()
    COLORS.clear()
    COLORS.update(THEMES[name])
    return name


def shade(hex_color: str, factor: float) -> str:
    """Lighten (>1) or darken (<1) a hex color."""
    h = hex_color.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    clamp = lambda v: max(0, min(255, int(v * factor)))
    return f"#{clamp(r):02x}{clamp(g):02x}{clamp(b):02x}"


def _round_pts(x1, y1, x2, y2, r):
    return [x1 + r, y1, x2 - r, y1, x2, y1, x2, y1 + r,
            x2, y2 - r, x2, y2, x2 - r, y2, x1 + r, y2,
            x1, y2, x1, y2 - r, x1, y1 + r, x1, y1]


class RoundButton(tk.Canvas):
    """Circular or pill-shaped button drawn on a canvas, with hover effect."""

    def __init__(self, master, text="", command=None, diameter=44,
                 bg=COLORS["accent"], fg="#FFFFFF", hover_bg=None,
                 font=(FONT, 11, "bold"), pill=False, padx=22,
                 tooltip=None):
        self._text = text
        self._command = command
        self._bg = bg
        self._hover = hover_bg or shade(bg, 0.88)
        self._fg = fg
        self._font = font
        self._pill = pill or bool(text)
        self._padx = padx
        self._diameter = diameter
        parent_bg = COLORS["bg"]
        try:
            parent_bg = master.cget("bg")
        except Exception:
            pass
        if self._pill and text:
            w = self._text_width() + padx * 2
            h = diameter
        else:
            w = h = diameter
        self._enabled = True
        self._current_color = bg
        super().__init__(master, width=w, height=h, bg=parent_bg,
                         highlightthickness=0, cursor="hand2")
        self._draw(self._bg)
        self.bind("<Enter>", lambda e: self._draw(shade(self._current_color, 0.88)))
        self.bind("<Leave>", lambda e: self._draw(self._current_color))
        self.bind("<Button-1>", self._press)
        self.bind("<ButtonRelease-1>", self._release)
        if tooltip:
            self._tooltip_tip = None
            self.bind("<Enter>", lambda e: self._show_tip(tooltip), add="+")
            self.bind("<Leave>", lambda e: self._hide_tip(), add="+")

    def _text_width(self) -> int:
        f = tkfont.Font(font=self._font)
        return int(f.measure(self._text))

    # ------------------------------------------------------------ tip --
    def _show_tip(self, text):
        self._hide_tip()
        x = self.winfo_rootx() + self.winfo_width() // 2
        y = self.winfo_rooty() + self.winfo_height() + 6
        tw = tk.Toplevel(self)
        tw.wm_overrideredirect(True)
        tw.attributes("-topmost", True)
        tk.Label(tw, text=text, bg="#3A342E", fg="white",
                 font=(FONT, 8), padx=7, pady=3).pack()
        tw.update_idletasks()
        tw.wm_geometry(f"+{max(0, x - tw.winfo_reqwidth() // 2)}+{y}")
        self._tooltip_tip = tw

    def _hide_tip(self):
        tip = getattr(self, "_tooltip_tip", None)
        if tip is not None:
            tip.destroy()
        self._tooltip_tip = None

    # ----------------------------------------------------------- draw --
    def _draw(self, color):
        try:
            self.delete("all")
        except tk.TclError:
            return  # canvas gone mid-teardown
        w, h = self.winfo_reqwidth(), self.winfo_reqheight()
        photo = _aa_round_photo(self._pill, w, h, color)
        if photo is not None:
            self.create_image(0, 0, anchor="nw", image=photo)
        else:
            if self._pill:
                self.create_polygon(_round_pts(1, 1, w - 1, h - 1, h // 2),
                                    fill=color, outline=color, smooth=True,
                                    splinesteps=180)
            else:
                self.create_oval(1, 1, w - 1, h - 1, fill=color, outline=color)
        self.create_text(w / 2, h / 2, text=self._text,
                         fill=self._fg, font=self._font)

    # ---------------------------------------------------------- events --
    def _press(self, _event=None):
        if not self._enabled or self._command is None:
            return
        self._draw(shade(self._current_color, 0.75))

    def _release(self, _event=None):
        if not self._enabled:
            return
        self._draw(shade(self._current_color, 0.88))
        if self._command is not None:
            self.after(70, self._command)

    def set_enabled(self, enabled: bool):
        self._enabled = bool(enabled)
        self.configure(cursor="hand2" if enabled else "arrow")
        self._draw(self._bg if enabled else shade(self._bg, 1.45))

    def set_text(self, text: str):
        """Swap label text; pill buttons resize to fit (text + margins)."""
        old_w = self.winfo_reqwidth()
        self._text = text
        if self._pill:
            new_w = self._text_width() + 2 * self._padx
            self.configure(width=max(new_w, 2 * self._diameter))
        else:
            new_w = old_w
        self._draw(self._current_color)

    def recolor(self, color: str):
        self._current_color = color
        self._draw(color)


class StatCard(tk.Canvas):
    """Rounded stat card: section logo top-left with description below,
    total number on the right. chip/value colors can differ per card."""

    def __init__(self, master, icon, title, value="0", width=136, height=100,
                 chip=None, value_color=None):
        super().__init__(master, width=width, height=height, bg=master["bg"],
                         highlightthickness=0)
        self._card_w, self._card_h = width, height
        self._icon, self._title = icon, title
        self._value_text = str(value)
        self._chip = chip or COLORS["accent_soft"]
        self._value_color = value_color or COLORS["accent_dark"]
        self.bind("<Configure>", lambda e: self._paint())
        self._paint()

    def _paint(self):
        c = self
        try:
            c.delete("all")
        except tk.TclError:
            return  # canvas gone mid-teardown
        w, h = self._card_w, self._card_h
        c.create_polygon(_round_pts(1, 1, w - 1, h - 1, 13),
                         fill=COLORS["card"], outline=COLORS["border"],
                         smooth=True, width=1, splinesteps=180)
        c.create_oval(10, 8, 46, 44, fill=self._chip, outline="")
        c.create_text(28, 26, text=self._icon, font=(FONT, 15), anchor="c")
        c.create_text(29, 56, text=self._title, font=(FONT, 7),
                      fill=COLORS["muted"], width=76, justify="center")
        c.create_text(w - 11, 42, anchor="e", text=self._value_text,
                      font=(FONT, 19, "bold"), fill=self._value_color)

    def set_value(self, value):
        self._value_text = str(value)
        self._paint()


class RoundedCard(tk.Canvas):
    """White rounded container; put widgets inside `.inner`."""

    def __init__(self, master, radius=16, padx=16, pady=14, **kw):
        super().__init__(master, bg=COLORS["bg"], highlightthickness=0, **kw)
        self._radius = radius
        self._padx, self._pady = padx, pady
        self.inner = tk.Frame(self, bg=COLORS["card"])
        self._win = None
        self.bind("<Configure>", self._on_resize)

    def _on_resize(self, event):
        w, h = event.width, event.height
        self.delete("bg")
        self.create_polygon(_round_pts(1, 1, w - 1, h - 1, self._radius),
                            fill=COLORS["card"], outline=COLORS["border"],
                            smooth=True, width=1, tags="bg")
        if self._win is None:
            self._win = self.create_window(self._padx, self._pady,
                                           anchor="nw", window=self.inner)
        else:
            self.itemconfigure(self._win,
                               width=w - 2 * self._padx,
                               height=h - 2 * self._pady)
        self.tag_lower("bg")


class MonthCalendar(tk.Canvas):
    """Compact month calendar: localized, event dots, today ring,
    clickable days. get_marks() -> iterable of ISO date strings."""

    _MOUSE_WHEEL_STEPS = 2

    def __init__(self, master, get_marks=None, on_pick=None,
                 height=160, **kw):
        super().__init__(master, height=height, bg=master["bg"],
                         highlightthickness=0, **kw)
        from datetime import date as _d
        t = _d.today()
        self._view = (t.year, t.month)
        self._today = t
        self._selected = None
        self._get_marks = get_marks
        self._on_pick = on_pick
        self.bind("<Configure>", lambda e: self.refresh())
        # single dispatcher: robust for items recreated on every redraw
        self.bind("<Button-1>", self._route_click)
        self.bind("<Enter>", self._hover)
        self.bind("<Motion>", self._hover)
        self.bind("<Leave>",
                  lambda e: self.configure(cursor="arrow"))
        # mouse wheel month navigation (Linux + Windows + macOS)
        self.bind("<Button-4>", lambda e: self.shift_month(-1))
        self.bind("<Button-5>", lambda e: self.shift_month(1))
        self.bind("<MouseWheel>",
                  lambda e: self.shift_month(-1 if e.delta > 0 else 1))
        self.refresh()

    # --------------------------------------------------------- public --
    def refresh(self):
        """Redraw; re-queries marks so new events appear."""
        try:
            self.delete("all")
        except tk.TclError:
            return
        w = max(self.winfo_width(), 210)
        h = max(self.winfo_height(), 150)

        def _nav(x, ch, tag):
            # pickable hit box painted in the canvas bg (glyph drawn on top)
            self.create_rectangle(x - 13, 4, x + 13, 29,
                                  fill=self.cget("bg"), outline="",
                                  tags=("navhit", tag))
            self.create_text(x, 16, text=ch, font=(FONT, 13, "bold"),
                             fill=COLORS["accent"], tags=(tag, "navhit"))

        _nav(14, "\u2039", "nav_prev")
        _nav(w - 14, "\u203A", "nav_next")

        import i18n
        y, m = self._view
        title = f"{i18n.month_name(m)} {y}"
        self.create_text(w / 2, 16, text=title.title(),
                         font=(FONT, 10, "bold"), fill=COLORS["text"])

        cols, x0, gw = 7, 8, w - 16
        cw = gw / cols
        initials = i18n.day_initials()
        for i, name in enumerate(initials):
            self.create_text(x0 + cw * (i + .5), 36, text=name,
                             font=(FONT, 7, "bold"), fill=COLORS["muted"])

        marks = set()
        if self._get_marks is not None:
            try:
                marks = {str(v)[:10] for v in self._get_marks()}
            except Exception:
                marks = set()

        from datetime import date as _d
        first_wd = _d(y, m, 1).weekday()   # Monday = 0
        grid_y0, row_h = 50, min((h - 58) / 6, 24)
        r = 9
        for idx in range(42):
            day_num = idx - first_wd + 1
            try:
                d = _d(y, m, day_num)
            except ValueError:
                continue
            cx = x0 + cw * (idx % cols + .5)
            cy = grid_y0 + row_h * (idx // cols) + row_h / 2
            iso = d.isoformat()
            dimmed = d.month != m
            fg = COLORS["muted"] if dimmed else COLORS["text"]
            tags = (f"day:{iso}", "daycell")
            if d == self._today:
                self.create_oval(cx - r, cy - r, cx + r, cy + r,
                                 fill=COLORS["accent"], outline="",
                                 tags=("todaycircle",))
                fg = "#FFFFFF"
            elif iso == self._selected:
                self.create_oval(cx - r, cy - r, cx + r, cy + r,
                                 outline=COLORS["accent"], width=2,
                                 fill="", tags=("selring",))
            self.create_text(cx, cy - (2 if iso in marks else 0),
                             text=str(d.day), font=(FONT, 9), fill=fg,
                             tags=tags)
            if iso in marks and not dimmed:
                self.create_oval(cx - 2, cy + r - 3, cx + 2, cy + r + 1,
                                 fill=COLORS["accent_dark"], outline="",
                                 tags=tags)

    def shift_month(self, delta: int):
        y, m = self._view
        m += delta
        while m < 1:
            m += 12
            y -= 1
        while m > 12:
            m -= 12
            y += 1
        self._view = (y, m)
        self.refresh()

    def set_selected(self, iso):
        self._selected = iso
        self.refresh()

    # -------------------------------------------------------- private --
    def _route_click(self, event):
        try:
            items = self.find_withtag("current")
        except tk.TclError:
            return
        for item in items:
            try:
                tags = self.gettags(item)
            except tk.TclError:
                continue
            for t in tags:
                if t == "nav_prev":
                    return self.shift_month(-1)
                if t == "nav_next":
                    return self.shift_month(1)
                if t.startswith("day:"):
                    iso = t[4:]
                    nxt = None if iso == self._selected else iso
                    self.set_selected(nxt)
                    if self._on_pick is not None:
                        try:
                            self._on_pick(nxt)
                        except Exception:
                            pass
                    return

    def _hover(self, _event):
        clickable = False
        try:
            for item in self.find_withtag("current"):
                for t in self.gettags(item):
                    if (t.startswith("day:") or t.startswith("nav_")
                            or t == "navhit"):
                        clickable = True
                        break
                if clickable:
                    break
        except tk.TclError:
            return
        self.configure(cursor="hand2" if clickable else "arrow")
