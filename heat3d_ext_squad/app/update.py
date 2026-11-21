"""
Updates: a newer published GitHub release is announced with its notes, and
applied only when the user says so - or by itself when the user chose
automatic updates (`--auto-update`, the GUI's "Update automatically", which is
`"auto_update": true` in the tool's settings file, or `HEAT3D_AUTO_UPDATE=1`).
"Skip this version" is remembered in the same file.

A standalone copy (the downloaded executable) is replaced by the release's
archive for this platform, after its SHA-256 matched the release's
`SHA256SUMS` and the digest GitHub reports for the file. A copy the 3DHeat
app installed (`HEAT3D_MANAGED=1`) is updated by the app, not by itself. A
checkout or pip install is updated the way the tool always did (`apply_source`).
The check costs one request every few hours at most and never stops a tool:
offline, it carries on with the version it has. `HEAT3D_NO_UPDATE=1` turns it off.
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tarfile
import tempfile
import time
import urllib.error
import urllib.request
import zipfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

from . import paths
from .spec import load_settings, save_settings

CHECK_EVERY = 6 * 3600
TIMEOUT = 5.0
DOWNLOAD_TIMEOUT = 60.0
_ALLOWED_HOSTS = ("api.github.com", "github.com", "objects.githubusercontent.com",
                  "release-assets.githubusercontent.com", "codeload.github.com")


@dataclass
class Release:
    version: str
    tag: str
    notes: str
    url: str
    archive: str = ""
    #: asset name -> {"url": ..., "digest": "sha256:<hex>" or ""}
    assets: dict = field(default_factory=dict)


@dataclass
class Target:
    """The tool being updated."""

    repo: str
    tool_id: str
    name: str
    version: str
    #: How a checkout / pip install / source copy is updated (the tool's own code); None: not possible.
    apply_source: Callable[[Release], str] | None = None


def parse(version: str) -> tuple[int, ...]:
    core = str(version).strip().lstrip("vV").split("-")[0].split("+")[0]
    out = []
    for part in core.split("."):
        digits = "".join(ch for ch in part if ch.isdigit())
        out.append(int(digits) if digits else 0)
    return tuple(out)


def is_newer(candidate: str, current: str) -> bool:
    a, b = parse(candidate), parse(current)
    width = max(len(a), len(b))
    return a + (0,) * (width - len(a)) > b + (0,) * (width - len(b))


def _flag(name: str) -> bool:
    return os.environ.get(name, "").strip().lower() not in ("", "0", "false", "no", "off")


def disabled() -> bool:
    return _flag("HEAT3D_NO_UPDATE")


def managed() -> bool:
    return _flag("HEAT3D_MANAGED")


def frozen() -> bool:
    return bool(getattr(sys, "frozen", False))


#: Set by `--auto-update` on the command line, for this run.
AUTO_THIS_RUN = False


def auto_enabled(tool_id: str) -> bool:
    return AUTO_THIS_RUN or _flag("HEAT3D_AUTO_UPDATE") or bool(load_settings(tool_id).get("auto_update"))


def set_auto(tool_id: str, on: bool) -> None:
    s = load_settings(tool_id)
    s["auto_update"] = bool(on)
    save_settings(tool_id, s)


def skip(tool_id: str, version: str) -> None:
    s = load_settings(tool_id)
    s["skip_version"] = version
    save_settings(tool_id, s)


def skipped(tool_id: str) -> str | None:
    v = load_settings(tool_id).get("skip_version")
    return str(v) if v else None


def _check_url(url: str) -> None:
    from urllib.parse import urlparse

    u = urlparse(url)
    if u.scheme != "https" or (u.hostname or "") not in _ALLOWED_HOSTS:
        raise RuntimeError(f"refusing to download from {u.hostname or url}")


class _Redirects(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        _check_url(newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def _get(url: str, *, ua: str, timeout: float = TIMEOUT, accept: str = "application/vnd.github+json") -> bytes:
    _check_url(url)
    opener = urllib.request.build_opener(_Redirects())
    req = urllib.request.Request(url, headers={"User-Agent": ua, "Accept": accept})
    with opener.open(req, timeout=timeout) as r:
        return r.read()


def _cache(repo: str) -> Path:
    return paths.data_dir() / "update-check" / f"{repo.split('/')[-1]}.json"


def latest(target: Target, *, use_cache: bool = True) -> Release | None:
    """The newest published release (drafts are never seen), or None when it cannot be found out."""
    cache = _cache(target.repo)
    if use_cache:
        try:
            data = json.loads(cache.read_text(encoding="utf-8"))
            if time.time() - float(data.get("checked", 0)) < CHECK_EVERY:
                r = data.get("release")
                return Release(**r) if r else None
        except (OSError, ValueError, TypeError):
            pass
    try:
        info = json.loads(_get(f"https://api.github.com/repos/{target.repo}/releases/latest",
                               ua=f"{target.tool_id}-updater"))
        release = Release(
            version=str(info["tag_name"]).lstrip("vV"),
            tag=str(info["tag_name"]),
            notes=str(info.get("body") or ""),
            url=str(info.get("html_url") or ""),
            archive=str(info.get("zipball_url") or ""),
            assets={str(a["name"]): {"url": str(a["browser_download_url"]), "digest": str(a.get("digest") or "")}
                    for a in info.get("assets", []) if "name" in a and "browser_download_url" in a},
        )
    except urllib.error.HTTPError as e:
        release = None
        if e.code != 404:  # 404: nothing published yet, cached like an answer
            return None
    except (urllib.error.URLError, OSError, ValueError, KeyError, TypeError, RuntimeError):
        return None
    try:
        cache.parent.mkdir(parents=True, exist_ok=True)
        cache.write_text(json.dumps({"checked": time.time(), "release": release.__dict__ if release else None}),
                         encoding="utf-8")
    except OSError:
        pass
    return release


def available(target: Target, *, use_cache: bool = True, include_skipped: bool = False) -> Release | None:
    """A release newer than this copy (and not skipped, unless asked), or None."""
    if disabled():
        return None
    r = latest(target, use_cache=use_cache)
    if not r or not is_newer(r.version, target.version):
        return None
    if not include_skipped and skipped(target.tool_id) == r.version:
        return None
    return r


# ------------------------------------------------------------ verification


def asset_name(tool_id: str, version: str, platform: str | None = None) -> str:
    platform = platform or paths.platform_key()
    ext = "zip" if platform.startswith("windows") else "tar.gz"
    return f"{tool_id}-{version}-{platform}.{ext}"


def parse_sums(text: str) -> dict[str, str]:
    out = {}
    for line in text.splitlines():
        parts = line.strip().split()
        if len(parts) == 2 and len(parts[0]) == 64:
            out[parts[1].lstrip("*")] = parts[0].lower()
    return out


def verify(blob: bytes, name: str, sums: dict[str, str], digest: str = "") -> str:
    """The blob's SHA-256 when it matches SHA256SUMS (and GitHub's digest when given); raises otherwise."""
    got = hashlib.sha256(blob).hexdigest()
    want = sums.get(name)
    if not want:
        raise RuntimeError(f"{name} is not in SHA256SUMS")
    if got != want:
        raise RuntimeError(f"{name}: SHA-256 {got} does not match SHA256SUMS ({want})")
    if digest:
        algo, _, hexd = digest.partition(":")
        if algo.lower() == "sha256" and hexd.lower() != got:
            raise RuntimeError(f"{name}: SHA-256 does not match the digest GitHub reports")
    return got


def _safe_member(name: str, top: str) -> bool:
    n = name.replace("\\", "/")
    if n.startswith("/") or (len(n) > 1 and n[1] == ":"):
        return False
    parts = [p for p in n.split("/") if p not in ("", ".")]
    return bool(parts) and parts[0] == top and ".." not in parts


def unpack(blob: bytes, name: str, into: Path, top: str) -> Path:
    """Unpack a verified archive into `into`; every member must lie under `top/`. Returns `into/top`."""
    import io

    into.mkdir(parents=True, exist_ok=True)
    if name.endswith(".zip"):
        with zipfile.ZipFile(io.BytesIO(blob)) as z:
            for info in z.infolist():
                if not _safe_member(info.filename, top):
                    raise RuntimeError(f"archive member outside {top}/: {info.filename}")
                if (info.external_attr >> 16) & 0o170000 == 0o120000:
                    raise RuntimeError(f"archive member is a link: {info.filename}")
            z.extractall(into)
    else:
        with tarfile.open(fileobj=io.BytesIO(blob), mode="r:gz") as t:
            for m in t.getmembers():
                if not _safe_member(m.name, top) or not (m.isfile() or m.isdir()):
                    if m.issym() and _safe_member(m.name, top):
                        # a link inside the folder may point only inside it
                        target = (Path(m.name).parent / m.linkname).as_posix()
                        if not m.linkname.startswith("/") and _safe_member(os.path.normpath(target).replace("\\", "/"), top):
                            continue
                    raise RuntimeError(f"archive member not allowed: {m.name}")
            try:
                t.extractall(into, filter="tar")
            except TypeError:  # Python without extraction filters
                t.extractall(into)
    return into / top


# ------------------------------------------------------------------- apply


def install_dir() -> Path:
    """The standalone copy's folder (`<id>/`, holding the executable)."""
    return Path(sys.executable).resolve().parent


