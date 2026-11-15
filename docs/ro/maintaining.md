---
title: "Întreținerea acestor documente"
nav_order: 91
lang: ro
source: maintaining.md
source_hash: "b0b7836a5545"
nav_exclude: true
search_exclude: true
---
# Întreținerea acestor documente {#maintaining-these-docs}

O listă de verificare pentru fiecare lansare, ca paginile să nu rămână niciodată în urma codului.

1. **Regenerați referința.** `python tools/gen_docs_reference.py` rescrie
   [Referința comenzilor](../cli-reference.md) din `--help`-ul propriu al programului și din coloanele de ieșire.
   `python tools/gen_docs_reference.py --check` iese cu codul 1 când pagina salvată este veche.
2. **Listați ce s-a schimbat.** `git log v<VERSION>..HEAD --oneline`, unde `<VERSION>` este ultima
   versiune lansată (fișierul `VERSION` de la lansare). Dați fiecărei funcții noi, opțiuni și coloane
   de ieșire un loc pe o pagină și un rând în secțiunea **Docs** din [`CHANGELOG.md`](https://github.com/Holdi601/3DHeat-Ext-Squad/blob/main/CHANGELOG.md).
3. **Revizuire independentă.** Cineva care nu a scris paginile citește README-ul și fiecare pagină
   modificată, cu imaginile cu tot, de trei ori: ca un începător care n-a folosit niciodată un terminal,
   ca un copil de 8 ani și ca un expert care verifică fiecare opțiune față de `--help`. Exemplele folosesc
   doar nume și numere inventate.
4. **Remediați** tot ce găsește revizuirea.
5. **Traduceri.** Fiecare pagină tradusă înregistrează hash-ul paginii engleze din care a fost făcută.
   Traduceți din nou paginile a căror sursă engleză s-a schimbat, apoi revizuiți fiecare limbă: text
   clar, etichete corecte în diagrame, aceleași cuvinte ca interfața tradusă a vizualizatorului 3DHeat.
6. **Rulați testele** (`pytest`).
7. **Publicați** doar după acordul proprietarului.

## Traduceri: comenzile {#translations-the-commands}

Site-ul este tradus în cele 40 de limbi ale vizualizatorului 3DHeat: engleza în `docs/`, fiecare
altă limbă în `docs/<lang>/`, cu aceleași nume de fișiere. `tools/docs_i18n.py` ține evidența:

```bash
python tools/docs_i18n.py hashes             # after any English change: record each page's hash
python tools/docs_i18n.py svg-strings        # after any picture change: the labels to translate
python tools/docs_i18n.py status             # per language: current, outdated, missing pages
python tools/docs_i18n.py todo --lang de     # the German pages to (re)translate
python tools/docs_i18n.py svg-build --lang de    # German pictures from docs/assets/i18n/svg/de.json
python tools/docs_i18n.py finish --lang de   # stamp the German pages with their English hash
python tools/docs_i18n.py check              # exit 1 when hashes or labels are stale
```

Traduceți doar ce listează `todo`: păstrați Markdown-ul, legăturile, codul, numele fișierelor și ale
coloanelor așa cum sunt; traduceți titlurile și descrierile imaginilor; folosiți cuvintele proprii ale
vizualizatorului 3DHeat pentru butoanele și panourile sale (din `src/i18n/locales/<lang>/`). Paginile
de referință generate și imaginile din terminal rămân în engleză. Pe site, o traducere veche spune
asta și trimite la pagina engleză; una lipsă revine la engleză. Meniul de limbi din antet și
redirecționarea de pe pagina principală, după limba browserului, vin din `docs/_includes/`.
