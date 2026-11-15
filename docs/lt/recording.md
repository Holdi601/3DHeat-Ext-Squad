---
title: "Demo įrašymas"
nav_order: 2
lang: "lt"
source: recording.md
source_hash: "5139aa7d896f"
nav_exclude: true
search_exclude: true
---
# Demo įrašymas {#recording-a-demo}

Squad demo įrašomi **serveryje**, ne žaidimo kliento.

1. Serverio `Admins.cfg` faile suteikite administratorių grupei `demos`
   leidimą.
2. Žaidimo konsolėje paleiskite `AdminDemoRec <name>`, kai prasideda rungtynės.
   Tai turi įvesti administratorius pačiame žaidime; vienas pranešimas teigia, kad RCON to nepriima.
3. Sužaiskite rungtynes, tada paleiskite `AdminDemoStop`.
4. Demo įrašomas į `<server>/SquadGame/Saved/Demos/<name>.replay`.
   Nukopijuokite jį iš serverio į kompiuterį, kuriame jis bus konvertuojamas.

`Server.cfg` taip pat turi nustatymą `RecordDemos`, pagal numatytuosius išjungtą. Mažoms rungtynėms tikėkitės maždaug
70–80 MB per valandą; pilno 100 žaidėjų serverio dydis neišmatuotas.

Demo saugo visų serveryje esančių žmonių vardus ir prisijungimo ID: traktuokite jį kaip asmens duomenis
([Apribojimai, atnaujinimai ir sąlygos](limits.md#personal-data)).

Toliau: [Demo konvertavimas](converting.md).
