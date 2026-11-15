---
title: "Demók átalakítása"
nav_order: 3
lang: hu
source: converting.md
source_hash: "e8c77423085b"
nav_exclude: true
search_exclude: true
---
# Demók átalakítása {#converting-demos}

```text
heat3d-squad-demo <demos or folders> -o <folder> [--flat] [--json]
python -m heat3d_ext_squad ...          ugyanaz, telepítés nélkül
```

## Lépésről lépésre {#step-by-step}

Még nem használt parancssort? Előbb olvassa el a [Mielőtt elkezdi](before-you-start.md) oldalt.

1. Telepítés egyszer: `git clone https://github.com/Holdi601/3DHeat-Ext-Squad`,
   nyisson terminált ebben a mappában, és futtassa a `python -m pip install -e .`
   parancsot (Python 3.10 vagy újabb; ez hozza a pyarrow-t és a numpy-t).
2. Tegye a `.replay` fájlokat egy mappába, vagy nevezze meg őket egyenként.
3. Futtassa a `heat3d-squad-demo <folder> -o out` parancsot.
4. Demónként egy sort kell látnia: a rétegét, a játékosok és sorok számát, és hogy hova
   került a táblázat. Minden demóból négy laza fájl lesz az `out/<map>/` mappában (nem
   `.3dheat` tároló); a `.parquet` fájlt töltse be a 3DHeat megjelenítőben.

![Futtatás egy szintetikus demón](../assets/img/run.svg)

A kép egy olyan demón mutatja a futtatást, amelyet a tesztek építenek (`tests/test_stream.py`),
nem valódi meccsen.

## Kapcsolók {#options}

| Kapcsoló | Alapérték | Mit csinál |
|---|---|---|
| `demos` (egy vagy több) | - | `.replay` fájlok, vagy ezeket tartalmazó mappák |
| `-o`, `--out` | kötelező | a mappa, ahová írni kell; minden demó a `<out>/<map>/` mappába kerül |
| `--flat` | ki | közvetlenül a mappába ír, a `<map>/` mappa nélkül |
| `--json` | ki | demónként egy JSON-sort ír a szabványos kimenetre (a parancsot hívó programoknak): `demo`, `ok`, `parquet`, `match`, `sidecars`, `lost`, `rows`, `players`, `layer`, `recorded_unix`; a sikertelen demó `demo`, `ok: false` és `error` mezőt ír |
| `--version` | - | kiírja a verziót, majd leáll |

Minden kapcsoló úgy, ahogy a program kiírja: [Parancsleírás](../cli-reference.md).

A map-mappa a térkép neve, amelyet a demó által megnevezett pályaútvonalból vesz
(a `/Game/Maps/<Map>/Gameplay_Layers/<Layer>` útvonalból a `<Map>` lesz).

Kilépési állapot: 0, ha minden demó átalakult; 1, ha bármelyik nem sikerült (a többi
attól még megíródik), vagy ha nem találtunk `.replay` fájlt.

## Mi jön ki {#what-comes-out}

| Fájl | Mit tartalmaz |
|---|---|
| `<demo>.parquet` | a táblázat: pozíciók és események, soronként egy ([A táblázat](output-table.md)) |
| `<demo>.match.json` | a meccs dokumentuma ([A meccs dokumentuma](output-match.md)) |
| `<demo>.entities.parquet` | kísérőfájl: minden tulajdonságfrissítés és távoli hívás, teljes egészében |
| `<demo>.packets.parquet` | kísérőfájl: a fájl darabjai és minden, ami nem olvasódott be, teljes egészében |

A táblázat és a meccs dokumentuma ugyanaz a pár, amelyet a 3DHeat CS2 eszköz ír. A
megjelenítő közvetlenül megnyitja a táblázatot, és egy egész mappa betöltésekor kihagyja
a kísérőfájlokat.

## Példák {#examples}

```bash
heat3d-squad-demo D:\SquadDemos -o out                 # minden demó egy mappában
heat3d-squad-demo one.replay two.replay -o out --flat  # közvetlenül az out/ mappába
heat3d-squad-demo D:\SquadDemos -o out --json          # demónként egy JSON-sor
```

A `D:\SquadDemos` példa mappa a D: meghajtón; használja a sajátját.
