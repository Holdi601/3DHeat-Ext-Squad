---
title: "Demo salvestamine"
nav_order: 2
lang: et
source: recording.md
source_hash: "5139aa7d896f"
nav_exclude: true
search_exclude: true
---
# Demo salvestamine {#recording-a-demo}

Squadi demod salvestatakse **serveril**, mitte mängu kliendi poolt.

1. Serveri `Admins.cfg`-s anna admini grupile luba `demos`.
2. Mängu konsoolis käivita `AdminDemoRec <name>`, kui mäng algab.
   Admin peab selle käsu ise mängus kirjutama; üks teade ütleb, et RCON seda ei võta vastu.
3. Mängi mäng läbi, seejärel käivita `AdminDemoStop`.
4. Demo kirjutatakse faili `<server>/SquadGame/Saved/Demos/<name>.replay`.
   Kopeeri see serverist masinasse, kus seda teisendad.

`Server.cfg`-s on ka säte `RecordDemos`, vaikimisi väljas. Väikese mängu puhul on see umbes 70 kuni 80 MB tunnis; täis 100-mängijaga serveri suurust ei ole mõõdetud.

Demo sisaldab kõigi serveril olevate inimeste nimesid ja veebi-ID-sid: kohtle seda isikuandmetena
([Piirangud, uuendused ja tingimused](limits.md#personal-data)).

Edasi: [Demode teisendamine](converting.md).
