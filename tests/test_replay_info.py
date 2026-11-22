"""The header-only reader on demos built here: made-up values, no real game data."""

from __future__ import annotations

import pytest

from heat3d_ext_squad import container
from heat3d_ext_squad.replay_info import info

from test_layers import header

#: 2026-11-07 12:00:00 on the recording's clock.
RECORDED = 1794052800.0


def demo(tmp_path, **kw):
    p = tmp_path / "test.replay"
    p.write_bytes(container.build(kw.pop("h", header()), [(0, 1000, b"frames"), (1000, 2000, b"more")],
                                  length_ms=754250, friendly="Test Recording", recorded_unix=RECORDED, **kw))
    return p


def test_what_the_header_says(tmp_path):
    i = info(demo(tmp_path))
    assert i["map"] == "Test_Map"
    assert i["layer"] == "Test_Layer_v1"
    assert i["level_path"] == "/Game/Maps/Test_Map/Gameplay_Layers/Test_Layer_v1"
    assert i["mode"] == "Layer"
    assert i["date"] == "2026-11-07T12:00:00"
    assert i["duration_s"] == 754.25
    assert i["game_version"] == "v10.3.1"
    assert i["engine_version"] == "5.5.4"
    assert i["recording_name"] == "Test Recording"
    assert i["platform"] == "LinuxServer"
    # Not in the header: left empty, not guessed.
    assert i["players"] == [] and i["teams"] == [] and i["outcome"] is None and i["map_title"] is None


def test_the_mode_from_the_layer_name(tmp_path):
    h = header(levels=[("/Game/Maps/Test_Map/Gameplay_Layers/Test_Map_AAS_v2", 0)])
    assert info(demo(tmp_path, h=h))["mode"] == "AAS"
    h = header(levels=[("/Game/Maps/Test_Map/Gameplay_Layers/Training", 0)])
    assert info(demo(tmp_path, h=h))["mode"] is None


def test_an_older_file_without_a_timestamp(tmp_path):
    p = tmp_path / "old.replay"
    p.write_bytes(container.build(header(), [(0, 10, b"abc")], file_version=2, length_ms=10))
    i = info(p)
    assert i["date"] is None and i["map"] == "Test_Map"


def test_garbage_is_not_a_demo(tmp_path):
    p = tmp_path / "junk.replay"
    p.write_bytes(b"this is not a replay at all, just some text" * 10)
    with pytest.raises(ValueError, match="not a Squad demo"):
        info(p)
    p.write_bytes(b"")
    with pytest.raises(ValueError):
        info(p)


def test_another_games_replay_is_refused(tmp_path):
    h = header(branch="//Other/1.0", levels=[("/Game/Levels/Arena", 0)])
    with pytest.raises(ValueError, match="another game"):
        info(demo(tmp_path, h=h))
