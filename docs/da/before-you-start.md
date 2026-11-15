---
title: Før du går i gang
nav_order: 1.5
lang: "da"
source: before-you-start.md
source_hash: "ca4b6281fdfc"
nav_exclude: true
search_exclude: true
---
# Før du går i gang {#before-you-start}

Ny til kommandolinjen? Denne side fører dig fra ingenting til en første kørsel.
Det tager cirka ti minutter, én gang.

## 1. Installer Python {#install-python}

Dette værktøj kræver **Python 3.10 eller nyere**.

- **Windows:** hent Python fra [python.org/downloads](https://www.python.org/downloads/)
  og kør installationsprogrammet. På dets første skærm sætter du flueben i **Add python.exe to PATH**,
  og klikker derefter på **Install Now**.
- **macOS og Linux:** Python 3 er ofte allerede installeret. Hvor siderne siger
  `python`, skriver du `python3`.

## 2. Hent dette værktøj {#get-this-tool}

Åbn [github.com/Holdi601/3DHeat-Ext-Squad](https://github.com/Holdi601/3DHeat-Ext-Squad), klik på den
grønne knap **Code**, derefter **Download ZIP**, og pak den ud i en mappe efter eget valg. Bruger du git:
`git clone https://github.com/Holdi601/3DHeat-Ext-Squad`.

## 3. Åbn en terminal i den mappe {#open-a-terminal-in-that-folder}

En terminal er et vindue, hvor du skriver kommandoer.

- **Windows:** åbn mappen i Stifinder, klik i adresselinjen, skriv
  `powershell` og tryk Enter. Et blåt eller sort vindue åbner, allerede i
  mappen.
- **macOS:** åbn **Terminal**, skriv `cd ` (med et mellemrum), træk mappen ind i
  vinduet og tryk Enter.

`cd` betyder "skift mappe": `cd C:\Tools\3DHeat-Ext-Squad` går til den mappe.

## 4. Installer værktøjet {#install-the-tool}

Skriv dette og tryk Enter:

```bash
python -m pip install -e .
```

Til sidst bør du se: `Successfully installed heat3d-ext-squad-demo-...`.

## 5. Kør det {#run-it}

```bash
heat3d-squad-demo --version
```

Du bør se noget i retning af:

```text
heat3d-squad-demo 0.1.0
```

Næste: [Optag en demo](recording.md), og derefter [Konverter demoer](converting.md).

## Sådan læser du kommandoerne på disse sider {#how-to-read-the-commands-on-these-pages}

| Du ser | Det betyder |
|---|---|
| `<folder>` | en pladsholder: skriv i stedet din egen værdi, uden `< >` |
| `[--force]` | valgfrit: udelad det, eller skriv det som vist |
| `a\|b` | et valg: skriv `a` eller `b` |
| `# a note` | en kommentar til dig: skriv den ikke |
| `"C:\My Files\x"` | sæt en sti med mellemrum i anførselstegn |
| `D:\Demos` | en eksempelmappe i Windows: brug din egen |

## Når noget går galt {#when-something-goes-wrong}

| Meddelelsen | Hvad du gør |
|---|---|
| `'python' is not recognized` | Python er ikke installeret, eller feltet PATH blev ikke sat flueben i: installer det igen og sæt flueben (eller skriv `py` i stedet for `python`). |
| `'heat3d-squad-demo' is not recognized` | Kør trin 4 igen i værktøjets mappe, eller skriv `python -m heat3d_ext_squad` i stedet for `heat3d-squad-demo`: det gør det samme. |
| `No module named heat3d_ext_squad` | Du er ikke i værktøjets mappe, eller trin 4 mislykkedes: `cd` derhen og kør trin 4. |
| `No module named pip` | Kør `python -m ensurepip`, og derefter trin 4. |
| alt andet | Læs den sidste linje i meddelelsen, og åbn en issue på GitHub med den. |

Hver kommando slutter også med en **exit-status**: 0 betyder, at den lykkedes. For at se den
skriver du `echo $LASTEXITCODE` i PowerShell eller `echo $?` på macOS og Linux.
