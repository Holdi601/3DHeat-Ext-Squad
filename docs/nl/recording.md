---
title: Een demo opnemen
nav_order: 2
lang: "nl"
source: recording.md
source_hash: "5139aa7d896f"
nav_exclude: true
search_exclude: true
---
# Een demo opnemen {#recording-a-demo}

Squad-demo's worden **op de server** opgenomen, niet door de spelclient.

1. Geef in `Admins.cfg` van de server de groep van de beheerder de rechten `demos`.
2. Typ in de spelconsole `AdminDemoRec <name>` zodra de wedstrijd begint.
   Een beheerder moet dit in het spel zelf typen; één melding zegt dat RCON het niet accepteert.
3. Speel de wedstrijd, en typ dan `AdminDemoStop`.
4. De demo wordt geschreven naar `<server>/SquadGame/Saved/Demos/<name>.replay`.
   Kopieer hem van de server naar de computer waarop je hem omzet.

`Server.cfg` heeft ook een instelling `RecordDemos`, standaard uit. Reken op ongeveer
70 tot 80 MB per uur voor een kleine wedstrijd; de grootte voor een volledige server met 100 spelers
is niet gemeten.

Een demo bevat de namen en online-id's van iedereen op de server: behandel hem als
persoonsgegevens ([Beperkingen, updates en voorwaarden](limits.md#personal-data)).

Volgende: [Demo's omzetten](converting.md).
