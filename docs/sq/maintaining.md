---
title: "Mirëmbajtja e këtyre dokumenteve"
nav_order: 91
lang: sq
source: maintaining.md
source_hash: "b0b7836a5545"
nav_exclude: true
search_exclude: true
---
# Mirëmbajtja e këtyre dokumenteve {#maintaining-these-docs}

Një listë kontrolli për çdo botim, që faqet të mos mbeten kurrë pas kodit.

1. **Rigjenero referencën.** `python tools/gen_docs_reference.py` rishkruan
   [Referenca e komandave](../cli-reference.md) nga `--help` i vetë programit dhe
   nga kolonat e daljes. `python tools/gen_docs_reference.py --check` del me 1 kur
   faqja e commit-uar është e vjetruar.
2. **Listo çfarë ndryshoi.** `git log v<VERSION>..HEAD --oneline`, ku
   `<VERSION>` është versioni i fundit i botuar (skedari `VERSION` në botim).
   Çdo veçori, opsion dhe kolonë e re e daljes merr një vend në një faqe, dhe një
   rresht në pjesën **Docs** të [`CHANGELOG.md`](https://github.com/Holdi601/3DHeat-Ext-Squad/blob/main/CHANGELOG.md).
3. **Rishikim i pavarur.** Dikush që nuk i ka shkruar faqet lexon
   README dhe çdo faqe të ndryshuar, edhe pamjet, tri herë: si fillestar që
   s'ka përdorur kurrë terminal, si një 8-vjeçar, dhe si ekspert që
   kontrollon çdo opsion me `--help`. Shembujt përdorin vetëm emra dhe
   numra të sajuar.
4. **Rregullo** çdo gjë që gjen rishikimi.
5. **Përkthimet.** Çdo faqe e përkthyer ruan hash-in e faqes angleze
   nga e cila u bë. Përkthe sërish faqet e të cilave burimi anglez ndryshoi,
   pastaj rishiko çdo gjuhë: tekst i qartë, etiketa të sakta në diagrame, të njëjtat
   fjalë si ndërfaqja e përkthyer e vetë shikuesit.
6. **Ekzekuto testet** (`pytest`).
7. **Bëj push** vetëm pas lejes së pronarit.

## Përkthimet: komandat {#translations-the-commands}

Faqja përkthehet në 40 gjuhët e shikuesit 3DHeat: anglishtja në `docs/`, çdo gjuhë tjetër
në `docs/<lang>/` me të njëjtat emra skedarësh. `tools/docs_i18n.py` mban llogaritë:

```bash
python tools/docs_i18n.py hashes             # after any English change: record each page's hash
python tools/docs_i18n.py svg-strings        # after any picture change: the labels to translate
python tools/docs_i18n.py status             # per language: current, outdated, missing pages
python tools/docs_i18n.py todo --lang de     # the German pages to (re)translate
python tools/docs_i18n.py svg-build --lang de    # German pictures from docs/assets/i18n/svg/de.json
python tools/docs_i18n.py finish --lang de   # stamp the German pages with their English hash
python tools/docs_i18n.py check              # exit 1 when hashes or labels are stale
```

Përkthe vetëm çfarë liston `todo`: ruaj Markdown, lidhjet, kodin, emrat e skedarëve dhe të kolonave siç janë,
përkthe titujt dhe përshkrimet e pamjeve, dhe përdor fjalët e vetë shikuesit 3DHeat për butonat
dhe panelet e tij (`src/i18n/locales/<lang>/`). Faqet e referencës së gjeneruar dhe pamjet e terminalit mbeten
në anglisht. Në faqe, një përkthim i vjetruar e thotë këtë dhe lidh faqen angleze; një faqe që mungon
kthehet te anglishtja. Menyja e gjuhës në krye dhe ridrejtimi sipas gjuhës së shfletuesit në faqen kryesore
vijnë nga `docs/_includes/`.
