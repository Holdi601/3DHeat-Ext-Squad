# 3DHeat Squad demo reader

Reads Squad server demos and turns them into 3DHeat heatmap tables. The output covers every player's and every bot's position over the match, on foot and in ground vehicles, with their name, team, faction, squad, health and view pitch; wounds, revives and deaths; every vehicle, deployable and emplacement spawned, damaged, destroyed and removed; and, in the match document, every other property the server replicated.

```bash
pip install -e .                       # installs the heat3d-squad-demo command
heat3d-squad-demo match.replay -o out  # or a folder of .replay files
```

Each demo becomes `out/<map>/<demo>.parquet` and `out/<map>/<demo>.match.json`. This is the same pair the 3DHeat CS2 tool writes, and the 3DHeat viewer opens the table directly. Use `--flat` to leave out the map folder, and `--json` to print one line of JSON per demo for programs that call the command.

The command works on its own. The 3DHeat Watcher runs it on new demos when it is installed (adapter `squad-demos`). The Watcher never imports this package, so a problem here touches nothing else.

## Recording a demo

Squad demos are recorded on the server, not by the game client:

1. In `Admins.cfg`, give the admin's group the `demos` permission.
2. In the game's console, run `AdminDemoRec <name>`, play the match, then run `AdminDemoStop`. An admin has to type these in the game itself; one report says RCON does not accept them.
3. The demo is written to `<server>/SquadGame/Saved/Demos/<name>.replay`. Copy it off the server.

`Server.cfg` also has a `RecordDemos` setting, off by default. Expect roughly 70–80 MB per hour for a small match; the size for a full 100-player server has not been measured.

## What is read

