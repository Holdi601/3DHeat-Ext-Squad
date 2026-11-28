"""
The unattended check's manners (`check-new`): it stays out of the way.

- `skip_reason`  "running" while the game runs (a process whose exe sits under the install, or the
                 tool's own `GameSpec.running`), "updating" while it updates (Steam: the app manifest's
                 StateFlags is not 4, or `steamapps/downloading/<appid>` exists; other stores: a file in
                 the install's top two levels written in the last 10 minutes), else None.
- `lower_priority`  this process at low priority: Windows BELOW_NORMAL and background I/O, Linux nice 10
                 and idle I/O. Best effort; whatever the system refuses is left as it is.

Nothing here touches a game process: it only reads which programs run (their exe paths).
"""

from __future__ import annotations

import os
import sys
import time
from pathlib import Path

from . import paths

#: A store's install counts as updating while one of its files is younger than this.
RECENT_S = 10 * 60


def _norm(p: str) -> str:
    return os.path.normcase(os.path.abspath(p))


def _under(exe: str, root: str) -> bool:
    e = _norm(exe)
    return e == root or e.startswith(root.rstrip("\\/") + os.sep)


def process_exes() -> list[str]:
    """The exe paths of the running processes this user may read (psutil when bundled, else the OS)."""
    try:
        import psutil  # type: ignore

        out = []
        for p in psutil.process_iter(["exe"]):
            exe = p.info.get("exe")
            if exe:
                out.append(exe)
        return out
    except ImportError:
        pass
    except Exception:
        return []
    if os.name == "nt":
        return _windows_exes()
    return _proc_exes()


def _windows_exes() -> list[str]:
    import ctypes
    from ctypes import wintypes as w

    k = ctypes.windll.kernel32
    k.OpenProcess.restype = w.HANDLE
    k.OpenProcess.argtypes = [w.DWORD, w.BOOL, w.DWORD]
    k.QueryFullProcessImageNameW.argtypes = [w.HANDLE, w.DWORD, w.LPWSTR, ctypes.POINTER(w.DWORD)]
    k.CloseHandle.argtypes = [w.HANDLE]
    k.K32EnumProcesses.argtypes = [ctypes.POINTER(w.DWORD), w.DWORD, ctypes.POINTER(w.DWORD)]
    n = 4096
    while True:
        pids = (w.DWORD * n)()
        got = w.DWORD()
        if not k.K32EnumProcesses(pids, ctypes.sizeof(pids), ctypes.byref(got)):
            return []
        if got.value < ctypes.sizeof(pids) or n >= 1 << 18:
            break
        n *= 4
    out = []
    buf = ctypes.create_unicode_buffer(32768)
    for pid in pids[: got.value // ctypes.sizeof(w.DWORD)]:
        if not pid:
            continue
        h = k.OpenProcess(0x1000, False, pid)  # PROCESS_QUERY_LIMITED_INFORMATION
        if not h:
            continue
        try:
            size = w.DWORD(len(buf))
            if k.QueryFullProcessImageNameW(h, 0, buf, ctypes.byref(size)):
                out.append(buf.value)
        finally:
            k.CloseHandle(h)
    return out


def _proc_exes() -> list[str]:
    out = []
    try:
        pids = [d for d in os.listdir("/proc") if d.isdigit()]
    except OSError:
        return []
    for pid in pids:
        try:
            out.append(os.readlink(f"/proc/{pid}/exe"))
        except OSError:
            pass
        try:  # a Windows game under Wine/Proton: the exe is wine's, the game is the first argument
            with open(f"/proc/{pid}/cmdline", "rb") as f:
                arg0 = f.read(4096).split(b"\0", 1)[0].decode("utf-8", "replace")
            if arg0[:3].upper() == "Z:\\":
                out.append("/" + arg0[3:].replace("\\", "/"))
            elif arg0.startswith("/"):
                out.append(arg0)
        except OSError:
            pass
    return out


def game_running(install: Path, exes: list[str] | None = None) -> bool:
    root = _norm(str(install))
    me = _norm(sys.executable)
    return any(_under(e, root) and _norm(e) != me for e in (process_exes() if exes is None else exes))


def _steam_app(install: Path) -> tuple[Path, str | None] | None:
    """(library, app id) when the install sits in a Steam library (`<lib>/steamapps/common/<dir>/...`)."""
    p = Path(install)
    for d in (p, *p.parents):
        if d.parent.name.lower() == "common" and d.parent.parent.name.lower() == "steamapps":
            lib = d.parent.parent.parent
            return lib, paths.steam_app_id(lib, d.name)
    return None


def _acf_state(library: Path, appid: str) -> str | None:
    try:
        text = (library / "steamapps" / f"appmanifest_{appid}.acf").read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    return dict(paths._KV.findall(text)).get("StateFlags")


def recently_written(install: Path, now: float | None = None, within: float | None = None) -> bool:
    """A file or folder in the install's top two levels changed in the last `within` seconds (RECENT_S)."""
    limit = (time.time() if now is None else now) - (RECENT_S if within is None else within)
    try:
        top = list(os.scandir(install))
    except OSError:
        return False
    for e in top:
        try:
            if e.stat(follow_symlinks=False).st_mtime > limit:
                return True
            if e.is_dir(follow_symlinks=False):
                with os.scandir(e.path) as sub:
                    for f in sub:
                        if f.stat(follow_symlinks=False).st_mtime > limit:
                            return True
        except OSError:
            continue
    return False


def game_updating(install: Path, now: float | None = None) -> bool:
    steam = _steam_app(install)
    if steam is not None and steam[1]:
        lib, appid = steam
        state = _acf_state(lib, appid)
        if state is not None and state.strip() != "4":
            return True
        return (lib / "steamapps" / "downloading" / appid).exists()
    return recently_written(install, now)


def skip_reason(g, install: Path) -> str | None:
    """Why `check-new` leaves a game alone now: "running", "updating", or None."""
    try:
        busy = g.running(install) if getattr(g, "running", None) is not None else game_running(install)
    except Exception:
        busy = False
    if busy:
        return "running"
    try:
        return "updating" if game_updating(install) else None
    except Exception:
        return None


def lower_priority() -> None:
    """This process (and what it starts) at low CPU and I/O priority; best effort."""
    try:
        if os.name == "nt":
            import ctypes
            from ctypes import wintypes as w

            k = ctypes.windll.kernel32
            k.GetCurrentProcess.restype = w.HANDLE
            k.SetPriorityClass.argtypes = [w.HANDLE, w.DWORD]
            h = k.GetCurrentProcess()
            k.SetPriorityClass(h, 0x00004000)  # BELOW_NORMAL_PRIORITY_CLASS
            k.SetPriorityClass(h, 0x00100000)  # PROCESS_MODE_BACKGROUND_BEGIN: low I/O and memory priority
            return
        try:
            os.nice(10)
        except OSError:
            pass
        if sys.platform.startswith("linux"):
            import ctypes
            import platform

            nr = {"x86_64": 251, "amd64": 251, "aarch64": 30, "arm64": 30, "i386": 289, "i686": 289}.get(
                platform.machine().lower())
            if nr:
                libc = ctypes.CDLL(None, use_errno=True)
                libc.syscall(nr, 1, 0, 3 << 13)  # ioprio_set(IOPRIO_WHO_PROCESS, self, IOPRIO_CLASS_IDLE)
    except Exception:
        pass
