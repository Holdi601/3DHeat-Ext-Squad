---
title: "Ier Dir ufänkt"
nav_order: 1.5
lang: lb
source: before-you-start.md
source_hash: "ca4b6281fdfc"
nav_exclude: true
search_exclude: true
---
# Ier Dir ufänkt {#before-you-start}

Nei op der Kommandozeil? Dës Säit féiert Iech vun Null bis bei Ären éischte Start. Et dauert ongeféier zéng Minutten, eemol.

## 1. Python installéieren {#install-python}

Dëst Tool brauch **Python 3.10 oder méi nei**.

- **Windows:** Python vun [python.org/downloads](https://www.python.org/downloads/) eroflueden
  an den Installer starten. Um éischten Ecran **Add python.exe to PATH** ukräizen,
  dann op **Install Now** klicken.
- **macOS a Linux:** Python 3 ass dacks schonn do. Wou op dëse Säiten
  `python` steet, tippt `python3`.

## 2. Dëst Tool kréien {#get-this-tool}

Mécht [github.com/Holdi601/3DHeat-Ext-Squad](https://github.com/Holdi601/3DHeat-Ext-Squad) op, klickt op de
gréngen **Code**-Knäppchen, dann op **Download ZIP**, an entzippt et an en Dossier
no Wahl. Wann Dir git benotzt: `git clone https://github.com/Holdi601/3DHeat-Ext-Squad`.

## 3. E Terminal an deem Dossier opmaachen {#open-a-terminal-in-that-folder}

E Terminal ass e Fënster, wou Dir Kommandoe tippt.

- **Windows:** Mécht den Dossier am Explorer op, klickt an d'Adressleist, tippt
  `powershell` an dréckt Enter. E bloe oder schwaarzt Fënster geet op, schonn
  an deem Dossier.
- **macOS:** Mécht d'**Terminal** op, tippt `cd ` (mat engem Espace), zitt den Dossier an
  d'Fënster an dréckt Enter.

`cd` heescht „change folder“ (Dossier wiesselen): `cd C:\Tools\3DHeat-Ext-Squad` geet an dee Dossier.

## 4. D'Tool installéieren {#install-the-tool}

Tippt dëst an dréckt Enter:

```bash
python -m pip install -e .
```

Um Enn solltet Dir gesinn: `Successfully installed heat3d-ext-squad-demo-...`.

## 5. Starten {#run-it}

```bash
heat3d-squad-demo --version
```

Dir sollt eppes wéi dat gesinn:

```text
heat3d-squad-demo 0.1.0
```

Als Nächst: [Eng Demo ophuelen](recording.md), dann [Demoe konvertéieren](converting.md).

## Wéi Dir d'Kommandoe op dëse Säite liest {#how-to-read-the-commands-on-these-pages}

| Dir gesitt | Et heescht |
|---|---|
| `<folder>` | e Platzhalter: tippt Äre Wäert amplaz, ouni d'`< >` |
| `[--force]` | optional: looss et fort, oder tippt et esou wéi gewisen |
| `a\|b` | eng Auswiel: tippt `a` oder `b` |
| `# a note` | e Kommentar fir Iech: net tippen |
| `"C:\My Files\x"` | e Wee mat Espacen an Ureechnungszeechen setzen |
| `D:\Demos` | e Beispill-Windows-Dossier: benotzt Äre ganzen |

## Wann eppes falsch geet {#when-something-goes-wrong}

| D'Meldung | Wat maachen |
|---|---|
| `'python' is not recognized` | Python ass net installéiert, oder d'PATH-Këschtchen war net ugekräizt: nach eemol installéieren an ukräizen (oder `py` amplaz `python` tippen). |
| `'heat3d-squad-demo' is not recognized` | Schrëtt 4 nach eemol am Dossier vum Tool maachen, oder `python -m heat3d_ext_squad` amplaz `heat3d-squad-demo` tippen: et mécht datselwecht. |
| `No module named heat3d_ext_squad` | Dir sidd net am Dossier vum Tool, oder Schrëtt 4 ass feelgeschloen: mat `cd` dohinner goen a Schrëtt 4 maachen. |
| `No module named pip` | `python -m ensurepip` ausféieren, dann Schrëtt 4. |
| soss eppes | Liest déi lescht Zeil vun der Meldung, dann mécht en Issue op GitHub domat op. |

All Kommando endet och mat engem **Exit-Status**: 0 heescht, et huet geklappt. Fir en ze gesinn,
tippt `echo $LASTEXITCODE` an der PowerShell oder `echo $?` op macOS a Linux.
