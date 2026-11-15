---
title: "Înainte de a începe"
nav_order: 1.5
lang: ro
source: before-you-start.md
source_hash: "ca4b6281fdfc"
nav_exclude: true
search_exclude: true
---
# Înainte de a începe {#before-you-start}

Nu ați mai lucrat în linia de comandă? Această pagină vă duce de la zero până la prima rulare.
Durează vreo zece minute, o singură dată.

## 1. Instalați Python {#install-python}

Acest instrument are nevoie de **Python 3.10 sau mai nou**.

- **Windows:** descărcați Python de la [python.org/downloads](https://www.python.org/downloads/)
  și rulați programul de instalare. Pe primul ecran bifați **Add python.exe to PATH**,
  apoi apăsați **Install Now**.
- **macOS și Linux:** Python 3 este de obicei deja instalat. Acolo unde aceste pagini spun
  `python`, scrieți `python3`.

## 2. Obțineți acest instrument {#get-this-tool}

Deschideți [github.com/Holdi601/3DHeat-Ext-Squad](https://github.com/Holdi601/3DHeat-Ext-Squad), apăsați
butonul verde **Code**, apoi **Download ZIP**, și dezarhivați-l într-un dosar
la alegere. Dacă folosiți git: `git clone https://github.com/Holdi601/3DHeat-Ext-Squad`.

## 3. Deschideți un terminal în acel dosar {#open-a-terminal-in-that-folder}

Un terminal este o fereastră în care scrieți comenzi.

- **Windows:** deschideți dosarul în Explorer, faceți clic în bara de adrese, scrieți
  `powershell` și apăsați Enter. Se deschide o fereastră albastră sau neagră,
  deja în acel dosar.
- **macOS:** deschideți **Terminal**, scrieți `cd ` (cu un spațiu), trageți dosarul în
  fereastră și apăsați Enter.

`cd` înseamnă „schimbă dosarul”: `cd C:\Tools\3DHeat-Ext-Squad` duce în acel dosar.

## 4. Instalați instrumentul {#install-the-tool}

Scrieți aceasta și apăsați Enter:

```bash
python -m pip install -e .
```

La final ar trebui să vedeți: `Successfully installed heat3d-ext-squad-demo-...`.

## 5. Rulați-l {#run-it}

```bash
heat3d-squad-demo --version
```

Ar trebui să vedeți ceva de genul:

```text
heat3d-squad-demo 0.1.0
```

Mai departe: [Înregistrarea unei demo](recording.md), apoi [Convertirea demo-urilor](converting.md).

## Cum se citesc comenzile din aceste pagini {#how-to-read-the-commands-on-these-pages}

| Ce vedeți | Ce înseamnă |
|---|---|
| `<folder>` | un loc rezervat: scrieți propria valoare în locul lui, fără `< >` |
| `[--force]` | opțional: lăsați-l pe dinafară sau scrieți-l exact așa |
| `a\|b` | o alegere: scrieți `a` sau `b` |
| `# a note` | un comentariu pentru dumneavoastră: nu îl scrieți |
| `"C:\My Files\x"` | puneți între ghilimele un drum care are spații |
| `D:\Demos` | un exemplu de dosar Windows: folosiți-l pe al dumneavoastră |

## Când apare o problemă {#when-something-goes-wrong}

| Mesajul | Ce să faceți |
|---|---|
| `'python' is not recognized` | Python nu este instalat, sau nu s-a bifat PATH: instalați-l din nou și bifați-l (sau scrieți `py` în loc de `python`). |
| `'heat3d-squad-demo' is not recognized` | Rulați din nou pasul 4 în dosarul instrumentului, sau scrieți `python -m heat3d_ext_squad` în loc de `heat3d-squad-demo`: face același lucru. |
| `No module named heat3d_ext_squad` | Nu sunteți în dosarul instrumentului, sau pasul 4 a eșuat: mergeți acolo cu `cd` și rulați pasul 4. |
| `No module named pip` | Rulați `python -m ensurepip`, apoi pasul 4. |
| orice altceva | Citiți ultimul rând al mesajului, apoi deschideți un issue pe GitHub cu el. |

Fiecare comandă se încheie și cu un **cod de stare**: 0 înseamnă că a mers. Ca să-l vedeți,
scrieți `echo $LASTEXITCODE` în PowerShell sau `echo $?` pe macOS și Linux.
