"""
The window a 3DHeat tool opens when started without arguments.

Four steps, one page each: 1 find the game (and what else a run needs, and
where the maps go), 2 choose the maps to extract or the job to run, 3 watch it
work (progress, time left, cancel), 4 done (open in 3DHeat, open the folder,
what to do when something failed). Recorders and watchers run until stopped
on step 3. Updates are offered, never applied without asking unless the user
ticked "Update automatically".

The work runs as a child process of the same executable (`extract
--progress-json`, or one of the tool's commands), so the window stays
responsive and a crash in one map cannot take it down. Same file in every tool.
"""

from __future__ import annotations

import json
import os
import queue
import re
import shutil
import subprocess
import sys
import threading
import time
import webbrowser
from pathlib import Path

from . import paths, update
from .manifest import game_status
from .spec import Spec, Task, game_folders, load_settings, save_settings, standard_checks
from .theme import BRAND_BAR, HeatBar, Theme, app_id, badge, dot, dpi_aware, load_png, mix, title_bar

STATE_TEXT = {"new": "New", "changed": "Game update", "outdated": "Older version",
              "current": "Up to date", "missing": "Gone from the game"}  # short: the heading above says it in full
PENDING = ("new", "changed", "outdated")
APP_PAGE = "https://holdi601.github.io/3DHeat/"
URL = re.compile(r"https?://[^\s)\"']+")


def self_command(spec: Spec) -> list[str]:
    if update.frozen():
        return [sys.executable]
    return [sys.executable, "-m", spec.module]


class Model:
    """What the window shows, without any window (also what `--gui-selftest` builds)."""

    def __init__(self, spec: Spec):
        self.spec = spec
        self.refresh()

    def refresh(self) -> None:
        self.levels = paths.levels_dir()
        self.found = game_folders(self.spec)
        self.checks = standard_checks(self.spec, self.found, self.levels)
        self.status = [game_status(g, self.found.get(g.key), self.levels, self.spec.id)
                       for g in self.spec.games if g.maps is not None]

    def problems(self) -> list:
        return [c for c in self.checks if not c.ok]


