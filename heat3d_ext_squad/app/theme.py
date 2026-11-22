"""
The look of every 3DHeat tool window: the viewer's colours (dark and light),
its fonts, rounded cards and buttons, the heat-ramp progress bar and the
step bar. Plain Tk/ttk only (part of Python), so a tool needs nothing extra.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ASSETS = Path(__file__).resolve().parent / "assets"

# The viewer's design tokens (src/app.css), dark and light.
DARK = dict(
    bg="#07090d", panel="#0e1218", panel2="#151a22", surface3="#1b222d", hover="#1f2733",
    line="#242c38", line_strong="#344052", text="#e6ebf2", dim="#a3adbd", faint="#7d8899",
    accent="#46c8ff", accent_hover="#74d6ff", accent_press="#1d76ad", accent_ink="#04131c",
    good="#3ddc84", warn="#ffb547", bad="#ff5d5d", warm="#ff6a3d",
)
LIGHT = dict(
    bg="#e9edf2", panel="#fbfcfd", panel2="#f0f3f7", surface3="#e6ebf1", hover="#e3e9f0",
    line="#d3dae3", line_strong="#b9c3cf", text="#121821", dim="#3f4a5a", faint="#5f6b7c",
    accent="#0b6fb8", accent_hover="#095e9c", accent_press="#074c7f", accent_ink="#ffffff",
    good="#157a43", warn="#9a6200", bad="#c62828", warm="#c2491f",
)
#: The brand bar on top stays dark in both modes (the logo is drawn for dark).
BRAND_BAR = "#0b0f15"
#: The logo's heat ramp, blue to red (docs/brand.md).
HEAT = ["#0e5aa9", "#0bafda", "#3becb5", "#f3e349", "#ff730d", "#d91b14"]


# ------------------------------------------------------------------ colours
def _rgb(c: str) -> tuple[int, int, int]:
    c = c.lstrip("#")
    return int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16)


def _hex(r: float, g: float, b: float) -> str:
    return "#%02x%02x%02x" % tuple(max(0, min(255, round(v))) for v in (r, g, b))


def mix(a: str, b: str, t: float) -> str:
    """`a` with `t` of `b` over it."""
    ra, ga, ba = _rgb(a)
    rb, gb, bb = _rgb(b)
    return _hex(ra + (rb - ra) * t, ga + (gb - ga) * t, ba + (bb - ba) * t)


def ramp(t: float, stops: list[str] = HEAT) -> str:
    t = max(0.0, min(1.0, t)) * (len(stops) - 1)
    i = min(int(t), len(stops) - 2)
    return mix(stops[i], stops[i + 1], t - i)


# ------------------------------------------------------------- system state
def system_prefers_light() -> bool:
    try:
        if os.name == "nt":
            import winreg

            with winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize") as k:
                return winreg.QueryValueEx(k, "AppsUseLightTheme")[0] == 1
        if sys.platform == "darwin":
            r = subprocess.run(["defaults", "read", "-g", "AppleInterfaceStyle"], capture_output=True, text=True, timeout=2)
            return "dark" not in r.stdout.lower()
        r = subprocess.run(["gsettings", "get", "org.gnome.desktop.interface", "color-scheme"],
                           capture_output=True, text=True, timeout=2)
        return "light" in r.stdout.lower()
    except Exception:
        return False  # dark is the 3DHeat default


def dpi_aware() -> None:
    """Sharp text on Windows at 125 % / 150 % (call before the first Tk window)."""
    if os.name != "nt":
        return
    try:
        import ctypes

        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass


def app_id(tool_id: str) -> None:
    """Its own taskbar button and icon on Windows, not Python's."""
    if os.name != "nt":
        return
    try:
        import ctypes

        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(f"3DHeat.{tool_id}")
    except Exception:
        pass


