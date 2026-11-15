---
title: Konvertera demos
nav_order: 3
lang: sv
source: converting.md
source_hash: "e8c77423085b"
nav_exclude: true
search_exclude: true
---
# Konvertera demos {#converting-demos}

```text
heat3d-squad-demo <demos or folders> -o <folder> [--flat] [--json]
python -m heat3d_ext_squad ...          samma sak, utan att installera
```

## Steg för steg {#step-by-step}

Har du aldrig använt kommandoraden förut? Läs [Innan du börjar](before-you-start.md) först.

1. Installera en gång: `git clone https://github.com/Holdi601/3DHeat-Ext-Squad`,
   öppna en terminal i mappen, kör `python -m pip install -e .`
   (Python 3.10 eller senare; det tar med sig pyarrow och numpy).
2. Lägg filerna `.replay` i en mapp, eller ange dem en och en.
3. Kör `heat3d-squad-demo <folder> -o out`.
4. Du ser en rad per demo: dess lager, spelare och rader, och var tabellen hamnade.
   Varje demo blir fyra lösa filer i `out/<map>/` (inte en `.3dheat`-behållare); läs in `.parquet` i 3DHeat-visaren.

![En körning på en syntetisk demo](../assets/img/run.svg)

Bilden visar en körning på en demo som testerna skapar (`tests/test_stream.py`),
inte en riktig match.

## Alternativ {#options}

| Alternativ | Standard | Gör |
|---|---|---|
| `demos` (en eller flera) | - | `.replay`-filer, eller mappar som innehåller dem |
| `-o`, `--out` | krävs | mappen att skriva i; varje demo hamnar i `<out>/<map>/` |
| `--flat` | av | skriv direkt i mappen, utan mappen `<map>/` |
| `--json` | av | skriv ut en JSON-rad per demo på standard ut (för program som anropar kommandot): `demo`, `ok`, `parquet`, `match`, `sidecars`, `lost`, `rows`, `players`, `layer`, `recorded_unix`; en demo som misslyckades skriver `demo`, `ok: false` och `error` i stället |
| `--version` | - | skriv ut versionen och stanna |

Alla alternativ, så som programmet skriver ut dem: [Kommandoreferens](../cli-reference.md).

Mappen för kartan är kartans namn, hämtat från nivåsökvägen som demon anger (`/Game/Maps/<Map>/Gameplay_Layers/<Layer>` ger `<Map>`).

Avslutskod: 0 när varje demo konverterades; 1 när någon misslyckades (de andra skrivs ändå) eller när ingen `.replay`-fil hittades.

## Vad som kommer ut {#what-comes-out}

| Fil | Vad den innehåller |
|---|---|
| `<demo>.parquet` | tabellen: positioner och händelser, en rad var ([Tabellen](output-table.md)) |
| `<demo>.match.json` | matchdokumentet ([Matchdokumentet](output-match.md)) |
| `<demo>.entities.parquet` | sidofil: varje egenskapsuppdatering och fjärranrop, helt |
| `<demo>.packets.parquet` | sidofil: filens delar och allt som inte gick att läsa, helt |

Tabellen och matchdokumentet är samma par som 3DHeat CS2-verktyget skriver. Visaren öppnar tabellen direkt
och hoppar över sidofilerna när en hel mapp läses in.

## Exempel {#examples}

```bash
heat3d-squad-demo D:\SquadDemos -o out                 # alla demos i en mapp
heat3d-squad-demo one.replay two.replay -o out --flat  # direkt i out/
heat3d-squad-demo D:\SquadDemos -o out --json          # en JSON-rad per demo
```

`D:\SquadDemos` är en exempelmapp på enheten D: använd din egen.
