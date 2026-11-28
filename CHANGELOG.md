# Changelog

## 0.4.0

- `plugin.json`: the manifest 3DHeat's Games page reads to know what this tool does, which games it is
  for and how to call it. The release archive carries it and the tool's icon (`icon-64.png`) beside the
  program.
- The shared app (3DHeat extractor kit) with new-content detection: `status --json` reports content
  entries and the install's new items beside the maps, and `check-new [--json] [--auto-extract]` is the
  unattended check that skips the game while it runs or updates and extracts only what is new (never
  replaces files).
- Outputs made before the extract record (`.heat3d-extract.json`) existed are no longer all called
  outdated: when every output is newer than the game files it was made from it counts as current
  (`"untracked": true` in `status --json`), otherwise outdated.
- Matches converted by 0.3.0 stay current (`currentFrom` in `plugin.json`): this release does not
  change the converted output, so 3DHeat does not convert them again.

## 0.3.0

- Its own icon: the 3DHeat cube with a text badge for its game (letters in 3DHeat's colours), as the
  program, window, taskbar and docs icon.
- A new window: the 3DHeat look in dark and light (follows the system, switchable), the logo and
  icon, sharp at any display scaling. Four steps: find the game (each requirement with its fix),
  choose (maps ticked when there is something to do, filters, search; jobs with their fields
  inline), work (progress, time left, cancel), done (open in 3DHeat, open the output folder, and
  for a failure what went wrong and what to do, copy details, report a problem).
- No console window on Windows: the program is a window program. From a terminal it still prints
  as before; `heat3d-squad-cli.cmd` beside it waits for it in a terminal and passes its exit code.
- The update offer in the same look: Update now / Later / Skip this version, and "Update
  automatically" from the dialog.
- CI draws every page and dialog of the window (on Linux under a virtual display) and checks the
  Windows build is a window program.
- `heat3d-squad convert <replay>... -o <out> [--progress-json]` and `heat3d-squad info <replay> --json` (what the
  replay says about its match, read from its header without converting it), the same verbs in every
  3DHeat replay reader; the old command lines work as before.

## 0.2.0

- A standalone program for Windows and Linux (no Python needed), built by CI with a `SHA256SUMS` file. Without
  arguments it opens a window: a Squad server found through Steam and its demo folder (or one you choose), the
  demo conversion into the viewer's matches folder, and updates. `--check --json` and `status --json` for
  scripts; demos hold matches, not maps, so `extract` has nothing to extract.
- Updates ask first (update now / later / skip this version) unless automatic updates were chosen
  (`--auto-update`, the window's checkbox, or `HEAT3D_AUTO_UPDATE=1`).

## 0.1.0

- Squad server demos (`.replay`) into a heatmap table and a match document.
- Everything a demo holds: bots, health, wounds, revives, deaths, vehicles,
  deployables, seats, shots and vehicle hits.
- Nothing lost: a completeness self-check and two raw sidecars.
- `--flat`, `--json`, `--version`.
- Installs with one pip line from the release zip, no Git needed; a pip install knows its version and updates itself with pip when a newer release is out.
- README: a quick start for new users.

## Docs

Where each feature is documented
([holdi601.github.io/3DHeat-Ext-Squad](https://holdi601.github.io/3DHeat-Ext-Squad/)):

| Feature | Page |
|---|---|
| Installing, a first run | [Before you start](docs/before-you-start.md) |
| Recording a demo on the server | [Recording a demo](docs/recording.md) |
| The command and its options (`-o`, `--flat`, `--json`, `--version`) | [Converting demos](docs/converting.md), [Command reference](docs/cli-reference.md) |
| The table: columns and events | [The table](docs/output-table.md) |
| The match document, the sidecars, the self-check | [The match document and sidecars](docs/output-match.md) |
| How a demo is read, and how it was checked | [How a demo is read](docs/how-it-works.md) |
| What is not read, game updates, personal data, licence | [Limits, updates and terms](docs/limits.md) |
| Release checklist for the docs | [Maintaining these docs](docs/maintaining.md) |
