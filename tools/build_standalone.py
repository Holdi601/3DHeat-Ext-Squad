"""
Build the standalone executable of this tool for the system it runs on.

    python tools/build_standalone.py            -> dist-standalone/<id>-<version>-<platform>.zip|.tar.gz
    python tools/build_standalone.py --smoke    -> and run it: --version, --help, --gui-selftest,
                                                   --check --json, status --json, extract --new

`standalone.json` names the spec module; PyInstaller (onedir) does the build.
Used by .github/workflows/standalone.yml; nothing here reads game files.
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
        sys.executable, "-m", "PyInstaller", "--noconfirm", "--onedir", "--console", "--name", spec.id,
        "--paths", str(ROOT), "--distpath", str(work / "dist"), "--workpath", str(work / "work"), "--specpath", str(work),
        "--collect-submodules", package, "--collect-data", package, "--hidden-import", "tkinter",
        *[a for h in cfg.get("hidden_imports", []) for a in ("--hidden-import", h)],
        *[a for c in cfg.get("collect", []) for a in ("--collect-all", c)],
        *[a for c in cfg.get("collect_submodules", []) for a in ("--collect-submodules", c)],
        str(entry),
    ]
    subprocess.run(args, check=True, cwd=ROOT)
    folder = work / "dist" / spec.id
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
