---
title: Voordat je begint
nav_order: 1.5
lang: "nl"
source: before-you-start.md
source_hash: "ca4b6281fdfc"
nav_exclude: true
search_exclude: true
---
# Voordat je begint {#before-you-start}

Nog nooit met de opdrachtregel gewerkt? Deze pagina brengt je van niets tot een eerste keer draaien.
Het duurt ongeveer tien minuten, één keer.

## 1. Installeer Python {#install-python}

Deze tool heeft **Python 3.10 of later** nodig.

- **Windows:** download Python via [python.org/downloads](https://www.python.org/downloads/)
  en start het installatieprogramma. Vink op het eerste scherm **Add python.exe to PATH** aan,
  en klik dan op **Install Now**.
- **macOS en Linux:** Python 3 staat vaak al op de computer. Waar deze pagina's
  `python` schrijven, typ je `python3`.

## 2. Haal deze tool op {#get-this-tool}

Open [github.com/Holdi601/3DHeat-Ext-Squad](https://github.com/Holdi601/3DHeat-Ext-Squad), klik op de groene knop
**Code**, dan op **Download ZIP**, en pak het uit in een map naar keuze. Gebruik je git: `git clone https://github.com/Holdi601/3DHeat-Ext-Squad`.

## 3. Open een terminal in die map {#open-a-terminal-in-that-folder}

Een terminal is een venster waarin je opdrachten typt.

- **Windows:** open de map in Verkenner, klik in de adresbalk, typ
  `powershell` en druk op Enter. Er opent een blauw of zwart venster, al in die map.
- **macOS:** open **Terminal**, typ `cd ` (met een spatie), sleep de map in het
  venster en druk op Enter.

`cd` betekent "map wisselen": `cd C:\Tools\3DHeat-Ext-Squad` gaat naar die map.

## 4. Installeer de tool {#install-the-tool}

Typ dit en druk op Enter:

```bash
python -m pip install -e .
```

Aan het eind zie je: `Successfully installed heat3d-ext-squad-demo-...`.

## 5. Start hem {#run-it}

```bash
heat3d-squad-demo --version
```

Je ziet iets als:

```text
heat3d-squad-demo 0.1.0
```

Volgende: [Een demo opnemen](recording.md), dan [Demo's omzetten](converting.md).

## Zo lees je de opdrachten op deze pagina's {#how-to-read-the-commands-on-these-pages}

| Je ziet | Het betekent |
|---|---|
| `<folder>` | een plaatsaanduiding: typ in plaats daarvan je eigen waarde, zonder de `< >` |
| `[--force]` | optioneel: laat het weg, of typ het zoals getoond |
| `a\|b` | een keuze: typ `a` of `b` |
| `# a note` | een opmerking voor jou: niet typen |
| `"C:\My Files\x"` | zet een pad met spaties tussen aanhalingstekens |
| `D:\Demos` | een voorbeeldmap op Windows: gebruik je eigen |

## Als er iets misgaat {#when-something-goes-wrong}

| De melding | Wat je doet |
|---|---|
| `'python' is not recognized` | Python is niet geïnstalleerd, of het vakje PATH was niet aangevinkt: installeer het opnieuw en vink het aan (of typ `py` in plaats van `python`). |
| `'heat3d-squad-demo' is not recognized` | Voer stap 4 opnieuw uit in de map van de tool, of typ `python -m heat3d_ext_squad` in plaats van `heat3d-squad-demo`: dat doet hetzelfde. |
| `No module named heat3d_ext_squad` | Je bent niet in de map van de tool, of stap 4 is mislukt: ga met `cd` naar die map en voer stap 4 uit. |
| `No module named pip` | Voer `python -m ensurepip` uit, en daarna stap 4. |
| iets anders | Lees de laatste regel van de melding, en open dan een issue op GitHub met die regel. |

Elke opdracht eindigt ook met een **exitstatus**: 0 betekent dat het gelukt is. Om die te zien,
typ je `echo $LASTEXITCODE` in PowerShell, of `echo $?` op macOS en Linux.
