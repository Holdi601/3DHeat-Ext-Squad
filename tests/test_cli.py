"""The command line, on a synthetic demo."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from heat3d_ext_squad.cli import main, map_folder

from test_stream import synthetic_demo

PACKAGE = Path(__file__).resolve().parents[1]


def test_map_folder():
    assert map_folder("/Game/Maps/Some_Map/Gameplay_Layers/Some_Layer_v1") == "Some_Map"
    assert map_folder("/Game/Other/Level") == "Level"
    assert map_folder("") == "unknown"


def test_writes_map_folder_and_reports_json(tmp_path, capsys):
    demo = tmp_path / "in" / "one.replay"
    demo.parent.mkdir()
    demo.write_bytes(synthetic_demo())
    assert main([str(demo.parent), "-o", str(tmp_path / "out"), "--json"]) == 0
    line = json.loads(capsys.readouterr().out.strip())
    assert line["ok"] and line["rows"] == 5 and line["players"] == 1
    assert (tmp_path / "out" / "Test_Map" / "one.parquet").is_file()
    assert (tmp_path / "out" / "Test_Map" / "one.match.json").is_file()


def test_a_bad_file_is_reported_and_fails(tmp_path, capsys):
    bad = tmp_path / "bad.replay"
    bad.write_bytes(b"not a replay at all")
    assert main([str(bad), "-o", str(tmp_path / "out"), "--json"]) == 1
    assert json.loads(capsys.readouterr().out.strip())["ok"] is False


def test_runs_as_a_module(tmp_path):
    demo = tmp_path / "m.replay"
    demo.write_bytes(synthetic_demo())
    out = subprocess.run([sys.executable, "-m", "heat3d_ext_squad", str(demo), "-o", str(tmp_path), "--flat"],
                         cwd=PACKAGE, capture_output=True, text=True, timeout=120)
    assert out.returncode == 0, out.stderr
    assert (tmp_path / "m.parquet").is_file()
