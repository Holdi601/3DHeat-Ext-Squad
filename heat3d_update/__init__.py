"""
Keeping the tools current: a check against the project's GitHub releases, a
notice when a newer one is out, and the update itself.

3DHeat Watcher calls `startup()` when it begins. That check costs one HTTPS request at most
every few hours (the answer is cached), never blocks for more than a few
seconds, and never stops a tool from running: offline, rate-limited or behind a
proxy, the tool simply carries on with the version it has.

How an update is applied depends on how the tools were installed:

- **A git checkout** (`git clone`): `git pull --ff-only`. Refused while the
  checkout has local changes - those are someone's work, and an update is not
  allowed to decide what happens to them.
- **A downloaded copy** (the release zip): the release's source archive is
  downloaded, checked to be the version it says it is, and copied over this
  folder. Files that are not part of a release - recordings, virtual
  environments, settings, anything the user made - are never touched, and
  modules a release removed are removed from the packages it ships, so a stale
  one cannot shadow its replacement.

Nothing is updated without the user knowing: a command-line tool asks first
(and only notifies when there is nobody to ask), the watcher updates itself
while no game is running and says so. `HEAT3D_NO_UPDATE=1` switches both the
check and the update off.
"""

from __future__ import annotations

import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
import zipfile
from dataclasses import dataclass
from pathlib import Path

#: The public repository whose releases are the versions.
REPO = "Holdi601/3DHeat-Ext-Squad"
#: The folder all the tools live in: the repository's root.
ROOT = Path(__file__).resolve().parents[1]
#: How long an answer from GitHub is trusted before asking again.
CHECK_EVERY = 6 * 3600
#: Never wait longer than this for GitHub; a slow network is not a reason to stall a tool.
TIMEOUT = 5.0


@dataclass
class Release:
    version: str
    tag: str
    notes: str
    url: str
    archive: str


def installed_version() -> str:
    try:
        return (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    except OSError:
        return "0"


def parse(version: str) -> tuple[int, ...]:
    """`v1.2.3` or `1.2.3` as numbers; anything after a dash is ignored."""
    core = version.strip().lstrip("vV").split("-")[0].split("+")[0]
    out = []
    for part in core.split("."):
        digits = "".join(ch for ch in part if ch.isdigit())
        out.append(int(digits) if digits else 0)
    return tuple(out)


def is_newer(candidate: str, current: str) -> bool:
    a, b = parse(candidate), parse(current)
    width = max(len(a), len(b))
    return a + (0,) * (width - len(a)) > b + (0,) * (width - len(b))


def disabled() -> bool:
    return os.environ.get("HEAT3D_NO_UPDATE", "").strip() not in ("", "0", "false", "no")


def _cache_path() -> Path:
    base = os.environ.get("LOCALAPPDATA") or str(Path.home() / ".cache")
    # One per tool: each tool has its own releases, and one answer must not stand in for another.
    return Path(base) / "3DHeat" / f"update-check-{REPO.split('/')[-1]}.json"


def _get(url: str) -> bytes:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "3DHeat-Watcher-updater", "Accept": "application/vnd.github+json"},
    )
    with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
        return response.read()


def latest(*, use_cache: bool = True) -> Release | None:
    """The newest published release, or None when it cannot be found out."""
    cache = _cache_path()
    if use_cache:
        try:
            data = json.loads(cache.read_text(encoding="utf-8"))
            if time.time() - float(data.get("checked", 0)) < CHECK_EVERY:
                r = data.get("release")
                return Release(**r) if r else None
        except (OSError, ValueError, TypeError):
            pass
    try:
        info = json.loads(_get(f"https://api.github.com/repos/{REPO}/releases/latest"))
        release = Release(
            version=str(info["tag_name"]).lstrip("vV"),
            tag=str(info["tag_name"]),
            notes=str(info.get("body") or ""),
            url=str(info.get("html_url") or ""),
            archive=str(info["zipball_url"]),
        )
    except urllib.error.HTTPError as e:
        # 404: nothing released yet. Cached like an answer, so it is not asked again at once.
        release = None
        if e.code != 404:
            return None
    except (urllib.error.URLError, OSError, ValueError, KeyError):
        return None
    try:
        cache.parent.mkdir(parents=True, exist_ok=True)
        cache.write_text(
            json.dumps({"checked": time.time(), "release": release.__dict__ if release else None}),
            encoding="utf-8",
        )
    except OSError:
        pass
    return release


def available() -> Release | None:
    """A release newer than this copy, or None."""
    if disabled():
        return None
    release = latest()
    return release if release and is_newer(release.version, installed_version()) else None


# ----------------------------------------------------------------------- apply


