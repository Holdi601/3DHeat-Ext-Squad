---
title: The table
nav_order: 4
---

# The table: `<demo>.parquet`

One row per sample or event. A sample is taken whenever the server replicated
the actor's movement, up to 8 times a second (the demo's recording rate)
while it moves.

![The first rows of a synthetic demo's table](assets/img/table.svg)

## Columns

| Column | What it is |
|---|---|
| `time` | seconds since the recording started |
| `x`, `y`, `z` | position in Unreal units (centimetres), Z up |
| `dirX`, `dirY`, `dirZ` | where a soldier looks: the body's yaw and the view's pitch, as a unit vector (a vehicle's: level) |
| `yaw`, `pitch` | the same in degrees; `pitch` up from the horizon, soldiers only |
| `health` | the soldier's, bot's or vehicle's health at that moment, where the server sent it (a soldier's falls below 0 while wounded) |
| `speed` | the replicated speed, cm/s |
| `player` | the player's name; `bot <id>` for a bot; for a vehicle or deployable nobody owns, its class; for a shot from a vehicle's weapon, the player seated on that vehicle |
| `team`, `faction` | Squad's team number (1, 2) and its faction setup, **at that moment**: players can change sides |
| `squad` | the squad number, -1 when not in one |
| `event` | what the row is (below) |
| `pawn` | the soldier blueprint (`SQSquidBot` for a bot), the vehicle, or for `fire` the weapon |
| `seat` | for a turret or passenger seat, the seat's own pawn |
| `detail` | for `fire` the weapon's call that placed the shot, for `hit` the damage type, for `removed` why the channel closed (`Destroyed`, `Dormancy`...) |
| `entity` | the actor the row is about (its net GUID): the `entity` of the sidecars' rows |
| `match` | the demo's name |

## Events

| `event` | On the row of | What |
|---|---|---|
| `position` | a soldier or bot on foot | a movement sample |
| `vehicle` | a soldier in a ground vehicle or helicopter | a sample at the vehicle's position |
| `wounded`, `revived`, `death` | soldiers and bots | where it happened |
| `spawn`, `damaged`, `destroyed`, `removed` | vehicles, deployables, emplacements, crates, helicopters | where they were |
| `seat` | a player | took a seat |
| `fire` | the shooter | a shot: where it left, its direction as `yaw`/`pitch`/`dirX..Z` |
| `hit` | the vehicle | a vehicle hit: where |

How the events are read is in [How a demo is read](how-it-works.md#how-the-events-are-read).

## In the viewer

The Parquet footer carries reading instructions under the `heat3d` key: Z up,
no axis mirrored, unit scale 1, so the viewer needs no column mapping. Load
the table in the Heatmap tab; see the viewer's
[Getting data in](https://holdi601.github.io/3DHeat/getting-data-in.html)
and [Column mapping](https://holdi601.github.io/3DHeat/column-mapping.html).
