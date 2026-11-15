---
title: Pirms sākat
nav_order: 1.5
lang: lv
source: before-you-start.md
source_hash: "ca4b6281fdfc"
nav_exclude: true
search_exclude: true
---
# Pirms sākat {#before-you-start}

Vai nekad neesi strādājis ar komandrindu? Šī lapa palīdzēs tev no nulles nonākt līdz pirmajai palaišanai.
Tas aizņem apmēram desmit minūtes, vienu reizi.

## 1. Instalē Python {#install-python}

Šim rīkam vajag **Python 3.10 vai jaunāku versiju**.

- **Windows:** lejupielādē Python no [python.org/downloads](https://www.python.org/downloads/)
  un palaid instalētāju. Pirmajā ekrānā atzīmē **Add python.exe to PATH**,
  tad noklikšķini **Install Now**.
- **macOS un Linux:** Python 3 bieži jau ir uzstādīts. Kur šajās lapās rakstīts
  `python`, raksti `python3`.

## 2. Iegūsti šo rīku {#get-this-tool}

Atver [github.com/Holdi601/3DHeat-Ext-Squad](https://github.com/Holdi601/3DHeat-Ext-Squad), noklikšķini
zaļo pogu **Code**, tad **Download ZIP**, un izpako to mapē, kuru izvēlies. Ja izmanto git:
`git clone https://github.com/Holdi601/3DHeat-Ext-Squad`.

## 3. Atver termināli šajā mapē {#open-a-terminal-in-that-folder}

Terminālis ir logs, kurā raksti komandas.

- **Windows:** atver mapi Explorer, noklikšķini adreses joslā, ieraksti
  `powershell` un nospied Enter. Atveras zils vai melns logs, kas jau ir šajā mapē.
- **macOS:** atver **Terminal**, ieraksti `cd ` (ar atstarpi), ievelc mapi logā
  un nospied Enter.

`cd` nozīmē "mainīt mapi": `cd C:\Tools\3DHeat-Ext-Squad` ieiet šajā mapē.

## 4. Uzstādi rīku {#install-the-tool}

Ieraksti šo un nospied Enter:

```bash
python -m pip install -e .
```

Beigās tev vajadzētu redzēt: `Successfully installed heat3d-ext-squad-demo-...`.

## 5. Palaid to {#run-it}

```bash
heat3d-squad-demo --version
```

Tev vajadzētu redzēt kaut ko līdzīgu:

```text
heat3d-squad-demo 0.1.0
```

Tālāk: [Demo ierakstīšana](recording.md), pēc tam [Demo konvertēšana](converting.md).

## Kā lasīt komandas šajās lapās {#how-to-read-the-commands-on-these-pages}

| Tu redzi | Tas nozīmē |
|---|---|
| `<folder>` | vietturis: ieraksti savu vērtību, bez `< >` |
| `[--force]` | izvēles daļa: vari to izlaist vai ierakstīt, kā parādīts |
| `a\|b` | izvēle: ieraksti `a` vai `b` |
| `# a note` | komentārs tev: nekas nav jāraksta |
| `"C:\My Files\x"` | ceļu ar atstarpēm ieliec pēdiņās |
| `D:\Demos` | Windows mapes piemērs: izmanto savu |

## Ja kaut kas noiet greizi {#when-something-goes-wrong}

| Ziņojums | Ko darīt |
|---|---|
| `'python' is not recognized` | Python nav uzstādīts vai PATH rūtiņa nebija atzīmēta: uzstādi to vēlreiz un atzīmē (vai raksti `py` `python` vietā). |
| `'heat3d-squad-demo' is not recognized` | Atkārto 4. soli rīka mapē vai raksti `python -m heat3d_ext_squad` `heat3d-squad-demo` vietā: rezultāts ir tāds pats. |
| `No module named heat3d_ext_squad` | Tu neesi rīka mapē vai 4. solis neizdevās: ieej tajā ar `cd` un izpildi 4. soli. |
| `No module named pip` | Palaid `python -m ensurepip`, tad 4. soli. |
| jebkas cits | Izlasi ziņojuma pēdējo rindu un atver problēmu (issue) GitHub ar to. |

Katra komanda beidzas arī ar **izejas statusu**: 0 nozīmē, ka viss izdevās. Lai to redzētu,
PowerShell ieraksti `echo $LASTEXITCODE`, bet macOS un Linux `echo $?`.