def apply(target: Target, release: Release, *, restart_args: list[str] | None = None, log=print) -> str:
    """Bring this copy to `release`. Returns what was done; raises RuntimeError when it cannot."""
    if not frozen():
        if target.apply_source is None:
            raise RuntimeError(f"update from {release.url}")
        return target.apply_source(release)
    if managed():
        raise RuntimeError("this copy is kept by the 3DHeat app: update it in its Extractors panel")
    name = asset_name(target.tool_id, release.version)
    asset = release.assets.get(name)
    sums_asset = release.assets.get("SHA256SUMS")
    if not asset or not sums_asset:
        raise RuntimeError(f"release {release.version} has no {name} for this system")
    ua = f"{target.tool_id}-updater"
    try:
        sums = parse_sums(_get(sums_asset["url"], ua=ua, timeout=DOWNLOAD_TIMEOUT, accept="application/octet-stream").decode("utf-8", "replace"))
        log(f"downloading {name}")
        blob = _get(asset["url"], ua=ua, timeout=DOWNLOAD_TIMEOUT, accept="application/octet-stream")
    except (urllib.error.URLError, OSError) as e:
        raise RuntimeError(f"download failed: {e}") from e
    verify(blob, name, sums, asset.get("digest", ""))
    log("checksum verified")
    here = install_dir()
    staging = here.parent / f".{target.tool_id}-{release.version}-new"
    shutil.rmtree(staging, ignore_errors=True)
    new = unpack(blob, name, staging, target.tool_id)
    exe = new / (target.tool_id + (".exe" if os.name == "nt" else ""))
    if not exe.is_file():
        shutil.rmtree(staging, ignore_errors=True)
        raise RuntimeError("the archive holds no executable")
    _swap(here, new, staging, exe if restart_args is not None else None, restart_args or [])
    return f"updated to {release.version}"


