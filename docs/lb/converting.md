---
title: "Demoe konvertéieren"
nav_order: 3
lang: lb
source: converting.md
source_hash: "e8c77423085b"
nav_exclude: true
search_exclude: true
---
# Demoe konvertéieren {#converting-demos}

```text
heat3d-squad-demo <demos or folders> -o <folder> [--flat] [--json]
python -m heat3d_ext_squad ...          the same, without installing
```

## Schrëtt fir Schrëtt {#step-by-step}

Nei op der Kommandozeil? Liest fir d'éischt [Ier Dir ufänkt](before-you-start.md).

1. Eemol installéieren: `git clone https://github.com/Holdi601/3DHeat-Ext-Squad`,
   e Terminal an deem Dossier opmaachen, `python -m pip install -e .` ausféieren
   (Python 3.10 oder méi nei; et bréngt pyarrow an numpy mat).
2. D'`.replay`-Dateien an en Dossier leeën, oder se eenzel nennen.
3. `heat3d-squad-demo <folder> -o out` ausféieren.
4. Dir sollt eng Zeil pro Demo gesinn: säi Layer, d'Spiller a Rei, a wou d'Tabell
   higaangen ass. All Demo gëtt véier eenzel Dateien an `out/<map>/` (kee
   `.3dheat`-Container); lued de `.parquet` am 3DHeat-Viewer.

![Een Duerchlaf op enger syntheteschen Demo](../assets/img/run.svg)

D'Bild weist en Duerchlaf op enger Demo, déi d'Tester bauen (`tests/test_stream.py`),
net e richtege Match.

## Optiounen {#options}

| Optioun | Standard | Mécht |
|---|---|---|
| `demos` (eng oder méi) | - | `.replay`-Dateien, oder Dossieren, déi se halen |
| `-o`, `--out` | erfuerderlech | den Dossier, an deen geschriwwe gëtt; all Demo geet an `<out>/<map>/` |
| `--flat` | aus | direkt an den Dossier schreiwen, ouni den `<map>/`-Dossier |
| `--json` | aus | eng Zeil JSON pro Demo op stdout ausginn (fir Programmer, déi de Kommando opruffen): `demo`, `ok`, `parquet`, `match`, `sidecars`, `lost`, `rows`, `players`, `layer`, `recorded_unix`; eng Demo, déi feelgeschloen ass, gëtt amplaz `demo`, `ok: false` an `error` aus |
| `--version` | - | d'Versioun ausginn an ophalen |

All Optioun, esou wéi de Programm se ausgëtt: [Kommando-Referenz](../cli-reference.md).

Den Map-Dossier ass den Numm vun der Map, geholl aus dem Level-Wee, deen d'Demo nennt
(`/Game/Maps/<Map>/Gameplay_Layers/<Layer>` gëtt `<Map>`).

Exit-Status: 0, wann all Demo konvertéiert gouf; 1, wann eng feelgeschloen ass (déi aner
ginn trotzdem geschriwwen) oder wann keng `.replay`-Datei fonnt gouf.

## Wat erauskënnt {#what-comes-out}

| Datei | Wat se hält |
|---|---|
| `<demo>.parquet` | d'Tabell: Positiounen an Evenementer, eng Zeil pro Stéck ([D'Tabell](output-table.md)) |
| `<demo>.match.json` | d'Match-Dokument ([D'Match-Dokument](output-match.md)) |
| `<demo>.entities.parquet` | Niewendatei: all Property-Update an all Remote-Call, komplett |
| `<demo>.packets.parquet` | Niewendatei: d'Chunks vun der Datei an alles, wat sech net liese gelooss huet, komplett |

D'Tabell an d'Match-Dokument si datselwecht Paar, dat och den 3DHeat-CS2-Tool schreift.
De Viewer mécht d'Tabell direkt op a léisst d'Niewendateien aus, wann en ganzen
Dossier gelueden gëtt.

## Beispiller {#examples}

```bash
heat3d-squad-demo D:\SquadDemos -o out                 # every demo in a folder
heat3d-squad-demo one.replay two.replay -o out --flat  # straight into out/
heat3d-squad-demo D:\SquadDemos -o out --json          # one JSON line per demo
```

`D:\SquadDemos` ass e Beispill-Dossier op der Plack D: benotzt Äre ganzen.
