---
title: "Áður en þú byrjar"
nav_order: 1.5
lang: "is"
source: before-you-start.md
source_hash: "ca4b6281fdfc"
nav_exclude: true
search_exclude: true
---
# Áður en þú byrjar {#before-you-start}

Hefurðu aldrei notað skipanalínu? Þessi síða leiðir þig frá engu að fyrstu keyrslu.
Það tekur um tíu mínútur, einu sinni.

## 1. Settu upp Python {#install-python}

Þetta verkfæri þarf **Python 3.10 eða nýrra**.

- **Windows:** sæktu Python á [python.org/downloads](https://www.python.org/downloads/)
  og keyrðu uppsetningarforritið. Á fyrsta skjánum skaltu haka við **Add python.exe to PATH**
  og smella síðan á **Install Now**.
- **macOS og Linux:** Python 3 er oft þegar til staðar. Þar sem þessar síður segja
  `python` skaltu skrifa `python3`.

## 2. Náðu í þetta verkfæri {#get-this-tool}

Opnaðu [github.com/Holdi601/3DHeat-Ext-Squad](https://github.com/Holdi601/3DHeat-Ext-Squad), smelltu á
græna hnappinn **Code**, síðan **Download ZIP**, og pakkaðu skránni upp í möppu að
eigin vali. Ef þú notar git: `git clone https://github.com/Holdi601/3DHeat-Ext-Squad`.

## 3. Opnaðu skipanalínu í þeirri möppu {#open-a-terminal-in-that-folder}

Skipanalína er gluggi þar sem þú skrifar skipanir.

- **Windows:** opnaðu möppuna í Explorer, smelltu í vistfangastikuna, skrifaðu
  `powershell` og ýttu á Enter. Blár eða svartur gluggi opnast, þegar í
  þeirri möppu.
- **macOS:** opnaðu **Terminal**, skrifaðu `cd ` (með bili), dragðu möppuna inn í
  gluggann og ýttu á Enter.

`cd` þýðir „change folder“ (skipta um möppu): `cd C:\Tools\3DHeat-Ext-Squad` fer í þá möppu.

## 4. Settu verkfærið upp {#install-the-tool}

Skrifaðu þetta og ýttu á Enter:

```bash
python -m pip install -e .
```

Í lokin ættirðu að sjá: `Successfully installed heat3d-ext-squad-demo-...`.

## 5. Keyrðu það {#run-it}

```bash
heat3d-squad-demo --version
```

Þú ættir að sjá eitthvað svipað og þetta:

```text
heat3d-squad-demo 0.1.0
```

Næst: [Upptaka á demo](recording.md), síðan [Umbreyting á demo](converting.md).

## Hvernig á að lesa skipanirnar á þessum síðum {#how-to-read-the-commands-on-these-pages}

| Þú sérð | Það þýðir |
|---|---|
| `<folder>` | staðgengill: skrifaðu þitt eigið gildi í staðinn, án `< >` |
| `[--force]` | valkvætt: slepptu því eða skrifaðu það eins og sýnt er |
| `a\|b` | val: skrifaðu `a` eða `b` |
| `# a note` | athugasemd handa þér: ekki skrifa hana |
| `"C:\My Files\x"` | settu slóð sem hefur bil innan gæsalappa |
| `D:\Demos` | dæmi um Windows-möppu: notaðu þína eigin |

## Þegar eitthvað fer úrskeiðis {#when-something-goes-wrong}

| Skilaboðin | Hvað á að gera |
|---|---|
| `'python' is not recognized` | Python er ekki uppsett, eða PATH-reiturinn var ekki merktur: settu það upp aftur og hakaðu við hann (eða skrifaðu `py` í stað `python`). |
| `'heat3d-squad-demo' is not recognized` | Keyrðu skref 4 aftur í möppu verkfærisins, eða skrifaðu `python -m heat3d_ext_squad` í stað `heat3d-squad-demo`: það gerir það sama. |
| `No module named heat3d_ext_squad` | Þú ert ekki í möppu verkfærisins, eða skref 4 mistókst: farðu þangað með `cd` og keyrðu skref 4. |
| `No module named pip` | Keyrðu `python -m ensurepip`, síðan skref 4. |
| eitthvað annað | Lestu síðustu línu skilaboðanna og opnaðu svo issue á GitHub með henni. |

Hver skipun endar líka á **útgöngustöðu**: 0 þýðir að hún tókst. Til að sjá hana
skaltu skrifa `echo $LASTEXITCODE` í PowerShell eða `echo $?` í macOS og Linux.