def _swap(here: Path, new: Path, staging: Path, restart: Path | None, args: list[str]) -> None:
    old = here.parent / f".{here.name}-old-{int(time.time())}"
    if os.name != "nt":
        os.replace(here, old)  # a running program's files may be renamed on POSIX
        os.replace(new, here)
        shutil.rmtree(old, ignore_errors=True)
        shutil.rmtree(staging, ignore_errors=True)
        if restart is not None:
            os.execv(str(here / restart.name), [str(here / restart.name), *args])
        return
    # Windows keeps the running program's files locked: a small script waits for this process to end.
    script = Path(tempfile.gettempdir()) / f"heat3d-swap-{os.getpid()}.cmd"
    quoted = " ".join(f'"{a}"' for a in args)
    lines = [
        "@echo off",
        ":wait",
        f'tasklist /FI "PID eq {os.getpid()}" 2>NUL | find "{os.getpid()}" >NUL && (timeout /t 1 /nobreak >NUL & goto wait)',
        f'move "{here}" "{old}" >NUL || goto end',
        f'move "{new}" "{here}" >NUL || (move "{old}" "{here}" >NUL & goto end)',
        f'rmdir /s /q "{old}"',
        f'rmdir /s /q "{staging}"',
    ]
    if restart is not None:
        lines.append(f'start "" "{here / restart.name}" {quoted}')
    lines += [":end", '(goto) 2>nul & del "%~f0"']
    script.write_text("\r\n".join(lines) + "\r\n", encoding="ascii", errors="replace")
    flags = getattr(subprocess, "CREATE_NO_WINDOW", 0) | getattr(subprocess, "DETACHED_PROCESS", 0)
    subprocess.Popen(["cmd", "/c", str(script)], creationflags=flags, close_fds=True)