def title_bar(root, dark: bool, colour: str | None = None) -> None:
    """Windows 10/11: a dark (or light) title bar to match the window."""
    if os.name != "nt":
        return
    try:
        import ctypes

        root.update_idletasks()
        hwnd = ctypes.windll.user32.GetParent(root.winfo_id())
        on = ctypes.c_int(1 if dark else 0)
        for attr in (20, 19):  # DWMWA_USE_IMMERSIVE_DARK_MODE (new, old)
            if ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, attr, ctypes.byref(on), 4) == 0:
                break
        if colour:
            r, g, b = _rgb(colour)
            c = ctypes.c_int(r | (g << 8) | (b << 16))
            ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, 35, ctypes.byref(c), 4)  # caption colour (11)
    except Exception:
        pass


# ------------------------------------------------------------------- images
def rounded_data(w: int, h: int, r: float, fill: str, bg: str, outline: str | None = None, bw: float = 1.0) -> str:
    """Pixel rows of an anti-aliased rounded rectangle blended over `bg` (for PhotoImage.put)."""

    def cover(cx: float, cy: float, inset: float) -> float:
        x0, y0, x1, y1 = inset, inset, w - inset, h - inset
        rr = max(0.0, r - inset)
        dx = max(x0 + rr - cx, 0.0, cx - (x1 - rr))
        dy = max(y0 + rr - cy, 0.0, cy - (y1 - rr))
        if dx > 0 and dy > 0:
            d = rr - (dx * dx + dy * dy) ** 0.5
        else:
            d = min(cx - x0, x1 - cx, cy - y0, y1 - cy)
        return max(0.0, min(1.0, d + 0.5))

    rows = []
    for y in range(h):
        row = []
        for x in range(w):
            cx, cy = x + 0.5, y + 0.5
            outer = cover(cx, cy, 0.0)
            if outline:
                row.append(mix(mix(bg, outline, outer), fill, cover(cx, cy, bw)))
            else:
                row.append(mix(bg, fill, outer))
        rows.append("{" + " ".join(row) + "}")
    return " ".join(rows)


def load_png(master, name: str):
    import tkinter as tk

    p = ASSETS / name
    try:
        return tk.PhotoImage(master=master, file=str(p)) if p.is_file() else None
    except tk.TclError:
        return None


