---
title: "Održavanje ove dokumentacije"
nav_order: 91
lang: "bs"
source: maintaining.md
source_hash: "b0b7836a5545"
nav_exclude: true
search_exclude: true
---
# Održavanje ove dokumentacije {#maintaining-these-docs}

Lista za provjeru pri svakom izdanju, da stranice nikad ne zaostanu za kodom.

1. **Ponovo generiši referencu.** `python tools/gen_docs_reference.py` prepisuje
   [Referencu naredbi](../cli-reference.md) iz programovog vlastitog `--help` i
   izlaznih kolona. `python tools/gen_docs_reference.py --check` izlazi s 1 kad
   je spremljena stranica zastarjela.
2. **Navedi šta se promijenilo.** `git log v<VERSION>..HEAD --oneline`, gdje je
   `<VERSION>` zadnja izdana verzija (datoteka `VERSION` pri izdanju).
   Svaka nova funkcija, opcija i izlazna kolona dobija mjesto na nekoj stranici i
   red u odjeljku **Docs** datoteke [`CHANGELOG.md`](https://github.com/Holdi601/3DHeat-Ext-Squad/blob/main/CHANGELOG.md).
3. **Nezavisan pregled.** Neko ko nije pisao stranice čita
   README i svaku promijenjenu stranicu, uključujući slike, triput: kao
   početnik koji nikad nije koristio terminal, kao osmogodišnjak i kao stručnjak
   koji provjerava svaku opciju prema `--help`. Primjeri koriste samo izmišljena imena i
   brojeve.
4. **Ispravi** sve što pregled nađe.
5. **Prijevodi.** Svaka prevedena stranica bilježi hash engleske stranice
   iz koje je nastala. Ponovo prevedi stranice čiji se engleski izvor promijenio,
   zatim pregledaj svaki jezik: jasan tekst, tačne oznake na dijagramima, iste
   riječi kao u prevedenom sučelju preglednika.
6. **Pokreni testove** (`pytest`).
7. **Push** tek nakon odobrenja vlasnika.

## Prijevodi: naredbe {#translations-the-commands}

Stranica je prevedena na 40 jezika 3DHeat preglednika: engleski u `docs/`, svaki drugi
jezik u `docs/<lang>/` s istim nazivima datoteka. `tools/docs_i18n.py` vodi evidenciju:

```bash
python tools/docs_i18n.py hashes             # after any English change: record each page's hash
python tools/docs_i18n.py svg-strings        # after any picture change: the labels to translate
python tools/docs_i18n.py status             # per language: current, outdated, missing pages
python tools/docs_i18n.py todo --lang de     # the German pages to (re)translate
python tools/docs_i18n.py svg-build --lang de    # German pictures from docs/assets/i18n/svg/de.json
python tools/docs_i18n.py finish --lang de   # stamp the German pages with their English hash
python tools/docs_i18n.py check              # exit 1 when hashes or labels are stale
```

Prevedi samo ono što navodi `todo`: Markdown, veze, kod, nazive datoteka i kolona ostavi kakvi jesu,
prevedi naslove i opise slika, a za dugmad i panele 3DHeat preglednika koristi njegove vlastite riječi
(`src/i18n/locales/<lang>/`). Generirane referentne stranice i slike terminala ostaju
na engleskom. Na stranici zastarjeli prijevod to kaže i povezuje englesku stranicu; nedostajući
se vraća na engleski. Jezični izbornik u zaglavlju i preusmjeravanje početne stranice prema jeziku preglednika
dolaze iz `docs/_includes/`.
