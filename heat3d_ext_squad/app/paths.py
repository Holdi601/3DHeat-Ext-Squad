"""
Where things are on this machine: the 3DHeat data folder, the levels folder the
viewer reads, this tool's settings file, and the Steam libraries games sit in.

Nothing here names a game. A game's own folder names are passed in by the
tool that looks for it, and a Steam app id is only ever read from the
library's own manifests, never written down.
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path


def platform_key() -> str:
    """`windows-x64`, `linux-x64` or `macos-arm64` (the release asset this machine takes)."""
    if sys.platform == "win32":
        return "windows-x64"
    if sys.platform == "darwin":
        return "macos-arm64"
    return "linux-x64"


def data_dir() -> Path:
    """`%LOCALAPPDATA%\\3DHeat` on Windows, `${XDG_DATA_HOME:-~/.local/share}/3dheat` elsewhere."""
    if sys.platform == "win32":
        base = os.environ.get("LOCALAPPDATA") or str(Path.home() / "AppData" / "Local")
        return Path(base) / "3DHeat"
    base = os.environ.get("XDG_DATA_HOME") or str(Path.home() / ".local" / "share")
    return Path(base) / "3dheat"


def levels_dir() -> Path:
    """The folder the viewer reads levels from: `HEAT3D_LEVELS`, else `<data>/levels`."""
    given = os.environ.get("HEAT3D_LEVELS", "").strip()
    return Path(given) if given else data_dir() / "levels"


def settings_file(tool_id: str) -> Path:
    return data_dir() / "extractors" / "settings" / f"{tool_id}.json"


def free_bytes(folder: Path) -> int | None:
    """Free space where `folder` is (or would be created), or None when it cannot be told."""
    import shutil

    p = Path(folder)
    while not p.exists():
        if p.parent == p:
            return None
        p = p.parent
    try:
        return shutil.disk_usage(p).free
    except OSError:
        return None


# ---------------------------------------------------------------------- Steam

_PATH = re.compile(r'"path"\s*"([^"]+)"')
_KV = re.compile(r'"(\w+)"\s*"([^"]*)"')


def steam_roots() -> list[Path]:
    """Every Steam installation this user has (native, flatpak, Steam Deck, Windows, macOS)."""
    home = Path.home()
    found: list[Path] = []
    if sys.platform == "win32":
        try:
            import winreg

            for hive, key in ((winreg.HKEY_CURRENT_USER, r"Software\Valve\Steam"),
                              (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Valve\Steam")):
                try:
                    with winreg.OpenKey(hive, key) as k:
                        for name in ("SteamPath", "InstallPath"):
                            try:
                                found.append(Path(winreg.QueryValueEx(k, name)[0]))
                            except OSError:
                                pass
                except OSError:
                    pass
        except ImportError:
            pass
        for env in ("ProgramFiles(x86)", "ProgramFiles"):
            if os.environ.get(env):
                found.append(Path(os.environ[env]) / "Steam")
    elif sys.platform == "darwin":
        found.append(home / "Library" / "Application Support" / "Steam")
    else:
        found += [
            home / ".steam" / "steam",
            home / ".steam" / "root",
            home / ".local" / "share" / "Steam",
            home / ".var" / "app" / "com.valvesoftware.Steam" / ".local" / "share" / "Steam",
            home / ".var" / "app" / "com.valvesoftware.Steam" / ".steam" / "steam",
        ]
    out: list[Path] = []
    seen: set[str] = set()
    for r in found:
        try:
            key = os.path.normcase(str(r.resolve()))
        except OSError:
            continue
        if key not in seen and (r / "steamapps").is_dir():
            seen.add(key)
            out.append(r)
    return out


def steam_libraries(roots: list[Path] | None = None) -> list[Path]:
    """Every Steam library folder (the folders that hold `steamapps`)."""
    libs: list[Path] = []
    seen: set[str] = set()

    def add(p: Path) -> None:
        try:
            key = os.path.normcase(str(p.resolve()))
        except OSError:
            return
        if key not in seen and (p / "steamapps").is_dir():
            seen.add(key)
            libs.append(p)

    for root in steam_roots() if roots is None else roots:
        add(root)
        for vdf in (root / "steamapps" / "libraryfolders.vdf", root / "config" / "libraryfolders.vdf"):
            try:
                text = vdf.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            for m in _PATH.finditer(text):
                add(Path(m.group(1).replace("\\\\", "\\")))
    return libs


def steam_game_dirs(installdir: str, libraries: list[Path] | None = None) -> list[Path]:
    """`<library>/steamapps/common/<installdir>` in every library where it exists."""
    out = []
    for lib in steam_libraries() if libraries is None else libraries:
        p = lib / "steamapps" / "common" / installdir
        if p.is_dir():
            out.append(p)
    return out


def steam_app_id(library: Path, installdir: str) -> str | None:
    """The app id whose manifest in `library` names `installdir`, read from the manifests."""
    try:
        manifests = list((library / "steamapps").glob("appmanifest_*.acf"))
    except OSError:
        return None
    for m in manifests:
        try:
            kv = dict(_KV.findall(m.read_text(encoding="utf-8", errors="replace")))
        except OSError:
            continue
        if kv.get("installdir", "").lower() == installdir.lower() and kv.get("appid"):
            return kv["appid"]
    return None


def proton_prefix(game_dir: Path) -> Path | None:
    """The Proton/Wine prefix (`.../compatdata/<appid>/pfx`) of a Steam game, on Linux."""
    library = game_dir.parent.parent.parent  # <lib>/steamapps/common/<dir>
    appid = steam_app_id(library, game_dir.name)
    if not appid:
        return None
    pfx = library / "steamapps" / "compatdata" / appid / "pfx"
    return pfx if pfx.is_dir() else None


def proton_user_dir(game_dir: Path, *parts: str) -> Path | None:
    """A folder in the Windows user profile inside a game's Proton prefix (e.g. `Documents`, `My Games`)."""
    pfx = proton_prefix(game_dir)
    if pfx is None:
        return None
    p = pfx.joinpath("drive_c", "users", "steamuser", *parts)
    return p if p.exists() else None


def first(paths, test) -> Path | None:
    """The first of `paths` (None and missing ones skipped) that `test` accepts."""
    for p in paths:
        if not p:
            continue
        p = Path(p).expanduser()
        try:
            if test(p):
                return p
        except OSError:
            continue
    return None