# -------------------------------------------------------------------- theme
class Theme:
    """Colours, fonts and ttk styles for one window; `set_mode()` + `apply()` switch dark/light in place."""

    def __init__(self, root, mode: str = "system"):
        import tkinter.font as tkfont

        self.root = root
        self.scale = max(1.0, root.winfo_fpixels("1i") / 96.0)
        #: Images by key, kept for the window's life and redrawn in place on a mode switch
        #: (ttk image elements and labels keep pointing at the same image).
        self.images: dict[str, object] = {}
        fams = set(tkfont.families(root))
        pick = lambda *names: next((n for n in names if n in fams), None)  # noqa: E731
        self.family = pick("Segoe UI Variable Text", "Segoe UI", "Inter", "SF Pro Text", "Helvetica Neue",
                           "Cantarell", "Noto Sans", "Ubuntu", "DejaVu Sans") or tkfont.nametofont("TkDefaultFont").actual("family")
        self.display = pick("Segoe UI Variable Display", "Segoe UI Semibold", "Inter", "SF Pro Display") or self.family
        self.mono = pick("Cascadia Mono", "Consolas", "SF Mono", "Menlo", "DejaVu Sans Mono") or "TkFixedFont"
        self.set_mode(mode)

    def px(self, v: float) -> int:
        """A size in pixels at 96 dpi, in this screen's pixels."""
        return int(round(v * self.scale))

    def font(self, size: float = 10, weight: str = "normal", family: str | None = None):
        return (family or self.family, int(round(size)), weight)

    def set_mode(self, mode: str) -> None:
        self.mode = mode
        self.dark = (not system_prefers_light()) if mode == "system" else mode != "light"
        self.c = dict(DARK if self.dark else LIGHT)
        c = self.c
        c["accent_fill"] = mix(c["panel"], c["accent"], 0.14)
        c["bad_fill"] = mix(c["panel"], c["bad"], 0.10)
        c["warn_fill"] = mix(c["panel"], c["warn"], 0.10)
        c["danger_hover"] = mix(c["bad"], "#ffffff", 0.15)

    def rimg(self, key: str, w: int, h: int, r: float, fill: str, bg: str, outline: str | None = None, bw: float = 1.0):
        """A rounded image by key: made once, redrawn in place after that."""
        import tkinter as tk

        data = rounded_data(w, h, r, fill, bg, outline, bw)
        img = self.images.get(key)
        if img is None:
            img = tk.PhotoImage(master=self.root, width=w, height=h)
            self.images[key] = img
        else:
            img.blank()
            img.configure(width=w, height=h)
        img.put(data)
        return img

    # ---------------------------------------------------------------- styles
    def apply(self) -> None:
        from tkinter import ttk

        root, c, px = self.root, self.c, self.px
        st = ttk.Style(root)
        try:
            st.theme_use("clam")
        except Exception:
            pass
        names = set(st.element_names())

        def element(name: str, img, *states, border: int) -> None:
            if name not in names:
                st.element_create(name, "image", img, *states, border=border, padding=0, sticky="nsew")
                names.add(name)

        root.configure(bg=c["bg"])
        base = self.font(10)
        st.configure(".", background=c["bg"], foreground=c["text"], font=base, troughcolor=c["panel2"],
                     bordercolor=c["line"], lightcolor=c["panel2"], darkcolor=c["panel2"], focuscolor=c["accent"],
                     selectbackground=c["accent_fill"], selectforeground=c["text"], fieldbackground=c["panel2"],
                     insertcolor=c["text"], arrowcolor=c["dim"], relief="flat")
        st.configure("TFrame", background=c["bg"])
        st.configure("TLabel", background=c["bg"], foreground=c["text"])

        # cards: rounded, a one-pixel line; tinted ones for errors and warnings
        # ttk tiles an image element's middle to fill the widget: a wide middle keeps a large card cheap to draw
        r = px(12)
        size = 2 * r + 96
        for name, fill, line in (("Card", c["panel"], c["line"]),
                                 ("BadCard", c["bad_fill"], mix(c["line"], c["bad"], 0.55)),
                                 ("WarnCard", c["warn_fill"], mix(c["line"], c["warn"], 0.5))):
            img = self.rimg(f"{name}.img", size, size, r, fill, c["bg"], line)
            element(f"{name}.bg", img, border=r + 1)
            st.layout(f"{name}.TFrame", [(f"{name}.bg", {"sticky": "nsew", "children": [("Frame.padding", {"sticky": "nsew"})]})])
            st.configure(f"{name}.TFrame", background=fill, padding=px(16))

        # buttons: rounded fills per kind, on the page, on a card, on an error / warning card
        br = px(8)
        bsize = 2 * br + 32
        kinds = {
            "Primary": (c["accent"], c["accent_hover"], c["accent_press"], c["accent_ink"], None),
            "Secondary": (c["surface3"], c["hover"], c["line"], c["text"], c["line_strong"]),
            "Danger": (c["bad"], c["danger_hover"], mix(c["bad"], "#000000", 0.2), "#ffffff", None),
            "Ghost": (None, c["hover"], c["surface3"], c["dim"], None),
        }
        for surface, sbg in surfaces(c):
            for kind, (fill, hov, prs, ink, line) in kinds.items():
                name = f"{surface}{kind}"
                imgs = {state: self.rimg(f"{name}.{state}", bsize, bsize, br, f, sbg, line) for state, f in (
                    ("normal", fill or sbg), ("active", hov), ("pressed", prs),
                    ("disabled", mix(sbg, fill, 0.4) if fill else sbg))}
                focus = self.rimg(f"{name}.focus", bsize, bsize, br, hov, sbg, c["accent"], bw=max(1.5, px(2)))
                element(f"{name}.btn", imgs["normal"], ("disabled", imgs["disabled"]), ("pressed", imgs["pressed"]),
                        ("active", imgs["active"]), ("focus", focus), border=br + 1)
                for big in (False, True):
                    style = f"{surface}{'Big.' if big else ''}{kind}.TButton"
                    st.layout(style, [(f"{name}.btn", {"sticky": "nsew", "children": [("Button.padding", {
                        "sticky": "nsew", "children": [("Button.label", {"sticky": "nsew"})]})]})])
                    st.configure(style, foreground=ink, background=sbg, anchor="center",
                                 padding=(px(26), px(11)) if big else (px(14), px(6)),
                                 font=self.font(11 if big else 9.5, "bold" if (big or kind == "Primary") else "normal"))
                    st.map(style, foreground=[("disabled", mix(sbg, ink, 0.55))])

        # chips (filters, the maps / other jobs switch)
        cr = px(13)
        csize = 2 * cr + 24
        on = self.rimg("chip.on", csize, csize, cr, c["accent_fill"], c["bg"], c["accent"])
        off = self.rimg("chip.off", csize, csize, cr, c["panel"], c["bg"], c["line"])
        hov = self.rimg("chip.hover", csize, csize, cr, c["hover"], c["bg"], c["line_strong"])
        element("Chip.bg", off, ("selected", on), ("active", hov), border=cr + 1)
        st.layout("Chip.TRadiobutton", [("Chip.bg", {"sticky": "nsew", "children": [("Radiobutton.padding", {
            "sticky": "nsew", "children": [("Radiobutton.label", {"sticky": "nsew"})]})]})])
        st.configure("Chip.TRadiobutton", padding=(px(12), px(4)), foreground=c["dim"], background=c["bg"], font=self.font(9.5))
        st.map("Chip.TRadiobutton", foreground=[("selected", c["accent"]), ("active", c["text"])])

        # fields
        for w in ("TEntry", "TCombobox"):
            st.configure(w, fieldbackground=c["panel2"], foreground=c["text"], bordercolor=c["line"],
                         lightcolor=c["panel2"], darkcolor=c["panel2"], padding=(px(8), px(5)), insertcolor=c["text"],
                         arrowcolor=c["dim"], background=c["panel2"], selectbackground=c["accent_fill"],
                         selectforeground=c["text"])
            st.map(w, bordercolor=[("focus", c["accent"])], lightcolor=[("focus", c["panel2"])],
                   fieldbackground=[("readonly", c["panel2"])], foreground=[("disabled", c["faint"])],
                   background=[("readonly", c["panel2"]), ("active", c["hover"])])
        root.option_add("*TCombobox*Listbox.background", c["panel2"])
        root.option_add("*TCombobox*Listbox.foreground", c["text"])
        root.option_add("*TCombobox*Listbox.selectBackground", c["accent_fill"])
        root.option_add("*TCombobox*Listbox.selectForeground", c["text"])
        root.option_add("*TCombobox*Listbox.font", base)

        for surface, sbg in surfaces(c):
            st.configure(f"{surface}TCheckbutton", background=sbg, foreground=c["dim"], indicatorbackground=c["panel2"],
                         indicatorforeground=c["accent"], indicatormargin=(0, 0, px(6), 0), bordercolor=c["line_strong"],
                         font=self.font(9.5), upperbordercolor=c["line_strong"], lowerbordercolor=c["line_strong"])
            st.map(f"{surface}TCheckbutton", background=[("active", sbg)], foreground=[("active", c["text"])],
                   indicatorbackground=[("selected", c["panel2"]), ("active", c["hover"])])

        # the map list
        st.configure("Treeview", background=c["panel"], fieldbackground=c["panel"], foreground=c["text"],
                     bordercolor=c["panel"], lightcolor=c["panel"], darkcolor=c["panel"], rowheight=px(30),
                     font=self.font(10))
        st.map("Treeview", background=[("selected", c["hover"])], foreground=[("selected", c["text"])])
        st.configure("Treeview.Heading", background=c["panel"], foreground=c["faint"], bordercolor=c["panel"],
                     lightcolor=c["panel"], darkcolor=c["panel"], relief="flat", font=self.font(8.5, "bold"),
                     padding=(px(6), px(4)))
        st.map("Treeview.Heading", background=[("active", c["panel"])], foreground=[("active", c["text"])])
        st.layout("Treeview", [("Treeview.treearea", {"sticky": "nsew"})])

        # slim scroll bars without arrows
        for o in ("Vertical", "Horizontal"):
            st.layout(f"{o}.TScrollbar", [(f"{o}.Scrollbar.trough", {"sticky": "ns" if o == "Vertical" else "ew", "children": [
                (f"{o}.Scrollbar.thumb", {"expand": "1", "sticky": "nsew"})]})])
            st.configure(f"{o}.TScrollbar", troughcolor=c["panel"], background=c["surface3"], bordercolor=c["panel"],
                         lightcolor=c["surface3"], darkcolor=c["surface3"], gripcount=0, arrowsize=px(8), width=px(8))
            st.map(f"{o}.TScrollbar", background=[("active", c["line_strong"])])


