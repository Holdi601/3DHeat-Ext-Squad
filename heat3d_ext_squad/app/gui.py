"""
The window a standalone extractor opens when started without arguments.

It shows what was found and what is missing, the levels folder it writes
into, the maps of each game with their state (new / changed / outdated /
current), runs the tool's tasks, and offers updates (asking first unless the
user ticked "Update automatically"). The work itself runs as a child process
of the same executable (`extract --progress-json`, or one of the tool's
commands), so the window stays responsive and a crash in a map cannot take it down.
"""

from __future__ import annotations

import json
import os
import queue
import subprocess
import sys
import threading
from pathlib import Path

from . import paths, update
from .manifest import game_status
from .spec import Spec, Task, game_folders, load_settings, save_settings, standard_checks

STATE_TEXT = {"new": "new", "changed": "changed by a game update", "outdated": "older extractor",
              "current": "up to date", "missing": "gone from the install"}


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


def selftest(spec: Spec, target: update.Target) -> int:
    m = Model(spec)
    assert m.checks, "no checks"
    for t in spec.tasks:
        t.argv({i.key: "x" for i in t.inputs}, m.levels)
    try:
        import tkinter as tk

        root = tk.Tk()
        root.withdraw()
        App(root, spec, target, m, check_updates=False)
        root.update_idletasks()
        root.destroy()
        shown = "window built"
    except Exception as e:  # no display (CI on Linux without X): the model is what is tested
        shown = f"no window ({type(e).__name__})"
    print(f"gui-selftest ok: {len(m.checks)} checks, {sum(len(s['maps']) for s in m.status)} maps, {shown}")
    return 0


def run(spec: Spec, target: update.Target) -> int:
    import tkinter as tk

    root = tk.Tk()
    App(root, spec, target, Model(spec))
    root.mainloop()
    return 0