# ------------------------------------------------------------- 3DHeat itself
def find_app() -> list[str] | None:
    """The 3DHeat desktop app on this computer, as the command that opens its Library; None if not installed."""
    env = os.environ.get("HEAT3D_APP")
    if env and Path(env).exists():
        return [env, "--library"]
    if os.name == "nt":
        cands: list[Path] = []
        try:
            import winreg

            for hive, base in ((winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Uninstall"),
                               (winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Uninstall"),
                               (winreg.HKEY_LOCAL_MACHINE, r"Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall")):
                try:
                    root = winreg.OpenKey(hive, base)
                except OSError:
                    continue
                for i in range(winreg.QueryInfoKey(root)[0]):
                    try:
                        with winreg.OpenKey(root, winreg.EnumKey(root, i)) as k:
                            if winreg.QueryValueEx(k, "DisplayName")[0] != "3DHeat":
                                continue
                            for v in ("InstallLocation", "DisplayIcon"):
                                try:
                                    p = Path(str(winreg.QueryValueEx(k, v)[0]).split(",")[0].strip('"'))
                                    cands.append(p if p.suffix.lower() != ".exe" else p.parent)
                                except OSError:
                                    pass
                    except OSError:
                        continue
        except ImportError:
            pass
        for env_name, sub in (("LOCALAPPDATA", "3DHeat"), ("LOCALAPPDATA", r"Programs\3DHeat"), ("ProgramFiles", "3DHeat")):
            if os.environ.get(env_name):
                cands.append(Path(os.environ[env_name]) / sub)
        for d in cands:
            exe = d / "3dheat-app.exe"
            if exe.is_file():
                return [str(exe), "--library"]
        return None
    if sys.platform == "darwin":
        for d in (Path("/Applications/3DHeat.app"), Path.home() / "Applications" / "3DHeat.app"):
            if d.exists():
                return ["open", "-a", str(d), "--args", "--library"]
        return None
    exe = shutil.which("3dheat-app")
    return [exe, "--library"] if exe else None


def open_folder(p: Path) -> None:
    try:
        p.mkdir(parents=True, exist_ok=True)
        if os.name == "nt":
            os.startfile(str(p))  # noqa: S606 - the user's own folder
        elif sys.platform == "darwin":
            subprocess.Popen(["open", str(p)])
        else:
            subprocess.Popen(["xdg-open", str(p)])
    except OSError:
        pass


def advice(text: str, spec: Spec) -> str:
    """One plain line on what to do about an error message."""
    t = text.lower()
    if "oodle" in t or "oo2core" in t:
        return "The tool needs a library from your own game install. Check step 1, then try again."
    if "permission" in t or "access is denied" in t or "winerror 5" in t or "being used by another process" in t:
        return "Close the game and 3DHeat (they may hold the files open), then try again."
    if "no space" in t or "disk full" in t or "errno 28" in t:
        return "The disk is full. Free some space, or choose another folder for the maps in step 1."
    if "memoryerror" in t or "out of memory" in t:
        return "The computer ran out of memory. Close other programs and extract fewer maps at once."
    if "filenotfound" in t or "no such file" in t or "not found" in t:
        return "A game file is missing. Let the game finish updating, check its folder in step 1, then try again."
    if "timeout" in t or "timed out" in t or "connection" in t:
        return "A connection timed out. Check the internet connection and try again."
    return "Try again. If it fails again, press “Copy details” and report it on the tool's GitHub page."


def fmt_time(s: float) -> str:
    s = int(max(0, s))
    return f"{s // 3600}:{s // 60 % 60:02d}:{s % 60:02d}" if s >= 3600 else f"{s // 60}:{s % 60:02d}"


def fmt_left(s: float) -> str:
    if s < 50:
        return "less than a minute left"
    m = round(s / 60)
    if m < 60:
        return f"about {m} min left"
    return f"about {m // 60} h {m % 60:02d} min left"


def short_name(spec: Spec) -> str:
    n = spec.name
    return n[len("3DHeat "):] if n.startswith("3DHeat ") else n


# ------------------------------------------------------------------ running
def selftest(spec: Spec, target: update.Target) -> int:
    """Build the model; with a display, also every page and dialog of the window (CI)."""
    m = Model(spec)
    assert m.checks, "no checks"
    for t in spec.tasks:
        t.argv({i.key: "x" for i in t.inputs}, m.levels)
    try:
        import tkinter as tk

        root = tk.Tk()
        root.withdraw()
    except Exception as e:  # no display (CI on Linux without X): the model is what is tested
        shown = f"no window ({type(e).__name__})"
    else:
        try:
            app = App(root, spec, target, m, check_updates=False)
            app.exercise()
            root.update_idletasks()
            shown = "window built, every page drawn"
        finally:
            root.destroy()
    print(f"gui-selftest ok: {len(m.checks)} checks, {sum(len(s['maps']) for s in m.status)} maps, {shown}")
    return 0


def run(spec: Spec, target: update.Target) -> int:
    import tkinter as tk

    dpi_aware()
    app_id(spec.id)
    root = tk.Tk()
    root.withdraw()
    App(root, spec, target, Model(spec))
    root.deiconify()
    root.mainloop()
    return 0


class App:
    STEPS = ("Find the game", "Choose", "Work", "Done")

    def __init__(self, root, spec: Spec, target: update.Target, model: Model, check_updates: bool = True):
        import tkinter as tk

        self.tk = tk
        self.root, self.spec, self.target, self.model = root, spec, target, model
        self.events: queue.Queue = queue.Queue()
        self.proc: subprocess.Popen | None = None
        self.settings = load_settings(spec.id)
        self.theme = Theme(root, str(self.settings.get("theme", "system")))
        self.app_cmd = find_app()
        self.page = "setup" if self._blocked() or not (spec.has_maps() or spec.tasks) else "choose"
        self.tab = tk.StringVar(value="maps" if spec.has_maps() else "tasks")
        self.filter = tk.StringVar(value="todo")
        self.search = tk.StringVar()
        self.search.trace_add("write", lambda *a: (self.fill_tree(), getattr(self, "_ph_update", lambda: None)()))
        self.levels_var = tk.StringVar(value=str(model.levels))
        self.auto_var = tk.BooleanVar(value=bool(self.settings.get("auto_update")))
        self.checked: set[str] = {self._key(s["game"], m["id"]) for s in model.status for m in s["maps"] if m["state"] in PENDING}
        self.inputs: dict[str, dict[str, object]] = {}
        self.run: dict = {}
        self.log_lines: list[str] = []
        self.show_log = False
        self.queue: list[tuple[list[str], int]] = []
        self.flash_after = None
        self.primary = None
        self.pulse_on = False
        # The tray icon of a background recorder (spec.tray), made at its first recording.
        self.tray = None
        self.live_task: Task | None = None
        self.pausing = False
        self.hidden_told = False

        root.title(spec.name if spec.name.startswith("3DHeat") else f"3DHeat {spec.name}")
        self.task_sel = spec.tasks[0].id if spec.tasks else ""
        px = self.theme.px
        w, h = px(1120), px(740)
        sw, sh = root.winfo_screenwidth(), root.winfo_screenheight()
        w, h = min(w, sw - px(40)), min(h, sh - px(80))
        root.geometry(f"{w}x{h}+{max(0, (sw - w) // 2)}+{max(0, (sh - h) // 3)}")
        root.minsize(min(px(880), w), min(px(600), h))
        geo = os.environ.get("HEAT3D_GUI_GEOMETRY", "")  # screenshots: "small", "max" or WxH
        if geo == "small":
            root.geometry(f"{min(px(880), w)}x{min(px(600), h)}")
        elif geo == "max":
            try:
                root.state("zoomed")
            except Exception:
                root.attributes("-zoomed", True)
        elif geo:
            root.geometry(geo)
        icons = [i for i in (load_png(root, "tool-32.png") or load_png(root, "icon-32.png"),
                             load_png(root, "tool-64.png") or load_png(root, "icon-64.png"),
                             load_png(root, "tool-256.png") or load_png(root, "icon-256.png")) if i]
        if icons:
            self._icons = icons
            root.iconphoto(True, *icons)
        root.protocol("WM_DELETE_WINDOW", self.close)
        root.bind("<Return>", lambda e: self.primary() if self.primary and not isinstance(e.widget, tk.Text) else None)
        self.build()
        if os.environ.get("HEAT3D_GUI_DEMO"):
            root.after(300, lambda: self.demo(os.environ["HEAT3D_GUI_DEMO"]))
        root.after(100, self.pump)
        if check_updates:
            threading.Thread(target=self._bg_update_check, daemon=True).start()

    # ------------------------------------------------------------ helpers
    @staticmethod
    def _key(game: str, map_id: str) -> str:
        return f"{game}\x1f{map_id}"

    def _blocked(self) -> bool:
        """Step 1 first when no game is found (or a check fails)."""
        return bool(self.model.problems())

    def c(self, name: str) -> str:
        """A theme colour by name, or a literal colour."""
        return self.theme.c.get(name, name)

    def label(self, parent, text: str = "", *, size: float = 10, weight: str = "normal", fg: str = "text",
              bg: str = "bg", wrap: int = 0, family: str | None = None, **kw):
        tk = self.tk
        lab = tk.Label(parent, text=text, font=self.theme.font(size, weight, family), fg=self.c(fg),
                       bg=self.c(bg), anchor="w", justify="left", bd=0, **kw)
        if wrap:
            lab.config(wraplength=self.theme.px(wrap))
        return lab

    def frame(self, parent, bg: str = "bg", **kw):
        kw.setdefault("highlightthickness", 0)
        return self.tk.Frame(parent, bg=self.c(bg), bd=0, **kw)

    def card(self, parent, kind: str = "Card", pad: int = 16):
        from tkinter import ttk

        f = ttk.Frame(parent, style=f"{kind}.TFrame", padding=self.theme.px(pad))
        return f

    def button(self, parent, text: str, command, kind: str = "Secondary", surface: str = "", big: bool = False, **kw):
        from tkinter import ttk

        return ttk.Button(parent, text=text, command=command, style=f"{surface}{'Big.' if big else ''}{kind}.TButton",
                          cursor="hand2", takefocus=True, **kw)

    def link(self, parent, text: str, command, bg: str = "bg", fg: str = "accent"):
        lab = self.label(parent, text, size=9.5, fg=fg, bg=bg, cursor="hand2")
        lab.bind("<Button-1>", lambda e: command())
        lab.bind("<Enter>", lambda e: lab.config(font=self.theme.font(9.5) + ("underline",)))
        lab.bind("<Leave>", lambda e: lab.config(font=self.theme.font(9.5)))
        return lab

    def flash(self, text: str, tone: str = "dim", seconds: float = 10) -> None:
        try:
            self.flash_label.config(text=text, fg=self.c(tone))
        except Exception:
            return
        if self.flash_after:
            self.root.after_cancel(self.flash_after)
        self.flash_after = self.root.after(int(seconds * 1000), lambda: self.flash_label.config(text=""))

    # ------------------------------------------------------------- layout
    def build(self) -> None:
        """The whole window; again after a dark/light switch. Brand bar on top; a rail on the left (the tool,
        the steps, what is found, settings); the page fills the rest and grows with the window."""
        for w in self.root.winfo_children():
            if not isinstance(w, self.tk.Toplevel):
                w.destroy()
        t = self.theme
        t.apply()
        title_bar(self.root, t.dark, self.c("bg") if t.dark else None)
        px = t.px

        # brand bar: the 3DHEAT lockup, the tool's name, the version
        bar = self.frame(self.root, BRAND_BAR, height=px(56))
        bar.pack(fill="x")
        bar.pack_propagate(False)
        logo = load_png(self.root, "lockup-64.png" if px(30) > 40 else "lockup-32.png")
        if logo is not None:
            self._logo = logo
            self.tk.Label(bar, image=logo, bg=BRAND_BAR, bd=0).pack(side="left", padx=(px(20), px(14)))
        self.tk.Frame(bar, bg="#273040", width=1, height=px(26)).pack(side="left")
        self.label(bar, short_name(self.spec), size=12.5, weight="bold", fg="#e6ebf2", bg=BRAND_BAR,
                   family=t.display).pack(side="left", padx=(px(14), px(10)))
        sub = self.spec.description or ("maps for 3DHeat" if self.spec.has_maps() else "for 3DHeat")
        self.label(bar, sub, size=9, fg="#7d8899", bg=BRAND_BAR).pack(side="left")
        self.label(bar, f"v{self.spec.version}", size=8.5, fg="#a3adbd", bg="#151a22", padx=px(8), pady=px(2)).pack(
            side="right", padx=px(18))
        self.tk.Frame(self.root, bg="#46c8ff" if t.dark else self.c("accent"), height=max(1, px(1))).pack(fill="x")

        # the rail
        rail = self.frame(self.root, "panel", width=px(250))
        rail.pack(side="left", fill="y")
        rail.pack_propagate(False)
        self.tk.Frame(self.root, bg=self.c("line"), width=1).pack(side="left", fill="y")
        self.rail = rail
        self._rail()

        # the page
        main = self.frame(self.root)
        main.pack(side="left", fill="both", expand=True)
        self.flash_label = self.label(main, "", size=9, fg="dim")
        self.flash_label.pack(side="bottom", fill="x", padx=px(28), pady=(0, px(8)))
        self.body = self.frame(main)
        self.body.pack(fill="both", expand=True, padx=px(28), pady=(px(18), px(4)))
        self.show(self.page)

    def _rail(self) -> None:
        from tkinter import ttk

        t, px, rail = self.theme, self.theme.px, self.rail
        for w in rail.winfo_children():
            w.destroy()
        # the tool
        head = self.frame(rail, "panel")
        head.pack(fill="x", padx=px(18), pady=(px(18), px(10)))
        icon = load_png(self.root, "tool-64.png") or load_png(self.root, "icon-64.png")
        if icon is not None:
            if px(48) < 60:
                icon = icon.subsample(max(1, round(64 / px(48))))
            self._tool_icon = icon
            self.tk.Label(head, image=icon, bg=self.c("panel"), bd=0).pack(side="left", padx=(0, px(10)))
        names = self.frame(head, "panel")
        names.pack(side="left", fill="x")
        self.label(names, short_name(self.spec), size=11, weight="bold", bg="panel", family=t.display).pack(anchor="w")
        self.label(names, "for 3DHeat", size=8.5, fg="faint", bg="panel").pack(anchor="w")

        # the steps, top to bottom
        self.label(rail, "STEPS", size=8, weight="bold", fg="faint", bg="panel").pack(anchor="w", padx=px(20), pady=(px(10), px(4)))
        self.step_rows = []
        for i, text in enumerate(self._step_labels()):
            row = self.frame(rail, "panel", cursor="hand2")
            row.pack(fill="x", padx=px(10), pady=1)
            mark = self.tk.Label(row, bd=0, compound="center", font=t.font(9, "bold"))
            mark.pack(side="left", padx=(px(10), px(10)), pady=px(7))
            lab = self.tk.Label(row, text=text, bd=0, anchor="w", font=t.font(10))
            lab.pack(side="left", fill="x", expand=True)
            for w in (row, mark, lab):
                w.bind("<Button-1>", lambda e, i=i: self._step_click(i))
            self.step_rows.append((row, mark, lab))

        # what was found
        self.label(rail, "STATUS", size=8, weight="bold", fg="faint", bg="panel").pack(anchor="w", padx=px(20), pady=(px(18), px(4)))
        self.status_box = self.frame(rail, "panel")
        self.status_box.pack(fill="x", padx=px(14))
        self._rail_status()

        # settings at the bottom
        bottom = self.frame(rail, "panel")
        bottom.pack(side="bottom", fill="x", padx=px(18), pady=(0, px(14)))
        if self.spec.notice:
            self.label(bottom, self.spec.notice, size=8, fg="faint", bg="panel", wrap=210).pack(side="bottom", anchor="w",
                                                                                              pady=(px(10), 0))
        ttk.Checkbutton(bottom, text="Update automatically", variable=self.auto_var, style="Card.TCheckbutton",
                        command=lambda: update.set_auto(self.spec.id, self.auto_var.get())).pack(side="bottom", anchor="w",
                                                                                                 pady=(px(6), 0))
        links = self.frame(bottom, "panel")
        links.pack(side="bottom", fill="x")
        self.link(links, "Check for updates", lambda: self.check_updates(manual=True), bg="panel").pack(side="left")
        self.link(links, "☾ Dark" if not t.dark else "☀ Light", self.toggle_theme, bg="panel",
                  fg="dim").pack(side="right")
        self.tk.Frame(bottom, bg=self.c("line"), height=1).pack(side="bottom", fill="x", pady=(0, px(10)))

    def _rail_status(self) -> None:
        """One line per check: a dot and a short word; a click goes to step 1."""
        px = self.theme.px
        box = self.status_box
        for w in box.winfo_children():
            w.destroy()
        for chk in self.model.checks:
            tone = "good" if chk.ok else ("warn" if chk.id == "disk" else "bad")
            row = self.frame(box, "panel", cursor="hand2")
            row.pack(fill="x", pady=px(2))
            d = dot(self.theme, row, self.c(tone), self.c("panel"), 9)
            d.pack(side="left", padx=(px(6), px(8)))
            text = chk.label
            if chk.id.startswith("game:"):
                text = chk.label.replace(" install", "") + (" found" if chk.ok else " not found")
            elif chk.id == "disk":
                text = (chk.detail.split(" where")[0] if chk.ok else "Low disk space")
            text = text if len(text) <= 30 else text[:29] + "…"
            lab = self.label(row, text, size=9, fg="dim" if chk.ok else tone, bg="panel")
            lab.pack(side="left", fill="x")
            for w in (row, d, lab):
                w.bind("<Button-1>", lambda e: self.show("setup") if self.proc is None else None)

    def _paint_steps(self, idx: int) -> None:
        t, c = self.theme, self.theme.c
        d = t.px(24)
        for key, fill, line in (("done", c["accent"], None), ("cur", c["accent_fill"], c["accent"]),
                                ("todo", c["panel"], c["line_strong"])):
            t.rimg(f"rail.{key}", d, d, d / 2, fill, c["panel"], line, bw=max(1.5, t.px(1.5)))
        enabled = set() if self.proc is not None else {0, 1} | ({3} if self.run.get("ended") else set())
        labels = self._step_labels()
        for i, (row, mark, lab) in enumerate(self.step_rows):
            done, cur = i < idx, i == idx
            key = "done" if done else "cur" if cur else "todo"
            bg = c["accent_fill"] if cur else c["panel"]
            row.config(bg=bg, cursor="hand2" if i in enabled and not cur else "")
            mark.config(image=t.images[f"rail.{key}"], text="✓" if done else str(i + 1), bg=bg,
                        fg=c["accent_ink"] if done else c["accent"] if cur else c["faint"])
            lab.config(text=labels[i], bg=bg, fg=c["text"] if cur else c["dim"] if (done or i in enabled) else c["faint"],
                       font=t.font(10, "bold" if cur else "normal"))

    def _step_labels(self) -> tuple[str, ...]:
        third = "Extract"
        task = self.run.get("task")
        if task is not None:
            third = {"live": "Record" if "record" in task.label.lower() else "Run"}.get(task.kind, "Convert")
        elif not self.spec.has_maps():
            third = "Run"
        return ("Find the game" if self.spec.games else "Check", "Choose", third, "Done")

    def _step_click(self, i: int) -> None:
        if self.proc is not None:
            return
        page = ("setup", "choose", "run", "done")[i]
        if page == "done" and not self.run.get("ended") or page == "run" and not self.run:
            return
        self.show(page)

    def toggle_theme(self) -> None:
        mode = "light" if self.theme.dark else "dark"
        self.settings = load_settings(self.spec.id)
        self.settings["theme"] = mode
        save_settings(self.spec.id, self.settings)
        self.theme.set_mode(mode)
        self.build()

    def show(self, page: str) -> None:
        self.page = page
        for w in self.body.winfo_children():
            w.destroy()
        self.primary = None
        self.bar = None
        self.log_text = None
        self._paint_steps(("setup", "choose", "run", "done").index(page))
        try:
            self._rail_status()
        except Exception:
            pass
        getattr(self, f"page_{page}")()

    def autowrap(self, lab, parent=None, margin: int = 0):
        """A label whose text wraps at its container's width less `margin`, with the window. The container's
        width must not depend on the label (a card or frame that fills its parent), or the two would chase
        each other."""
        box = parent if parent is not None else lab.master

        def wrap(e):
            try:
                w = max(120, e.width - margin)
                if lab.winfo_exists() and abs(int(lab.cget("wraplength") or 0) - w) > 2:
                    lab.config(wraplength=w)
            except Exception:
                pass

        box.bind("<Configure>", wrap, add="+")
        return lab

    def wrap_beside(self, lab, bar) -> None:
        """A label on the left of an action bar that wraps into the room the bar's right-hand buttons leave."""
        px = self.theme.px

        def wrap(e):
            try:
                used = sum(w.winfo_reqwidth() + px(8) for w in bar.pack_slaves()
                           if w is not lab and w.pack_info().get("side") == "right")
                w = max(px(80), e.width - used - px(12))
                if lab.winfo_exists() and abs(int(lab.cget("wraplength") or 0) - w) > 2:
                    lab.config(wraplength=w)
            except Exception:
                pass

        bar.bind("<Configure>", wrap, add="+")

    def heading(self, parent, title: str, sub: str = "", right=None):
        px = self.theme.px
        row = self.frame(parent)
        row.pack(fill="x")
        self.label(row, title, size=18, weight="bold", family=self.theme.display).pack(side="left", anchor="w")
        if right is not None:
            right(row)
        if sub:
            box = self.frame(parent)
            box.pack(fill="x", pady=(px(2), px(12)))
            lab = self.label(box, sub, size=10, fg="dim", wrap=700)
            lab.pack(anchor="w")
            self.autowrap(lab, box, px(4))
        else:
            self.frame(parent, height=px(12)).pack()
        return row

    def action_bar(self, parent):
        px = self.theme.px
        bar = self.frame(parent)
        bar.pack(side="bottom", fill="x", pady=(px(12), px(6)))
        return bar

    # ------------------------------------------------------------- step 1
    def page_setup(self) -> None:
        self._compact = 0 < self._window_height() < self.theme.px(760)
        px, spec = self.theme.px, self.spec
        games = ", ".join(g.label for g in spec.games)
        if spec.games and spec.has_maps():
            sub = f"This tool reads the maps from your own {games} install and puts them where 3DHeat finds them."
        elif spec.games:
            sub = f"This tool turns what {games} leaves on your computer into files 3DHeat opens."
        else:
            sub = "Everything this tool needs, and where its results go."
        self.heading(self.body, "Find the game" if spec.games else "Check the setup", sub)
        bar = self.action_bar(self.body)
        problems = self.model.problems()
        go = self.button(bar, "Continue anyway  →" if problems else "Continue  →", lambda: self.show("choose"),
                         "Primary", big=True)
        go.pack(side="right")
        self.primary = lambda: self.show("choose")
        self.button(bar, "Check again", self.refresh, "Ghost").pack(side="right", padx=(0, px(8)))
        if problems:
            hint = self.label(bar, f"{len(problems)} thing{'s' if len(problems) != 1 else ''} to look at; "
                              "you can still go on and use what works.", size=9.5, fg="warn")
            hint.pack(side="left", fill="x", expand=True)
            self.wrap_beside(hint, bar)
        else:
            self.label(bar, "All set.", size=9.5, fg="good").pack(side="left")

        list_ = self.frame(self.body)
        list_.pack(fill="both", expand=True)
        # a card for each game and each problem; what else is fine goes on one line
        fine = [c for c in self.model.checks if c.ok and not c.id.startswith("game:")]
        for chk in self.model.checks:
            if chk not in fine:
                self._check_card(list_, chk)
        if fine:
            card = self.card(list_, pad=10 if self._compact else 12)
            card.pack(fill="x", pady=(0, px(8)))
            row = self.frame(card, "panel")
            row.pack(fill="x", padx=px(4))
            dot(self.theme, row, self.c("good"), self.c("panel")).pack(side="left", padx=(0, px(12)))
            self.label(row, "Also ready:", size=10, weight="bold", bg="panel").pack(side="left", padx=(0, px(8)))
            text = "   ·   ".join(c.detail.split(" where")[0] if c.id == "disk" else c.label for c in fine)
            rest = self.label(row, text, size=9.5, fg="dim", bg="panel", wrap=600)
            rest.pack(side="left", fill="x")
            self.autowrap(rest, card, px(220))
        if self._window_height() > px(760):
            self._how_it_works(list_)
        # where the maps go
        card = self.card(list_, pad=10 if self._compact else 16)
        card.pack(fill="x", pady=(0, px(8)))
        dot(self.theme, card, self.c("accent"), self.c("panel")).grid(row=0, column=0, rowspan=2, sticky="n",
                                                                         padx=(0, px(12)), pady=(px(5), 0))
        self.label(card, "Where the maps go" if spec.has_maps() else "3DHeat's data folder", size=10.5, weight="bold",
                   bg="panel").grid(row=0, column=1, sticky="w")
        where = self.label(card, f"{self.levels_var.get()}   — 3DHeat reads its levels from here", size=9.5,
                           fg="dim", bg="panel", wrap=560)
        where.grid(row=1, column=1, sticky="we")
        self.autowrap(where, card, px(300))
        acts = self.frame(card, "panel")
        acts.grid(row=0, column=2, rowspan=2, sticky="e")
        self.button(acts, "Open", lambda: open_folder(Path(self.levels_var.get())), "Ghost", "Card.").pack(side="right")
        self.button(acts, "Change…", self.choose_levels, "Secondary", "Card.").pack(side="right", padx=(0, px(6)))
        card.columnconfigure(1, weight=1)

    def _window_height(self) -> int:
        try:
            if self.root.state() == "zoomed":
                return self.root.winfo_screenheight()
            return max(self.root.winfo_height(), int(self.root.geometry().split("x")[1].split("+")[0]))
        except Exception:
            return 0

    def _how_it_works(self, parent) -> None:
        """Three short steps at the foot of step 1, for a first start on a tall window."""
        px, t = self.theme.px, self.theme
        maps = self.spec.has_maps()
        card = self.card(parent, pad=18)
        card.pack(side="bottom", fill="x", pady=(px(8), 0))
        self.label(card, "HOW IT WORKS", size=8, weight="bold", fg="faint", bg="panel").pack(anchor="w", pady=(0, px(8)))
        row = self.frame(card, "panel")
        row.pack(fill="x")
        steps = (("Find", "The game is found by itself. If it lives somewhere else, choose its folder above."),
                 ("Choose", "New and changed maps come ticked; extract them with one button." if maps else
                  "Pick a job and where its results go; your last choices are kept."),
                 ("Open in 3DHeat", "Everything lands where 3DHeat looks: its Library and level list show it."))
        for i, (head, text) in enumerate(steps):
            col = self.frame(row, "panel")
            col.grid(row=0, column=i, sticky="nwe", padx=(0 if i == 0 else px(18), 0))
            row.columnconfigure(i, weight=1, uniform="how")
            top = self.frame(col, "panel")
            top.pack(fill="x")
            d = px(22)
            img = t.rimg("how.num", d, d, d / 2, self.c("accent_fill"), self.c("panel"), self.c("accent"), bw=max(1.5, px(1.5)))
            self.tk.Label(top, image=img, text=str(i + 1), compound="center", bd=0, bg=self.c("panel"), fg=self.c("accent"),
                          font=t.font(9, "bold")).pack(side="left", padx=(0, px(8)))
            self.label(top, head, size=10.5, weight="bold", bg="panel").pack(side="left")
            body = self.label(col, text, size=9.5, fg="dim", bg="panel", wrap=260)
            body.pack(fill="x", anchor="w", pady=(px(6), 0))
            self.autowrap(body, col, px(4))

    def _check_card(self, parent, chk) -> None:
        px = self.theme.px
        kind = "Card" if chk.ok else ("WarnCard" if chk.id == "disk" else "BadCard")
        bg = {"Card": "panel", "WarnCard": "warn_fill", "BadCard": "bad_fill"}[kind]
        surface = f"{kind}."
        card = self.card(parent, kind, pad=10 if self._compact else 16)
        card.pack(fill="x", pady=(0, px(8)))
        tone = "good" if chk.ok else ("warn" if chk.id == "disk" else "bad")
        dot(self.theme, card, self.c(tone), self.c(bg)).grid(row=0, column=0, rowspan=2, sticky="n",
                                                               padx=(0, px(12)), pady=(px(5), 0))
        head = self.label(card, chk.label, size=10.5, weight="bold", bg=bg, wrap=560)
        head.grid(row=0, column=1, sticky="we")
        self.autowrap(head, card, px(300))
        detail = chk.detail
        url = URL.search(detail or "")
        if not chk.ok and chk.id.startswith("game:"):
            detail = detail or "Not found on this computer."
        box = self.frame(card, bg)
        box.grid(row=1, column=1, sticky="we")
        dl = self.label(box, detail, size=9.5, fg="dim", bg=bg, wrap=580)
        dl.pack(fill="x", anchor="w")
        self.autowrap(dl, card, px(300))
        short = self._first_sentence(detail or "")
        if self._compact and short != detail and len(detail) > 120:  # a short window: the gist, the rest on a click
            dl.config(text=short)
            more = self.link(box, "Show more", lambda: None, bg=bg)
            more.pack(anchor="w")

            def fold(_=None, lab=dl, link=more, full=detail, gist=short):
                opened = link.cget("text") == "Show less"
                lab.config(text=gist if opened else full)
                link.config(text="Show more" if opened else "Show less")

            more.bind("<Button-1>", fold)
        acts = self.frame(card, bg)
        acts.grid(row=0, column=2, rowspan=2, sticky="e", padx=(px(12), 0))
        if chk.id.startswith("game:"):
            key = chk.id[5:]
            self.button(acts, "Change…" if chk.ok else "Choose folder…", lambda k=key: self.choose_game(k),
                        "Secondary" if chk.ok else "Primary", surface).pack(side="right")
        elif not chk.ok and url:
            self.button(acts, "Open download page", lambda u=url.group(0).rstrip(".,;"): webbrowser.open(u),
                        "Primary", surface).pack(side="right")
        elif not chk.ok and chk.id == "disk":
            self.button(acts, "Choose another folder…", self.choose_levels, "Secondary", surface).pack(side="right")
        card.columnconfigure(1, weight=1)

    @staticmethod
    def _first_sentence(text: str) -> str:
        m = next((m for m in re.finditer(r"[.;:](\s|$)", text) if m.start() > 20), None)
        return text[:m.start() + 1] if m else text

    # ------------------------------------------------------------- step 2
    def page_choose(self) -> None:
        from tkinter import ttk

        px, spec = self.theme.px, self.spec
        if spec.has_maps() and spec.tasks:
            seg = self.frame(self.body)
            seg.pack(anchor="w", pady=(px(2), px(6)))
            for value, text in (("maps", "Maps"), ("tasks", "Replays and more")):
                ttk.Radiobutton(seg, text=text, value=value, variable=self.tab, style="Chip.TRadiobutton",
                                command=lambda: self.show("choose"), cursor="hand2").pack(side="left", padx=(0, px(6)))
        if self.tab.get() == "maps" and spec.has_maps():
            self.page_maps()
        else:
            self.page_tasks()

    def _counts(self) -> dict[str, int]:
        tot = {s: 0 for s in STATE_TEXT}
        for s in self.model.status:
            for m in s["maps"]:
                tot[m["state"]] = tot.get(m["state"], 0) + 1
        return tot

    def page_maps(self) -> None:
        from tkinter import ttk

        px = self.theme.px
        status = [s for s in self.model.status]
        found = [s for s in status if s["found"]]
        tot = self._counts()
        n = sum(tot.values())
        todo = tot["new"] + tot["changed"] + tot["outdated"]
        labels = ", ".join(s["label"] for s in status)
        if not found:
            self.heading(self.body, "Choose maps")
            self._empty(f"{labels} was not found", "Choose the game's folder, and its maps show up here.",
                        "Choose folder…", lambda: self.choose_game(status[0]["game"]) if status else self.show("setup"))
            return
        bits = [f"{tot['new']} new"] + ([f"{tot['changed']} changed by a game update"] if tot["changed"] else []) + \
               ([f"{tot['outdated']} made by an older version"] if tot["outdated"] else []) + [f"{tot['current']} up to date"]
        self.heading(self.body, "Choose maps", f"{n} maps in your {labels} install: " + ", ".join(bits) + ".")
        if n == 0:
            self._empty("No maps found in this install", "Start the game once and let it finish updating, then check again.",
                        "Check again", self.refresh)
            return

        bar = self.action_bar(self.body)
        self.count_label = self.label(bar, "", size=10, weight="bold")
        self.count_label.pack(side="left")
        for text, how in (("To do", "todo"), ("All", "all"), ("None", "none")):
            self.link(bar, text, lambda h=how: self.select(h)).pack(side="left", padx=(px(12), 0))
        self.go = self.button(bar, "", self.extract_checked, "Primary", big=True)
        self.go.pack(side="right")
        self.primary = self.extract_checked

        row = self.frame(self.body)
        row.pack(fill="x", pady=(0, px(8)))
        chips = (("todo", f"To do  {todo}"), ("all", f"All  {n}"), ("current", f"Up to date  {tot['current']}")) + \
                ((("missing", f"Gone  {tot['missing']}"),) if tot["missing"] else ())
        for value, text in chips:
            ttk.Radiobutton(row, text=text, value=value, variable=self.filter, style="Chip.TRadiobutton",
                            command=self.fill_tree, cursor="hand2").pack(side="left", padx=(0, px(6)))
        sbox = self.frame(row, "panel2", highlightthickness=1, highlightbackground=self.c("line"),
                          highlightcolor=self.c("accent"))
        sbox.pack(side="right")
        self.label(sbox, "⌕", size=11, fg="faint", bg="panel2").pack(side="left", padx=(px(8), 0))
        ent = self.tk.Entry(sbox, textvariable=self.search, bd=0, bg=self.c("panel2"), fg=self.c("text"),
                            insertbackground=self.c("text"), font=self.theme.font(10), width=24, relief="flat")
        ent.pack(side="left", padx=px(6), pady=px(5))
        self._placeholder(ent, "Search maps")

        card = self.card(self.body, pad=6)
        card.pack(fill="both", expand=True)
        cols = ("pick", "map", "state", "made")
        tree = ttk.Treeview(card, columns=cols, show="headings", selectmode="browse", takefocus=True)
        for col, text, width, stretch, least in (("pick", "", 44, False, 36), ("map", "MAP", 360, True, 160),
                                                 ("state", "STATE", 170, True, 130), ("made", "MADE WITH", 96, False, 70)):
            tree.heading(col, text=text, anchor="w")
            tree.column(col, width=px(width), minwidth=px(least), stretch=stretch, anchor="center" if col == "pick" else "w")
        sb = ttk.Scrollbar(card, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y", padx=(px(2), 0))
        tree.pack(fill="both", expand=True)
        c = self.theme.c
        for state, fg in (("new", c["accent"]), ("changed", c["warn"]), ("outdated", c["warn"]), ("current", c["dim"]),
                          ("missing", c["faint"])):
            tree.tag_configure(state, foreground=fg)
        tree.tag_configure("game", foreground=c["text"], font=self.theme.font(10, "bold"))
        tree.bind("<Button-1>", self._tree_click)
        tree.bind("<space>", lambda e: self._toggle(tree.focus()))
        self.tree = tree
        self.fill_tree()

    def _placeholder(self, ent, text: str) -> None:
        ph = self.label(ent.master, text, size=10, fg="faint", bg="panel2", cursor="xterm")
        ph.bind("<Button-1>", lambda e: ent.focus_set())

        def update(*_):
            try:
                if self.search.get() or self.root.focus_get() is ent:
                    ph.place_forget()
                else:
                    ph.place(in_=ent, x=0, rely=0.5, anchor="w")
            except Exception:
                pass

        ent.bind("<FocusIn>", update, add="+")
        ent.bind("<FocusOut>", update, add="+")
        self._ph_update = update
        self.root.after_idle(update)

    def _query(self) -> str:
        return self.search.get().strip().lower()

    def fill_tree(self) -> None:
        tree = getattr(self, "tree", None)
        if tree is None or not tree.winfo_exists():
            return
        tree.delete(*tree.get_children())
        f, q = self.filter.get(), self._query()
        multi = len(self.model.status) > 1
        notes = {}
        for s in self.model.status:
            for ms in s.get("_states", []):
                src = getattr(ms, "source", None)
                if src is not None and getattr(src, "note", ""):
                    notes[self._key(s["game"], ms.id)] = src.note
        for s in self.model.status:
            rows = []
            for m in s["maps"]:
                st = m["state"]
                if f == "todo" and st not in PENDING or f == "current" and st != "current" or f == "missing" and st != "missing":
                    continue
                key = self._key(s["game"], m["id"])
                hay = f"{m['title']} {m['id']} {notes.get(key, '')}".lower()
                if q and q not in hay:
                    continue
                rows.append((key, m))
            if not rows:
                continue
            if multi:
                tree.insert("", "end", iid=f"game:{s['game']}", values=("", s["label"], f"{len(rows)} maps", ""), tags=("game",))
            for key, m in rows:
                title = m["title"] + (f"   · {notes[key]}" if key in notes else "")
                pick = "" if m["state"] == "missing" else ("☑" if key in self.checked else "☐")
                tree.insert("", "end", iid=key, values=(pick, title, STATE_TEXT.get(m["state"], m["state"]),
                                                         m["extracted_version"] or ""), tags=(m["state"],))
        if not tree.get_children():
            tree.insert("", "end", iid="none", values=("", "Nothing here" + (" matches the search" if q else
                        " to do: every map is up to date" if f == "todo" else ""), "", ""), tags=("missing",))
        self._update_count()

    def _tree_click(self, e) -> None:
        if self.tree.identify_region(e.x, e.y) == "heading":
            return
        row = self.tree.identify_row(e.y)
        if row:
            self._toggle(row)

    def _toggle(self, row: str) -> None:
        if "\x1f" not in row or self.tree.set(row, "pick") == "":
            return
        if row in self.checked:
            self.checked.discard(row)
        else:
            self.checked.add(row)
        self.tree.set(row, "pick", "☑" if row in self.checked else "☐")
        self._update_count()

    def select(self, how: str) -> None:
        if how == "none":
            self.checked.clear()
        else:
            self.checked = {self._key(s["game"], m["id"]) for s in self.model.status if s["found"] for m in s["maps"]
                            if (m["state"] in PENDING if how == "todo" else m["state"] != "missing")}
        self.fill_tree()

    def _update_count(self) -> None:
        n = len(self.checked)
        try:
            self.count_label.config(text=f"{n} selected" if n else "Nothing selected")
            self.go.config(text=f"Extract {n} map{'s' if n != 1 else ''}  →" if n else "Extract", state="normal" if n else "disabled")
        except Exception:
            pass

    def _empty(self, title: str, sub: str, action: str, command) -> None:
        px = self.theme.px
        card = self.card(self.body, pad=32)
        card.pack(fill="both", expand=True)
        inner = self.frame(card, "panel")
        inner.place(relx=0.5, rely=0.45, anchor="center")
        self.label(inner, title, size=14, weight="bold", bg="panel").pack()
        self.label(inner, sub, size=10, fg="dim", bg="panel", wrap=480).pack(pady=(px(4), px(14)))
        self.button(inner, action, command, "Primary", "Card.").pack()
        self.primary = command

    def page_tasks(self) -> None:
        """Jobs: a list on the left, the chosen job's card on the right (one job: its card alone)."""
        px = self.theme.px
        tasks = self.spec.tasks
        if not self.spec.has_maps():
            self.heading(self.body, "What would you like to do?",
                         (self.spec.description[0].upper() + self.spec.description[1:] + ".") if self.spec.description
                         else "Pick a job; its results open in 3DHeat.")
        if not tasks:
            self._empty("Nothing to do here", "This tool has no jobs to run.", "Back", lambda: self.show("setup"))
            return
        if self.task_sel not in {t.id for t in tasks}:
            self.task_sel = tasks[0].id
        area = self.frame(self.body)
        area.pack(fill="both", expand=True)
        if len(tasks) > 1:
            try:
                wide = self.root.winfo_width() > px(1300) or self.root.state() == "zoomed"
            except Exception:
                wide = False
            lst = self.frame(area, width=px(300) if wide else px(232))
            lst.pack(side="left", fill="y", padx=(0, px(16)))
            lst.pack_propagate(False)
            for t in tasks:
                self._task_tile(lst, t)
        self._task_card(area, next(t for t in tasks if t.id == self.task_sel))

    def _task_tile(self, parent, t: Task) -> None:
        px, c = self.theme.px, self.theme.c
        sel = t.id == self.task_sel
        bg = c["accent_fill"] if sel else c["panel"]
        tile = self.tk.Frame(parent, bg=bg, highlightthickness=1, highlightbackground=c["accent"] if sel else c["line"],
                             cursor="hand2")
        tile.pack(fill="x", pady=(0, px(8)))
        kind = {"live": "●  runs until you stop it", "quick": "shows a short answer", "open": "opens a folder"}.get(
            t.kind, "converts, then opens in 3DHeat")
        a = self.label(tile, t.label, size=10.5, weight="bold", bg=bg, wrap=200)
        a.pack(fill="x", anchor="w", padx=px(14), pady=(px(10), 0))
        self.autowrap(a, tile, px(30))
        b = self.label(tile, kind, size=8.5, fg="bad" if t.kind == "live" else "faint", bg=bg)
        b.pack(anchor="w", padx=px(14), pady=(0, px(10)))

        def pick(_=None, t=t):
            self.task_sel = t.id
            self.show("choose")

        def hover(on: bool):
            if not sel:
                for w in (tile, a, b):
                    w.config(bg=c["hover"] if on else c["panel"])

        for w in (tile, a, b):
            w.bind("<Button-1>", pick)
        tile.bind("<Enter>", lambda e: hover(True))
        tile.bind("<Leave>", lambda e: hover(False))

    def _task_values(self, t: Task) -> dict[str, str]:
        saved = load_settings(self.spec.id).get("tasks", {}).get(t.id, {})
        levels = Path(self.levels_var.get())
        out = {}
        for i in t.inputs:
            default = i.default(levels) if callable(i.default) else (i.default or "")
            out[i.key] = str(saved.get(i.key) or default or "")
        return out

    def _task_card(self, parent, t: Task) -> None:
        from tkinter import ttk

        px = self.theme.px
        card = self.card(parent, pad=22)
        card.pack(side="left", fill="both", expand=True)
        head = self.frame(card, "panel")
        head.pack(fill="x")
        title = self.label(head, t.label, size=14, weight="bold", bg="panel", family=self.theme.display, wrap=500)
        title.pack(fill="x", anchor="w")
        self.autowrap(title, head, px(4))
        if t.kind == "live":
            self.label(card, "●  runs until you stop it", size=9, fg="bad", bg="panel").pack(anchor="w", pady=(px(2), 0))
        if t.help:
            h = self.label(card, t.help[0].upper() + t.help[1:] + ("" if t.help.endswith(".") else "."), size=10, fg="dim",
                           bg="panel", wrap=600)
            h.pack(fill="x", anchor="w", pady=(px(4), 0))
            self.autowrap(h, card, px(48))
        vals = self._task_values(t)
        vars_: dict[str, object] = {}
        if t.inputs:
            grid = self.frame(card, "panel")
            grid.pack(fill="x", pady=(px(16), 0))
            for r, i in enumerate(t.inputs):
                lab = self.label(grid, i.label, size=9.5, weight="bold", fg="dim", bg="panel", wrap=400)
                lab.grid(row=3 * r, column=0, columnspan=2, sticky="we", pady=(px(8) if r else 0, px(3)))
                self.autowrap(lab, grid, px(4))
                var = self.tk.StringVar(value=vals.get(i.key, ""))
                vars_[i.key] = var
                if i.kind == "choice" and i.choices:
                    shown = [lab for _, lab in i.choices]
                    cur = next((lab for v, lab in i.choices if v == var.get()), shown[0])
                    disp = self.tk.StringVar(value=cur)
                    box = ttk.Combobox(grid, textvariable=disp, values=shown, state="readonly", font=self.theme.font(10))
                    box.bind("<<ComboboxSelected>>", lambda e, i=i, d=disp, v=var: v.set(
                        next(val for val, lab in i.choices if lab == d.get())))
                    var.set(next(v for v, lab in i.choices if lab == cur))
                    box.grid(row=3 * r + 1, column=0, sticky="we")
                else:
                    ttk.Entry(grid, textvariable=var, font=self.theme.font(10)).grid(row=3 * r + 1, column=0, sticky="we")
                    if i.kind in ("folder", "file", "files"):
                        self.button(grid, "Browse…", lambda i=i, v=var: self._browse(i, v), "Secondary", "Card.").grid(
                            row=3 * r + 1, column=1, sticky="e", padx=(px(8), 0))
                if i.hint:
                    hl = self.label(grid, i.hint, size=8.5, fg="faint", bg="panel", wrap=400)
                    hl.grid(row=3 * r + 2, column=0, columnspan=2, sticky="we")
                    self.autowrap(hl, grid, px(4))
            grid.columnconfigure(0, weight=1)
        self.inputs[t.id] = vars_
        acts = self.frame(card, "panel")
        acts.pack(side="bottom", fill="x", pady=(px(16), 0))
        default_action = {"run": "Start", "live": "Start", "quick": "Show", "open": "Open"}.get(t.kind, "Start")
        primary = t.kind in ("run", "live")
        self.button(acts, (t.action or default_action) + ("  →" if primary else ""), lambda t=t: self.start_task(t),
                    "Primary", "Card.", big=primary).pack(side="right")
        self.primary = lambda t=t: self.start_task(t)
        if t.output and any(i.key == t.output for i in t.inputs):
            self.link(acts, "Open the folder", lambda t=t: open_folder(Path(str(self.inputs[t.id][t.output].get()))),
                      bg="panel").pack(side="left")


    def _browse(self, i, var) -> None:
        from tkinter import filedialog

        cur = var.get()
        start = cur if cur and Path(cur).is_dir() else (str(Path(cur).parent) if cur else None)
        if i.kind == "folder":
            v = filedialog.askdirectory(title=i.label, initialdir=start, parent=self.root)
        elif i.kind == "file":
            v = filedialog.askopenfilename(title=i.label, initialdir=start, parent=self.root)
        else:
            v = os.pathsep.join(filedialog.askopenfilenames(title=i.label, initialdir=start, parent=self.root))
        if v:
            var.set(v)

    # ------------------------------------------------------------- step 3
    def page_run(self) -> None:
        px = self.theme.px
        r = self.run
        if not r:
            self._empty("Nothing is running", "Choose maps or a job first.", "Choose", lambda: self.show("choose"))
            return
        live = r.get("kind") == "live"
        self.heading(self.body, r["title"], r.get("sub", ""))
        bar = self.action_bar(self.body)
        if self.proc is not None:
            self.button(bar, "Stop" if live else "Cancel", self.stop, "Danger" if live else "Secondary",
                        big=live).pack(side="right")
        if r.get("out"):
            self.button(bar, "Open the folder", lambda: open_folder(Path(r["out"])), "Ghost").pack(side="right", padx=(0, px(8)))
        self.details_link = self.link(bar, "Hide details" if self.show_log else "Show details", self.toggle_log)
        self.details_link.pack(side="left")

        card = self.card(self.body, pad=22)
        card.pack(fill="x")
        row = self.frame(card, "panel")
        row.pack(fill="x")
        if live:
            self.rec_dot = dot(self.theme, row, self.c("bad"), self.c("panel"), 14)
            self.rec_dot.pack(side="left", padx=(0, px(10)))
            self._pulse()
        self.now_label = self.label(row, r.get("now", "Starting…"), size=13, weight="bold", bg="panel")
        self.now_label.pack(side="left")
        self.count_text = self.label(row, "", size=10, fg="dim", bg="panel")
        self.count_text.pack(side="right")
        self.bar = HeatBar(card, self.theme, self.c("panel"), height=10)
        self.bar.cv.pack(fill="x", pady=(px(14), px(8)))
        times = self.frame(card, "panel")
        times.pack(fill="x")
        self.elapsed_label = self.label(times, "", size=9.5, fg="faint", bg="panel")
        self.elapsed_label.pack(side="left")
        self.eta_label = self.label(times, "", size=9.5, fg="dim", bg="panel")
        self.eta_label.pack(side="right")
        self.last_line = self.label(card, "", size=9, fg="faint", bg="panel", family=self.theme.mono)
        self.last_line.pack(fill="x", pady=(px(8), 0))
        self._log_box(self.body)
        self._render_progress()

    def _log_box(self, parent) -> None:
        if not self.show_log:
            self.log_text = None
            return
        px = self.theme.px
        card = self.card(parent, pad=8)
        card.pack(fill="both", expand=True, pady=(px(10), 0))
        txt = self.tk.Text(card, height=10, wrap="word", bg=self.c("panel"), fg=self.c("dim"), bd=0, highlightthickness=0,
                           font=self.theme.font(9, family=self.theme.mono), insertbackground=self.c("text"),
                           selectbackground=self.c("accent_fill"))
        txt.pack(fill="both", expand=True)
        txt.insert("end", "\n".join(self.log_lines[-2000:]) + ("\n" if self.log_lines else ""))
        txt.see("end")
        txt.config(state="disabled")
        self.log_text = txt

    def toggle_log(self) -> None:
        self.show_log = not self.show_log
        self.show(self.page)

    def _pulse(self) -> None:
        if self.page != "run" or self.proc is None or not getattr(self, "rec_dot", None):
            return
        try:
            self.pulse_on = not self.pulse_on
            bg = self.c("panel")
            img = self.theme.rimg(f"pulse.{self.pulse_on}", self.theme.px(14), self.theme.px(14), self.theme.px(7),
                                  self.c("bad") if self.pulse_on else mix(bg, self.c("bad"), 0.35), bg)
            self.rec_dot.config(image=img)
            self.root.after(700, self._pulse)
        except Exception:
            pass

    def _render_progress(self) -> None:
        r = self.run
        if not r or self.page != "run" or self.bar is None:
            return
        try:
            total, done = r.get("total", 0), r.get("done", 0)
            elapsed = (r.get("ended") or time.time()) - r["t0"]
            if r.get("kind") == "live" or not total:
                if self.proc is not None:
                    self.bar.busy()
                else:
                    self.bar.set(1.0)
                self.count_text.config(text="")
                self.eta_label.config(text="")
            else:
                self.bar.set(done / total)
                failed = r.get("failed", 0)
                self.count_text.config(text=f"{done} of {total}" + (f"  ·  {failed} failed" if failed else ""))
                stamps = r.get("stamps", [])
                if self.proc is not None and len(stamps) >= 1 and done < total:
                    per = (stamps[-1] - r["t0"]) / len(stamps)
                    self.eta_label.config(text=fmt_left(per * (total - done) - (time.time() - stamps[-1])))
                else:
                    self.eta_label.config(text="")
            self.elapsed_label.config(text=("Recording for " if r.get("kind") == "live" else "Running for ") + fmt_time(elapsed))
            self.now_label.config(text=r.get("now", ""))
            self.last_line.config(text=(r.get("last") or "")[:140])
        except Exception:
            pass

    # ------------------------------------------------------------- step 4
    def page_done(self) -> None:
        px = self.theme.px
        r = self.run
        if not r.get("ended"):
            self.show("choose")
            return
        ok, failed, code, stopped = r.get("ok", 0), r.get("failed", 0), r.get("code", 0), r.get("stopped", False)
        maps = r.get("kind") == "maps"
        if stopped:
            kind, title = "stopped", ("Recording stopped" if r.get("kind") == "live" else "Stopped")
            sub = (f"{ok} map{'s' if ok != 1 else ''} were finished before you stopped." if maps else
                   "What was recorded so far is saved." if r.get("kind") == "live" else "The run was stopped.")
        elif maps and failed and ok:
            kind, title, sub = "partial", f"{ok} map{'s' if ok != 1 else ''} extracted, {failed} failed", "The rest is ready in 3DHeat."
        elif failed or code not in (0, None):
            kind, title, sub = "failed", "Something went wrong", "Nothing is lost; you can try again."
        else:
            kind = "ok"
            title = (f"{ok} map{'s' if ok != 1 else ''} extracted" if maps else "Done")
            sub = "Open 3DHeat and they are in the Library." if maps else (r.get("done_text") or "The results are ready for 3DHeat.")
        bar = self.action_bar(self.body)
        self.details_link = self.link(bar, "Hide details" if self.show_log else "Show details", self.toggle_log)
        self.details_link.pack(side="left")
        back = "Extract more maps" if maps else "Back"
        self.button(bar, back, lambda: self.show("choose"), "Ghost").pack(side="right")

        head = self.frame(self.body)
        head.pack(fill="x", pady=(px(8), px(12)))
        badge(self.theme, head, kind, self.c("bg"), 60).pack(side="left", padx=(0, px(18)))
        txt = self.frame(head)
        txt.pack(side="left", fill="x", expand=True)
        self.label(txt, title, size=18, weight="bold", family=self.theme.display).pack(anchor="w")
        self.label(txt, sub, size=10, fg="dim", wrap=700).pack(anchor="w", pady=(px(2), 0))
        acts = self.frame(self.body)
        acts.pack(fill="x", pady=(0, px(12)))
        if kind in ("ok", "partial") or (kind == "stopped" and (ok or r.get("kind") == "live")):
            managed = update.managed()
            if managed:
                text, cmd = "Back to 3DHeat", self.root.destroy
            elif self.app_cmd:
                text, cmd = "Open in 3DHeat", self.open_app
            else:
                text, cmd = "Get 3DHeat", lambda: webbrowser.open(APP_PAGE)
            self.button(acts, text + "  →", cmd, "Primary", big=True).pack(side="left")
            self.primary = cmd
        else:
            self.button(acts, "Try again", self.retry, "Primary", big=True).pack(side="left")
            self.primary = self.retry
        if r.get("out"):
            self.button(acts, "Open output folder", lambda: open_folder(Path(r["out"])), "Secondary").pack(
                side="left", padx=(px(10), 0))
        if kind in ("failed", "partial"):
            self._error_card(self.body, r)
        self._log_box(self.body)

    def _error_card(self, parent, r: dict) -> None:
        px = self.theme.px
        card = self.card(parent, "BadCard")
        card.pack(fill="x")
        self.label(card, "What went wrong", size=10.5, weight="bold", bg="bad_fill").pack(anchor="w")
        errs = r.get("errors", [])
        lines = [f"• {mid}: {why}" for mid, why in errs[:6]]
        if len(errs) > 6:
            lines.append(f"• and {len(errs) - 6} more")
        if not lines:
            last = next((l for l in reversed(self.log_lines) if re.search(r"error|failed|exception|not found", l, re.I)), "")
            lines = [last or (self.log_lines[-1] if self.log_lines else f"The run ended with code {r.get('code')}.")]
        self.label(card, "\n".join(l[:160] for l in lines), size=9.5, fg="text", bg="bad_fill", wrap=820,
                   family=self.theme.mono).pack(anchor="w", pady=(px(4), px(8)))
        what = advice(" ".join(why for _, why in errs) + " " + " ".join(lines), self.spec)
        row = self.frame(card, "bad_fill")
        row.pack(fill="x")
        self.label(row, "What to do:  ", size=9.5, weight="bold", bg="bad_fill").pack(side="left", anchor="n")
        self.label(row, what, size=9.5, fg="text", bg="bad_fill", wrap=640).pack(side="left", anchor="n")
        acts = self.frame(card, "bad_fill")
        acts.pack(fill="x", pady=(px(10), 0))
        self.button(acts, "Report a problem", lambda: webbrowser.open(f"https://github.com/{self.spec.repo}/issues"),
                    "Ghost", "BadCard.").pack(side="right")
        self.button(acts, "Copy details", self.copy_details, "Secondary", "BadCard.").pack(side="right", padx=(0, px(6)))

    def copy_details(self) -> None:
        text = f"{self.spec.id} {self.spec.version} ({paths.platform_key()})\n" + "\n".join(self.log_lines[-300:])
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.flash("Copied. Paste it into the report.", "good")

    def open_app(self) -> None:
        cmd = self.app_cmd
        if not cmd:
            webbrowser.open(APP_PAGE)
            return
        try:
            flags = (getattr(subprocess, "DETACHED_PROCESS", 0) | getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)) if os.name == "nt" else 0
            subprocess.Popen(cmd, creationflags=flags, close_fds=True, stdin=subprocess.DEVNULL,
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            self.flash("Opening 3DHeat…", "good")
        except OSError as e:
            self.flash(f"Could not open 3DHeat: {e}", "bad")

    def retry(self) -> None:
        again = self.run.get("again")
        if again:
            again()
        else:
            self.show("choose")

    # ------------------------------------------------------------ actions
    def refresh(self) -> None:
        os.environ["HEAT3D_LEVELS"] = self.levels_var.get()
        before = {self._key(s["game"], m["id"]) for s in self.model.status for m in s["maps"]}
        self.model.refresh()
        now = {self._key(s["game"], m["id"]): m["state"] for s in self.model.status for m in s["maps"]}
        # new to-do maps start ticked; ticks on maps that are gone or now current go
        self.checked = {k for k in self.checked if k in now and now[k] != "missing"} | \
                       {k for k, st in now.items() if st in PENDING and k not in before}
        if self.page in ("setup", "choose"):
            self.show(self.page)

    def choose_game(self, key: str) -> None:
        from tkinter import filedialog

        label = next((g.label for g in self.spec.games if g.key == key), "the game")
        d = filedialog.askdirectory(title=f"{label}: the folder the game is installed in", parent=self.root)
        if not d:
            return
        s = load_settings(self.spec.id)
        s.setdefault("games", {})[key] = d
        save_settings(self.spec.id, s)
        self.model.refresh()
        if self.model.found.get(key) is None:
            self.flash(f"{label} was not found in that folder. Choose the folder the game is installed in.", "bad")
        else:
            self.checked |= {self._key(st["game"], m["id"]) for st in self.model.status for m in st["maps"] if m["state"] in PENDING}
            self.flash(f"{label} found.", "good")
        self.show(self.page)

    def choose_levels(self) -> None:
        from tkinter import filedialog

        d = filedialog.askdirectory(title="Where 3DHeat's maps go", initialdir=self.levels_var.get(), parent=self.root)
        if d:
            self.levels_var.set(d)
            self.refresh()

    def extract_checked(self) -> None:
        if not self.checked or self.proc is not None:
            return
        by_game: dict[str, list[str]] = {}
        for k in sorted(self.checked):
            g, m = k.split("\x1f", 1)
            by_game.setdefault(g, []).append(m)
        total = sum(len(v) for v in by_game.values())
        cmds, off = [], 0
        for g, ids in by_game.items():
            cmds.append(([*self_command(self.spec), "extract", "--progress-json", "--game", g, *ids], off))
            off += len(ids)
        sub_dir = next((g.subdir for g in self.spec.games if g.key in by_game and g.subdir), "")
        out = str(Path(self.levels_var.get()) / sub_dir)
        self.begin(dict(kind="maps", title=f"Extracting {total} map{'s' if total != 1 else ''}", total=total, out=out,
                        sub="Each map is read from your game files and written for 3DHeat. You can keep playing; "
                            "large maps take a few minutes.",
                        again=self.extract_checked), cmds)

    def start_task(self, t: Task) -> None:
        if self.proc is not None:
            self.flash("Another job is still running.", "warn")
            return
        vals = {k: str(v.get()).strip() for k, v in self.inputs.get(t.id, {}).items()}
        missing = [i.label for i in t.inputs if not vals.get(i.key)]
        if missing:
            self.flash(f"Fill in: {missing[0]}", "bad")
            return
        s = load_settings(self.spec.id)
        s.setdefault("tasks", {})[t.id] = vals
        save_settings(self.spec.id, s)
        argv = t.argv(vals, Path(self.levels_var.get()))
        cmd = [*self_command(self.spec), *argv]
        out = vals.get(t.output) if t.output else self.levels_var.get()
        if t.kind == "open":
            self._spawn_quiet(cmd)
            return
        if t.kind == "quick":
            self._quick(t, cmd)
            return
        live = t.kind == "live"
        self.begin(dict(kind="live" if live else "task", task=t, title=t.label, out=out,
                        sub=(t.help[0].upper() + t.help[1:] + "." if t.help else "") if not live else
                        "Play as usual; this window keeps recording until you press Stop."
                        + (" Closing it keeps recording: the icon by the clock opens it again." if self.spec.tray else ""),
                        done_text="The results are in the output folder and open in 3DHeat.",
                        again=lambda t=t: self.start_task(t)), [(cmd, 0)])
        if live and self.proc is not None:
            self.live_task = t
            self._tray("recording", t.label)

    # ------------------------------------------------------------ tray (spec.tray)
    def _tray(self, state: str, what: str | None = None) -> None:
        if not self.spec.tray:
            return
        if self.tray is None and state == "recording":
            from . import tray

            self.tray = tray.start(short_name(self.spec), lambda a: self.events.put(("tray", a)))
        if self.tray is not None:
            self.tray.show(state, what)

    def _tray_action(self, action: str) -> None:
        if action == "open":
            self.root.deiconify()
            self.root.lift()
            try:
                self.root.focus_force()
            except Exception:
                pass
        elif action == "pause":
            if self.proc is not None and self.run.get("kind") == "live":
                self.pausing = True
                self.stop()
        elif action == "resume":
            if self.proc is None and self.live_task is not None:
                self.start_task(self.live_task)
        elif action == "quit":
            self.stop()
            self._quit()

    def _quit(self) -> None:
        if self.tray is not None:
            self.tray.close()
            self.tray = None
        self.root.destroy()

    def _env(self) -> dict:
        return dict(os.environ, HEAT3D_NO_UPDATE="1", HEAT3D_LEVELS=self.levels_var.get(),
                    PYTHONUNBUFFERED="1", PYTHONIOENCODING="utf-8")

    def _spawn_quiet(self, cmd: list[str]) -> None:
        try:
            subprocess.Popen(cmd, env=self._env(), creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
                             stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except OSError as e:
            self.flash(f"Could not start: {e}", "bad")

    def _quick(self, t: Task, cmd: list[str]) -> None:
        self.flash(f"{t.label}…", "dim")

        def work():
            try:
                r = subprocess.run(cmd, env=self._env(), capture_output=True, text=True, encoding="utf-8", errors="replace",
                                   timeout=120, creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
                                   stdin=subprocess.DEVNULL)
                text = (r.stdout + ("\n" + r.stderr if r.stderr.strip() else "")).strip() or "(nothing to show)"
            except (OSError, subprocess.TimeoutExpired) as e:
                text = f"Could not run it: {e}"
            self.events.put(("dialog", (t.label, text)))

        threading.Thread(target=work, daemon=True).start()

    def begin(self, info: dict, cmds: list[tuple[list[str], int]]) -> None:
        info.update(t0=time.time(), done=0, ok=0, failed=0, errors=[], stamps=[], now="Starting…", code=0)
        info.setdefault("total", 0)
        self.run = info
        self.log_lines = []
        self.queue = list(cmds)
        self._next()
        self.show("run")
        self._tick()

    def _next(self) -> None:
        cmd, off = self.queue.pop(0)
        self.run["offset"] = off
        try:
            self.proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.DEVNULL,
                                         env=self._env(), creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
                                         text=True, encoding="utf-8", errors="replace")
        except OSError as e:
            self.log_lines.append(f"could not start: {e}")
            self.queue.clear()
            self._finished(1)
            return
        progress = self.run.get("kind") == "maps"
        for stream, kind in ((self.proc.stdout, "out"), (self.proc.stderr, "err")):
            threading.Thread(target=self._read, args=(stream, kind, progress), daemon=True).start()
        threading.Thread(target=lambda p=self.proc: self.events.put(("exit", (p, p.wait()))), daemon=True).start()

    def _read(self, stream, kind: str, progress: bool) -> None:
        for line in stream:
            line = line.rstrip("\n")
            if progress and kind == "out" and line.startswith("{"):
                try:
                    self.events.put(("progress", json.loads(line)))
                    continue
                except ValueError:
                    pass
            self.events.put(("log", line))

    def _tick(self) -> None:
        if self.proc is None:
            return
        self._render_progress()
        if self.tray is not None:
            self.tray.refresh()
        self.root.after(1000, self._tick)

    def stop(self) -> None:
        if self.proc is not None:
            self.run["stopped"] = True
            self.queue.clear()
            try:
                self.proc.terminate()
            except OSError:
                pass

    def close(self) -> None:
        if self.proc is not None and self.tray is not None and self.run.get("kind") == "live":
            # A recording goes on in the tray; the icon opens the window again.
            self.root.withdraw()
            if not self.hidden_told:
                self.hidden_told = True
                self.tray.notify("Still recording. The icon by the clock opens the window, pauses or quits.")
            return
        if self.proc is not None:
            from tkinter import messagebox

            if not messagebox.askyesno("Still working", "A job is still running. Stop it and close?", parent=self.root):
                return
            self.stop()
        self._quit()

    def pump(self) -> None:
        try:
            while True:
                kind, data = self.events.get_nowait()
                if kind == "log":
                    self._log(data)
                elif kind == "progress":
                    self._progress(data)
                elif kind == "exit":
                    p, code = data
                    if p is self.proc:
                        self._exited(code)
                elif kind == "update":
                    self.offer_update(data)
                elif kind == "say":
                    self.flash(data, "dim", 14)
                    self._log(data)
                elif kind == "dialog":
                    self.text_dialog(*data)
                elif kind == "tray":
                    self._tray_action(data)
                elif kind == "quit":
                    self.root.after(800, lambda: os._exit(0))
        except queue.Empty:
            pass
        try:
            self.root.after(100, self.pump)
        except Exception:
            pass

    def _log(self, line: str) -> None:
        self.log_lines.append(line)
        if len(self.log_lines) > 5000:
            del self.log_lines[:1000]
        if line.strip() and self.run:
            self.run["last"] = line.strip()
            if self.run.get("kind") != "maps":
                m = re.match(r"\[(\d+)/(\d+)\]\s*(.*)", line.strip())
                if m:
                    self.run.update(done=int(m.group(1)) - 1, total=int(m.group(2)), now=m.group(3)[:80])
                elif self.run.get("kind") == "live":
                    self.run["now"] = "Recording"
                else:
                    self.run["now"] = "Working…"
        t = getattr(self, "log_text", None)
        if t is not None:
            try:
                t.config(state="normal")
                t.insert("end", line + "\n")
                t.see("end")
                t.config(state="disabled")
            except Exception:
                self.log_text = None
        if self.page == "run" and self.run:
            try:
                self.last_line.config(text=self.run.get("last", "")[:140])
                self.now_label.config(text=self.run.get("now", ""))
            except Exception:
                pass

    def _progress(self, d: dict) -> None:
        r = self.run
        ev = d.get("event")
        if ev == "map":
            idx = r.get("offset", 0) + int(d.get("index", 0))
            r["done"] = idx
            r["stamps"].append(time.time())
            if d.get("state") == "ok":
                r["ok"] += 1
            else:
                r["failed"] += 1
                r["errors"].append((d.get("id", "?"), d.get("detail", "")))
            r["now"] = f"Finished {d.get('id')}" if d.get("state") == "ok" else f"{d.get('id')} failed"
        self._render_progress()

    def _exited(self, code: int) -> None:
        self.proc = None
        if code not in (0, None) and not self.run.get("stopped"):
            self.run["code"] = code
        if self.queue and not self.run.get("stopped"):
            self._next()
            return
        self._finished(code)

    def _finished(self, code) -> None:
        if self.bar is not None:
            self.bar.stop()
        self.proc = None
        r = self.run
        if r.get("kind") == "live" and self.tray is not None:
            self.tray.show("paused" if self.pausing else "idle")
            if not r.get("stopped"):  # ended by itself (an error): the window says why
                self.tray.notify("Recording ended.")
                self.root.deiconify()
        self.pausing = False
        r["ended"] = time.time()
        if r.get("kind") == "maps":
            r["code"] = 0 if not r.get("failed") and not r.get("code") else (r.get("code") or 1)
        elif not r.get("stopped"):
            r["code"] = code
        self.model.refresh()
        now = {self._key(s["game"], m["id"]): m["state"] for s in self.model.status for m in s["maps"]}
        self.checked = {k for k in self.checked if now.get(k) in PENDING}
        if r.get("kind") != "maps" and r.get("ok", 0) == 0 and not r.get("code"):
            r["ok"] = 1
        self.show("done")
        try:
            self.root.bell() if r.get("failed") or (r.get("code") and not r.get("stopped")) else None
        except Exception:
            pass

    # ------------------------------------------------------------ dialogs
    def dialog(self, title: str, width: int = 560):
        tk = self.tk
        win = tk.Toplevel(self.root, bg=self.c("bg"))
        win.title(title)
        win.transient(self.root)
        win.resizable(True, True)
        try:
            win.iconphoto(False, *self._icons)
        except Exception:
            pass
        title_bar(win, self.theme.dark, self.c("bg") if self.theme.dark else None)
        win.bind("<Escape>", lambda e: win.destroy())
        body = self.frame(win)
        body.pack(fill="both", expand=True, padx=self.theme.px(22), pady=self.theme.px(18))
        win.update_idletasks()
        x = self.root.winfo_rootx() + (self.root.winfo_width() - self.theme.px(width)) // 2
        y = self.root.winfo_rooty() + self.theme.px(80)
        win.geometry(f"{self.theme.px(width)}x{self.theme.px(420)}+{max(0, x)}+{max(0, y)}")
        return win, body

    def _text(self, parent, text: str, height: int = 12):
        card = self.card(parent, pad=8)
        card.pack(fill="both", expand=True, pady=(self.theme.px(10), self.theme.px(14)))
        t = self.tk.Text(card, height=height, wrap="word", bg=self.c("panel"), fg=self.c("text"), bd=0,
                         highlightthickness=0, font=self.theme.font(9.5), selectbackground=self.c("accent_fill"))
        t.insert("1.0", text)
        t.config(state="disabled")
        t.pack(fill="both", expand=True)
        return t

    def text_dialog(self, title: str, text: str) -> None:
        win, body = self.dialog(title)
        self.label(body, title, size=14, weight="bold", family=self.theme.display).pack(anchor="w")
        row = self.frame(body)
        row.pack(side="bottom", fill="x")
        self.button(row, "Close", win.destroy, "Primary").pack(side="right")
        self._text(body, text)

    # ------------------------------------------------------------ updates
    def _bg_update_check(self, manual: bool = False) -> None:
        try:
            r = update.available(self.target, use_cache=not manual, include_skipped=manual)
        except Exception:
            r = None
        if r is not None:
            self.events.put(("update", r))
        elif manual:
            self.events.put(("say", f"You have the newest version ({self.spec.version})."))

    def check_updates(self, manual: bool = False) -> None:
        if manual:
            self.flash("Looking for a newer version…", "dim")
        threading.Thread(target=self._bg_update_check, kwargs={"manual": manual}, daemon=True).start()

    def offer_update(self, r: update.Release) -> None:
        if update.managed():
            self.flash(f"Version {r.version} is out. Update it in 3DHeat: Extractors.", "accent", 20)
            return
        if update.auto_enabled(self.spec.id):
            self.apply_update(r)
            return
        win, body = self.dialog("Update available")
        self.label(body, f"Version {r.version} is ready", size=15, weight="bold", family=self.theme.display).pack(anchor="w")
        self.label(body, f"You have {self.spec.version}. What's new:", size=10, fg="dim").pack(anchor="w", pady=(self.theme.px(2), 0))
        row = self.frame(body)
        row.pack(side="bottom", fill="x")

        def now():
            win.destroy()
            self.apply_update(r)

        def skip():
            update.skip(self.spec.id, r.version)
            win.destroy()

        self.button(row, "Update now", now, "Primary").pack(side="right")
        self.button(row, "Later", win.destroy, "Secondary").pack(side="right", padx=(0, self.theme.px(8)))
        self.button(row, "Skip this version", skip, "Ghost").pack(side="left")
        from tkinter import ttk

        ttk.Checkbutton(body, text="Update automatically from now on", variable=self.auto_var,
                        command=lambda: update.set_auto(self.spec.id, self.auto_var.get())).pack(side="bottom", anchor="w",
                                                                                                 pady=(0, self.theme.px(8)))
        self._text(body, r.notes.strip() or "(no release notes)")
        win.bind("<Return>", lambda e: now())

    def apply_update(self, r: update.Release) -> None:
        if self.proc is not None:
            self.flash("The update waits until the job has finished.", "warn")
            return
        self.flash(f"Updating to {r.version}…", "accent", 60)

        def work():
            try:
                msg = update.apply(self.target, r, restart_args=[] if update.frozen() else None,
                                   log=lambda s: self.events.put(("say", s)))
                self.events.put(("say", msg + (" Restarting…" if update.frozen() else " Start the tool again.")))
                if update.frozen():
                    self.events.put(("quit", None))
            except RuntimeError as e:
                self.events.put(("say", f"Update not applied: {e}"))

        threading.Thread(target=work, daemon=True).start()

    # ------------------------------------------------------------ self-test
    def demo(self, what: str) -> None:
        """A page with made-up progress, for screenshots (env HEAT3D_GUI_DEMO): setup, tasks, run, live,
        done, partial, failed, update, light. Runs nothing."""
        task = self.spec.tasks[0] if self.spec.tasks else None
        live = next((t for t in self.spec.tasks if t.kind == "live"), task)
        t0 = time.time()
        fake = dict(t0=t0 - 95, total=12, done=5, ok=5, failed=0, errors=[], stamps=[t0 - 95 + 19 * i for i in range(1, 6)],
                    now="Finished map five", out=str(self.model.levels), code=0, last="[6/12] reading map six")
        if what == "light":
            self.theme.set_mode("light")
            self.build()
        elif what == "setup":
            self.show("setup")
        elif what == "tasks":
            self.tab.set("tasks")
            self.show("choose")
        elif what in ("run", "live"):
            self.run = dict(fake, kind="maps" if what == "run" else "live", task=live if what == "live" else None,
                            title="Extracting 12 maps" if what == "run" else (live.label if live else "Recording"),
                            sub="Each map is read from your game files and written for 3DHeat." if what == "run" else
                            "Play as usual; this window keeps recording until you press Stop.")
            if what == "live":
                self.run.update(total=0, now="Recording", last="lap 3: 1:42.318")
            self.proc = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(600)"],
                                         creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
            self.show("run")
            self._tick()
        elif what in ("done", "partial", "failed"):
            self.run = dict(fake, kind="maps", title="Extracting 12 maps", ended=t0, done=12,
                            ok={"done": 12, "partial": 10, "failed": 0}[what], failed={"done": 0, "partial": 2, "failed": 12}[what])
            if what != "done":
                self.run["errors"] = [("map_seven", "FileNotFoundError: a game file is missing"),
                                      ("map_nine", "PermissionError: the file is in use")][: 2]
                self.run["code"] = 1
            self.log_lines = ["[1/12] map one", "failed map_seven: FileNotFoundError: a game file is missing"]
            self.show("done")
        elif what == "update":
            self.offer_update(update.Release(version="9.9.0", tag="v9.9.0", url="",
                                             notes="- Maps load faster\n- A clearer window\n- Fixes for large installs"))

    def exercise(self) -> None:
        """Draw every page and dialog once with made-up progress (`--gui-selftest`); runs nothing."""
        root = self.root
        for page in ("setup", "choose"):
            self.show(page)
            root.update_idletasks()
        if self.spec.has_maps() and self.spec.tasks:
            self.tab.set("tasks")
            self.show("choose")
            self.tab.set("maps")
        self.select("all")
        self.select("todo")
        task = self.spec.tasks[0] if self.spec.tasks else None
        for kind in ("maps", "task", "live"):
            self.run = dict(kind=kind, task=task, title="Self-test", t0=time.time() - 30, total=4, done=1, ok=1, failed=0,
                            errors=[], stamps=[time.time() - 10], now="map one", out=str(self.model.levels), code=0)
            self.show("run")
            self._log("[2/4] map two")
            self._progress({"event": "map", "index": 2, "id": "two", "state": "failed", "detail": "FileNotFoundError: x"})
            self.show_log = True
            self.show("run")
            for code, stopped in ((0, False), (1, False), (0, True)):
                self.run.update(ended=time.time(), code=code, stopped=stopped)
                self.show("done")
                root.update_idletasks()
            self.show_log = False
        self.run = {}
        self.text_dialog("Self-test", "text")
        rel = update.Release(version="99.0.0", tag="v99.0.0", notes="notes", url="")
        win_before = set(root.winfo_children())
        if not update.managed() and not update.auto_enabled(self.spec.id):
            self.offer_update(rel)
        for w in set(root.winfo_children()) - win_before:
            w.destroy()
        for w in root.winfo_children():
            if isinstance(w, self.tk.Toplevel):
                w.destroy()
        self.theme.set_mode("light" if self.theme.dark else "dark")
        self.build()
        root.update_idletasks()
