"""
The notification-area (tray) icon of a tool that records in the background
(`Spec.tray`): the tool's own icon, what it is doing as the tooltip and the
menu's first line, and Open / Pause or Resume / Quit.

Closing the window while a recording runs hides it to the tray instead of
asking; Pause stops the recording (what was recorded is saved), Resume starts
the same one again, Quit stops it and ends the program.

Windows only, through the shell's own notification-area calls (no extra
package): the icon has a hidden window of its own on a thread of its own, and
its menu only posts to the main window's event queue, so every action happens
on the window's thread. Elsewhere (or when the shell refuses the icon) there
is no icon and the window behaves as before.
"""

from __future__ import annotations

import os
import threading
import time
from dataclasses import dataclass

from .theme import ASSETS


@dataclass
class TrayState:
    """What the icon shows: idle, recording (since when, what) or paused."""

    tool: str
    state: str = "idle"  # idle | recording | paused
    what: str = ""
    since: float = 0.0

    def status(self, now: float | None = None) -> str:
        if self.state == "recording":
            mins = int(((now if now is not None else time.time()) - self.since) // 60)
            took = f"{mins // 60} h {mins % 60:02d} min" if mins >= 60 else f"{mins} min"
            return f"Recording: {self.what} ({took})" if self.what else f"Recording ({took})"
        if self.state == "paused":
            return f"Paused: {self.what}" if self.what else "Paused"
        return "Not recording"

    def tooltip(self, now: float | None = None) -> str:
        # The shell keeps 127 characters of a tooltip.
        return f"{self.tool} - {self.status(now)}"[:127]

    def menu(self) -> list[tuple[str, str | None]]:
        """(text, action) from top to bottom; action None is a line that only says something, "-" a separator."""
        items: list[tuple[str, str | None]] = [(self.status(), None), ("-", None), ("Open", "open")]
        if self.state == "recording":
            items.append(("Pause", "pause"))
        elif self.state == "paused":
            items.append(("Resume", "resume"))
        items.append(("Quit", "quit"))
        return items


class Tray:
    """The icon; `post(action)` hands "open", "pause", "resume" or "quit" to the window."""

    WM_TRAY = 0x8000 + 1  # WM_APP + 1: the icon's own messages
    WM_SYNC = 0x8000 + 2  # the tooltip changed (sent from the window's thread)
    WM_CLOSE = 0x0010

    def __init__(self, tool: str, post):
        self.state = TrayState(tool)
        self._post = post
        self._hwnd = None
        self._lock = threading.Lock()
        self._balloon: str | None = None
        ready = threading.Event()
        self._error: Exception | None = None
        self._thread = threading.Thread(target=self._loop, args=(ready,), name="tray", daemon=True)
        self._thread.start()
        ready.wait(5)
        if self._hwnd is None:
            raise RuntimeError(f"no tray icon: {self._error}")

    # ---------------------------------------------------------------- the thread with the icon
    def _loop(self, ready: threading.Event) -> None:
        import ctypes
        from ctypes import wintypes as w

        u32, sh, k32 = ctypes.windll.user32, ctypes.windll.shell32, ctypes.windll.kernel32
        LRESULT = ctypes.c_ssize_t
        WNDPROC = ctypes.WINFUNCTYPE(LRESULT, w.HWND, w.UINT, w.WPARAM, w.LPARAM)
        u32.DefWindowProcW.argtypes = [w.HWND, w.UINT, w.WPARAM, w.LPARAM]
        u32.DefWindowProcW.restype = LRESULT
        u32.CreateWindowExW.restype = w.HWND
        u32.CreateWindowExW.argtypes = [w.DWORD, w.LPCWSTR, w.LPCWSTR, w.DWORD, ctypes.c_int, ctypes.c_int,
                                        ctypes.c_int, ctypes.c_int, w.HWND, w.HMENU, w.HINSTANCE, w.LPVOID]
        u32.LoadImageW.restype = w.HANDLE
        u32.LoadImageW.argtypes = [w.HINSTANCE, w.LPCWSTR, w.UINT, ctypes.c_int, ctypes.c_int, w.UINT]
        u32.LoadIconW.restype = w.HICON
        u32.LoadIconW.argtypes = [w.HINSTANCE, ctypes.c_void_p]
        u32.CreatePopupMenu.restype = w.HMENU
        u32.AppendMenuW.argtypes = [w.HMENU, w.UINT, ctypes.c_size_t, w.LPCWSTR]
        u32.TrackPopupMenu.argtypes = [w.HMENU, w.UINT, ctypes.c_int, ctypes.c_int, ctypes.c_int, w.HWND, w.LPVOID]
        u32.DestroyMenu.argtypes = [w.HMENU]
        u32.SetForegroundWindow.argtypes = [w.HWND]
        u32.PostMessageW.argtypes = [w.HWND, w.UINT, w.WPARAM, w.LPARAM]
        u32.GetMessageW.argtypes = [ctypes.POINTER(w.MSG), w.HWND, w.UINT, w.UINT]
        u32.DestroyWindow.argtypes = [w.HWND]
        k32.GetModuleHandleW.restype = w.HMODULE

        class GUID(ctypes.Structure):
            _fields_ = [("a", w.DWORD), ("b", w.WORD), ("c", w.WORD), ("d", ctypes.c_ubyte * 8)]

        class NOTIFYICONDATAW(ctypes.Structure):
            _fields_ = [("cbSize", w.DWORD), ("hWnd", w.HWND), ("uID", w.UINT), ("uFlags", w.UINT),
                        ("uCallbackMessage", w.UINT), ("hIcon", w.HICON), ("szTip", w.WCHAR * 128),
                        ("dwState", w.DWORD), ("dwStateMask", w.DWORD), ("szInfo", w.WCHAR * 256),
                        ("uVersion", w.UINT), ("szInfoTitle", w.WCHAR * 64), ("dwInfoFlags", w.DWORD),
                        ("guidItem", GUID), ("hBalloonIcon", w.HICON)]

        class WNDCLASSW(ctypes.Structure):
            _fields_ = [("style", w.UINT), ("lpfnWndProc", WNDPROC), ("cbClsExtra", ctypes.c_int),
                        ("cbWndExtra", ctypes.c_int), ("hInstance", w.HINSTANCE), ("hIcon", w.HICON),
                        ("hCursor", w.HANDLE), ("hbrBackground", w.HBRUSH), ("lpszMenuName", w.LPCWSTR),
                        ("lpszClassName", w.LPCWSTR)]

        sh.Shell_NotifyIconW.argtypes = [w.DWORD, ctypes.POINTER(NOTIFYICONDATAW)]
        NIM_ADD, NIM_MODIFY, NIM_DELETE = 0, 1, 2
        NIF_MESSAGE, NIF_ICON, NIF_TIP, NIF_INFO = 1, 2, 4, 0x10
        WM_LBUTTONUP, WM_LBUTTONDBLCLK, WM_RBUTTONUP, WM_CONTEXTMENU = 0x0202, 0x0203, 0x0205, 0x007B
        MF_STRING, MF_SEPARATOR, MF_GRAYED = 0, 0x800, 1
        TPM_RETURNCMD, TPM_RIGHTBUTTON = 0x100, 2

        def data(flags: int) -> NOTIFYICONDATAW:
            d = NOTIFYICONDATAW()
            d.cbSize = ctypes.sizeof(NOTIFYICONDATAW)
            d.hWnd, d.uID, d.uFlags, d.uCallbackMessage = self._hwnd, 1, flags, self.WM_TRAY
            d.hIcon = icon
            d.szTip = self.state.tooltip()
            return d

        def menu() -> None:
            items = self.state.menu()
            m = u32.CreatePopupMenu()
            for n, (text, action) in enumerate(items, 1):
                if text == "-":
                    u32.AppendMenuW(m, MF_SEPARATOR, 0, None)
                else:
                    u32.AppendMenuW(m, MF_STRING | (0 if action else MF_GRAYED), n, text)
            pt = w.POINT()
            u32.GetCursorPos(ctypes.byref(pt))
            u32.SetForegroundWindow(self._hwnd)  # else the menu stays open after a click elsewhere
            chosen = u32.TrackPopupMenu(m, TPM_RETURNCMD | TPM_RIGHTBUTTON, pt.x, pt.y, 0, self._hwnd, None)
            u32.PostMessageW(self._hwnd, 0, 0, 0)
            u32.DestroyMenu(m)
            if 0 < chosen <= len(items) and items[chosen - 1][1]:
                self._post(items[chosen - 1][1])

        def proc(hwnd, msg, wp, lp):
            if msg == self.WM_TRAY:
                ev = lp & 0xFFFF
                if ev in (WM_RBUTTONUP, WM_CONTEXTMENU):
                    menu()
                elif ev in (WM_LBUTTONUP, WM_LBUTTONDBLCLK):
                    self._post("open")
                return 0
            if msg == self.WM_SYNC:
                d = data(NIF_TIP)
                with self._lock:
                    if self._balloon:
                        d.uFlags |= NIF_INFO
                        d.szInfo, d.szInfoTitle = self._balloon[:255], self.state.tool[:63]
                        self._balloon = None
                sh.Shell_NotifyIconW(NIM_MODIFY, ctypes.byref(d))
                return 0
            if msg == self.WM_CLOSE:
                sh.Shell_NotifyIconW(NIM_DELETE, ctypes.byref(data(0)))
                u32.DestroyWindow(hwnd)
                u32.PostQuitMessage(0)
                return 0
            return u32.DefWindowProcW(hwnd, msg, wp, lp)

        try:
            self._proc = WNDPROC(proc)  # kept: the window calls it for as long as it lives
            hinst = k32.GetModuleHandleW(None)
            cls = WNDCLASSW()
            cls.lpfnWndProc, cls.hInstance = self._proc, hinst
            cls.lpszClassName = f"heat3d-tray-{os.getpid()}-{id(self)}"
            if not u32.RegisterClassW(ctypes.byref(cls)):
                raise OSError("RegisterClassW")
            # A hidden top-level window (a message-only one gets no menu focus).
            hwnd = u32.CreateWindowExW(0, cls.lpszClassName, self.state.tool, 0, 0, 0, 0, 0, None, None, hinst, None)
            if not hwnd:
                raise OSError("CreateWindowExW")
            ico = next((p for p in (ASSETS / "tool.ico", ASSETS / "app.ico") if p.is_file()), None)
            icon = u32.LoadImageW(None, str(ico), 1, 16, 16, 0x10) if ico else None  # IMAGE_ICON, LR_LOADFROMFILE
            if not icon:
                icon = u32.LoadIconW(None, 32512)  # IDI_APPLICATION
            self._hwnd = hwnd
            if not sh.Shell_NotifyIconW(NIM_ADD, ctypes.byref(data(NIF_MESSAGE | NIF_ICON | NIF_TIP))):
                u32.DestroyWindow(hwnd)
                self._hwnd = None
                raise OSError("Shell_NotifyIconW")
        except Exception as e:
            self._error = e
            ready.set()
            return
        ready.set()
        msg = w.MSG()
        while u32.GetMessageW(ctypes.byref(msg), None, 0, 0) > 0:
            u32.TranslateMessage(ctypes.byref(msg))
            u32.DispatchMessageW(ctypes.byref(msg))

    def _send(self, msg: int) -> None:
        if self._hwnd is not None:
            import ctypes

            ctypes.windll.user32.PostMessageW(self._hwnd, msg, 0, 0)

    # ---------------------------------------------------------------- what the window calls
    def show(self, state: str, what: str | None = None) -> None:
        s = self.state
        if state == "recording" and s.state != "recording":
            s.since = time.time()
        s.state = state
        if what is not None:
            s.what = what
        self.refresh()

    def refresh(self) -> None:
        self._send(self.WM_SYNC)

    def notify(self, text: str) -> None:
        with self._lock:
            self._balloon = text
        self._send(self.WM_SYNC)

    def close(self) -> None:
        self._send(self.WM_CLOSE)
        self._thread.join(2)
        self._hwnd = None


def start(tool: str, post) -> Tray | None:
    """The tray icon, or None where there is none (not Windows, or the shell refused it)."""
    if os.name != "nt" or os.environ.get("HEAT3D_NO_TRAY"):
        return None
    try:
        return Tray(tool, post)
    except Exception:
        return None