def surfaces(c: dict) -> tuple[tuple[str, str], ...]:
    """Style prefixes for what a widget sits on: the page, a card, an error card, a warning card."""
    return (("", c["bg"]), ("Card.", c["panel"]), ("BadCard.", c["bad_fill"]), ("WarnCard.", c["warn_fill"]))


# ------------------------------------------------------------------ widgets
class HeatBar:
    """A progress bar coloured by the logo's heat ramp; `set(fraction)`, or `busy()` when the end is unknown."""

    def __init__(self, parent, theme: Theme, bg: str, height: int = 10):
        import tkinter as tk

        self.t, self.bg = theme, bg
        self.h = theme.px(height)
        self.cv = tk.Canvas(parent, height=self.h, bg=bg, highlightthickness=0, bd=0)
        self.frac = 0.0
        self.anim = None
        self.phase = 0.0
        self.cv.bind("<Configure>", lambda e: self.draw())

    def set(self, frac: float) -> None:
        self.stop()
        self.frac = max(0.0, min(1.0, frac))
        self.draw()

    def busy(self) -> None:
        if self.anim is None:
            self._tick()

    def stop(self) -> None:
        if self.anim is not None:
            try:
                self.cv.after_cancel(self.anim)
            except Exception:
                pass
            self.anim = None

    def _tick(self) -> None:
        self.phase = (self.phase + 0.01) % 1.35
        self.draw()
        self.anim = self.cv.after(33, self._tick)

    def draw(self) -> None:
        import math

        cv, c = self.cv, self.t.c
        try:
            w = max(2, cv.winfo_width())
        except Exception:
            return
        h = self.h
        r = h / 2
        cv.delete("all")
        cv.create_rectangle(0, 0, w, h, fill=c["surface3"], outline="")
        if self.anim is not None:
            a, b = (self.phase - 0.35) * w, self.phase * w
        else:
            a, b = 0.0, self.frac * w
        a, b = max(0.0, a), min(float(w), b)
        if b - a >= 1:
            step = max(2, w // 140)
            x = a
            while x < b:
                x2 = min(b, x + step)
                cv.create_rectangle(x, 0, x2, h, fill=ramp(x / w), outline="")
                x = x2
        # the pill's round ends: the page colour outside two half circles
        arc = [(r - r * math.sin(t), r - r * math.cos(t)) for t in (i * math.pi / 16 for i in range(17))]
        cv.create_polygon(0, 0, *[v for p in arc for v in p], 0, h, fill=self.bg, outline="")
        cv.create_polygon(w, 0, *[v for x, y in arc for v in (w - x, y)], w, h, fill=self.bg, outline="")


class Steps:
    """The step bar: 1 Game, 2 Choose, 3 Run, 4 Done; earlier steps can be clicked."""

    def __init__(self, parent, theme: Theme, labels: list[str], on_click=None):
        import tkinter as tk

        self.t = theme
        self.labels = labels
        self.current = 0
        self.enabled: set[int] = set()
        self.on_click = on_click
        self.cv = tk.Canvas(parent, height=theme.px(40), bg=theme.c["bg"], highlightthickness=0, bd=0)
        self.cv.bind("<Configure>", lambda e: self.draw())
        self.hits: list[tuple[float, float, int]] = []
        self.cv.bind("<Button-1>", self._click)
        self.cv.bind("<Motion>", self._motion)

    def set(self, current: int, enabled: set[int]) -> None:
        self.current, self.enabled = current, enabled
        self.draw()

    def _target(self, x: float) -> int | None:
        for a, b, i in self.hits:
            if a <= x <= b and i in self.enabled and i != self.current:
                return i
        return None

    def _motion(self, e) -> None:
        self.cv.config(cursor="hand2" if self._target(e.x) is not None else "")

    def _click(self, e) -> None:
        i = self._target(e.x)
        if i is not None and self.on_click:
            self.on_click(i)

    def draw(self) -> None:
        t, c, cv = self.t, self.t.c, self.cv
        cv.delete("all")
        cv.config(bg=c["bg"])
        w = max(1, cv.winfo_width())
        n = len(self.labels)
        d = t.px(24)
        y = t.px(20)
        pad = t.px(24)
        seg = (w - 2 * pad) / max(1, n)
        self.hits = []
        ends = []
        for key, fill, line in (("done", c["accent"], None), ("cur", c["accent_fill"], c["accent"]),
                                ("todo", c["bg"], c["line_strong"])):
            t.rimg(f"step.{key}", d, d, d / 2, fill, c["bg"], line, bw=max(1.5, t.px(1.5)))
        for i, label in enumerate(self.labels):
            x = pad + i * seg
            done, cur = i < self.current, i == self.current
            key = "done" if done else "cur" if cur else "todo"
            cv.create_image(x, y, image=t.images[f"step.{key}"], anchor="w")
            cv.create_text(x + d / 2, y, text="✓" if done else str(i + 1), font=t.font(9, "bold"),
                           fill=c["accent_ink"] if done else c["accent"] if cur else c["faint"])
            fg = c["text"] if cur else c["dim"] if (done or i in self.enabled) else c["faint"]
            tx = cv.create_text(x + d + t.px(8), y, text=label, anchor="w", fill=fg, font=t.font(10, "bold" if cur else "normal"))
            bb = cv.bbox(tx) or (x, 0, x + seg / 2, 0)
            self.hits.append((x, bb[2], i))
            ends.append((x, bb[2]))
        for i in range(1, n):
            x0, x1 = ends[i - 1][1] + t.px(12), ends[i][0] - t.px(12)
            if x1 > x0:
                cv.create_line(x0, y, x1, y, fill=c["accent"] if i <= self.current else c["line"], width=max(1, t.px(1.5)))


def dot(theme: Theme, parent, colour: str, bg: str, size: int = 10):
    """A small round status mark."""
    import tkinter as tk

    px = theme.px(size)
    img = theme.rimg(f"dot.{colour}.{bg}.{px}", px, px, px / 2, colour, bg)
    return tk.Label(parent, image=img, bg=bg, bd=0)


def badge(theme: Theme, parent, kind: str, bg: str, size: int = 64):
    """The big round mark on the last step: ok, partial, failed or stopped."""
    import tkinter as tk

    c = theme.c
    px = theme.px(size)
    colour = {"ok": c["good"], "partial": c["warn"], "failed": c["bad"], "stopped": c["faint"]}[kind]
    glyph = {"ok": "✓", "partial": "!", "failed": "✕", "stopped": "■"}[kind]
    cv = tk.Canvas(parent, width=px, height=px, bg=bg, highlightthickness=0, bd=0)
    img = theme.rimg(f"badge.{kind}.{bg}.{px}", px, px, px / 2, mix(bg, colour, 0.16), bg, colour, bw=max(2, theme.px(2)))
    cv.create_image(0, 0, image=img, anchor="nw")
    cv.create_text(px / 2, px / 2, text=glyph, fill=colour, font=theme.font(size * 0.34, "bold"))
    return cv
