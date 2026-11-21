"""
What has been extracted, so a game update or a new map pack is noticed and only
the maps it touched are extracted again.

`<levels>/<game>/.heat3d-extract.json` holds per map the extractor version, the
game build, and size, time and SHA-256 of every game file the map was made from.
Comparing an install against it gives each map a state:

- `new`       in the install, never extracted
- `changed`   a source file differs (size or time changed, and its hash too)
- `outdated`  extracted by an older extractor than the game's `output_version`,
              or extracted before there was a manifest
- `current`   nothing to do
- `missing`   extracted once, no longer in the install (reported, never deleted)
"""

from __future__ import annotations

import datetime as _dt
import hashlib
import json
import os
from dataclasses import dataclass
from pathlib import Path

from .spec import GameSpec, MapSource

NAME = ".heat3d-extract.json"
STATES = ("new", "changed", "outdated", "current", "missing")


def _parse(v: str | None) -> tuple[int, ...]:
    core = str(v or "0").strip().lstrip("vV").split("-")[0].split("+")[0]
    out = []
    for part in core.split("."):
        digits = "".join(c for c in part if c.isdigit())
        out.append(int(digits) if digits else 0)
    return tuple(out)


def older(a: str | None, b: str | None) -> bool:
    x, y = _parse(a), _parse(b)
    w = max(len(x), len(y))
    return x + (0,) * (w - len(x)) < y + (0,) * (w - len(y))


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def _rel(path: Path, game: Path) -> str:
    try:
        return path.relative_to(game).as_posix()
    except ValueError:
        return path.name


@dataclass
class MapState:
    id: str
    title: str
    state: str
    extracted_version: str | None = None
    note: str = ""
    source: MapSource | None = None

    def as_json(self) -> dict:
        return {"id": self.id, "title": self.title, "state": self.state,
                "extracted_version": self.extracted_version}


class Manifest:
    def __init__(self, folder: Path, extractor: str):
        self.folder = Path(folder)
        self.file = self.folder / NAME
        self.extractor = extractor
        self.entries: dict[str, dict] = {}
        try:
            data = json.loads(self.file.read_text(encoding="utf-8"))
            if isinstance(data, dict) and isinstance(data.get("entries"), dict):
                self.entries = data["entries"]
        except (OSError, ValueError):
            pass

    def save(self) -> None:
        self.folder.mkdir(parents=True, exist_ok=True)
        doc = {"schema": 1, "extractor": self.extractor, "entries": dict(sorted(self.entries.items()))}
        tmp = self.file.with_name(NAME + ".tmp")
        tmp.write_text(json.dumps(doc, indent=1), encoding="utf-8")
        os.replace(tmp, self.file)

    def record(self, game: Path, m: MapSource, outputs: list[Path], version: str, build: str | None,
               levels: Path) -> None:
        sources = {}
        for s in m.sources:
            st = s.stat()
            sources[_rel(s, game)] = {"size": st.st_size, "mtime_ns": st.st_mtime_ns, "sha256": sha256(s)}
        outs = []
        for o in outputs:
            try:
                outs.append(Path(o).resolve().relative_to(Path(levels).resolve()).as_posix())
            except ValueError:
                outs.append(Path(o).name)
        self.entries[m.id] = {
            "extractor_version": version,
            "game_build": build,
            "sources": sources,
            "outputs": outs,
            "extracted_at": _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        }

    def state_of(self, game: Path, m: MapSource, g: GameSpec, out: Path) -> MapState:
        e = self.entries.get(m.id)
        if e is None:
            existing = []
            if g.existing_outputs is not None:
                try:
                    existing = [p for p in g.existing_outputs(out, m) if Path(p).exists()]
                except Exception:
                    existing = []
            return MapState(m.id, m.title, "outdated" if existing else "new", None, m.note, m)
        version = e.get("extractor_version")
        recorded = e.get("sources") or {}
        now = {_rel(s, game): s for s in m.sources}
        if set(recorded) != set(now):
            return MapState(m.id, m.title, "changed", version, m.note, m)
        for rel, s in now.items():
            r = recorded[rel]
            try:
                st = s.stat()
            except OSError:
                return MapState(m.id, m.title, "changed", version, m.note, m)
            if st.st_size == r.get("size") and st.st_mtime_ns == r.get("mtime_ns"):
                continue
            # Touched: only the content says whether it changed.
            if st.st_size != r.get("size") or sha256(s) != r.get("sha256"):
                return MapState(m.id, m.title, "changed", version, m.note, m)
        if older(version, g.output_version):
            return MapState(m.id, m.title, "outdated", version, m.note, m)
        return MapState(m.id, m.title, "current", version, m.note, m)


def game_status(g: GameSpec, game: Path | None, levels: Path, extractor: str) -> dict:
    """The state of every map of one game, as `status --json` reports it (plus the sources, for extract)."""
    out = Path(levels) / g.subdir if g.subdir else Path(levels)
    doc: dict = {"game": g.key, "label": g.label, "found": game is not None, "build": None, "maps": [],
                 "counts": {s: 0 for s in STATES}}
    states: list[MapState] = []
    if game is not None:
        if g.build is not None:
            try:
                doc["build"] = g.build(game)
            except Exception:
                doc["build"] = None
        if g.maps is not None:
            man = Manifest(out, extractor)
            maps = g.maps(game)
            states = [man.state_of(game, m, g, out) for m in maps]
            ids = {m.id for m in maps}
            for mid, e in sorted(man.entries.items()):
                if mid not in ids:
                    states.append(MapState(mid, mid, "missing", e.get("extractor_version")))
    for s in states:
        doc["counts"][s.state] += 1
    doc["maps"] = [s.as_json() for s in states]
    doc["_states"] = states
    return doc
