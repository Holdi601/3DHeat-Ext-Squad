"""
What a Squad server demo says about the match: who played, on which team and
in which squad, and where each of them was.

The engine part (`stream.py`, `movement.py`) gives actors and named
properties. Squad's part is which classes and properties carry what, read off
the replay's own net field exports (class and property names) and checked on
real v10.3.1 demos:

- `/Script/Squad.SQPlayerState`: `PlayerNamePrivate` (the name, an FString),
  `TeamState` and `SquadState` (references to those actors), `CurrentPawn`
  (what the player controls right now: their soldier, a vehicle, or a seat
  pawn of a vehicle), `Soldier`.
- `/Script/Squad.SQTeamState`: the team number (a 32-bit integer the replay
  names by the engine's hardcoded name 253, `ID`-like) and `FactionSetupId`
  (an FName such as `FSTemplate_ABC`).
- `/Script/Squad.SQSquadState`: the squad number (the same hardcoded name)
  and `TeamId`.
- Soldiers are the blueprints under `/Game/Blueprints/Soldiers/`; their
  `PlayerState` points back at the player.
- A seat pawn's `Owner` (or `AttachParent`) is the vehicle it sits in.
- Positions are each actor's `ReplicatedMovement`.

A player's track is then: for each stretch of time their `CurrentPawn` stays
the same, the movement of that pawn - or of the vehicle the pawn sits in.
Helicopters replicate their movement through their own component in another
format, which is not decoded; a player in a helicopter has no rows for that
time.

Every other replicated property the stream names is kept too (`Match.props`),
decoded as far as its bits say what it is (`decode`): a flag, a number, a
string, a name, else its bits in hex. Some are read for the table: a
soldier's `RemoteViewPitch` (where it looks up and down), an actor's
`Health`, a player's `CurrentSeat`; and every damageable actor's spawn and
removal (vehicles, deployables, emplacements) is an event.
"""

from __future__ import annotations

import bisect
import math
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .bits import BitReader, ReadError
from .container import ReplayFile, read
from .movement import helicopter_movement, rep_movement
from .keep import Keeper, keep_container
from .stream import Actor, Group, Stats, Stream
from .stream import _leaf as path_leaf

#: The engine's hardcoded FName that SQTeamState and SQSquadState use for their number.
NUMBER_NAMES = ("#name253", "ID", "Id", "TeamId")

WANTED = {
    "ReplicatedMovement",
    "PlayerNamePrivate", "TeamState", "SquadState", "CurrentPawn", "Soldier", "PlayerState",
    "FactionSetupId", "TeamId", "#name253", "Owner", "AttachParent", "SquadName", "ServerName",
}

#: Properties that are replication bookkeeping, not the game: counted, not kept.
NOISE = {"ReplayLastTransformUpdateTimeStamp", "ReplicatedMovement"}

#: How the names of properties and parameters that hold an object (a packed net GUID) end. A player's
#: `CurrentSeat` read so is, at every change, the seat the soldier's `MulticastUpdateCurrentSeat` call names.
OBJECT_WORDS = ("Class", "State", "Seat", "Pawn", "Actor", "Instigator", "Causer", "Owner", "Controller", "Target",
                "Vehicle", "Weapon", "Soldier", "Parent")

#: Properties whose 32 or 64 bits are a floating-point number, by a word in their name; other 32-bit ones are
#: integers. `Input`: a vehicle's throttle, brake and handbrake read so lie in 0..1, its steering in -1..1, in
#: every update of the demos read.
FLOAT_WORDS = ("Health", "Time", "Rate", "Multiplier", "Duration", "Seconds", "Thrust", "Scale", "Distance",
               "Speed", "Interval", "Radius", "Damage", "Percent", "Progress", "Ratio", "Stamina", "Input")

#: A soldier's health is gone below this: dead, not wounded (a soldier who gives up or bleeds out is set to -300).
DEAD_BELOW = -100.0

#: Properties holding a person's online ids: never written into the table or the match document, nor decoded
#: into the sidecar (whose bits hold them, as the demo does).
IDS = {"UniqueID", "OnlineUserId", "SquadCreatorSteamID", "SteamID", "EOSID"}

