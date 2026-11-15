---
title: The match document and sidecars
nav_order: 5
---

# The match document and sidecars

Beside the table, each demo gets `<demo>.match.json` and two sidecars,
`<demo>.entities.parquet` and `<demo>.packets.parquet`. The viewer reads the
match document in its Match tab.

## The match document

`<demo>.match.json` (the match document) holds at its top level `map`, `layer`, `level_path`, `game_version`, `engine_version`, `recorded_unix`, `duration_s`, `teams`, `squads`, `game_state`, `actors`, `players`, `rows`, `events`, `not_read`, `file`, `header`, `chunks`, `stream`, `shots` and `selfCheck` (the full list: [Command reference](cli-reference.md)). In words: the map and layer, the game and engine versions, the recording time, the length, and:

- **the teams**: number, faction and everything their state replicated (tickets, availabilities, commander) as it changed;
- **the squads**: number, team, name, creator, leader, members;
- **the game state**: server name and settings, game mode, match state and id, map and layer rotations, votes, timers, the message of the day;
- **the actors**: every vehicle, deployable, emplacement, ammo crate and helicopter - class, where and when it spawned, when it went, whose, and its replicated state (health, build state, seats...);
- **a line for each player**: samples on foot and in vehicles, distance walked, soldier classes played, vehicles used, team changes, seats taken, and everything the player state replicated (ping, level, role, current seat...); and a line for each bot;
- **the events** counted, the **property census** (how often each class's properties were sent) and the **remote call census**, the shots and hits, what was **not** read, and the reader's diagnostics;
- **the file and the header**: every field of the info block and the demo header, the chunk table, the net field export tables (`net_field_exports`), the channels' close reasons, and the classes found for objects the exports do not name (`stream.class_resolution`);
- **the self-check** (`selfCheck.completeness`, see [Completeness](#completeness)).

Online ids (Steam, EOS) are left out on purpose.

A quick look at a converted demo:

```bash
python -c "import json; d = json.load(open('out/<map>/<demo>.match.json')); print(d['map'], d['layer'], d['duration_s'], len(d['players']))"
```

## Completeness

This reader follows the rule all 3DHeat converters share: decode what can be read now, keep the rest whole, and say how much of each kind it did ([Converters keep everything](https://github.com/Holdi601/3DHeat/blob/main/docs/converters.md)). Each match document has `selfCheck.completeness`: per type of item met in the demo, how many were `seen`, `decoded`, `partial` (decoded in part and kept whole), `raw` (kept whole only) and `lost` (must be 0). The types are counted where the reader meets them: `file.info`, `chunk.<kind>`, `frame`, `packet`, `bunch`, `open`, `close`, `export.field`, `export.guid`, `external`, `property:<class>`, `rpc:<class>`, `block:<object>`, `subobject.*`.

On the real demos read, `lost` is 0: their items run from hundreds of thousands to millions; about half decode fully, the rest are partial or raw.

**Read** (into the table and the match document):

- the info block, the demo header (every field; two trailing bytes not known are kept as hex), the chunk table;
- every frame, packet and bunch (split whole into what they carry), every actor opened (with its spawn location, rotation, scale and velocity) and closed (with why: `Destroyed`, `Dormancy`...);
- every replicated property, as far as its bits say ([Decoding properties](how-it-works.md#decoding-properties)), positions from `FRepMovement` and from the helicopters' movement component, the casualties, vehicles' health, seats;
- every remote call by name, with its parameters where the demo exports the function's group: shots (`fire`) and vehicle hits (`hit`) into the table;
- the net field export tables and the net GUIDs (their count; the paths are in the entities sidecar).

**Kept raw** (whole, with what is read of it beside it):

- `<demo>.entities.parquet`, columns `time`, `type` (`<class>.<property>`, `<class>.<call>`, or the object's name), `name` (the actor's class), `entity` (the actor's net GUID, as the table's `entity`), `kind`, `object` (the subobject), `channel`, `handle`, `group` (the class path of the export group), `decoded` (JSON), `bits` and `payload` (the bits, lowest first, padded to whole bytes):
  - every property update (`kind` `property`), the movement included, with what is decoded; raw only where nothing is (unnamed handles, structures such as `RotationReplicatedMovement` of turrets, and properties left as bits);
  - every remote call and custom-delta field (`rpc`), the parameters decoded where the function's group was exported; raw where not (`RepInventory`, `PlayerStateData`);
  - every content block of an object whose class could not be found (`block`: `Buoyancy`, `GameplayTasksComponent`, `AmmoRackComponent`...), with its header decoded;
  - every actor channel opened and closed (`open`, `close`), every subobject deleted or destroyed;
  - the context a later decoder needs to read the file alone: every net field export (`export.field`: group path, handle, property name, checksum) and every exported net GUID (`export.guid`: its path, outer and flags), at the time the stream gave them.
- `<demo>.packets.parquet`, columns `time`, `type`, `name`, `channel`, `offset` (in the file), `decoded`, `bits`, `payload`: the info block, the header chunk, every checkpoint chunk (a checkpoint is the state of every actor at its time, which the stream from the start holds too), every event chunk, and every frame, packet or bunch that does not read (one bunch per demo: the recorder's own spectator's opening bunch), whole.

The entities rows are grouped by `kind`, `type` and `entity`, each in time order; sort by `time` for the stream's order.

**Not available:**

- what a server demo does not record: clients' inputs, what a player saw;
- client-side effects: hit markers, sounds, the kill feed's text (the server sends the calls, not their display);
- online IDs decoded: kept as bits only (see [Personal data](limits.md#personal-data)).
