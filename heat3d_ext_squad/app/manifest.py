"""
What has been extracted, so a game update or a new map pack is noticed and only
the maps it touched are extracted again.

`<levels>/<game>/.heat3d-extract.json` holds per map the extractor version, the
game build, and size, time and SHA-256 of every game file the map was made from.
Comparing an install against it gives each map a state:

- `new`       in the install, never extracted
- `changed`   a source file differs (size or time changed, and its hash too)
- `outdated`  extracted by an older extractor than the game's `output_version`,
              or extracted before there was a manifest and older than its game files
- `current`   nothing to do
- `missing`   extracted once, no longer in the install (reported, never deleted)

Other content (a catalogue, a model pack: `GameSpec.contents`) gets the same
states; its manifest key is `content:<id>`. The items a catalogue lists are
compared too: ids the install holds that the extracted catalogue lacks are
new items (`items` in the status).

An untracked entry (outputs exist, no manifest entry: extracted before
manifests existed) is first asked of the tool (`GameSpec.adopt`): "current"
records it in the manifest (so `status` may write the manifest), "changed"
reports it changed. Without an answer, outputs that are all newer than every
game file they were made from count as `current` with `"untracked": true`
(not recorded); otherwise the entry is `outdated`.

A source whose size and time match the record is taken as unchanged, unless
its time is within RACY_NS of the record (a file rewritten in the same tick
keeps its time): then its hash decides.
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
CONTENT = "content:"
#: At most this many item ids per kind in `items.new` (the counts are always complete).
ITEM_IDS = 50
#: A source modified this close to (or after) its record is hashed even when size and time match.
RACY_NS = 2_000_000_000


def entry_key(m: MapSource) -> str:
    """The manifest key: a map's id, `content:<id>` for other content."""
    return m.id if getattr(m, "kind", "map") == "map" else CONTENT + m.id


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
    kind: str = "map"
    #: Outputs exist without a manifest entry and look current by their times (not recorded).
    untracked: bool = False

    def as_json(self) -> dict:
        d = {"id": self.id, "title": self.title, "state": self.state, "extracted_version": self.extracted_version}
        if self.untracked:
            d["untracked"] = True
        if self.kind != "map":
            d = {"id": self.id, "kind": self.kind, **{k: v for k, v in d.items() if k != "id"}}
        return d


class Manifest:
    def __init__(self, folder: Path, extractor: str):
        self.folder = Path(folder)
        self.file = self.folder / NAME
        self.extractor = extractor
        self.entries: dict[str, dict] = {}
        #: Entries added by `state_of` (adopted): the caller saves the manifest.
        self.dirty = False
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
        self.entries[entry_key(m)] = {
            "extractor_version": version,
            "game_build": build,
            "sources": sources,
            "outputs": outs,
            "extracted_at": _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        }
        if getattr(m, "kind", "map") != "map":
            self.entries[entry_key(m)]["kind"] = m.kind

    def state_of(self, game: Path, m: MapSource, g: GameSpec, out: Path, *, build: str | None = None,
                 levels: Path | None = None) -> MapState:
        kind = getattr(m, "kind", "map")

        def st(state: str, version: str | None = None) -> MapState:
            return MapState(m.id, m.title, state, version, m.note, m, kind)

        e = self.entries.get(entry_key(m))
        if e is None:
            outs = existing_outputs(g, out, m)
            if not outs:
                return st("new")
            answer = None
            if g.adopt is not None:
                try:
                    answer = g.adopt(game, m, out)
                except Exception:
                    answer = None
            if isinstance(answer, (tuple, list)) and len(answer) == 2 and answer[1] in ("current", "changed"):
                version, state = (None if answer[0] is None else str(answer[0])), answer[1]
                if state == "changed":
                    return st("changed", version)
                try:
                    self.record(game, m, outs, version, build,
                                levels if levels is not None else Path(out).parent)
                    self.dirty = True
                except OSError:
                    pass
                return st("outdated" if older(version, g.output_version) else "current", version)
            if _outputs_newer(outs, m.sources):
                s = st("current")
                s.untracked = True
                return s
            return st("outdated")
        version = e.get("extractor_version")
        recorded = e.get("sources") or {}
        now = {_rel(s, game): s for s in m.sources}
        if set(recorded) != set(now):
            return st("changed", version)
        at = _iso_ns(e.get("extracted_at"))
        for rel, s in now.items():
            r = recorded[rel]
            try:
                stat = s.stat()
            except OSError:
                return st("changed", version)
            if (stat.st_size == r.get("size") and stat.st_mtime_ns == r.get("mtime_ns")
                    and (at is None or stat.st_mtime_ns < at - RACY_NS)):
                continue
            # Touched: only the content says whether it changed.
            if stat.st_size != r.get("size") or sha256(s) != r.get("sha256"):
                return st("changed", version)
        if older(version, g.output_version):
            return st("outdated", version)
        return st("current", version)

    def last_build(self) -> str | None:
        """The game build recorded by the latest extract, or None."""
        best = None
        for e in self.entries.values():
            if isinstance(e, dict) and e.get("game_build") is not None:
                if best is None or str(e.get("extracted_at") or "") >= str(best.get("extracted_at") or ""):
                    best = e
        return None if best is None else str(best["game_build"])


