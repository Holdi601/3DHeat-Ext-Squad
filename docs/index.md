---
title: Home
nav_order: 1
---

# 3DHeat Squad

**What is it?** A small program that turns a recording of a Squad match into
files the [3DHeat](https://github.com/Holdi601/3DHeat) viewer
([documentation](https://holdi601.github.io/3DHeat/)) can draw: where every
player was, second by second, and what happened where.

**Why would I use it?** To see a match from above: where the fighting was,
which routes squads took, where vehicles died.

**Example:** `match.replay` (a demo, recorded on a Squad server) ->
`match.parquet` (one row per position or event) + `match.match.json` (the
match document: teams, squads, players). The outputs are ordinary Parquet
and JSON files, so anything else can read them too.

What it is useful for:

- **Where a match was fought.** Every player's and bot's position, on foot, in
  ground vehicles and in helicopters, about eight times a second, with team,
  faction, squad, health and view pitch.
- **What happened where.** Wounds, revives and deaths; every shot and every
  hit on a vehicle; every vehicle, deployable and emplacement spawned,
  damaged, destroyed and removed.
- **The whole match in one document.** Teams, squads, the game state, every
  actor, a line per player and per bot, and a self-check that nothing the
  demo holds was lost.

![From a Squad server to the viewer](assets/img/flow.svg)

## Quick start

You need Windows, Python 3.10 or later ("Add python.exe to PATH" ticked in its
installer) and Squad demos (`.replay` files), recorded on a Squad server, not
by the game: an admin runs `AdminDemoRec <name>` and `AdminDemoStop`, and the
server writes `<server>\SquadGame\Saved\Demos\<name>.replay` (70 to 80 MB an
hour for a small match; [Recording a demo](recording.md)). Copy them to your
PC; no Git is needed. New to the command line? Read [Before you start](before-you-start.md) first.

```bash
python -m pip install https://github.com/Holdi601/3DHeat-Ext-Squad/archive/refs/tags/v0.1.0.zip
heat3d-squad-demo match.replay -o out       # one demo
heat3d-squad-demo D:\SquadDemos -o out      # every demo in a folder (use your own)
```

You should see one line per demo:
`match.replay: <layer>, <n> players, <n> rows -> out\<map>\match.parquet`. Each
demo becomes four files in `out\<map>\` (`--flat` puts them straight into
`out`): `<demo>.parquet` (the table to open), `<demo>.match.json` and two
sidecars ([Converting demos](converting.md)).

Then open the `.parquet` in the [3DHeat viewer](https://github.com/Holdi601/3DHeat#quick-start):
download it (**Code -> Download ZIP**, unpack), double-click `start.bat` (it
offers to install Node.js when it is missing and opens `http://127.0.0.1:5273`),
then **Source -> Files...**, pick the file (or drop it on the Source panel)
and click **Load file**
([Getting data in](https://holdi601.github.io/3DHeat/getting-data-in.html)).

When a new release is out, the tool says so when it starts and offers to
update itself (`python -m heat3d_ext_squad.update` does the same).

## Pages

| Page | What it covers |
|---|---|
| [Before you start](before-you-start.md) | Python, a terminal, a first run |
| [Recording a demo](recording.md) | making a server write a demo, and finding it |
| [Converting demos](converting.md) | the command, every option, example output |
| [The table](output-table.md) | every column and every `event` |
| [The match document and sidecars](output-match.md) | the `.match.json`, the two sidecars, the self-check |
| [How a demo is read](how-it-works.md) | the layers of the reader, and what was verified |
| [Limits, updates and terms](limits.md) | what is not read, what a Squad update can break, personal data, licence |
| [Command reference](cli-reference.md) | every option and column, generated from the code |
| [Maintaining these docs](maintaining.md) | the release checklist |

## Related

- The 3DHeat viewer: [github.com/Holdi601/3DHeat](https://github.com/Holdi601/3DHeat),
  documentation at [holdi601.github.io/3DHeat](https://holdi601.github.io/3DHeat/).
- The file formats the viewer reads, including the one-file-a-match
  container: [One file a match (.3dheat)](https://holdi601.github.io/3DHeat/container.html).
  This converter writes the loose files: the table, the match document and
  its sidecars side by side.
- The 3DHeat Watcher runs this converter on new demos when it is installed
  (adapter `squad-demos`): [3DHeat Watcher](https://holdi601.github.io/3DHeat-Watcher/).
- Each game reader is its own small project with its own licence file, releases
  and issue tracker, so it can be installed, updated, maintained - or withdrawn
  on a rights holder's request - on its own, without affecting the viewer or
  the other tools.

## The 3DHeat tools

| Tool | What it does | Code | Docs |
|---|---|---|---|
| 3DHeat viewer | shows the data: heatmaps, race analysis, match review | [3DHeat](https://github.com/Holdi601/3DHeat) | [docs](https://holdi601.github.io/3DHeat/) |
| GameFiles | levels and courses from a game's own files | [3DHeat-GameFiles](https://github.com/Holdi601/3DHeat-GameFiles) | [docs](https://holdi601.github.io/3DHeat-GameFiles/) |
| GameCapture | lap telemetry, and levels rebuilt from gameplay video | [3DHeat-GameCapture](https://github.com/Holdi601/3DHeat-GameCapture) | [docs](https://holdi601.github.io/3DHeat-GameCapture/) |
| Unreal Exporter | an Unreal Editor plugin: a level as one `.glb` | [3DHeat-UnrealExporter](https://github.com/Holdi601/3DHeat-UnrealExporter) | [docs](https://holdi601.github.io/3DHeat-UnrealExporter/) |
| CS2 | Counter-Strike 2 demos and maps | [3DHeat-CS2](https://github.com/Holdi601/3DHeat-CS2) | [docs](https://holdi601.github.io/3DHeat-CS2/) |
| Watcher | records what games publish while you play | [3DHeat-Watcher](https://github.com/Holdi601/3DHeat-Watcher) | [docs](https://holdi601.github.io/3DHeat-Watcher/) |
| Ext-WarThunder | War Thunder replays | [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder) | [docs](https://holdi601.github.io/3DHeat-Ext-WarThunder/) |
| Ext-WoT | World of Tanks replays | [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT) | [docs](https://holdi601.github.io/3DHeat-Ext-WoT/) |
| Ext-WoWs | World of Warships replays | [3DHeat-Ext-WoWs](https://github.com/Holdi601/3DHeat-Ext-WoWs) | [docs](https://holdi601.github.io/3DHeat-Ext-WoWs/) |
| Ext-Squad | Squad server demos | [3DHeat-Ext-Squad](https://github.com/Holdi601/3DHeat-Ext-Squad) | [docs](https://holdi601.github.io/3DHeat-Ext-Squad/) |
| Ext-DCS | DCS World maps as 3D levels | [3DHeat-Ext-DCS](https://github.com/Holdi601/3DHeat-Ext-DCS) | [docs](https://holdi601.github.io/3DHeat-Ext-DCS/) |
| Ext-IL2 | IL-2 Sturmovik maps as 3D levels | [3DHeat-Ext-IL2](https://github.com/Holdi601/3DHeat-Ext-IL2) | [docs](https://holdi601.github.io/3DHeat-Ext-IL2/) |
| Ext-Dota | the Dota 2 map from your own install as a 3D level | [3DHeat-Ext-Dota](https://github.com/Holdi601/3DHeat-Ext-Dota) | [docs](https://holdi601.github.io/3DHeat-Ext-Dota/) |
| Ext-DotaReplay | Dota 2 replays | [3DHeat-Ext-DotaReplay](https://github.com/Holdi601/3DHeat-Ext-DotaReplay) | [docs](https://holdi601.github.io/3DHeat-Ext-DotaReplay/) |
| Ext-Riot | League of Legends and VALORANT replays (what they carry unencrypted) | [3DHeat-Ext-Riot](https://github.com/Holdi601/3DHeat-Ext-Riot) | [docs](https://holdi601.github.io/3DHeat-Ext-Riot/) |
| Ext-Forza | Forza courses, races and cars from your own install | [3DHeat-Ext-Forza](https://github.com/Holdi601/3DHeat-Ext-Forza) | [docs](https://holdi601.github.io/3DHeat-Ext-Forza/) |
| Ext-Battlefield | Battlefield levels (Frostbite) as 3D levels | [3DHeat-Ext-Battlefield](https://github.com/Holdi601/3DHeat-Ext-Battlefield) | [docs](https://holdi601.github.io/3DHeat-Ext-Battlefield/) |
| Ext-BeamNG | BeamNG.drive courses | [3DHeat-Ext-BeamNG](https://github.com/Holdi601/3DHeat-Ext-BeamNG) | [docs](https://holdi601.github.io/3DHeat-Ext-BeamNG/) |
| Ext-ACRally | Assetto Corsa Rally stages as courses | [3DHeat-Ext-ACRally](https://github.com/Holdi601/3DHeat-Ext-ACRally) | [docs](https://holdi601.github.io/3DHeat-Ext-ACRally/) |
| Ext-Reforger | Arma Reforger worlds (Enfusion) as 3D levels | [3DHeat-Ext-Reforger](https://github.com/Holdi601/3DHeat-Ext-Reforger) | [docs](https://holdi601.github.io/3DHeat-Ext-Reforger/) |
| Ext-R6 | Rainbow Six Siege match replays | [3DHeat-Ext-R6](https://github.com/Holdi601/3DHeat-Ext-R6) | [docs](https://holdi601.github.io/3DHeat-Ext-R6/) |
