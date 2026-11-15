---
title: Qabel ma tibda
nav_order: 1.5
lang: "mt"
source: before-you-start.md
source_hash: "ca4b6281fdfc"
nav_exclude: true
search_exclude: true
---
# Qabel ma tibda {#before-you-start}

Ġdid mal-linja tal-kmandi? Din il-paġna tieħdok minn xejn sal-ewwel użu.
Tieħu madwar għaxar minuti, darba biss.

## 1. Installa Python {#install-python}

Din l-għodda teħtieġ **Python 3.10 jew aktar ġdid**.

- **Windows:** niżżel Python minn [python.org/downloads](https://www.python.org/downloads/)
  u ħaddem l-installer. Fl-ewwel skrin, immarka **Add python.exe to PATH**,
  imbagħad ikklikkja **Install Now**.
- **macOS u Linux:** Python 3 spiss ikun diġà hemm. Fejn dawn il-paġni
  jgħidu `python`, ittajpja `python3`.

## 2. Ġib din l-għodda {#get-this-tool}

Iftaħ [github.com/Holdi601/3DHeat-Ext-Squad](https://github.com/Holdi601/3DHeat-Ext-Squad), ikklikkja
l-buttuna ħadra **Code**, imbagħad **Download ZIP**, u ħoll iż-zip f'folder
li tagħżel int. Jekk tuża git: `git clone https://github.com/Holdi601/3DHeat-Ext-Squad`.

## 3. Iftaħ terminal f'dak il-folder {#open-a-terminal-in-that-folder}

Terminal huwa tieqa fejn tittajpja l-kmandi.

- **Windows:** iftaħ il-folder fl-Explorer, ikklikkja fil-bar tal-indirizz, ittajpja
  `powershell` u agħfas Enter. Tiftaħ tieqa blu jew sewda, diġà f'dak il-folder.
- **macOS:** iftaħ **Terminal**, ittajpja `cd ` (b'spazju), kaxkar il-folder
  fit-tieqa u agħfas Enter.

`cd` tfisser "biddel il-folder": `cd C:\Tools\3DHeat-Ext-Squad` jmur f'dak il-folder.

## 4. Installa l-għodda {#install-the-tool}

Ittajpja dan u agħfas Enter:

```bash
python -m pip install -e .
```

Fl-aħħar għandek tara: `Successfully installed heat3d-ext-squad-demo-...`.

## 5. Ħaddimha {#run-it}

```bash
heat3d-squad-demo --version
```

Għandek tara xi ħaġa bħal:

```text
heat3d-squad-demo 0.1.0
```

Li jmiss: [Tirrekordja demo](recording.md), imbagħad [Tikkonverti demos](converting.md).

## Kif taqra l-kmandi f'dawn il-paġni {#how-to-read-the-commands-on-these-pages}

| Tara | Tfisser |
|---|---|
| `<folder>` | placeholder: ittajpja l-valur tiegħek minfloku, mingħajr l-`< >` |
| `[--force]` | fakultattiv: ħallih barra, jew ittajpjah kif muri |
| `a\|b` | għażla: ittajpja `a` jew `b` |
| `# a note` | kumment għalik: tittajpjahx |
| `"C:\My Files\x"` | poġġi triq li fiha spazji bejn l-virgoletti |
| `D:\Demos` | folder ta' Windows bħala eżempju: uża tiegħek |

## Meta xi ħaġa tmur ħażin {#when-something-goes-wrong}

| Il-messaġġ | X'għandek tagħmel |
|---|---|
| `'python' is not recognized` | Python mhuwiex installat, jew il-kaxxa tal-PATH ma ġietx immarkata: installa mill-ġdid u immarkaha (jew ittajpja `py` minflok `python`). |
| `'heat3d-squad-demo' is not recognized` | Erġa' agħmel il-pass 4 fil-folder tal-għodda, jew ittajpja `python -m heat3d_ext_squad` minflok `heat3d-squad-demo`: jagħmel l-istess. |
| `No module named heat3d_ext_squad` | Mhux fil-folder tal-għodda, jew il-pass 4 falla: mur hemm b'`cd` u agħmel il-pass 4. |
| `No module named pip` | Ħaddem `python -m ensurepip`, imbagħad il-pass 4. |
| kull ħaġa oħra | Aqra l-aħħar linja tal-messaġġ, imbagħad iftaħ issue fuq GitHub biha. |

Kull kmand jispiċċa wkoll b'**exit status**: 0 ifisser li ħadem. Biex tarah,
ittajpja `echo $LASTEXITCODE` f'PowerShell jew `echo $?` fuq macOS u Linux.
