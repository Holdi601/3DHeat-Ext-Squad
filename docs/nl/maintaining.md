---
title: Deze documentatie onderhouden
nav_order: 91
lang: "nl"
source: maintaining.md
source_hash: "b0b7836a5545"
nav_exclude: true
search_exclude: true
---
# Deze documentatie onderhouden {#maintaining-these-docs}

Een checklist per release, zodat de pagina's nooit achterlopen op de code.

1. **Regenereer de referentie.** `python tools/gen_docs_reference.py` schrijft
   [Commandoreferentie](../cli-reference.md) opnieuw uit de eigen `--help` van het programma en
   de uitvoerkolommen. `python tools/gen_docs_reference.py --check` eindigt met 1 wanneer
   de vastgelegde pagina verouderd is.
2. **Noteer wat er veranderd is.** `git log v<VERSION>..HEAD --oneline`, waarbij
   `<VERSION>` de laatst uitgebrachte versie is (het bestand `VERSION` bij de release). Geef elke
   nieuwe functie, optie en uitvoerkolom een plek op een pagina, en een rij in het onderdeel **Docs** van
   [`CHANGELOG.md`](https://github.com/Holdi601/3DHeat-Ext-Squad/blob/main/CHANGELOG.md).
3. **Onafhankelijke controle.** Iemand die de pagina's niet schreef, leest de
   README en elke gewijzigde pagina, de afbeeldingen inbegrepen, drie keer: als beginner
   die nog nooit een terminal gebruikte, als een kind van acht, en als expert die elke optie
   controleert tegen `--help`. Voorbeelden gebruiken alleen verzonnen namen en getallen.
4. **Herstel** alles wat de controle vindt.
5. **Vertalingen.** Elke vertaalde pagina onthoudt de hash van de Engelse pagina waaruit ze
   is gemaakt. Vertaal opnieuw de pagina's waarvan de Engelse bron is veranderd,
   en controleer daarna elke taal: heldere tekst, juiste labels in de diagrammen, dezelfde
   woorden als de vertaalde interface van de viewer zelf.
6. **Draai de tests** (`pytest`).
7. **Publiceer** pas na de akkoordverklaring van de eigenaar.

## Vertalingen: de commando's {#translations-the-commands}

De site is vertaald naar de 40 talen van de interface van de 3DHeat-viewer: Engels in `docs/`, elke andere
taal in `docs/<lang>/` met dezelfde bestandsnamen. `tools/docs_i18n.py` houdt de administratie bij:

```bash
python tools/docs_i18n.py hashes             # na elke Engelse wijziging: de hash van elke pagina vastleggen
python tools/docs_i18n.py svg-strings        # na elke wijziging aan een afbeelding: de labels om te vertalen
python tools/docs_i18n.py status             # per taal: actueel, verouderd, ontbrekende pagina's
python tools/docs_i18n.py todo --lang de     # de Duitse pagina's om (opnieuw) te vertalen
python tools/docs_i18n.py svg-build --lang de    # Duitse afbeeldingen uit docs/assets/i18n/svg/de.json
python tools/docs_i18n.py finish --lang de   # de Duitse pagina's stempelen met hun Engelse hash
python tools/docs_i18n.py check              # eindigt met 1 wanneer hashes of labels verouderd zijn
```

Vertaal alleen wat `todo` aangeeft: laat Markdown, links, code, bestands- en kolomnamen staan,
vertaal titels en beschrijvingen van afbeeldingen, en gebruik de eigen woorden van de 3DHeat-viewer voor
zijn knoppen en panelen (zijn `src/i18n/locales/<lang>/`). Gegenereerde referentiepagina's en
terminalafbeeldingen blijven Engels. Op de site zegt een verouderde vertaling dat zelf en
verwijst naar de Engelse pagina; een ontbrekende valt terug op Engels. Het taalmenu in de
kop en de doorverwijzing van de startpagina op basis van de browsertaal komen uit `docs/_includes/`.