#: An actor that can be damaged or built: its spawn and removal are events.
DAMAGEABLE = {"Health", "bCanBeDamaged", "BuildState", "bRequiresFOB"}


def decode(name: str, b: BitReader) -> Any:
    """
    A replicated property's value, as far as its bits say: one bit a flag; an
    object (its net GUID) when its name ends as a reference's does and its
    bits are one packed GUID; a string when a length and that many bytes fill
    it exactly; a name when it reads as one exactly; 8, 16, 32 or 64 bits a
    number (a float when its name says so); else the bits as hex.
    """
    n = b.left()
    if n == 1:
        return bool(b.bit())
    start = b.pos
    if n % 8 == 0 and n <= 40 and name.endswith(OBJECT_WORDS):
        try:
            g = b.packed()
            if b.at_end():
                return {"guid": g}
        except ReadError:
            pass
        b.pos = start
    if n >= 32:
        try:
            v = b.fstring()
            if b.at_end():
                return v
        except ReadError:
            pass
        b.pos = start
    if n not in (8, 16, 32, 64):
        try:
            v = b.fname()
            if b.at_end():
                return v
        except ReadError:
            pass
        b.pos = start
    floaty = any(w in name for w in FLOAT_WORDS)
    if n == 8:
        return b.u8()
    if n == 16:
        return b.u16()
    if n == 32:
        return round(b.f32(), 6) if floaty else b.i32()
    if n == 64:
        return b.f64() if floaty or "Double" in name else b.u64()
    value, count = b.rest()
    raw = value.to_bytes((count + 7) // 8, "little")
    out: dict[str, Any] = {"bits": count, "hex": raw.hex()} if count <= 4096 else {"bits": count}
    texts = _texts(raw)
    if texts:
        out["text"] = texts
    return out


def _texts(raw: bytes) -> list[str]:
    """The strings inside a structure's bytes: a 32-bit length, then that many bytes ending in a zero, printable."""
    out = []
    i = 0
    while i + 5 <= len(raw):
        n = int.from_bytes(raw[i : i + 4], "little")
        if 2 <= n <= 512 and i + 4 + n <= len(raw) and raw[i + 4 + n - 1] == 0:
            text = raw[i + 4 : i + 4 + n - 1]
            if text and all(32 <= c < 127 for c in text):
                out.append(text.decode("ascii"))
                i += 4 + n
                continue
        i += 1
    return out


#: Words in a remote call parameter's name that make 192 bits a vector of three doubles (FVector).
VECTOR_WORDS = ("Location", "Origin", "Impulse", "Velocity", "Position", "Dir", "Normal", "Offset", "Vector", "Point")
#: ... and 48 bits a unit vector (FVector_NetQuantizeNormal: three 16-bit fixed-point numbers).
DIRECTION_WORDS = ("Dir", "Normal")


def decode_param(name: str, b: BitReader, stream: Stream | None = None) -> Any:
    """
    A remote call's parameter: a vector where its name and size say so (192
    bits three doubles; 48 bits a unit vector; else a quantized vector that
    reads exactly, as its integers and whether they are scaled), an object
    where its name says so and its bits are one packed net GUID, else as
    `decode` reads a property.
    """
    n = b.left()
    start = b.pos
    vectorish = any(w in name for w in VECTOR_WORDS)
    try:
        if vectorish and n == 192:
            return [b.f64(), b.f64(), b.f64()]
        if n == 48 and any(w in name for w in DIRECTION_WORDS):
            return [round((b.bits(16) - 32768) / 32767, 5) for _ in range(3)]
        if vectorish and 7 < n < 192:
            info = b.serialized_int(1 << 7)
            bits = info & 63
            if bits:
                sign = 1 << (bits - 1)
                xyz = [((b.bits(bits) ^ sign) - sign) for _ in range(3)]
                if b.at_end():
                    return {"quantized": xyz, "scaled": bool(info >> 6)}
    except ReadError:
        pass
    b.pos = start
    if n % 8 == 0 and 8 <= n <= 40 and name.endswith(OBJECT_WORDS):
        return object_ref(b, stream)
    return decode(name, b)


def object_ref(b: BitReader, stream: Stream | None = None) -> Any:
    """An object reference: its packed net GUID, with its class or path where the stream knows it."""
    start = b.pos
    try:
        g = b.packed()
        if b.at_end():
            out: dict[str, Any] = {"guid": g}
            a = stream.actors.get(g) if stream else None
            if a is not None:
                out["class"] = class_name(a.path)
            elif stream is not None and g in stream.guid_paths:
                out["path"] = stream.guid_paths[g]
            return out
    except ReadError:
        pass
    b.pos = start
    return decode("", b)


@dataclass
class Shot:
    t: float
    weapon: int  # the weapon, or for a hit the vehicle hit
    function: str
    origin: tuple[float, float, float]
    direction: tuple[float, float, float] | None
    kind: str = "fire"
    detail: str = ""


def _vec(v: Any) -> tuple[float, float, float] | None:
    if isinstance(v, list) and len(v) == 3 and all(isinstance(x, (int, float)) for x in v):
        return float(v[0]), float(v[1]), float(v[2])
    return None


def _matched(sh: Shot, fired) -> bool:
    """Whether an effects call repeats a shot already placed: same weapon, same direction, within a second."""
    return bool(sh.direction) and any(
        abs(f.t - sh.t) < 1.0 and f.direction and max(abs(a - b) for a, b in zip(f.direction, sh.direction)) < 1e-4
        for f in fired)


def shot_of(t: float, actor: int, function: str, params: dict) -> Shot | None:
    """
    A remote call that places a shot or a hit:

    - `MulticastFireProjectile(WithId)`: `OriginZeroBased`, three doubles, and
      `ShootDir`, a unit vector;
    - `MulticastFireMultipleProjectileEffects`: `Origin`, quantized in tenths
      (divided by 10 it is the `OriginZeroBased` of the matching
      `MulticastFireProjectile`), and `ShootDir`;
    - `MulticastPlayDamageEffects` on a vehicle: `ImpactLocationZeroBased`,
      and the `DamageTypeClass`.
    """
    if function in ("MulticastFireProjectile", "MulticastFireProjectileWithId"):
        o, d = _vec(params.get("OriginZeroBased")), _vec(params.get("ShootDir"))
        return Shot(t, actor, function, o, d) if o else None
    if function == "MulticastFireMultipleProjectileEffects":
        q = params.get("Origin")
        if isinstance(q, dict) and q.get("scaled") and _vec(q.get("quantized")):
            o = tuple(x / 10.0 for x in q["quantized"])
            return Shot(t, actor, function, o, _vec(params.get("ShootDir")))
        return None
    if function == "MulticastPlayDamageEffects":
        o = _vec(params.get("ImpactLocationZeroBased"))
        dmg = params.get("DamageTypeClass")
        detail = ""
        if isinstance(dmg, dict):
            detail = class_name(dmg.get("path", "")) or dmg.get("class", "") or ""
        return Shot(t, actor, function, o, None, "hit", detail) if o else None
    return None


@dataclass
class Player:
    guid: int
    name: str = ""
    teams: list[tuple[float, int]] = field(default_factory=list)  # (time, TeamState)
    squads: list[tuple[float, int]] = field(default_factory=list)  # (time, SquadState)
    pawns: list[tuple[float, int]] = field(default_factory=list)  # (time, CurrentPawn)


@dataclass
class Team:
    number: int | None = None
    faction: str = ""


@dataclass
class SquadUnit:
    number: int | None = None
    team: int | None = None


@dataclass
class Sample:
    t: float
    x: float
    y: float
    z: float
    yaw: float
    speed: float


@dataclass
class Match:
    name: str
    replay: ReplayFile
    stats: Stats
    players: dict[int, Player]
    teams: dict[int, Team]
    squads: dict[int, SquadUnit]
    actors: dict[int, Actor]
    tracks: dict[int, list[Sample]]
    owner: dict[int, int]  # pawn -> the vehicle it sits in
    soldier_player: dict[int, list[tuple[float, int]]]  # soldier -> (time, PlayerState)
    movement_errors: int = 0
    #: Every other property, where it changed: guid -> property -> [(time, value)].
    props: dict[int, dict[str, list[tuple[float, Any]]]] = field(default_factory=dict)
    #: How often each class's properties were sent (the bookkeeping ones too): class -> property -> count.
    census: dict[str, dict[str, int]] = field(default_factory=dict)
    #: Every item the demo holds, kept for the sidecars and the self-check (None when parsed without).
    keeper: Keeper | None = None
    #: The stream, for its export tables and what it counted.
    stream: Stream | None = None
    #: Shots fired, from the weapons' remote calls.
    shots: list[Shot] = field(default_factory=list)
    #: The sidecar files `output.write` wrote.
    sidecars: list[str] = field(default_factory=list)

    def value_at(self, guid: int, prop: str, t: float) -> Any:
        """A property's value at time `t`: the last change by then, None before the first."""
        changes = self.props.get(guid, {}).get(prop)
        if not changes:
            return None
        i = bisect.bisect_right([c[0] for c in changes], t) - 1
        return changes[i][1] if i >= 0 else None

    def player_name(self, guid: int) -> str:
        """The name of the player an actor belongs to: itself, its PlayerState, or its Owner's."""
        seen: set[int] = set()
        while guid and guid not in seen:
            seen.add(guid)
            if guid in self.players and self.players[guid].name:
                return self.players[guid].name
            ps = self.value_at(guid, "PlayerState", float("inf"))
            ps = ps.get("guid") if isinstance(ps, dict) else ps
            if isinstance(ps, int) and ps in self.players:
                return self.players[ps].name
            guid = self.owner.get(guid) or 0
        return ""

    def events(self) -> list[dict[str, Any]]:
        """
        Every damageable actor's spawn and removal (vehicles, deployables,
        emplacements, ammo crates), at its place; and every seat a player took.
        """
        out: list[dict[str, Any]] = []
        for guid, a in self.actors.items():
            names = self.props.get(guid, {})
            if not (DAMAGEABLE & set(names)) or is_soldier(class_name(a.path)) or a.location is None:
                continue
            kind = class_name(a.path)
            track = self.tracks.get(guid)
            # Whose it is; an actor nobody owns (a vehicle at its spawn, a crate) goes under its own class.
            who = self.player_name(guid) or kind
            yaw = a.rotation[1] if a.rotation else 0.0
            spawn = Sample(a.opened, a.location.x, a.location.y, a.location.z, yaw, 0.0)
            out.append(_row(spawn, who, None, None, "spawn", kind, kind, health=self.value_at(guid, "Health", a.opened),
                            entity=guid))
            if a.closed is not None:
                last = track[-1] if track else spawn
                end = Sample(a.closed, last.x, last.y, last.z, last.yaw, 0.0)
                out.append(_row(end, who, None, None, "removed", kind, kind,
                                health=self.value_at(guid, "Health", a.closed), entity=guid, detail=a.close_reason or ""))
            # Its health: each fall a "damaged" row where it was, the first at or below 0 "destroyed".
            times = [x.t for x in track] if track else []
            before = None
            for t, health in names.get("Health", []):
                if not isinstance(health, (int, float)) or isinstance(health, bool):
                    continue
                if before is not None and health < before or health <= 0:
                    i = bisect.bisect_right(times, t) - 1
                    at = track[i] if track and i >= 0 else spawn
                    here = Sample(t, at.x, at.y, at.z, at.yaw, 0.0)
                    out.append(_row(here, who, None, None, "destroyed" if health <= 0 else "damaged", kind, kind,
                                    health=health, entity=guid))
                    if health <= 0:
                        break
                before = health
        rows_by = {}
        for p in self.players.values():
            seats = self.props.get(p.guid, {}).get("CurrentSeat", [])
            for t, seat in seats:
                # The seat is a component of the vehicle (or of a seat pawn on it): its object, sent on that actor.
                seat = seat.get("guid") if isinstance(seat, dict) else seat
                if not isinstance(seat, int) or isinstance(seat, bool) or not seat:
                    continue
                holder = self.stream.subobjects.get(seat, seat) if self.stream else seat
                vehicle = holder if holder in self.tracks else self.owner.get(holder, holder)
                track = self.tracks.get(vehicle)
                if not track:
                    continue
                times = rows_by.setdefault(vehicle, [s.t for s in track])
                i = max(0, bisect.bisect_right(times, t) - 1)
                team, squad = self.team_of(p, t), self.squad_of(p, t)
                at = Sample(t, track[i].x, track[i].y, track[i].z, track[i].yaw, 0.0)
                out.append(_row(at, p.name or f"player {p.guid}", team, squad, "seat", self.kind(vehicle),
                                self.kind(holder), entity=vehicle))
        return out

    @property
    def level(self) -> str:
        h = self.replay.header
        return h.levels[0][0] if h and h.levels else ""

    @property
    def version(self) -> str:
        return self.replay.header.branch if self.replay.header else ""

    def team_of(self, p: Player, t: float = float("inf")) -> Team | None:
        """The player's team at time `t` (players change sides on some servers); the last one by default."""
        return self.teams.get(_at(p.teams, t))

    def squad_of(self, p: Player, t: float = float("inf")) -> SquadUnit | None:
        return self.squads.get(_at(p.squads, t))

    def kind(self, guid: int) -> str:
        a = self.actors.get(guid)
        return class_name(a.path) if a else ""

    def rows(self) -> list[dict[str, Any]]:
        """Every position as a row: whose it was, on foot or in what."""
        out: list[dict[str, Any]] = []
        covered: set[int] = set()
        for p in self.players.values():
            who = p.name or f"player {p.guid}"
            spans = self._spans(p)
            for i, (start, pawn) in enumerate(spans):
                if not pawn:
                    continue
                end = spans[i + 1][0] if i + 1 < len(spans) else float("inf")
                target = pawn if pawn in self.tracks else self.owner.get(pawn, pawn)
                track = self.tracks.get(target)
                if not track:
                    continue
                if target == pawn and is_soldier(self.kind(pawn)):
                    covered.add(pawn)
                on_foot = is_soldier(self.kind(target))
                times = [s.t for s in track]
                team = self.team_of(p, start)
                squad = self.squad_of(p, start)
                for s in track[bisect.bisect_left(times, start) : bisect.bisect_left(times, end)]:
                    out.append(_row(s, who, team, squad, "position" if on_foot else "vehicle",
                                    self.kind(target), self.kind(pawn), pitch=self._pitch(target, s.t),
                                    health=self.value_at(target, "Health", s.t), entity=target))
        # Soldiers nobody was found to control (bots without a player state,
        # a recording that missed the link): kept, under their own name.
        for guid, track in self.tracks.items():
            if guid in covered or not is_soldier(self.kind(guid)):
                continue
            bot = is_bot(self.kind(guid))
            who = self._soldier_owner_name(guid) or (f"bot {guid}" if bot else f"soldier {guid}")
            p = next((pl for pl in self.players.values() if pl.name == who), None)
            t0 = track[0].t
            team = self.team_of(p, t0) if p else None
            squad = self.squad_of(p, t0) if p else None
            for s in track:
                out.append(_row(s, who, team, squad, "position", self.kind(guid), self.kind(guid),
                                pitch=self._pitch(guid, s.t), health=self.value_at(guid, "Health", s.t), entity=guid))
        out += self.events()
        out += self.casualties()
        out += self.shot_rows()
        out.sort(key=lambda r: (r["time"], r["player"]))
        return out

    def shot_rows(self) -> list[dict[str, Any]]:
        """
        Every shot a weapon's remote calls place (`fire`: where it left, the
        direction it went as yaw and pitch, the weapon as `pawn`, the call as
        `detail`), and every hit a vehicle's `MulticastPlayDamageEffects`
        places (`hit`: where, the damage type as `detail`). A weapon sends a
        shot twice, `MulticastFireProjectile` and a moment later
        `MulticastFireMultipleProjectileEffects` with the same direction; the
        second is a row only where no first one matches it (some weapons send
        only the second).
        """
        fired: dict[int, list[Shot]] = {}
        for sh in self.shots:
            if sh.kind == "fire" and not sh.function.endswith("Effects"):
                fired.setdefault(sh.weapon, []).append(sh)
        out = []
        for sh in self.shots:
            if sh.kind == "fire" and sh.function.endswith("Effects") and _matched(sh, fired.get(sh.weapon, ())):
                continue
            kind = self.kind(sh.weapon)
            p = self._occupant(sh.weapon, sh.t) if sh.kind == "fire" else None
            who = self.player_name(sh.weapon) or (p.name if p else "") or kind
            p = p or next((pl for pl in self.players.values() if pl.name == who), None)
            team = self.team_of(p, sh.t) if p else None
            squad = self.squad_of(p, sh.t) if p else None
            yaw = pitch = None
            if sh.direction:
                dx, dy, dz = sh.direction
                yaw = math.degrees(math.atan2(dy, dx))
                pitch = math.degrees(math.asin(max(-1.0, min(1.0, dz))))
            out.append(_row(Sample(sh.t, *sh.origin, yaw or 0.0, 0.0), who, team, squad, sh.kind, kind, "",
                            pitch=pitch, entity=sh.weapon, detail=sh.detail or sh.function))
        return out

    def _occupant(self, guid: int, t: float) -> Player | None:
        """The player whose seat, at `t`, is on the actor `guid` or on what it is mounted on (a turret, a vehicle)."""
        chain: list[int] = []
        while guid and guid not in chain:
            chain.append(guid)
            guid = self.owner.get(guid) or 0
        for p in self.players.values():
            seat = self.value_at(p.guid, "CurrentSeat", t)
            seat = seat.get("guid") if isinstance(seat, dict) else None
            if not seat:
                continue
            holder = self.stream.subobjects.get(seat, seat) if self.stream else seat
            if holder in chain or self.owner.get(holder) in chain:
                return p
        return None

    def _pitch(self, guid: int, t: float) -> float | None:
        """
        A soldier's view pitch at `t`, degrees up. `RemoteViewPitch` is a byte
        spanning straight down (0) to straight up (255): on the demos read, its
        values lie around 120 at rest and reach 34 and 255 - the engine's own
        packing (a byte of a whole turn) would put soldiers 128 degrees under
        the horizon.
        """
        v = self.value_at(guid, "RemoteViewPitch", t)
        if not isinstance(v, int):
            return None
        return v * 180.0 / 255.0 - 90.0

    def casualties(self) -> list[dict[str, Any]]:
        """
        Every soldier and bot wounded, revived and killed, where it was then,
        from its `Health` and `bWounded`: wounded when `bWounded` turns on;
        revived when it turns off with health above 0; dead when the health
        falls below DEAD_BELOW (a player who gives up or bleeds out is set to
        -300), or - a bot, which is never wounded - to 0 or below.
        """
        out: list[dict[str, Any]] = []
        for guid, props in self.props.items():
            kind = self.kind(guid)
            if not is_soldier(kind):
                continue
            track = self.tracks.get(guid)
            if not track:
                continue
            times = [s.t for s in track]
            bot = is_bot(kind)
            who = self._soldier_owner_name(guid) or (f"bot {guid}" if bot else f"soldier {guid}")
            p = next((pl for pl in self.players.values() if pl.name == who), None)

            def add(t: float, event: str, health: Any) -> None:
                i = max(0, bisect.bisect_right(times, t) - 1)
                s = track[i]
                team = self.team_of(p, t) if p else None
                squad = self.squad_of(p, t) if p else None
                out.append(_row(Sample(t, s.x, s.y, s.z, s.yaw, 0.0), who, team, squad, event, kind, kind,
                                pitch=self._pitch(guid, t), health=health, entity=guid))

            for t, wounded in props.get("bWounded", []):
                health = self.value_at(guid, "Health", t)
                if wounded is True:
                    add(t, "wounded", health)
                elif isinstance(health, (int, float)) and health > 0:
                    add(t, "revived", health)
            for t, health in props.get("Health", []):
                if isinstance(health, (int, float)) and (health < DEAD_BELOW or (bot and health <= 0)):
                    add(t, "death", health)
                    break
        return out

    def _spans(self, p: Player) -> list[tuple[float, int]]:
        """
        (from time, pawn) for a player: their `CurrentPawn` changes, merged with
        the moments a soldier names them as its player state (and stops) - the
        soldier's link often arrives a moment before the player state's.
        """
        marks: list[tuple[float, int, int]] = [(t, pawn, 0) for t, pawn in p.pawns]
        for soldier, links in self.soldier_player.items():
            was = 0
            for t, ps in links:
                if ps == p.guid:
                    marks.append((t, soldier, 0))
                elif was == p.guid:
                    marks.append((t, 0, soldier))  # the soldier let go of the player
                was = ps
        marks.sort(key=lambda m: m[0])
        spans: list[tuple[float, int]] = []
        for t, pawn, released in marks:
            if released and (not spans or spans[-1][1] != released):
                continue  # the player had already moved on to another pawn
            spans.append((t, pawn))
        return spans

    def _soldier_owner_name(self, soldier: int) -> str:
        for _t, ps in self.soldier_player.get(soldier, []):
            if ps and ps in self.players and self.players[ps].name:
                return self.players[ps].name
        return ""


def _at(changes: list[tuple[float, int]], t: float) -> int:
    """The value in effect at `t` - the first one when `t` is before every change."""
    value = changes[0][1] if changes else 0
    for when, v in changes:
        if when > t:
            break
        value = v
    return value


def _row(s: Sample, who: str, team: Team | None, squad: SquadUnit | None, event: str, what: str, seat: str,
         pitch: float | None = None, health: Any = None, entity: int | None = None, detail: str = ""):
    return {
        "entity": -1 if entity is None else entity, "detail": detail,
        "time": s.t, "x": s.x, "y": s.y, "z": s.z, "yaw": s.yaw, "speed": s.speed,
        "player": who, "team": team.number if team and team.number is not None else -1,
        "faction": team.faction if team else "", "squad": squad.number if squad and squad.number is not None else -1,
        "event": event, "pawn": what, "seat": seat if seat != what else "",
        "pitch": float("nan") if pitch is None else pitch,
        "health": float(health) if isinstance(health, (int, float)) and not isinstance(health, bool) else float("nan"),
    }


def class_name(path: str) -> str:
    """`/Game/Blueprints/Soldiers/ABC/BP_Soldier_ABC_Rifleman.Default__BP_Soldier_ABC_Rifleman_C` -> `BP_Soldier_ABC_Rifleman`."""
    leaf = path.rsplit(".", 1)[-1]
    if leaf.startswith("Default__"):
        leaf = leaf[len("Default__"):]
    return leaf[:-2] if leaf.endswith("_C") else leaf


def is_soldier(kind: str) -> bool:
    """A soldier: a player's (`BP_Soldier...`) or a bot (`SQSquidBot`, the AI the seeding layers fill a server with)."""
    return kind.startswith("BP_Soldier") or is_bot(kind)


def is_bot(kind: str) -> bool:
    return kind.startswith("SQSquidBot")


def _leaf(g: Group) -> str:
    return g.path.rsplit(".", 1)[-1].rsplit("/", 1)[-1]


def load(path: str | Path) -> Match:
    buf = Path(path).read_bytes()
    return parse(buf, Path(path).stem)


def parse(buf: bytes, name: str = "replay", keep: bool = True) -> Match:
    replay = read(buf)
    eng = replay.header.engine_network_version if replay.header else 0
    keeper = Keeper() if keep else None
    if keeper:
        keep_container(keeper, replay, buf)
    players: dict[int, Player] = {}
    teams: dict[int, Team] = {}
    squads: dict[int, SquadUnit] = {}
    tracks: dict[int, list[Sample]] = {}
    owner: dict[int, int] = {}
    soldier_player: dict[int, list[tuple[float, int]]] = {}
    props: dict[int, dict[str, list[tuple[float, Any]]]] = {}
    census: dict[str, dict[str, int]] = {}
    shots: list[Shot] = []
    errors = [0]

    def keep_prop(t: float, actor: Actor, g: Group, obj: int, prop: str, b: BitReader) -> Any:
        """Any property, decoded as far as it goes, kept where it changed - the actor's own, or a subobject's."""
        leaf = g.leaf
        counts = census.setdefault(leaf, {})
        counts[prop] = counts.get(prop, 0) + 1
        w = BitReader(b.value, b.end, b.pos)
        try:
            value = decode(prop, w)
        except ReadError:
            return None
        if prop in NOISE:
            return value
        # A subobject's under its own name where it has one (`wheel_L1.Health`), else its class's.
        key = prop if obj == actor.guid else f"{path_leaf(s.guid_paths[obj]) if obj in s.guid_paths else leaf}.{prop}"
        changes = props.setdefault(actor.guid, {}).setdefault(key, [])
        if not changes or changes[-1][1] != value:
            changes.append((t, value))
        return value

    def on_property(t: float, actor: Actor | None, g: Group, obj: int, prop: str, b: BitReader) -> Any:
        if actor is None:
            return None
        if prop == "ReplicatedMovement":
            census.setdefault(g.leaf, {})[prop] = census.setdefault(g.leaf, {}).get(prop, 0) + 1
            heli = g.leaf == "SQHelicopterMovementComponent"
            try:
                if heli:
                    m, clock = helicopter_movement(BitReader(b.value, b.end, b.pos))
                else:
                    m = rep_movement(BitReader(b.value, b.end, b.pos), eng)
            except ReadError:
                errors[0] += 1
                return None
            # A component's movement is not the actor's - but for a helicopter's movement component, which moves it.
            if obj == actor.guid or heli:
                v = m.velocity
                tracks.setdefault(actor.guid, []).append(
                    Sample(t, m.location.x, m.location.y, m.location.z, m.yaw,
                           (v.x * v.x + v.y * v.y + v.z * v.z) ** 0.5))
            return {**m.as_dict(), "clock": clock} if heli else m.as_dict()
        value = keep_prop(t, actor, g, obj, prop, b)
        if prop in IDS:
            value = None  # an online id: in the sidecar's bits only
        if prop not in WANTED:
            return value
        leaf = g.leaf
        try:
            if leaf == "SQPlayerState":
                p = players.setdefault(actor.guid, Player(actor.guid))
                if prop == "PlayerNamePrivate":
                    p.name = b.fstring().strip()
                elif prop == "TeamState":
                    p.teams.append((t, b.packed()))
                elif prop == "SquadState":
                    p.squads.append((t, b.packed()))
                elif prop == "CurrentPawn":
                    p.pawns.append((t, b.packed()))
            elif leaf == "SQTeamState":
                team = teams.setdefault(actor.guid, Team())
                if prop in NUMBER_NAMES and team.number is None:
                    team.number = b.i32()
                elif prop == "FactionSetupId":
                    team.faction = b.fname()
            elif leaf == "SQSquadState":
                sq = squads.setdefault(actor.guid, SquadUnit())
                if prop == "TeamId":
                    sq.team = b.i32()
                elif prop in NUMBER_NAMES:
                    sq.number = b.i32()
            elif prop == "PlayerState" and obj == actor.guid:
                soldier_player.setdefault(actor.guid, []).append((t, b.packed()))
            elif prop in ("Owner", "AttachParent") and obj == actor.guid:
                parent = b.packed()
                if parent and parent != actor.guid:
                    owner[actor.guid] = parent
        except ReadError:
            errors[0] += 1
        return value

    def on_rpc(t: float, actor: Actor, g: Group, obj: int, function: str, params: dict) -> None:
        shot = shot_of(t, actor.guid, function, params)
        if shot is not None:
            shots.append(shot)

    s = Stream(replay, buf, wanted=None, on_property=on_property, on_rpc=on_rpc, keep=keeper,
               decode_value=lambda n, b: decode_param(n, b, s))
    stats = s.run()
    for track in tracks.values():  # read in stream order, except the blocks of objects named after the stream
        track.sort(key=lambda x: x.t)
    for per in props.values():
        for changes in per.values():
            changes.sort(key=lambda x: x[0])
    # A seat pawn's owner may itself be attached to the vehicle: follow the chain to something that moves.
    for pawn in list(owner):
        seen = {pawn}
        target = owner[pawn]
        while target not in tracks and target in owner and target not in seen:
            seen.add(target)
            target = owner[target]
        owner[pawn] = target
    return Match(name, replay, stats, players, teams, squads, s.actors, tracks, owner, soldier_player, errors[0],
                 props, census, keeper, s, shots)
