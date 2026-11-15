---
title: Održavanje ovih stranica
nav_order: 91
lang: hr
source: maintaining.md
source_hash: "b0b7836a5545"
nav_exclude: true
search_exclude: true
---
# Održavanje ovih stranica {#maintaining-these-docs}

Popis za svako izdanje, da stranice nikad ne zaostanu za kodom.

1. **Ponovno generirajte referencu.** `python tools/gen_docs_reference.py` ponovno piše
   [Referencu naredbi](../cli-reference.md) iz vlastite `--help` naredbe programa i stupaca izlaza. `python tools/gen_docs_reference.py --check` izlazi s 1 kad je zapisana stranica zastarjela.
2. **Popišite što se promijenilo.** `git log v<VERSION>..HEAD --oneline`, gdje je `<VERSION>` posljednja objavljena verzija (datoteka `VERSION` pri izdanju). Svaka nova značajka, opcija i izlazni stupac mora imati mjesto na stranici i redak u odjeljku **Docs** u [`CHANGELOG.md`](https://github.com/Holdi601/3DHeat-Ext-Squad/blob/main/CHANGELOG.md).
3. **Neovisni pregled.** Netko tko nije pisao stranice pročita README i svaku promijenjenu stranicu, uključujući slike, tri puta: kao početnik koji nikad nije koristio terminal, kao osmogodišnjak i kao stručnjak koji svaku opciju provjerava u `--help`. Primjeri koriste samo izmišljena imena i brojeve.
4. **Ispravite** sve što pregled pronađe.
5. **Prijevodi.** Svaka prevedena stranica bilježi hash engleske stranice iz koje je nastala. Ponovno prevedite stranice čiji se engleski izvor promijenio, zatim pregledajte svaki jezik: jasan tekst, ispravne oznake na dijagramima, iste riječi kao u prevedenom sučelju preglednika 3DHeat.
6. **Pokrenite testove** (`pytest`).
7. **Objavite** tek nakon odobrenja vlasnika.

## Prijevodi: naredbe {#translations-the-commands}

Stranica je prevedena na 40 jezika preglednika 3DHeat: engleski je u `docs/`, svaki drugi jezik u `docs/<lang>/` s istim imenima datoteka. `tools/docs_i18n.py` vodi evidenciju:

```bash
python tools/docs_i18n.py hashes             # nakon svake promjene engleskog: zabilježi hash svake stranice
python tools/docs_i18n.py svg-strings        # nakon promjene slike: oznake za prijevod
python tools/docs_i18n.py status             # po jeziku: aktualne, zastarjele, nedostajuće stranice
python tools/docs_i18n.py todo --lang de     # njemačke stranice za (ponovni) prijevod
python tools/docs_i18n.py svg-build --lang de    # njemačke slike iz docs/assets/i18n/svg/de.json
python tools/docs_i18n.py finish --lang de   # označi njemačke stranice hashom engleske
python tools/docs_i18n.py check              # izlazi s 1 kad su hashevi ili oznake zastarjeli
```

Prevodite samo ono što `todo` navodi: zadržite Markdown, poveznice, kod, imena datoteka i stupaca; prevedite naslove i opise slika, i koristite vlastite riječi preglednika 3DHeat za njegove gumbe i panele (njegov `src/i18n/locales/<lang>/`). Generirane referentne stranice i terminalne slike ostaju na engleskom. Na stranici zastarjeli prijevod to kaže i poveže englesku stranicu; nedostajući prijevod vraća se na engleski. Izbornik jezika u zaglavlju i automatsko preusmjeravanje početne stranice prema jeziku preglednika dolaze iz `docs/_includes/`.
