---
title: "Dës Dokumentatioun ënnerhalen"
nav_order: 91
lang: "lb"
source: maintaining.md
source_hash: "b0b7836a5545"
nav_exclude: true
search_exclude: true
---
# Dës Dokumentatioun ënnerhalen {#maintaining-these-docs}

Eng Checklëscht fir all Release, sou datt d'Säite ni hannert dem Code zeréckfalen.

1. **D'Referenz nei generéieren.** `python tools/gen_docs_reference.py` schreift
   d'[Kommando-Referenz](../cli-reference.md) nei aus dem `--help` vum Programm an
   senge Ausgab-Kolonnen. `python tools/gen_docs_reference.py --check` gëtt 1 zréck, wann
   déi committe Säit verfalen ass.
2. **Opschreiwen, wat sech geännert huet.** `git log v<VERSION>..HEAD --oneline`, wou
   `<VERSION>` déi lescht verëffentlecht Versioun ass (d'`VERSION`-Datei beim Release).
   All nei Funktioun, Optioun an Ausgab-Kolonn kritt e Plaz op enger Säit, an eng
   Zeil an der **Docs**-Sektioun vum [`CHANGELOG.md`](https://github.com/Holdi601/3DHeat-Ext-Squad/blob/main/CHANGELOG.md).
3. **Onofhängeg Iwwerpréiwung.** Een, deen d'Säite net geschriwwen huet, liest de
   README an all geännert Säit, d'Biller abegraff, dräi Mol: als Ufänger, deen ni
   e Terminal benotzt huet, als 8-Järegen, an als Expert,
   dee jidd Optioun géint `--help` préift. Beispiller benotzen nëmme erfonnen Nimm an
   Zuelen.
4. **Alles fixéieren**, wat d'Iwwerpréiwung fënnt.
5. **Iwwersetzungen.** All iwwersate Säit hält den Hash vun der englescher Säit fest,
   aus där se gemaach gouf. D'Säiten nei iwwersetzen, vun deenen déi englesch Quell sech geännert huet,
   dann all Sprooch nokucken: kloren Text, richteg Diagramm-Beschrëftungen, déiselwecht
   Wierder wéi an der iwwersater Interface vum Viewer.
6. **D'Tester lafe loossen** (`pytest`).
7. **Pushen** nëmmen nom Go vum Besëtzer.

## Iwwersetzungen: d'Kommandoen {#translations-the-commands}

De Site ass an déi 40 Sprooche vum 3DHeat-Viewer iwwersat: Englesch an `docs/`, all aner
Sprooch an `docs/<lang>/` mat de selwechten Dateinimm. `tools/docs_i18n.py` mécht d'Buchhaltung:

```bash
python tools/docs_i18n.py hashes             # after any English change: record each page's hash
python tools/docs_i18n.py svg-strings        # after any picture change: the labels to translate
python tools/docs_i18n.py status             # per language: current, outdated, missing pages
python tools/docs_i18n.py todo --lang de     # the German pages to (re)translate
python tools/docs_i18n.py svg-build --lang de    # German pictures from docs/assets/i18n/svg/de.json
python tools/docs_i18n.py finish --lang de   # stamp the German pages with their English hash
python tools/docs_i18n.py check              # exit 1 when hashes or labels are stale
```

Iwwersetzt nëmmen, wat `todo` opléscht: Markdown, Linken, Code, Datei- a Kolonnennimm bleiwen wéi se sinn,
Titele a Bildbeschreiwunge ginn iwwersat, a benotzt d'Wierder vum 3DHeat-Viewer fir seng Knäppercher
a Panelen (säin `src/i18n/locales/<lang>/`). Generéiert Referenzsäiten an Terminal-Biller bleiwen
Englesch. Um Site seet eng verfale Iwwersetzung dat an verlinkt d'englesch Säit; eng feelend
fällt zréck op Englesch. D'Sproochmenü am Header an d'Viraleedung op d'Browser-Sprooch vun der Startsäit
kommen aus `docs/_includes/`.