def _iso_ns(text) -> int | None:
    """`extracted_at` ("...Z", whole seconds) in nanoseconds since the epoch, or None."""
    try:
        t = _dt.datetime.strptime(str(text), "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=_dt.timezone.utc)
    except (TypeError, ValueError):
        return None
    return int(t.timestamp()) * 1_000_000_000


def _outputs_newer(outputs: list[Path], sources: list[Path]) -> bool:
    """Every output written after every source file changed (a source that cannot be read: False)."""
    try:
        newest_source = max((Path(s).stat().st_mtime_ns for s in sources), default=None)
        oldest_output = min(Path(o).stat().st_mtime_ns for o in outputs)
    except (OSError, ValueError):
        return False
    return newest_source is None or oldest_output > newest_source


def existing_outputs(g: GameSpec, out: Path, m: MapSource) -> list[Path]:
    """Outputs an untracked map or content entry already has (extracted before manifests existed)."""
    found: list[Path] = []
    if g.existing_outputs is not None:
        try:
            found = [Path(p) for p in g.existing_outputs(out, m) if Path(p).exists()]
        except Exception:
            found = []
    if not found and getattr(m, "kind", "map") == "catalog" and (Path(out) / "catalog.json").is_file():
        found = [Path(out) / "catalog.json"]
    return found


def catalog_file_items(out: Path) -> dict[str, list[str]]:
    """The default `extracted_items`: `<out>/catalog.json` items[] by "id" and "kind" (or "category")."""
    try:
        data = json.loads((Path(out) / "catalog.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    items = data.get("items") if isinstance(data, dict) else data
    got: dict[str, set[str]] = {}
    for it in items if isinstance(items, list) else []:
        if isinstance(it, dict) and it.get("id") is not None:
            kind = it.get("kind") or it.get("category") or "item"
            got.setdefault(str(kind), set()).add(str(it["id"]))
    return {k: sorted(v) for k, v in got.items()}


def item_diff(install: dict[str, list[str]] | None, extracted: dict[str, list[str]] | None) -> dict:
    """`items` of the status: counts per kind, the new ids (at most ITEM_IDS per kind), full new/gone counts."""
    inst = {str(k): {str(i) for i in v} for k, v in (install or {}).items()}
    done = {str(k): {str(i) for i in v} for k, v in (extracted or {}).items()}
    new: dict[str, list[str]] = {}
    new_count = gone_count = 0
    for k in sorted(set(inst) | set(done)):
        add = inst.get(k, set()) - done.get(k, set())
        gone_count += len(done.get(k, set()) - inst.get(k, set()))
        if add:
            new_count += len(add)
            new[k] = sorted(add)[:ITEM_IDS]
    return {"install": {k: len(v) for k, v in sorted(inst.items())},
            "extracted": {k: len(v) for k, v in sorted(done.items())},
            "new": new, "new_count": new_count, "gone_count": gone_count}


def game_status(g: GameSpec, game: Path | None, levels: Path, extractor: str) -> dict:
    """The state of every map of one game, as `status --json` reports it (plus the sources, for extract)."""
    out = Path(levels) / g.subdir if g.subdir else Path(levels)
    doc: dict = {"game": g.key, "label": g.label, "found": game is not None, "build": None, "maps": [],
                 "counts": {s: 0 for s in STATES}, "content": [], "content_counts": {s: 0 for s in STATES},
                 "items": item_diff({}, {}), "build_changed": False}
    states: list[MapState] = []
    cstates: list[MapState] = []
    if game is not None:
        if g.build is not None:
            try:
                doc["build"] = g.build(game)
            except Exception:
                doc["build"] = None
        man = Manifest(out, extractor) if g.maps is not None or g.contents is not None else None
        if g.maps is not None:
            maps = g.maps(game)
            states = [man.state_of(game, m, g, out, build=doc["build"], levels=levels) for m in maps]
            ids = {m.id for m in maps}
            for mid, e in sorted(man.entries.items()):
                if mid not in ids and not mid.startswith(CONTENT):
                    states.append(MapState(mid, mid, "missing", e.get("extractor_version")))
        if g.contents is not None:
            contents = [c for c in g.contents(game) if getattr(c, "kind", "map") != "map"]
            cstates = [man.state_of(game, c, g, out, build=doc["build"], levels=levels) for c in contents]
            ids = {entry_key(c) for c in contents}
            for key, e in sorted(man.entries.items()):
                if key.startswith(CONTENT) and key not in ids:
                    cid = key[len(CONTENT):]
                    cstates.append(MapState(cid, cid, "missing", e.get("extractor_version"), kind=str(e.get("kind") or "content")))
        if g.catalog_items is not None:
            try:
                install = g.catalog_items(game) or {}
                done = (g.extracted_items(out) if g.extracted_items is not None else catalog_file_items(out)) or {}
                doc["items"] = item_diff(install, done)
            except Exception as e:  # a catalogue that cannot be read: no item numbers, said why
                doc["items"]["error"] = f"{type(e).__name__}: {e}"
        if man is not None and man.dirty:
            try:
                man.save()  # adopted entries: extracted before manifests, confirmed by the tool
            except OSError:
                pass
        if man is not None and doc["build"] is not None:
            last = man.last_build()
            doc["build_changed"] = last is not None and last != str(doc["build"])
    for s in states:
        doc["counts"][s.state] += 1
    for s in cstates:
        doc["content_counts"][s.state] += 1
    doc["maps"] = [s.as_json() for s in states]
    doc["content"] = [s.as_json() for s in cstates]
    doc["_states"] = states
    doc["_content_states"] = cstates
    return doc