class App:
    def __init__(self, root, spec: Spec, target: update.Target, model: Model, check_updates: bool = True):
        import tkinter as tk
        from tkinter import ttk

        self.tk, self.ttk = tk, ttk
        self.root, self.spec, self.target, self.model = root, spec, target, model
        self.events: queue.Queue = queue.Queue()
        self.proc: subprocess.Popen | None = None
        root.title(f"{spec.name} for 3DHeat {spec.version}")
        root.minsize(720, 520)
        try:
            ttk.Style().theme_use("vista" if os.name == "nt" else "clam")
        except tk.TclError:
            pass
        outer = ttk.Frame(root, padding=10)
        outer.pack(fill="both", expand=True)

        self.setup = ttk.LabelFrame(outer, text="Setup", padding=8)
        self.setup.pack(fill="x")
        self.levels_var = tk.StringVar(value=str(model.levels))

        mid = ttk.Frame(outer)
        mid.pack(fill="both", expand=True, pady=(8, 0))
        self.tree = None
        if spec.has_maps():
            maps = ttk.LabelFrame(mid, text="Maps", padding=8)
            maps.pack(fill="both", expand=True)
            self.summary = ttk.Label(maps, text="")
            self.summary.pack(anchor="w")
            cols = ("state", "version")
            self.tree = ttk.Treeview(maps, columns=cols, selectmode="extended", height=10)
            self.tree.heading("#0", text="Map")
            self.tree.heading("state", text="State")
            self.tree.heading("version", text="Extracted with")
            self.tree.column("#0", width=320)
            self.tree.column("state", width=180)
            self.tree.column("version", width=110)
            self.tree.pack(fill="both", expand=True, pady=4)
            row = ttk.Frame(maps)
            row.pack(fill="x")
            ttk.Button(row, text="Check for new maps", command=self.refresh).pack(side="left")
            ttk.Button(row, text="Select new and changed", command=self.select_pending).pack(side="left", padx=4)
            ttk.Button(row, text="Extract selected", command=self.extract_selected).pack(side="left", padx=4)
            ttk.Button(row, text="Extract all new", command=lambda: self.run_extract(["--new", "--changed", "--outdated"])).pack(side="left", padx=4)
        if spec.tasks:
            tasks = ttk.LabelFrame(mid, text="Tasks", padding=8)
            tasks.pack(fill="x", pady=(8, 0))
            for t in spec.tasks:
                b = ttk.Button(tasks, text=t.label + "...", command=lambda t=t: self.ask_task(t))
                b.pack(side="left", padx=(0, 6))

        prog = ttk.Frame(outer)
        prog.pack(fill="x", pady=(8, 0))
        self.bar = ttk.Progressbar(prog, mode="determinate")
        self.bar.pack(fill="x")
        self.status_label = ttk.Label(prog, text="Ready")
        self.status_label.pack(anchor="w")
        self.stop_button = ttk.Button(prog, text="Stop", command=self.stop, state="disabled")
        self.stop_button.pack(anchor="e")
        self.log = tk.Text(outer, height=8, wrap="word", state="disabled")
        self.log.pack(fill="both", expand=False, pady=(4, 0))

        foot = ttk.Frame(outer)
        foot.pack(fill="x", pady=(8, 0))
        ttk.Button(foot, text="Check for updates", command=lambda: self.check_updates(manual=True)).pack(side="left")
        self.auto_var = tk.BooleanVar(value=bool(load_settings(spec.id).get("auto_update")))
        ttk.Checkbutton(foot, text="Update automatically", variable=self.auto_var,
                        command=lambda: update.set_auto(spec.id, self.auto_var.get())).pack(side="left", padx=8)
        if spec.notice:
            ttk.Label(foot, text=spec.notice, foreground="#666").pack(side="right")

        self.render()
        root.after(100, self.pump)
        if check_updates:
            threading.Thread(target=self._bg_update_check, daemon=True).start()

    # --------------------------------------------------------------- render
    def render(self) -> None:
        ttk, tk = self.ttk, self.tk
        for w in self.setup.winfo_children():
            w.destroy()
        for i, c in enumerate(self.model.checks):
            mark = "✔" if c.ok else "✖"
            ttk.Label(self.setup, text=mark, foreground="#2a7" if c.ok else "#c33").grid(row=i, column=0, sticky="w")
            ttk.Label(self.setup, text=c.label).grid(row=i, column=1, sticky="w", padx=4)
            ttk.Label(self.setup, text=c.detail, wraplength=430).grid(row=i, column=2, sticky="w")
            if c.id.startswith("game:"):
                key = c.id[5:]
                ttk.Button(self.setup, text="Choose folder...", command=lambda k=key: self.choose_game(k)).grid(row=i, column=3, sticky="e")
        r = len(self.model.checks)
        ttk.Label(self.setup, text="Levels folder").grid(row=r, column=1, sticky="w", padx=4, pady=(6, 0))
        ttk.Entry(self.setup, textvariable=self.levels_var, width=56).grid(row=r, column=2, sticky="we", pady=(6, 0))
        btns = ttk.Frame(self.setup)
        btns.grid(row=r, column=3, sticky="e", pady=(6, 0))
        ttk.Button(btns, text="Change...", command=self.choose_levels).pack(side="left")
        ttk.Button(btns, text="Open", command=lambda: open_folder(Path(self.levels_var.get()))).pack(side="left")
        self.setup.columnconfigure(2, weight=1)
        if self.tree is not None:
            self.tree.delete(*self.tree.get_children())
            totals = {"new": 0, "changed": 0, "outdated": 0, "current": 0, "missing": 0}
            for s in self.model.status:
                node = self.tree.insert("", "end", iid=f"game:{s['game']}", text=s["label"] + ("" if s["found"] else " (not found)"),
                                        values=("", ""), open=True)
                for m in s["maps"]:
                    totals[m["state"]] += 1
                    self.tree.insert(node, "end", iid=f"{s['game']}\x1f{m['id']}", text=m["title"],
                                     values=(STATE_TEXT.get(m["state"], m["state"]), m["extracted_version"] or ""))
            self.summary.config(text=f"{totals['new']} new, {totals['changed']} changed, {totals['outdated']} extracted "
                                     f"by an older version, {totals['current']} up to date")

    def refresh(self) -> None:
        os.environ["HEAT3D_LEVELS"] = self.levels_var.get()
        self.model.refresh()
        self.render()

    # -------------------------------------------------------------- actions
    def choose_game(self, key: str) -> None:
        from tkinter import filedialog

        d = filedialog.askdirectory(title="The game's install folder")
        if not d:
            return
        s = load_settings(self.spec.id)
        s.setdefault("games", {})[key] = d
        save_settings(self.spec.id, s)
        self.refresh()

    def choose_levels(self) -> None:
        from tkinter import filedialog

        d = filedialog.askdirectory(title="The 3DHeat levels folder", initialdir=self.levels_var.get())
        if d:
            self.levels_var.set(d)
            self.refresh()

    def select_pending(self) -> None:
        if self.tree is None:
            return
        want = {STATE_TEXT[s] for s in ("new", "changed", "outdated")}
        items = [c for g in self.tree.get_children() for c in self.tree.get_children(g)
                 if self.tree.set(c, "state") in want]
        self.tree.selection_set(items)

    def extract_selected(self) -> None:
        sel = [i for i in self.tree.selection() if "\x1f" in i] if self.tree is not None else []
        if not sel:
            self.say("Select one or more maps first.")
            return
        by_game: dict[str, list[str]] = {}
        for i in sel:
            g, m = i.split("\x1f", 1)
            by_game.setdefault(g, []).append(m)
        # one game per run keeps the progress simple; most tools have one game
        g, ids = next(iter(by_game.items()))
        self.run_extract(["--game", g, *ids])

    def run_extract(self, args: list[str]) -> None:
        self.start([*self_command(self.spec), "extract", "--progress-json", *args], progress=True)

    def ask_task(self, task: Task) -> None:
        from tkinter import filedialog, simpledialog

        values: dict[str, str] = {}
        levels = Path(self.levels_var.get())
        for inp in task.inputs:
            default = inp.default(levels) if callable(inp.default) else (inp.default or "")
            if inp.kind == "folder":
                v = filedialog.askdirectory(title=inp.label, initialdir=default or None)
            elif inp.kind == "file":
                v = filedialog.askopenfilename(title=inp.label, initialdir=default or None)
            elif inp.kind == "files":
                v = os.pathsep.join(filedialog.askopenfilenames(title=inp.label, initialdir=default or None))
            else:
                v = simpledialog.askstring(task.label, inp.label, initialvalue=default) or ""
            if not v and not default:
                return
            values[inp.key] = v or default
        argv = task.argv(values, levels)
        self.start([*self_command(self.spec), *argv], progress=False)

    def start(self, cmd: list[str], *, progress: bool) -> None:
        if self.proc is not None:
            self.say("Another run is still going.")
            return
        env = dict(os.environ, HEAT3D_NO_UPDATE="1", HEAT3D_LEVELS=self.levels_var.get(),
                   PYTHONUNBUFFERED="1", PYTHONIOENCODING="utf-8")
        flags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
        self.bar.config(mode="determinate" if progress else "indeterminate", value=0)
        if not progress:
            self.bar.start(15)
        self.stop_button.config(state="normal")
        self.status_label.config(text="Working...")
        try:
            self.proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env,
                                         creationflags=flags, text=True, encoding="utf-8", errors="replace")
        except OSError as e:
            self.say(f"could not start: {e}")
            self._finished(1)
            return
        for stream, kind in ((self.proc.stdout, "out"), (self.proc.stderr, "err")):
            threading.Thread(target=self._read, args=(stream, kind, progress), daemon=True).start()
        threading.Thread(target=lambda p=self.proc: self.events.put(("exit", p.wait())), daemon=True).start()

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

    def stop(self) -> None:
        if self.proc is not None:
            self.proc.terminate()

    def pump(self) -> None:
        try:
            while True:
                kind, data = self.events.get_nowait()
                if kind == "log":
                    self.say(data)
                elif kind == "progress":
                    ev = data.get("event")
                    if ev == "start":
                        self.bar.config(maximum=max(1, data.get("total", 1)), value=0)
                    elif ev == "map":
                        self.bar.config(value=data.get("index", 0))
                        self.status_label.config(text=f"{data.get('id')}: {data.get('state')}")
                    elif ev == "done":
                        self.status_label.config(text=f"{data.get('ok', 0)} extracted, {data.get('failed', 0)} failed")
                elif kind == "exit":
                    self._finished(data)
                elif kind == "update":
                    self.offer_update(data)
                elif kind == "say":
                    self.say(data)
                elif kind == "quit":
                    self.root.after(800, lambda: os._exit(0))
        except queue.Empty:
            pass
        self.root.after(100, self.pump)

    def _finished(self, code) -> None:
        self.bar.stop()
        self.proc = None
        self.stop_button.config(state="disabled")
        if code == 0:
            if self.status_label.cget("text") == "Working...":
                self.status_label.config(text="Done")
        else:
            self.status_label.config(text=f"Finished with errors (exit {code}); see the log")
        self.refresh()

    def say(self, text: str) -> None:
        self.log.config(state="normal")
        self.log.insert("end", text + "\n")
        self.log.see("end")
        self.log.config(state="disabled")

    # -------------------------------------------------------------- updates
    def _bg_update_check(self, manual: bool = False) -> None:
        try:
            r = update.available(self.target, use_cache=not manual, include_skipped=manual)
        except Exception:
            r = None
        if r is not None:
            self.events.put(("update", r))
        elif manual:
            self.events.put(("say", f"{self.spec.name} {self.spec.version} is the newest published version."))

    def check_updates(self, manual: bool = False) -> None:
        threading.Thread(target=self._bg_update_check, kwargs={"manual": manual}, daemon=True).start()

    def offer_update(self, r: update.Release) -> None:
        tk, ttk = self.tk, self.ttk
        if update.managed():
            self.say(f"{self.spec.name} {r.version} is out; update it in the 3DHeat app's Extractors panel.")
            return
        if update.auto_enabled(self.spec.id):
            self.apply_update(r)
            return
        win = tk.Toplevel(self.root)
        win.title("Update available")
        win.transient(self.root)
        ttk.Label(win, text=f"{self.spec.name} {r.version} is out (this is {self.spec.version}).", padding=8).pack(anchor="w")
        notes = tk.Text(win, height=12, width=70, wrap="word")
        notes.insert("1.0", r.notes.strip() or "(no release notes)")
        notes.config(state="disabled")
        notes.pack(fill="both", expand=True, padx=8)
        row = ttk.Frame(win, padding=8)
        row.pack(fill="x")

        def now():
            win.destroy()
            self.apply_update(r)

        def skip():
            update.skip(self.spec.id, r.version)
            win.destroy()

        ttk.Button(row, text="Update now", command=now).pack(side="left")
        ttk.Button(row, text="Later", command=win.destroy).pack(side="left", padx=6)
        ttk.Button(row, text="Skip this version", command=skip).pack(side="left")

    def apply_update(self, r: update.Release) -> None:
        if self.proc is not None:
            self.say("The update waits until the current run has finished.")
            return
        self.status_label.config(text=f"Updating to {r.version}...")

        def work():
            try:
                msg = update.apply(self.target, r, restart_args=[] if update.frozen() else None,
                                   log=lambda s: self.events.put(("say", s)))
                self.events.put(("say", msg + (" - restarting" if update.frozen() else " - start the tool again")))
                if update.frozen():
                    self.events.put(("quit", None))
            except RuntimeError as e:
                self.events.put(("say", f"Update not applied: {e}"))

        threading.Thread(target=work, daemon=True).start()


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
