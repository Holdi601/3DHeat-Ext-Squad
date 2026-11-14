---
title: Converting demos
nav_order: 3
---

# Converting demos

```text
heat3d-squad-demo <demos or folders> -o <folder> [--flat] [--json]
python -m heat3d_ext_squad ...          the same, without installing
```

## Step by step

1. Install once, from a clone of this repository:
   `pip install -e .` (Python 3.10 or later; needs pyarrow and numpy).
2. Put the `.replay` files in a folder, or name them one by one.
3. Run `heat3d-squad-demo <folder> -o out`.
4. Each demo becomes four files in `out/<map>/`; load the `.parquet` in the
   3DHeat viewer.

![A run on a synthetic demo](assets/img/run.svg)

The picture shows a run on a demo the tests build (`tests/test_stream.py`),
not a real match.

## Options

| Option | Default | Does |
|---|---|---|
| `demos` (one or more) | - | `.replay` files, or folders holding them |
| `-o`, `--out` | required | the folder to write into; each demo goes into `<out>/<map>/` |
| `--flat` | off | write straight into the folder, without the `<map>/` folder |
| `--json` | off | print one line of JSON per demo on stdout (for programs that call the command): the files written, `ok`, `lost`, `rows`, `players`, `layer`, `recorded_unix` |
| `--version` | - | print the version and stop |

The map folder is the map's name taken from the level path the demo names
(`/Game/Maps/<Map>/Gameplay_Layers/<Layer>` gives `<Map>`).

Exit status: 0 when every demo was converted; 1 when any failed (the others
are still written) or when no `.replay` file was found.

## What comes out

| File | What it holds |
|---|---|
| `<demo>.parquet` | the table: positions and events, one row each ([The table](output-table.md)) |
| `<demo>.match.json` | the match document ([The match document](output-match.md)) |
| `<demo>.entities.parquet` | sidecar: every property update and remote call, whole |
| `<demo>.packets.parquet` | sidecar: the file's chunks and anything that did not read, whole |

The table and match document are the same pair the 3DHeat CS2 tool writes.
The viewer opens the table directly and leaves the sidecars out when a whole
folder is loaded.

## Examples

```bash
heat3d-squad-demo D:\SquadDemos -o out                 # every demo in a folder
heat3d-squad-demo one.replay two.replay -o out --flat  # straight into out/
heat3d-squad-demo D:\SquadDemos -o out --json          # one JSON line per demo
```
