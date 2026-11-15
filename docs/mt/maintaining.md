---
title: Iżżomm dawn id-dokumenti
nav_order: 91
lang: "mt"
source: maintaining.md
source_hash: "b0b7836a5545"
nav_exclude: true
search_exclude: true
---
# Iżżomm dawn id-dokumenti {#maintaining-these-docs}

Lista ta' kontroll għal kull rilaxx, biex il-paġni ma jibqgħux lura mill-kodiċi.

1. **Erġa' iġġenera r-referenza.** `python tools/gen_docs_reference.py` jerġa' jikteb
   [Referenza tal-kmandi](../cli-reference.md) mill-`--help` u mill-kolonni
   tal-output tal-programm innifsu. `python tools/gen_docs_reference.py --check` joħroġ b'1 meta
   il-paġna kommessa tkun skaduta.
2. **Elenka x'inbidel.** `git log v<VERSION>..HEAD --oneline`, fejn
   `<VERSION>` hija l-aħħar verżjoni rilaxxata (il-fajl `VERSION` fir-rilaxx).
   Agħti lil kull feature, għażla u kolonna tal-output ġodda post fuq paġna, u
   ringiela fit-taqsima **Docs** ta' [`CHANGELOG.md`](https://github.com/Holdi601/3DHeat-Ext-Squad/blob/main/CHANGELOG.md).
3. **Reviżjoni indipendenti.** Xi ħadd li ma kitibx il-paġni jaqra
   r-README u kull paġna mibdula, l-istampi inklużi, tliet darbiet: bħala ġdid
   li qatt ma uża terminal, bħala tifel ta' 8 snin, u bħala espert
   li jivverifika kull għażla kontra `--help`. L-eżempji jużaw biss ismijiet u
   numri magħmulin.
4. **Ikkoreġi** kull ma ssib ir-reviżjoni.
5. **Traduzzjonijiet.** Kull paġna tradotta tirrekordja l-hash tal-paġna Ingliża
   li minnha saret. Erġa' ttraduċi l-paġni li s-sors Ingliż tagħhom inbidel,
   imbagħad irrevedi kull lingwa: test ċar, tikketti tad-dijagrammi korretti, l-istess
   kliem bħall-interface tradott tal-viewer.
6. **Ħaddem it-testijiet** (`pytest`).
7. **Agħfas push** biss wara l-ok tas-sid.

## Traduzzjonijiet: il-kmandi {#translations-the-commands}

Is-sit huwa tradott fit-40 lingwa tal-viewer ta' 3DHeat: Ingliż f'`docs/`, kull lingwa
oħra f'`docs/<lang>/` bl-istess ismijiet tal-fajls. `tools/docs_i18n.py` jagħmel il-bookkeeping:

```bash
python tools/docs_i18n.py hashes             # after any English change: record each page's hash
python tools/docs_i18n.py svg-strings        # after any picture change: the labels to translate
python tools/docs_i18n.py status             # per language: current, outdated, missing pages
python tools/docs_i18n.py todo --lang de     # the German pages to (re)translate
python tools/docs_i18n.py svg-build --lang de    # German pictures from docs/assets/i18n/svg/de.json
python tools/docs_i18n.py finish --lang de   # stamp the German pages with their English hash
python tools/docs_i18n.py check              # exit 1 when hashes or labels are stale
```

Ittraduċi biss dak li jelenka `todo`: żomm Markdown, links, kodiċi, ismijiet ta' fajls u kolonni kif inhuma,
ittraduċi t-titli u d-deskrizzjonijiet tal-istampi, u uża l-kliem proprju tal-viewer ta' 3DHeat għall-buttuni
u l-pannelli tiegħu (`src/i18n/locales/<lang>/`). Il-paġni ta' referenza ġġenerati u l-istampi tat-terminal jibqgħu
bl-Ingliż. Fuq is-sit, traduzzjoni skaduta tgħid hekk u torbot mal-paġna Ingliża; waħda neqsa
terġa' lura għall-Ingliż. Il-menu tal-lingwa fl-header u r-redirect tal-lingwa tal-browser tal-paġna ewlenija
jiġu minn `docs/_includes/`.