def _git(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True, text=True, timeout=120)


def is_checkout() -> bool:
    return (ROOT / ".git").exists() and shutil.which("git") is not None


def apply(release: Release) -> str:
    """Bring this copy to `release`. Returns what was done; raises RuntimeError when it cannot."""
    if is_checkout():
        status = _git("status", "--porcelain", "--untracked-files=no")
        if status.returncode != 0:
            raise RuntimeError(f"git status failed: {status.stderr.strip()}")
        if status.stdout.strip():
            raise RuntimeError(
                "this checkout has local changes; commit or stash them, then run `git pull`"
            )
        pulled = _git("pull", "--ff-only")
        if pulled.returncode != 0:
            raise RuntimeError(f"git pull failed: {pulled.stderr.strip() or pulled.stdout.strip()}")
        return f"updated to {installed_version()} with git pull"
    return _replace_from_archive(release)


def _replace_from_archive(release: Release) -> str:
    try:
        blob = _get(release.archive)
    except (urllib.error.URLError, OSError) as e:
        raise RuntimeError(f"download failed: {e}") from e
    with zipfile.ZipFile(io.BytesIO(blob)) as z:
        names = z.namelist()
        if not names:
            raise RuntimeError("the release archive is empty")
        top = names[0].split("/")[0] + "/"
        with tempfile.TemporaryDirectory(prefix="heat3d-update-") as tmp:
            for name in names:
                rel = name[len(top) :]
                # Nothing outside the archive's own folder, however it is spelled.
                if not rel or rel.startswith(("/", "\\")) or ".." in Path(rel).parts:
                    continue
                target = Path(tmp) / rel
                if name.endswith("/"):
                    target.mkdir(parents=True, exist_ok=True)
                    continue
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(z.read(name))
            staged = Path(tmp)
            version = (staged / "VERSION").read_text(encoding="utf-8").strip() if (staged / "VERSION").exists() else ""
            if parse(version) != parse(release.version):
                raise RuntimeError(f"the archive is version {version or '?'}, not {release.version}")
            _sync(staged, ROOT)
    return f"updated to {release.version} from the release archive"


def _sync(src: Path, dst: Path) -> None:
    """Copy `src` over `dst`, and drop modules a release no longer has from its own packages."""
    for path in src.rglob("*"):
        rel = path.relative_to(src)
        target = dst / rel
        if path.is_dir():
            target.mkdir(parents=True, exist_ok=True)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)
    # A tool's packages sit at the top of its repository; one level down is the
    # old monorepo's layout, kept so an update from it still cleans up.
    for package in [*src.glob("heat3d_*"), *src.glob("*/heat3d_*")]:
        if not package.is_dir():
            continue
        mine = dst / package.relative_to(src)
        for old in mine.rglob("*.py"):
            if not (package / old.relative_to(mine)).exists():
                old.unlink()


# --------------------------------------------------------------------- startup


def startup(tool: str, *, ask: bool | None = None) -> None:
    """
    Check for a newer release when a tool starts; say so, and offer to update.

    `ask` defaults to whether there is someone at a terminal to answer. When
    there is not - a scheduled run, a pipe - the notice is printed and the tool
    carries on unchanged. After an update the same command is started again, so
    what was asked for runs on the new version.
    """
    release = available()
    if release is None:
        return
    print(
        f"[{tool}] 3DHeat Watcher {release.version} is out (this is {installed_version()}). {release.url}",
        file=sys.stderr,
    )
    if ask is None:
        ask = sys.stdin.isatty() and sys.stderr.isatty()
    if not ask:
        print(f"[{tool}] Run `python -m heat3d_update` in {ROOT} to update.", file=sys.stderr)
        return
    try:
        answer = input("Update now? [Y/n] ").strip().lower()
    except EOFError:
        return
    if answer not in ("", "y", "yes", "j", "ja"):
        return
    try:
        print(apply(release), file=sys.stderr)
    except RuntimeError as e:
        print(f"[{tool}] Update not applied: {e}", file=sys.stderr)
        return
    restart()


def restart() -> None:
    """Run the same command again, on the code now on disk."""
    argv = getattr(sys, "orig_argv", None) or [sys.executable, *sys.argv]
    sys.stdout.flush()
    sys.stderr.flush()
    if os.name == "nt":
        # execv on Windows starts a new process and returns control to the shell
        # early; waiting and passing the exit code on keeps a terminal sane.
        code = subprocess.call(argv)
        os._exit(code)
    os.execv(argv[0], argv)


def ensure_importable() -> None:
    """Make `heat3d_update` importable from a tool started inside its own folder."""
    root = str(ROOT)
    if root not in sys.path:
        sys.path.insert(0, root)
