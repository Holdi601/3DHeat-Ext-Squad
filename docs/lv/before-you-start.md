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

Vai nekad neesat strādājis ar komandrindu? Šī lapa palīdzēs jums no nulles nonākt līdz pirmajai palaišanai.
Tas aizņem apmēram desmit minūtes, vienu reizi.

## 1. Uzstādiet Python {#install-python}

Šim rīkam vajag **Python 3.10 vai jaunāku versiju**.

- **Windows:** lejupielādējiet Python no [python.org/downloads](https://www.python.org/downloads/)
  un palaidiet instalētāju. Pirmajā ekrānā atzīmējiet **Add python.exe to PATH**,
  tad noklikšķiniet **Install Now**.
- **macOS un Linux:** Python 3 bieži jau ir uzstādīts. Kur šajās lapās rakstīts
  `python`, rakstiet `python3`.

## 2. Iegūstiet šo rīku {#get-this-tool}

Atveriet [github.com/Holdi601/3DHeat-Ext-Squad](https://github.com/Holdi601/3DHeat-Ext-Squad), noklikšķiniet
zaļo pogu **Code**, tad **Download ZIP**, un izpakojiet to mapē, kuru izvēlaties. Ja izmantojat git:
`git clone https://github.com/Holdi601/3DHeat-Ext-Squad`.

## 3. Atveriet termināli šajā mapē {#open-a-terminal-in-that-folder}

Termināls ir logs, kurā rakstāt komandas.

- **Windows:** atveriet mapi Explorer, noklikšķiniet adreses joslā, ierakstiet
  `powershell` un nospiediet Enter. Atveras zils vai melns logs, kas jau ir šajā mapē.
- **macOS:** atveriet **Terminal**, ierakstiet `cd ` (ar atstarpi), ievelciet mapi logā
  un nospiediet Enter.

`cd` nozīmē "mainīt mapi": `cd C:\Tools\3DHeat-Ext-Squad` ieiet šajā mapē.

## 4. Uzstādiet rīku {#install-the-tool}

Ierakstiet šo un nospiediet Enter:

```bash
python -m pip install -e .
```

Beigās jums vajadzētu redzēt: `Successfully installed heat3d-ext-squad-demo-...`.

## 5. Palaidiet to {#run-it}

```bash
heat3d-squad-demo --version
```

Jums vajadzētu redzēt kaut ko līdzīgu:

```text
heat3d-squad-demo 0.1.0
```

Tālāk: [Demo ierakstīšana](recording.md), pēc tam [Demo konvertēšana](converting.md).

## Kā lasīt komandas šajās lapās {#how-to-read-the-commands-on-these-pages}

| Jūs redzat | Tas nozīmē |
|---|---|
| `<folder>` | vietturis: ierakstiet savu vērtību, bez `< >` |
| `[--force]` | izvēles daļa: varat to izlaist vai ierakstīt, kā parādīts |
| `a\|b` | izvēle: ierakstiet `a` vai `b` |
| `# a note` | komentārs jums: nekas nav jāraksta |
| `"C:\My Files\x"` | ceļu ar atstarpēm ieliekiet pēdiņās |
| `D:\Demos` | Windows mapes piemērs: izmantojiet savu |

## Ja kaut kas noiet greizi {#when-something-goes-wrong}

| Ziņojums | Ko darīt |
|---|---|
| `'python' is not recognized` | Python nav uzstādīts vai PATH rūtiņa nebija atzīmēta: uzstādiet to vēlreiz un atzīmējiet (vai rakstiet `py` `python` vietā). |
| `'heat3d-squad-demo' is not recognized` | Atkārtojiet 4. soli rīka mapē vai rakstiet `python -m heat3d_ext_squad` `heat3d-squad-demo` vietā: rezultāts ir tāds pats. |
| `No module named heat3d_ext_squad` | Jūs neesat rīka mapē vai 4. solis neizdevās: ieejiet tajā ar `cd` un izpildiet 4. soli. |
| `No module named pip` | Palaidiet `python -m ensurepip`, tad 4. soli. |
| jebkas cits | Izlasiet ziņojuma pēdējo rindu un atveriet problēmu (issue) GitHub ar to. |

Katra komanda beidzas arī ar **izejas statusu**: 0 nozīmē, ka viss izdevās. Lai to redzētu,
PowerShell ierakstiet `echo $LASTEXITCODE`, bet macOS un Linux `echo $?`.