| Column | What it is |
|---|---|
| `time` | seconds since the recording started |
| `x`, `y`, `z` | position in Unreal units (centimetres), Z up |
| `dirX`, `dirY`, `dirZ` | where a soldier looks: the body's yaw and the view's pitch, as a unit vector (a vehicle's: level) |
| `yaw`, `pitch` | the same in degrees; `pitch` up from the horizon, soldiers only |
| `health` | the soldier's, bot's or vehicle's health at that moment, where the server sent it (a soldier's falls below 0 while wounded) |
| `speed` | the replicated speed, cm/s |
| `player` | the player's name; `bot <id>` for a bot; for a vehicle or deployable nobody owns, its class |
| `team`, `faction` | Squad's team number (1, 2) and its faction setup, **at that moment**: players can change sides |
| `squad` | the squad number, -1 when not in one |
| `event` | `position` on foot, `vehicle` while in a ground vehicle (the row then has the vehicle's position); `wounded`, `revived`, `death` (soldiers and bots); `spawn`, `damaged`, `destroyed`, `removed` (vehicles, deployables, emplacements, crates, helicopters: where they were); `seat` (a player took a seat) |
| `pawn` | the soldier blueprint (`SQSquidBot` for a bot), or the vehicle |
| `seat` | for a turret or passenger seat, the seat's own pawn |
| `match` | the demo's name |

The Parquet footer carries reading instructions under the `heat3d` key: Z up, no axis mirrored, unit scale 1. The match JSON holds the map and layer, the game and engine versions, the recording time, the length, and:

- **the teams**: number, faction and everything their state replicated (tickets, availabilities, commander) as it changed;
- **the squads**: number, team, name, creator, leader, members;
- **the game state**: server name and settings, game mode, match state and id, map and layer rotations, votes, timers, the message of the day;
- **the actors**: every vehicle, deployable, emplacement, ammo crate and helicopter - class, where and when it spawned, when it went, whose, and its replicated state (health, build state, seats...);
- **a line for each player**: samples on foot and in vehicles, distance walked, soldier classes played, vehicles used, team changes, seats taken, and everything the player state replicated (ping, level, role, current seat...); and a line for each bot;
- **the events** counted, the **property census** (how often each class's properties were sent), what was **not** read, and the reader's diagnostics.

Online ids (Steam, EOS) are left out on purpose.

Every replicated property is decoded as far as its bits say what it is: one bit a flag, a length and that many bytes a string, a name, 8/16/32/64 bits a number (a float where the property's name says so: health, time, rate...), anything else its bits in hex with the strings found inside.

A sample is taken whenever the server replicated the actor's movement, up to 8 times a second (the demo's recording rate) while the actor moves.

**How the events are read.** A soldier's `Health` and `bWounded` come from the server: wounded when `bWounded` turns on, revived when it turns off with health above 0, dead when the health drops below -100 (a player who gives up or bleeds out is set to -300); a bot, never wounded, dies at 0. A vehicle or deployable is `damaged` at each fall of its `Health`, `destroyed` at 0 or below. Spawns and removals are the actor channel opening and closing; a seat is the player state's `CurrentSeat`. The view pitch is the soldier's `RemoteViewPitch`, a byte from straight down (0) to straight up (255).

**Not read:**

- **Helicopter movement.** Helicopters replicate it through Squad's own movement component, in a different quantization (their health is read).
- **Who killed whom, and damage to soldiers by hit.** These travel as remote calls or in components the demo names no fields for (the `unresolved_content_blocks` in the diagnostics); only the victims' health is replicated.
- **The bot's team.** A bot's state carries a number that may be its team; not confirmed, not used.
- **Where a soldier looks sideways** beyond the body's yaw.

## How it works

An Unreal network replay is the server's own replication traffic, written down by its demo driver. Reading one is reading that traffic as a client would.

| Module | Layer |
|---|---|
| `container.py` | The local file streamer's file: an info block (magic `0x1CA2E27F`), then chunks. Chunk types are the header (`FNetworkDemoHeader`, magic `0x2CF5A13D`), replay data, checkpoints and events. |
| `bits.py` | Byte archives for frames and bit archives for packets. Packets are read lowest bit first. |
| `stream.py` | Frames, packets, bunches (partial bunches joined), actor channels, actor spawns and content blocks. Each block holds replicated properties as handle, bit count and bits. |
| `movement.py` | The engine's `FRepMovement`. |
| `squad.py` | Which Squad classes carry what. `SQPlayerState` holds the name, team state, squad state and current pawn; `SQTeamState` the team number and faction; `SQSquadState` the squad number. A seat pawn's owner is its vehicle. |
| `output.py`, `cli.py` | The table and the match document. |

A replay names its own fields. It carries the class paths and property names for every handle, and the paths of the objects it references. So every property can be found by name without the game's code. Only the bits of a property need its type. For movement that is the engine's own type; for Squad's properties the types are simple: strings, integers, object references and names.

## What was verified, and how

These were checked against two public Squad v10.3.1 server demos (Unreal Engine 5.5.4, engine network version 36), from the squad-replay project's test fixtures:

- **Counts.** The counts of frames, packets, actor opens, export groups and exported object paths match that project's independent parser exactly. So does the number of soldier movement samples.
- **Movement against velocity.** Each soldier sample's step from the previous one, divided by the time between them, matches the velocity the sample carries. The median ratio is within 0.8 to 1.2 on moving players.
- **Teams against blueprints.** Every row's team is the team whose faction the soldier's blueprint belongs to. This held for a player who changed sides during the match.
- **Errors.** One stream error per demo remains: a stray bit at the end of the opening bunch of the recorder's own spectator actor, which carries nothing used here.
- **Casualties against that project's kills.** On the Fallujah demo it counts 11 kills, the first at 75.399 s (the victim incapacitated), the last at 1,527.853 s; read here: 6 wounds and 5 deaths of players, the first wound of the same player at 75.399 s, the last wound of that kill's victim at 1,527.853 s. On the Jensen's Range demo its last kill, at 553.392 s, is when the M60T read here is destroyed (health -104).
- **Deployables.** 51 actors with a build state or an FOB requirement on Jensen's Range, against that project's 52 deployables.
- **Pitch.** The view pitch byte lies around 120 at rest and spans 34 to 255 over both demos: -66 to +90 degrees read as a byte over -90..+90. Read as the engine's usual byte of a whole turn it would put soldiers up to 128 degrees under the horizon, which they cannot look.
- **Bots.** The Fallujah seeding demo has 622 bots (`SQSquidBot`), each with its own track; 388 of them die.

Tests on demos built by the tests themselves cover the container, the archives, the stream and the whole path to the table:

```bash
pip install -e .[test]
pytest                                   # synthetic demos
HEAT3D_SQUAD_DEMOS=<folder> pytest       # plus real demos in that folder
```

## Game updates

The reader depends on the engine's replay format and a handful of Squad class and property names. It does not depend on property layouts it cannot see: the replay names those itself.

**What can break with a Squad update:**

- **An engine upgrade.** Squad moved to UE 5.7 with v10.4, and this is untested there. The upgrade can change the bunch header, the spawn data or `FRepMovement`. These are version-gated in the code where the step is known. Unknown steps (`ENG_PARTIAL_CUSTOM_EXPORTS`, the trailing movement bit) are pinned to what v10.3.1 does.
- **Iris replication.** If Squad switched to Iris, the stream inside the chunks would be new and this reader would not read it. Squad v10.3.1 uses the classic system (it runs ReplicationGraph).
- **Renamed classes or properties.** If Squad renamed its player, team or squad classes or their properties, names or teams would go missing, but positions would not.
- **What happens on failure.** When the format changes, the reader fails loudly with stream errors or movement errors in the diagnostics. It does not quietly produce wrong positions: `FRepMovement` is only accepted when its bits add up exactly.

## Personal data

A demo holds the names and online IDs of everyone on the server. The table and match document carry names, not IDs. Treat both like the demo itself.

## Licence and sources

MIT; see [`LICENSE`](LICENSE). Everything here was written for this package. No third-party code is included or linked: the only dependencies are pyarrow (Apache-2.0) and numpy (BSD-3-Clause).

Facts about the format came from these sources:

- **Unreal.Core** in [FortniteReplayDecompressor](https://github.com/Shiqan/FortniteReplayDecompressor) (MIT). It describes the generic Unreal replay layout: the info block, chunks, frames, bunches and net field exports.
- **[squad-replay](https://github.com/Codycody31/squad-replay)** (MPL-2.0). Its parser was read for the layout as Squad v10.3.1 writes it, for the version checks, and for which Squad classes carry roster data. Its published test demos and snapshot counts were used as an independent cross-check. None of its code was copied or translated: this reader is structured differently (a Python bit archive over whole packets, partial bunches joined bitwise, properties dispatched by name), and two things it does not do were found here on the demos themselves: the third partial-bunch flag and the trailing movement bit.

Squad is a trademark of Offworld Industries. This package reads files a Squad server writes; it does not touch the game, its code or its archives. Offworld's server licensing and administration policy says nothing on recording or analysing demos. Squad's EULA forbids reverse engineering the game itself, which this does not do.
