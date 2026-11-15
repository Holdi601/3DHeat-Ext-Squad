---
title: Demo's omzetten
nav_order: 3
lang: "nl"
source: converting.md
source_hash: "e8c77423085b"
nav_exclude: true
search_exclude: true
---
# Demo's omzetten {#converting-demos}

```text
heat3d-squad-demo <demos or folders> -o <folder> [--flat] [--json]
python -m heat3d_ext_squad ...          hetzelfde, zonder te installeren
```

## Stap voor stap {#step-by-step}

Nog nooit met de opdrachtregel gewerkt? Lees eerst [Voordat je begint](before-you-start.md).

1. Installeer eenmalig: `git clone https://github.com/Holdi601/3DHeat-Ext-Squad`,
   open een terminal in die map en voer `python -m pip install -e .` uit
   (Python 3.10 of later; het haalt pyarrow en numpy mee).
2. Zet de `.replay`-bestanden in een map, of noem ze één voor één.
3. Voer `heat3d-squad-demo <folder> -o out` uit.
4. Je ziet per demo één regel: de laag, de spelers en de rijen, en waar
   de tabel is opgeslagen. Elke demo wordt vier losse bestanden in `out/<map>/`
   (geen `.3dheat`-container); laad de `.parquet` in de 3DHeat-viewer.

![Een run op een synthetische demo](../assets/img/run.svg)

De afbeelding toont een run op een demo die de tests zelf maken (`tests/test_stream.py`),
niet op een echte wedstrijd.

## Opties {#options}

| Optie | Standaard | Doet |
|---|---|---|
| `demos` (een of meer) | - | `.replay`-bestanden, of mappen met die bestanden |
| `-o`, `--out` | verplicht | de map waarin je schrijft; elke demo gaat in `<out>/<map>/` |
| `--flat` | uit | schrijf rechtstreeks in de map, zonder de `<map>/`-map |
| `--json` | uit | print per demo één regel JSON op stdout (voor programma's die dit commando aanroepen): `demo`, `ok`, `parquet`, `match`, `sidecars`, `lost`, `rows`, `players`, `layer`, `recorded_unix`; een demo die mislukte print `demo`, `ok: false` en `error` in plaats daarvan |
| `--version` | - | print de versie en stop |

Elke optie, zoals het programma ze afdrukt: [Commandoreferentie](../cli-reference.md).

De naam van de kaartmap is de naam van de kaart uit het levelpad dat de demo noemt
(`/Game/Maps/<Map>/Gameplay_Layers/<Layer>` geeft `<Map>`).

Exitstatus: 0 als elke demo is omgezet; 1 als er één is mislukt (de andere worden wel
geschreven) of als er geen `.replay`-bestand is gevonden.

## Wat er uitkomt {#what-comes-out}

| Bestand | Wat het bevat |
|---|---|
| `<demo>.parquet` | de tabel: posities en gebeurtenissen, één rij per stuk ([De tabel](output-table.md)) |
| `<demo>.match.json` | het wedstrijddocument ([Het wedstrijddocument](output-match.md)) |
| `<demo>.entities.parquet` | bijbestand: elke eigenschapsupdate en elke remote call, volledig |
| `<demo>.packets.parquet` | bijbestand: de chunks van het bestand en alles wat niet gelezen kon worden, volledig |

De tabel en het wedstrijddocument zijn hetzelfde paar dat de 3DHeat CS2-tool schrijft.
De viewer opent de tabel rechtstreeks en laat de bijbestanden weg wanneer een hele map wordt geladen.

## Voorbeelden {#examples}

```bash
heat3d-squad-demo D:\SquadDemos -o out                 # elke demo in een map
heat3d-squad-demo one.replay two.replay -o out --flat  # rechtstreeks in out/
heat3d-squad-demo D:\SquadDemos -o out --json          # één JSON-regel per demo
```

`D:\SquadDemos` is een voorbeeldmap op station D: gebruik je eigen map.
