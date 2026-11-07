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
"""

from __future__ import annotations

import bisect
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .bits import BitReader, ReadError
from .container import ReplayFile, read
from .movement import rep_movement
from .stream import Actor, Group, Stats, Stream

#: The engine's hardcoded FName that SQTeamState and SQSquadState use for their number.
NUMBER_NAMES = ("#name253", "ID", "Id", "TeamId")

WANTED = {
    "ReplicatedMovement",
    "PlayerNamePrivate", "TeamState", "SquadState", "CurrentPawn", "Soldier", "PlayerState",
    "FactionSetupId", "TeamId", "#name253", "Owner", "AttachParent", "SquadName", "ServerName",
}


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
                                    self.kind(target), self.kind(pawn)))
        # Soldiers nobody was found to control (bots without a player state,
        # a recording that missed the link): kept, under their own name.
        for guid, track in self.tracks.items():
            if guid in covered or not is_soldier(self.kind(guid)):
                continue
            who = self._soldier_owner_name(guid) or f"soldier {guid}"
            p = next((pl for pl in self.players.values() if pl.name == who), None)
            t0 = track[0].t
            team = self.team_of(p, t0) if p else None
            squad = self.squad_of(p, t0) if p else None
            for s in track:
                out.append(_row(s, who, team, squad, "position", self.kind(guid), self.kind(guid)))
        out.sort(key=lambda r: (r["time"], r["player"]))
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


def _row(s: Sample, who: str, team: Team | None, squad: SquadUnit | None, event: str, what: str, seat: str):
    return {
        "time": s.t, "x": s.x, "y": s.y, "z": s.z, "yaw": s.yaw, "speed": s.speed,
        "player": who, "team": team.number if team and team.number is not None else -1,
        "faction": team.faction if team else "", "squad": squad.number if squad and squad.number is not None else -1,
        "event": event, "pawn": what, "seat": seat if seat != what else "",
    }


def class_name(path: str) -> str:
    """`/Game/Blueprints/Soldiers/ABC/BP_Soldier_ABC_Rifleman.Default__BP_Soldier_ABC_Rifleman_C` -> `BP_Soldier_ABC_Rifleman`."""
    leaf = path.rsplit(".", 1)[-1]
    if leaf.startswith("Default__"):
        leaf = leaf[len("Default__"):]
    return leaf[:-2] if leaf.endswith("_C") else leaf


def is_soldier(kind: str) -> bool:
    return kind.startswith("BP_Soldier")


def _leaf(g: Group) -> str:
    return g.path.rsplit(".", 1)[-1].rsplit("/", 1)[-1]


def load(path: str | Path) -> Match:
    buf = Path(path).read_bytes()
    return parse(buf, Path(path).stem)


def parse(buf: bytes, name: str = "replay") -> Match:
    replay = read(buf)
    eng = replay.header.engine_network_version if replay.header else 0
    players: dict[int, Player] = {}
    teams: dict[int, Team] = {}
    squads: dict[int, SquadUnit] = {}
    tracks: dict[int, list[Sample]] = {}
    owner: dict[int, int] = {}
    soldier_player: dict[int, list[tuple[float, int]]] = {}
    errors = [0]

    def on_property(t: float, actor: Actor | None, g: Group, obj: int, prop: str, b: BitReader) -> None:
        if actor is None:
            return
        leaf = _leaf(g)
        try:
            if prop == "ReplicatedMovement":
                if obj != actor.guid:
                    return  # a component's movement, not the actor's
                try:
                    m = rep_movement(b, eng)
                except ReadError:
                    errors[0] += 1
                    return
                v = m.velocity
                tracks.setdefault(actor.guid, []).append(
                    Sample(t, m.location.x, m.location.y, m.location.z, m.yaw,
                           (v.x * v.x + v.y * v.y + v.z * v.z) ** 0.5))
            elif leaf == "SQPlayerState":
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

    s = Stream(replay, buf, wanted=WANTED, on_property=on_property)
    stats = s.run()
    # A seat pawn's owner may itself be attached to the vehicle: follow the chain to something that moves.
    for pawn in list(owner):
        seen = {pawn}
        target = owner[pawn]
        while target not in tracks and target in owner and target not in seen:
            seen.add(target)
            target = owner[target]
        owner[pawn] = target
    return Match(name, replay, stats, players, teams, squads, s.actors, tracks, owner, soldier_player, errors[0])