# ----------------------------------------------------------------- the CLI


def notice(target: Target, release: Release, max_lines: int = 15) -> str:
    notes = [l for l in release.notes.strip().splitlines() if l.strip()]
    more = "\n  ..." if len(notes) > max_lines else ""
    body = "\n".join("  " + l for l in notes[:max_lines]) + more
    return f"{target.name} {release.version} is out (this is {target.version}). {release.url}" + (f"\n{body}" if body else "")


def startup(target: Target, *, ask: bool | None = None) -> None:
    """On a tool's start: say when a newer release is out; update when the user says so (or chose automatic)."""
    try:
        release = available(target)
    except Exception:
        return
    if release is None:
        return
    if managed() and frozen():
        print(f"[{target.tool_id}] {target.name} {release.version} is out; update it in the 3DHeat app's Extractors panel.",
              file=sys.stderr)
        return
    print(f"[{target.tool_id}] " + notice(target, release), file=sys.stderr)
    if auto_enabled(target.tool_id):
        _apply_and_restart(target, release)
        return
    if ask is None:
        ask = sys.stdin.isatty() and sys.stderr.isatty()
    if not ask:
        print(f"[{target.tool_id}] Update with `--update`, or turn on automatic updates with `--auto-update`.",
              file=sys.stderr)
        return
    try:
        answer = input("[U]pdate now, [L]ater, [S]kip this version? [u/L/s] ").strip().lower()
    except EOFError:
        return
    if answer in ("s", "skip"):
        skip(target.tool_id, release.version)
        print(f"[{target.tool_id}] {release.version} skipped; the next newer one will be announced.", file=sys.stderr)
    elif answer in ("u", "update", "y", "yes", "j", "ja"):
        _apply_and_restart(target, release)


def _apply_and_restart(target: Target, release: Release) -> None:
    try:
        msg = apply(target, release, restart_args=sys.argv[1:] if frozen() else None,
                    log=lambda s: print(f"[{target.tool_id}] {s}", file=sys.stderr))
    except RuntimeError as e:
        print(f"[{target.tool_id}] Update not applied: {e}", file=sys.stderr)
        return
    print(f"[{target.tool_id}] {msg}", file=sys.stderr)
    if frozen():
        os._exit(0)  # the new copy starts again with the same arguments
    restart()


def restart() -> None:
    """Run the same command again, on the code now on disk."""
    argv = getattr(sys, "orig_argv", None) or [sys.executable, *sys.argv]
    sys.stdout.flush()
    sys.stderr.flush()
    if os.name == "nt":
        os._exit(subprocess.call(argv))
    os.execv(argv[0], argv)
