---
title: "Demon tallentaminen"
nav_order: 2
lang: fi
source: recording.md
source_hash: "5139aa7d896f"
nav_exclude: true
search_exclude: true
---
# Demon tallentaminen {#recording-a-demo}

Squad-demot tallennetaan **palvelimella**, ei pelaajan asiakasohjelmalla.

1. Anna palvelimen `Admins.cfg`-tiedostossa ylläpitäjäryhmälle `demos`-oikeus.
2. Kirjoita pelin konsoliin `AdminDemoRec <name>`, kun ottelu alkaa.
   Ylläpitäjän on kirjoitettava tämä itse pelissä; yhden raportin mukaan RCON ei hyväksy sitä.
3. Pelaa ottelu, sitten suorita `AdminDemoStop`.
4. Demo kirjoitetaan tiedostoon `<server>/SquadGame/Saved/Demos/<name>.replay`.
   Kopioi se palvelimelta koneelle, jolla muunnat sen.

`Server.cfg`-tiedostossa on myös asetus `RecordDemos`, joka on oletuksena pois päältä.
Odota noin 70–80 Mt tunnissa pienelle ottelulle; täyden 100 pelaajan palvelimen koko
ei ole mitattu.

Demo sisältää kaikkien palvelimella olevien nimet ja verkkotunnukset: käsittele sitä
henkilötietona ([Rajoitukset, päivitykset ja ehdot](limits.md#personal-data)).

Seuraavaksi: [Demojen muuntaminen](converting.md).
