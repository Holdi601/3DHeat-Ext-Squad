---
title: "Áður en þú byrjar"
nav_order: 1.5
lang: is
source: before-you-start.md
source_hash: "ca4b6281fdfc"
nav_exclude: true
search_exclude: true
---
# Áður en þú byrjar

Ertu ný/r í skipanalínunni? Þessi síða leiðir þig frá engu að fyrstu keyrslu.
Það tekur um tíu mínútur, einu sinni.

## 1. Settu upp Python

Þetta tól þarf **Python 3.10 eða nýrra**.

- **Windows:** sæktu Python á [python.org/downloads](https://www.python.org/downloads/)
  og keyrðu uppsetningarforritið. Á fyrsta skjánum skaltu haka við **Add python.exe to PATH**
  og smella síðan á **Install Now**.
- **macOS og Linux:** Python 3 er oft þegar til staðar. Þar sem þessar síður segja
  `python` skaltu skrifa `python3`.

## 2. Náðu í þetta tól

Opnaðu [github.com/Holdi601/3DHeat-Ext-Squad](https://github.com/Holdi601/3DHeat-Ext-Squad), smelltu á
græna hnappinn **Code**, síðan **Download ZIP**, og pakkaðu skránni upp í möppu að
eigin vali. Ef þú notar git: `git clone https://github.com/Holdi601/3DHeat-Ext-Squad`.

## 3. Opnaðu skipanalínu í þeirri möppu

Skipanalína er gluggi þar sem þú skrifar skipanir.

- **Windows:** opnaðu möppuna í Explorer, smelltu í vistfangastikuna, skrifaðu
  `powershell` og ýttu á Enter. Blár eða svartur gluggi opnast, þegar í
  þeirri möppu.
- **macOS:** opnaðu **Terminal**, skrifaðu `cd ` (með bili), dragðu möppuna inn í
  gluggann og ýttu á Enter.

`cd` þýðir „change folder“ (skipta um möppu): `cd C:\Tools\3DHeat-Ext-Squad` fer í þá möppu.

## 4. Settu tólið upp

Skrifaðu þetta og ýttu á Enter:

```bash
python -m pip install -e .
```

Í lokin ættirðu að sjá: `Successfully installed heat3d-ext-squad-demo-...`.

## 5. Keyrðu það

```bash
heat3d-squad-demo --version
```

Þú ættir að sjá eitthvað svipað og þetta:

```text
heat3d-squad-demo 0.1.0
```

Næst: [Upptaka á demo](recording.md), síðan [Umbreyting á demo](converting.md).

## Hvernig á að lesa skipanirnar á þessum síðum

| Þú sérð | Það þýðir |
|---|---|
| `<folder>` | staðgengill: skrifaðu þitt eigið gildi í staðinn, án `< >` |
| `[--force]` | valkvætt: slepptu því eða skrifaðu það eins og sýnt er |
| `a\|b` | val: skrifaðu `a` eða `b` |
| `# a note` | athugasemd handa þér: ekki skrifa hana |
