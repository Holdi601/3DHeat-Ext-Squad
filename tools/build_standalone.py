"""
Build the standalone executable of this tool for the system it runs on.

    python tools/build_standalone.py            -> dist-standalone/<id>-<version>-<platform>.zip|.tar.gz
    python tools/build_standalone.py --smoke    -> and run it: --version, --help, --gui-selftest,
                                                   --check --json, status --json, extract --new

`standalone.json` names the spec module; PyInstaller (onedir) does the build.
Used by .github/workflows/standalone.yml; nothing here reads game files.

The archive also carries the tool's plugin manifest (`plugin.json` of the repository, see the
viewer's docs/plugins.md) and its icon (`icon-64.png`) beside the program: 3DHeat's manager reads
them to know what the tool does and how to call it.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib
import json
import os
import shutil
import subprocess
import sys
import tarfile
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def platform_key() -> str:
    if sys.platform == "win32":
        return "windows-x64"
    if sys.platform == "darwin":
        return "macos-arm64"
    return "linux-x64"


def load_spec():
    cfg = json.loads((ROOT / "standalone.json").read_text(encoding="utf-8"))
    sys.path.insert(0, str(ROOT))
    mod = importlib.import_module(cfg["spec"])
    return cfg, mod.SPEC


def window_flags() -> list[str]:
    """Windows: a window program (no console window when double-clicked; the command line still works, see
    app/entry.py) with the 3DHeat icon. Elsewhere a console program, as terminals and file managers expect."""
    if sys.platform != "win32":
        return ["--console"]
    package_icon = next(ROOT.glob("*/app/assets/tool.ico"), None) or next(ROOT.glob("*/app/assets/app.ico"), None)
    return ["--windowed", *(["--icon", str(package_icon)] if package_icon else [])]


def cli_shim(folder: Path, tool_id: str) -> None:
    """`<id>-cli.cmd`: the same program for a Windows terminal, which then waits for it and gets its exit code."""
    if sys.platform == "win32":
        (folder / f"{tool_id}-cli.cmd").write_text(
            f"@echo off\r\n\"%~dp0{tool_id}.exe\" %*\r\nexit /b %errorlevel%\r\n", encoding="ascii")


def is_window_program(exe: Path) -> bool:
    """The PE header says GUI subsystem (2), not console (3)."""
    b = exe.read_bytes()[:4096]
    pe = int.from_bytes(b[0x3C:0x40], "little")
    return int.from_bytes(b[pe + 0x5C:pe + 0x5E], "little") == 2


def plugin_files(folder: Path, spec) -> None:
    """`plugin.json` (checked against the spec) and `icon-64.png` beside the program."""
    manifest = ROOT / "plugin.json"
    if manifest.is_file():
        check_plugin(json.loads(manifest.read_text(encoding="utf-8")), spec)
        shutil.copyfile(manifest, folder / "plugin.json")
    icon = next(ROOT.glob("*/app/assets/tool-64.png"), None) or next(ROOT.glob("*/app/assets/icon-64.png"), None)
    if icon is not None:
        shutil.copyfile(icon, folder / "icon-64.png")


def check_plugin(m: dict, spec) -> None:
    """The manifest names this tool, as its main program, with this repository."""
    assert m.get("format") == "3dheat-plugin" and m.get("version") == 1, "plugin.json: not a version 1 plugin manifest"
    main = next((p for p in m.get("programs", []) if not p.get("legacy")), None)
    assert main is not None and main["id"] == spec.id, f"plugin.json: the main program is {main and main['id']}, not {spec.id}"
    assert main["repo"] == spec.repo, f"plugin.json: the repository is {main['repo']}, not {spec.repo}"
    for cap, c in (m.get("capabilities") or {}).items():
        own = next((p for p in m["programs"] if p["id"] == c["program"]), None)
        assert own is not None or c["program"] in m.get("companions", []), f"plugin.json: {cap} names no program of it"


def build(cfg, spec) -> Path:
    package = cfg["spec"].split(".")[0]
    work = ROOT / "build" / "standalone"
    shutil.rmtree(work, ignore_errors=True)
    work.mkdir(parents=True)
    entry = work / "entry.py"
    entry.write_text(
        f"from {cfg['spec']} import SPEC\nfrom {package}.app.entry import main\nraise SystemExit(main(SPEC))\n",
        encoding="utf-8",
    )
    args = [
        sys.executable, "-m", "PyInstaller", "--noconfirm", "--onedir", *window_flags(), "--name", spec.id,
        "--paths", str(ROOT), "--distpath", str(work / "dist"), "--workpath", str(work / "work"), "--specpath", str(work),
        "--collect-submodules", package, "--collect-data", package, "--hidden-import", "tkinter",
        *[a for h in cfg.get("hidden_imports", []) for a in ("--hidden-import", h)],
        *[a for c in cfg.get("collect", []) for a in ("--collect-all", c)],
        *[a for c in cfg.get("collect_submodules", []) for a in ("--collect-submodules", c)],
        str(entry),
    ]
    subprocess.run(args, check=True, cwd=ROOT)
    folder = work / "dist" / spec.id
    cli_shim(folder, spec.id)
    plugin_files(folder, spec)
    out = ROOT / "dist-standalone"
    out.mkdir(exist_ok=True)
    plat = platform_key()
    if plat.startswith("windows"):
        asset = out / f"{spec.id}-{spec.version}-{plat}.zip"
        with zipfile.ZipFile(asset, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
            for f in sorted(folder.rglob("*")):
                z.write(f, Path(spec.id) / f.relative_to(folder))
    else:
        asset = out / f"{spec.id}-{spec.version}-{plat}.tar.gz"
        with tarfile.open(asset, "w:gz") as t:
            t.add(folder, arcname=spec.id)
    digest = hashlib.sha256(asset.read_bytes()).hexdigest()
    (out / (asset.name + ".sha256")).write_text(f"{digest}  {asset.name}\n", encoding="ascii")
    print(f"built {asset.name} {asset.stat().st_size / 1e6:.1f} MB sha256 {digest}")
    return folder


def smoke(spec, folder: Path) -> None:
    exe = folder / (spec.id + (".exe" if os.name == "nt" else ""))
    with tempfile.TemporaryDirectory() as tmp:
        env = dict(os.environ, HEAT3D_LEVELS=str(Path(tmp) / "levels"), HEAT3D_NO_UPDATE="1",
                   LOCALAPPDATA=tmp, XDG_DATA_HOME=tmp)

        def run(*a: str) -> str:
            r = subprocess.run([str(exe), *a], capture_output=True, text=True, env=env, timeout=600)
            if r.returncode != 0:
                raise SystemExit(f"{spec.id} {' '.join(a)} exited {r.returncode}\n{r.stdout}\n{r.stderr}")
            print(f"ok: {spec.id} {' '.join(a)}")
            return r.stdout

        if os.name == "nt":
            assert is_window_program(exe), "the Windows build must be a window program (no console window)"
            assert (folder / f"{spec.id}-cli.cmd").is_file()
        assert run("--version").strip() == f"{spec.id} {spec.version}"
        assert spec.id in run("--help")
        assert "gui-selftest ok" in run("--gui-selftest")
        check = json.loads(run("--check", "--json"))
        assert check["id"] == spec.id and check["checks"], check
        status = json.loads(run("status", "--json"))
        assert status["id"] == spec.id and isinstance(status["games"], list), status
        lines = [json.loads(l) for l in run("extract", "--new", "--progress-json").splitlines() if l.startswith("{")]
        assert lines and lines[-1]["event"] == "done", lines
        for tool in spec.tools:
            run(tool, "--help")
        if getattr(spec, "replays", None) is not None:
            run("convert", "--help")
            run("info", "--help")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--smoke-only", action="store_true", help="smoke-test an existing build")
    a = ap.parse_args()
    cfg, spec = load_spec()
    folder = ROOT / "build" / "standalone" / "dist" / spec.id
    if not a.smoke_only:
        folder = build(cfg, spec)
    if a.smoke or a.smoke_only:
        smoke(spec, folder)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
