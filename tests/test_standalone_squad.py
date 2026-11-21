"""The standalone app on a synthetic Squad server install (empty folders, no demos)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from heat3d_ext_squad import standalone_spec
from heat3d_ext_squad.app import entry, update


@pytest.fixture(autouse=True)
def _isolated(tmp_path, monkeypatch):
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path / "appdata"))
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path / "appdata"))
    monkeypatch.setenv("HEAT3D_LEVELS", str(tmp_path / "levels"))
    monkeypatch.setenv("HEAT3D_NO_UPDATE", "1")
    update.AUTO_THIS_RUN = False


def _server(tmp_path: Path) -> Path:
    server = tmp_path / "Squad Dedicated Server"
    standalone_spec.demo_folder(server).mkdir(parents=True)
    return server


def test_find_from_the_install_or_its_demo_folder(tmp_path):
    server = _server(tmp_path)
    find = standalone_spec.SPEC.games[0].find
    assert find(str(server)) == server
    assert find(str(standalone_spec.demo_folder(server))) == server
    assert find(str(tmp_path / "elsewhere")) is None


def test_task_defaults_to_the_servers_demos(tmp_path, monkeypatch):
    server = _server(tmp_path)
    monkeypatch.setattr(standalone_spec, "game_folders", lambda s, given=None: {"squad": server})
    task = standalone_spec.SPEC.tasks[0]
    src, out = task.inputs
    assert src.default(tmp_path / "levels") == str(standalone_spec.demo_folder(server))
    assert Path(out.default(tmp_path / "levels")).parts[-2:] == ("matches", "squad")
    assert task.argv({"src": "d", "out": "o"}, tmp_path) == ["heat3d-squad-demo", "d", "-o", "o"]


def test_status_has_no_maps(capsys):
    spec = standalone_spec.SPEC
    assert not spec.has_maps()
    assert entry.main(spec, ["status", "--json"]) == 0
    doc = json.loads(capsys.readouterr().out)
    assert doc["id"] == "heat3d-squad" and doc["games"][0]["maps"] == []
    assert entry.main(spec, ["extract", "--new", "--progress-json"]) == 0
    lines = [json.loads(l) for l in capsys.readouterr().out.splitlines() if l.startswith("{")]
    assert lines[-1] == {"event": "done", "ok": 0, "failed": 0}
