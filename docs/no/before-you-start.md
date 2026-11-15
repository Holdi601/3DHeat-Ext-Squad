---
title: Før du starter
nav_order: 1.5
lang: "no"
source: before-you-start.md
source_hash: "ca4b6281fdfc"
nav_exclude: true
search_exclude: true
---
# Før du starter {#before-you-start}

Ny til kommandolinjen? Denne siden tar deg fra null til en første kjøring.
Det tar omtrent ti minutter, én gang.

## 1. Installer Python {#install-python}

Dette verktøyet krever **Python 3.10 eller nyere**.

- **Windows:** last ned Python fra [python.org/downloads](https://www.python.org/downloads/)
  og kjør installasjonen. På første skjerm, kryss av for **Add python.exe to PATH**,
  og klikk deretter på **Install Now**.
- **macOS og Linux:** Python 3 er ofte allerede installert. Der disse sidene skriver
  `python`, skriv `python3`.

## 2. Skaff dette verktøyet {#get-this-tool}

Åpne [github.com/Holdi601/3DHeat-Ext-Squad](https://github.com/Holdi601/3DHeat-Ext-Squad), klikk på den
grønne knappen **Code**, deretter **Download ZIP**, og pakk den ut i en mappe etter eget valg. Bruker du git:
`git clone https://github.com/Holdi601/3DHeat-Ext-Squad`.

## 3. Åpne en terminal i den mappen {#open-a-terminal-in-that-folder}

En terminal er et vindu der du skriver kommandoer.

- **Windows:** åpne mappen i Filutforsker, klikk i adressefeltet, skriv
  `powershell` og trykk Enter. Et blått eller svart vindu åpnes, allerede i
  den mappen.
- **macOS:** åpne **Terminal**, skriv `cd ` (med et mellomrom), dra mappen inn i
  vinduet og trykk Enter.

`cd` betyr «bytt mappe»: `cd C:\Tools\3DHeat-Ext-Squad` går til den mappen.

## 4. Installer verktøyet {#install-the-tool}

Skriv dette og trykk Enter:

```bash
python -m pip install -e .
```

Til slutt bør du se: `Successfully installed heat3d-ext-squad-demo-...`.

## 5. Kjør det {#run-it}

```bash
heat3d-squad-demo --version
```

Du bør se noe slikt:

```text
heat3d-squad-demo 0.1.0
```

Neste: [Ta opp en demo](recording.md), deretter [Konverter demoer](converting.md).

## Slik leser du kommandoene på disse sidene {#how-to-read-the-commands-on-these-pages}

| Du ser | Betyr |
|---|---|
| `<folder>` | en plassholder: skriv inn din egen verdi i stedet, uten `< >` |
| `[--force]` | valgfritt: utelat det, eller skriv det slik det vises |
| `a\|b` | et valg: skriv `a` eller `b` |
| `# a note` | en kommentar til deg: ikke skriv den |
| `"C:\My Files\x"` | sett en sti som har mellomrom i anførselstegn |
| `D:\Demos` | et eksempel på en Windows-mappe: bruk din egen |

## Når noe går galt {#when-something-goes-wrong}

| Meldingen | Hva du gjør |
|---|---|
| `'python' is not recognized` | Python er ikke installert, eller boksen for PATH var ikke avkrysset: installer på nytt og kryss av der (eller skriv `py` i stedet for `python`). |
| `'heat3d-squad-demo' is not recognized` | Kjør steg 4 på nytt i verktøyets mappe, eller skriv `python -m heat3d_ext_squad` i stedet for `heat3d-squad-demo`: det gjør det samme. |
| `No module named heat3d_ext_squad` | Du er ikke i verktøyets mappe, eller steg 4 mislyktes: `cd` dit og kjør steg 4. |
| `No module named pip` | Kjør `python -m ensurepip`, deretter steg 4. |
| alt annet | Les siste linje i meldingen, og åpne en sak på GitHub med den. |

Hver kommando avsluttes også med en **avslutningsstatus**: 0 betyr at den virket. For å se den,
skriv `echo $LASTEXITCODE` i PowerShell, eller `echo $?` på macOS og Linux.
