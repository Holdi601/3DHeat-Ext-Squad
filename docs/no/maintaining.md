---
title: Vedlikehold av disse dokumentene
nav_order: 91
lang: no
source: maintaining.md
source_hash: "b0b7836a5545"
nav_exclude: true
search_exclude: true
---
# Vedlikehold av disse dokumentene {#maintaining-these-docs}

En sjekkliste for hver utgivelse, slik at sidene aldri henger etter koden.

1. **Generer referansen på nytt.** `python tools/gen_docs_reference.py` skriver om
   [Kommandoreferanse](../cli-reference.md) fra programmets egen `--help` og
   utdatakolonnene. `python tools/gen_docs_reference.py --check` avslutter med 1 når
   den committede siden er utdatert.
2. **List opp hva som endret seg.** `git log v<VERSION>..HEAD --oneline`, der
   `<VERSION>` er den sist utgitte versjonen (filen `VERSION` ved utgivelse). Gi hver
   nye funksjon, hvert nye alternativ og hver ny utdatakolonne en plass på en side, og en
   rad i **Docs**-delen av [`CHANGELOG.md`](https://github.com/Holdi601/3DHeat-Ext-Squad/blob/main/CHANGELOG.md).
3. **Uavhengig gjennomgang.** Noen som ikke skrev sidene leser README og hver endret side,
   bildene inkludert, tre ganger: som en nybegynner som aldri har brukt en terminal, som en
   åtteåring, og som en ekspert som sjekker hvert alternativ mot `--help`. Eksemplene bruker
   bare oppdiktede navn og tall.
4. **Rett** alt gjennomgangen finner.
5. **Oversettelser.** Hver oversatt side registrerer hashen til den engelske siden den ble laget
   fra. Oversett på nytt de sidene der den engelske kilden endret seg, og gjennomgå så
   hvert språk: tydelig tekst, riktige diagramtekster, de samme ordene som visningsprogrammet
   3DHeat bruker i sitt oversatte grensesnitt.
6. **Kjør testene** (`pytest`).
7. **Send bare** etter eierens grønt lys.

## Oversettelser: kommandoene {#translations-the-commands}

Nettstedet er oversatt til 3DHeat-visningsprogrammets 40 språk: engelsk i `docs/`, hvert annet
språk i `docs/<lang>/` med samme filnavn. `tools/docs_i18n.py` står for bokføringen:

```bash
python tools/docs_i18n.py hashes             # after any English change: record each page's hash
python tools/docs_i18n.py svg-strings        # after any picture change: the labels to translate
python tools/docs_i18n.py status             # per language: current, outdated, missing pages
python tools/docs_i18n.py todo --lang de     # the German pages to (re)translate
python tools/docs_i18n.py svg-build --lang de    # German pictures from docs/assets/i18n/svg/de.json
python tools/docs_i18n.py finish --lang de   # stamp the German pages with their English hash
python tools/docs_i18n.py check              # exit 1 when hashes or labels are stale
```

Oversett bare det `todo` lister: behold Markdown, lenker, kode, fil- og kolonnenavn som de er,
oversett titler og bildebeskrivelser, og bruk det 3DHeat-visningsprogrammets egne ord for sine
knapper og paneler (dets `src/i18n/locales/<lang>/`). Genererte referansesider og terminalbilder
forblir engelske. På nettstedet sier en utdatert oversettelse fra det og lenker til den engelske
siden; en som mangler faller tilbake til engelsk. Språkmenyen i hodet og
nettleserspråk-viderekoblingen på hjemmesiden kommer fra `docs/_includes/`.
