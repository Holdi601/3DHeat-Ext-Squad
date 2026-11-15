---
title: "Dokumentaation ylläpito"
nav_order: 91
lang: fi
source: maintaining.md
source_hash: "b0b7836a5545"
nav_exclude: true
search_exclude: true
---
# Dokumentaation ylläpito {#maintaining-these-docs}

Julkaisukohtainen tarkistuslista, jotta sivut eivät koskaan jää jälkeen koodista.

1. **Viitteen uudelleenluonti.** `python tools/gen_docs_reference.py` kirjoittaa sivun
   [Komentoviite](../cli-reference.md) uudelleen ohjelman oman `--help`-tulosteen ja tulostesarakkeiden
   perusteella. `python tools/gen_docs_reference.py --check` päättyy tilaan 1, kun tallennettu sivu on
   vanhentunut.
2. **Listaa muutokset.** `git log v<VERSION>..HEAD --oneline`, missä `<VERSION>` on viimeisin julkaistu
   versio (tiedosto `VERSION` julkaisussa). Anna jokaiselle uudelle ominaisuudelle, asetukselle ja
   tulostesarakkeelle paikka sivulla ja rivi [`CHANGELOG.md`](https://github.com/Holdi601/3DHeat-Ext-Squad/blob/main/CHANGELOG.md)-tiedoston
   **Docs**-osiossa.
3. **Riippumaton tarkistus.** Joku, joka ei kirjoittanut sivuja, lukee README-tiedoston ja jokaisen muuttuneen
   sivun kuvineen kolme kertaa: aloittelijana, joka ei ole koskaan käyttänyt päätettä, kahdeksanvuotiaana ja
   asiantuntijana, joka tarkistaa jokaisen asetuksen `--help`-tulosteeseen. Esimerkeissä käytetään vain
   keksittyjä nimiä ja lukuja.
4. **Korjaa** kaikki, mitä tarkistus löytää.
5. **Käännökset.** Jokainen käännetty sivu tallentaa sen englanninkielisen sivun tiivisteen, josta se tehtiin.
   Käännä uudelleen ne sivut, joiden englanninkielinen lähde muuttui, ja tarkista sitten jokainen kieli:
   selkeä teksti, oikeat kaaviotunnisteet ja samat sanat kuin katselimen omassa käyttöliittymässä.
6. **Aja testit** (`pytest`).
7. **Työnnä** vain omistajan luvalla.

## Käännökset: komennot {#translations-the-commands}

Sivusto on käännetty 3DHeat-katselimen 40 kielelle: englanti kansiossa `docs/`, muut kielet kansiossa
`docs/<lang>/` samoilla tiedostonimillä. `tools/docs_i18n.py` hoitaa kirjanpidon:

```bash
python tools/docs_i18n.py hashes             # jokaisen englanninkielisen muutoksen jälkeen: tallenna jokaisen sivun tiiviste
python tools/docs_i18n.py svg-strings        # kuvamuutoksen jälkeen: käännettävät tunnisteet
python tools/docs_i18n.py status             # kielikohtaisesti: ajantasaiset, vanhentuneet, puuttuvat sivut
python tools/docs_i18n.py todo --lang de     # saksankieliset sivut, jotka pitää (uudelleen)kääntää
python tools/docs_i18n.py svg-build --lang de    # saksankieliset kuvat tiedostosta docs/assets/i18n/svg/de.json
python tools/docs_i18n.py finish --lang de   # leimaa saksankieliset sivut englanninkielisen tiivisteensä kanssa
python tools/docs_i18n.py check              # päättyy tilaan 1, kun tiivisteet tai tunnisteet ovat vanhentuneet
```

Käännä vain se, minkä `todo` listaa: säilytä Markdown, linkit, koodi sekä tiedosto- ja sarakenimet
sellaisina kuin ne ovat, käännä otsikot ja kuvakuvaukset sekä käytä katselimen omia sanoja sen
painikkeille ja paneeleille (sen `src/i18n/locales/<lang>/`). Luodut viitesivut ja päätekuvat
pysyvät englanninkielisinä. Sivustolla vanhentunut käännös kertoo sen ja linkittää englanninkieliseen
sivuun; puuttuva sivu palautuu englantiin. Otsikon kielivalikko ja etusivun selaimen kielen mukainen
uudelleenohjaus tulevat kansiosta `docs/_includes/`.
