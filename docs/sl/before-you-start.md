---
title: "Preden začneš"
nav_order: 1.5
lang: "sl"
source: before-you-start.md
source_hash: "ca4b6281fdfc"
nav_exclude: true
search_exclude: true
---
# Preden začneš {#before-you-start}

Še nisi vajen ukazne vrstice? Ta stran te vodi od nič do prvega zagona.
Traja približno deset minut, enkrat.

## 1. Namesti Python {#install-python}

To orodje potrebuje **Python 3.10 ali novejši**.

- **Windows:** prenesi Python na [python.org/downloads](https://www.python.org/downloads/)
  in zaženi namestitev. Na prvem zaslonu obkljukaj **Add python.exe to PATH**,
  nato klikni **Install Now**.
- **macOS in Linux:** Python 3 je pogosto že nameščen. Kjer te strani pišejo
  `python`, vtipkaj `python3`.

## 2. Pridobi to orodje {#get-this-tool}

Odpri [github.com/Holdi601/3DHeat-Ext-Squad](https://github.com/Holdi601/3DHeat-Ext-Squad),
klikni zeleni gumb **Code**, nato **Download ZIP**, in datoteko razpakiraj v mapo po
svoji izbiri. Če uporabljaš git: `git clone https://github.com/Holdi601/3DHeat-Ext-Squad`.

## 3. Odpri terminal v tej mapi {#open-a-terminal-in-that-folder}

Terminal je okno, v katerem vtipkaš ukaze.

- **Windows:** odpri mapo v Raziskovalcu, klikni v vrstico z naslovom, vtipkaj
  `powershell` in pritisni Enter. Odpre se okno (modro ali črno), ki je že v tej mapi.
- **macOS:** odpri **Terminal**, vtipkaj `cd ` (s presledkom), povleci mapo v
  okno in pritisni Enter.

`cd` pomeni »spremeni mapo«: `cd C:\Tools\3DHeat-Ext-Squad` odide v to mapo.

## 4. Namesti orodje {#install-the-tool}

Vtipkaj to in pritisni Enter:

```bash
python -m pip install -e .
```

Na koncu bi moral videti: `Successfully installed heat3d-ext-squad-demo-...`.

## 5. Zaženi ga {#run-it}

```bash
heat3d-squad-demo --version
```

Videti bi moral nekaj takega:

```text
heat3d-squad-demo 0.1.0
```

Naprej: [Snemanje posnetka](recording.md), nato [Pretvarjanje posnetkov](converting.md).

## Kako brati ukaze na teh straneh {#how-to-read-the-commands-on-these-pages}

| Kar vidiš | Pomeni |
|---|---|
| `<mapa>` | nadomestilo: namesto tega vtipkaj svojo vrednost, brez `< >` |
| `[--force]` | izbirno: lahko izpustiš, ali vtipkaš, kot je prikazano |
| `a\|b` | izbira: vtipkaj `a` ali `b` |
| `# opomba` | komentar zate: ne vtipkaj ga |
| `"C:\Moje datoteke\x"` | pot s presledki daj v narekovaje |
| `D:\Posnetki` | primer mape v sistemu Windows: uporabi svojo |

## Ko nekaj ne gre prav {#when-something-goes-wrong}

| Sporočilo | Kaj storiti |
|---|---|
| `'python' is not recognized` | Python ni nameščen ali pa ni bilo obkljukano polje PATH: namesti ga znova in obkljukaj (ali vtipkaj `py` namesto `python`). |
| `'heat3d-squad-demo' is not recognized` | Ponovi korak 4 v mapi orodja ali vtipkaj `python -m heat3d_ext_squad` namesto `heat3d-squad-demo`: naredi isto. |
| `No module named heat3d_ext_squad` | Nisi v mapi orodja ali korak 4 ni uspel: pojdi tja z `cd` in ponovi korak 4. |
| `No module named pip` | Zaženi `python -m ensurepip`, nato korak 4. |
| karkoli drugega | Preberi zadnjo vrstico sporočila in z njo odpri prijavo (issue) na GitHubu. |

Vsak ukaz se konča tudi z **izhodno kodo**: 0 pomeni, da je uspel. Da jo vidiš,
vtipkaj `echo $LASTEXITCODE` v PowerShellu ali `echo $?` na macOS in Linuxu.
