---
title: Command reference
nav_order: 90
---

# Command reference

Generated from the code by `tools/gen_docs_reference.py`: do not edit by hand.
The other pages explain each step.

## `heat3d-squad-demo`

```text
usage: heat3d-squad-demo [-h] -o OUT [--flat] [--json] [--version] demos [demos ...]

Squad server demos (.replay) into 3DHeat heatmap tables: every player's position, team
and squad.

positional arguments:
  demos          .replay files, or folders holding them

options:
  -h, --help     show this help message and exit
  -o, --out OUT  folder for <map>/<name>.parquet and .match.json
  --flat         write straight into the folder, without <map>/
  --json         one line of JSON per demo on stdout
  --version      show program's version number and exit
```

## Output columns

### The table: `<demo>.parquet`

| Column | Type |
|---|---|
| `time` | double |
| `x` | float |
| `y` | float |
| `z` | float |
| `dirX` | float |
| `dirY` | float |
| `dirZ` | float |
| `yaw` | float |
| `pitch` | float |
| `speed` | float |
| `health` | float |
| `team` | int16 |
| `squad` | int16 |
| `entity` | int64 |
| `player` | string |
| `faction` | string |
| `event` | string |
| `pawn` | string |
| `seat` | string |
| `detail` | string |
| `match` | string |

### Sidecar: `<demo>.entities.parquet`

| Column | Type |
|---|---|
| `time` | double |
| `type` | string |
| `name` | string |
| `entity` | int64 |
| `kind` | string |
| `object` | int64 |
| `channel` | int32 |
| `handle` | int32 |
| `group` | string |
| `decoded` | string |
| `bits` | int32 |
| `payload` | binary |

### Sidecar: `<demo>.packets.parquet`

| Column | Type |
|---|---|
| `time` | double |
| `type` | string |
| `name` | string |
| `channel` | int32 |
| `offset` | int64 |
| `decoded` | string |
| `bits` | int64 |
| `payload` | binary |

### The match document: `<demo>.match.json`

Top-level keys: `tool`, `tool_version`, `match`, `game`, `map`, `layer`, `level_path`, `game_version`, `engine_version`, `engine_network_version`, `recording_name`, `recorded_unix`, `duration_s`, `teams`, `squads`, `game_state`, `actors`, `players`, `rows`, `events`, `units`, `not_read`, `file`, `header`, `chunks`, `stream`, `shots`, `remote_call_census`, `net_field_exports`, `property_census`, `diagnostics`, `selfCheck`.
