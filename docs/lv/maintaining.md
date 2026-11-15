---
title: Šo lapu uzturēšana
nav_order: 91
lang: "lv"
source: maintaining.md
source_hash: "b0b7836a5545"
nav_exclude: true
search_exclude: true
---
# Šo lapu uzturēšana {#maintaining-these-docs}

Kontrolsaraksts katrai izlaidei, lai lapas nekad neatpaliek no koda.

1. **Atjaunojiet atsauci.** `python tools/gen_docs_reference.py` pārraksta
   [Komandu atsauce](../cli-reference.md) no programmas pašas `--help` un izvades kolonnām.
   `python tools/gen_docs_reference.py --check` beidzas ar kodu 1, ja saglabātā lapa ir novecojusi.
2. **Uzskaitiet izmaiņas.** `git log v<VERSION>..HEAD --oneline`, kur
   `<VERSION>` ir pēdējā izlaistā versija (fails `VERSION` izlaidē). Katrai jaunai funkcijai,
   iespējai un izvades kolonnai jāatrod vieta lapā un rinda sadaļā **Docs** failā
   [`CHANGELOG.md`](https://github.com/Holdi601/3DHeat-Ext-Squad/blob/main/CHANGELOG.md).
3. **Neatkarīga pārskatīšana.** Kāds, kas nav rakstījis lapas, izlasa README un katru mainīto lapu,
   arī attēlus, trīs reizes: kā iesācējs, kas nekad nav lietojis termināli, kā astoņgadnieks un kā
   eksperts, kas pārbauda katru iespēju pret `--help`. Piemēros izmanto tikai izdomātus nosaukumus
   un skaitļus.
4. **Labojiet** visu, ko atrod pārskatīšana.
5. **Tulkojumi.** Katra tulkotā lapa ieraksta to angļu lapas jaucējkodu, no kuras tā
   tika izveidota. Tulkojiet no jauna lapas, kuru angļu avots ir mainījies, tad pārskatiet katru valodu:
   skaidrs teksts, pareizas diagrammu etiķetes, tie paši vārdi, ko lieto skatītāja pašu tulkotajā saskarnē.
6. **Palaidiet testus** (`pytest`).
7. **Augšupielādējiet** tikai pēc īpašnieka atļaujas.

## Tulkojumi: komandas {#translations-the-commands}

Vietne ir tulkota 3DHeat skatītāja 40 valodās: angļu valoda ir `docs/`, katra cita valoda ir `docs/<lang>/` ar tiem pašiem failu nosaukumiem. `tools/docs_i18n.py` veic uzskaiti:

```bash
python tools/docs_i18n.py hashes             # pēc katras angļu izmaiņas: ieraksta katras lapas jaucējkodu
python tools/docs_i18n.py svg-strings        # pēc katras attēla izmaiņas: etiķetes, ko tulkot
python tools/docs_i18n.py status             # katrai valodai: aktuālās, novecojušās un trūkstošās lapas
python tools/docs_i18n.py todo --lang de     # vācu lapas, ko (pārtulkot) tulkot
python tools/docs_i18n.py svg-build --lang de    # vācu attēli no docs/assets/i18n/svg/de.json
python tools/docs_i18n.py finish --lang de   # apzīmo vācu lapas ar to angļu jaucējkodu
python tools/docs_i18n.py check              # beidzas ar kodu 1, ja jaucējkodi vai etiķetes ir novecojušas
```

Tulkojiet tikai to, ko `todo` uzskaita: saglabājiet Markdown, saites, kodu, failu un kolonnu nosaukumus kā tie ir,
tulkojiet nosaukumus un attēlu aprakstus, un izmantojiet skatītāja pašu vārdus tā pogām un paneļiem
(tā `src/i18n/locales/<lang>/`). Ģenerētās atsauces lapas un termināla attēli paliek angļu valodā.
Vietnē novecojis tulkojums to pasaka un saista ar angļu lapu; trūkstošs tulkojums tiek rādīts angļu valodā.
Valodu izvēlne galvenē un mājas lapas pārvirzīšana pēc pārlūka valodas nāk no `docs/_includes/`.
