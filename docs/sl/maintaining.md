---
title: "Vzdrževanje teh strani"
nav_order: 91
lang: "sl"
source: maintaining.md
source_hash: "b0b7836a5545"
nav_exclude: true
search_exclude: true
---
# Vzdrževanje teh strani {#maintaining-these-docs}

Kontrolni seznam za vsako izdajo, da strani nikoli ne zaostanejo za kodo.

1. **Ponovno ustvari priročnik.** `python tools/gen_docs_reference.py` na novo zapiše
   [Priročnik ukazov](../cli-reference.md) iz lastnega `--help` programa in izhodnih stolpcev.
   `python tools/gen_docs_reference.py --check` konča z 1, kadar je zapisana stran zastarela.
2. **Seznam sprememb.** `git log v<VERSION>..HEAD --oneline`, kjer je `<VERSION>` zadnja izdana
   različica (datoteka `VERSION` ob izdaji). Vsaka nova funkcija, možnost in izhodni stolpec mora
   dobiti mesto na strani in vrstico v razdelku **Docs** datoteke
   [`CHANGELOG.md`](https://github.com/Holdi601/3DHeat-Ext-Squad/blob/main/CHANGELOG.md).
3. **Neodvisen pregled.** Nekdo, ki strani ni pisal, prebere README in vsako spremenjeno stran, vključno
   s slikami, trikrat: kot začetnik, ki še nikoli ni uporabljal terminala, kot osemletnik in kot strokovnjak,
   ki vsako možnost preveri z `--help`. Primeri uporabljajo samo izmišljena imena in števila.
4. **Popravi** vse, kar pregled najde.
5. **Prevodi.** Vsaka prevedena stran hrani zgoščeno vrednost angleške strani, iz katere je nastala.
   Ponovno prevedi strani, katerih angleški vir se je spremenil, nato pregledaj vsak jezik: jasno besedilo,
   pravilne oznake na diagramih, iste besede kot prevedeni vmesnik pregledovalnika 3DHeat.
6. **Zaženi teste** (`pytest`).
7. **Objavi** samo z dovoljenjem lastnika.

## Prevodi: ukazi {#translations-the-commands}

Stran je prevedena v 40 jezikov pregledovalnika 3DHeat: angleščina je v `docs/`, vsak drug jezik v
`docs/<jezik>/` z istimi imeni datotek. `tools/docs_i18n.py` vodi evidenco:

```bash
python tools/docs_i18n.py hashes             # po vsaki spremembi angleščine: zapiši zgoščeno vrednost vsake strani
python tools/docs_i18n.py svg-strings        # po vsaki spremembi slike: oznake za prevod
python tools/docs_i18n.py status             # po jeziku: aktualne, zastarele, manjkajoče strani
python tools/docs_i18n.py todo --lang de     # nemške strani za (ponovni) prevod
python tools/docs_i18n.py svg-build --lang de    # nemške slike iz docs/assets/i18n/svg/de.json
python tools/docs_i18n.py finish --lang de   # označi nemške strani z zgoščeno vrednostjo angleške
python tools/docs_i18n.py check              # konča z 1, kadar so zgoščene vrednosti ali oznake zastarele
```

Prevedi samo tisto, kar navaja `todo`: ohrani Markdown, povezave, kodo, imena datotek in stolpcev; prevedi
naslove in opise slik; za gumbe in plošče uporabi besede samega pregledovalnika 3DHeat (njegov
`src/i18n/locales/<jezik>/`). Ustvarjene strani priročnikov in slike terminala ostanejo v angleščini. Na
spletnem mestu zastarel prevod to pove in povezuje angleško stran; manjkajoča stran se prikaže v angleščini.
Jezikovni meni v glavi in preusmeritev domače strani glede na jezik brskalnika prihajata iz `docs/_includes/`.
