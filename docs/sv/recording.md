---
title: Spela in en demo
nav_order: 2
lang: "sv"
source: recording.md
source_hash: "5139aa7d896f"
nav_exclude: true
search_exclude: true
---
# Spela in en demo {#recording-a-demo}

Squad-demos spelas in **på servern**, inte av spelklienten.

1. I serverns `Admins.cfg`, ge adminens grupp behörigheten `demos`.
2. I spelets konsol, kör `AdminDemoRec <name>` när matchen startar.
   En admin måste skriva det i spelet själv; en rapport säger att RCON inte godkänner det.
3. Spela matchen, kör sedan `AdminDemoStop`.
4. Demon skrivs till `<server>/SquadGame/Saved/Demos/<name>.replay`.
   Kopiera den från servern till datorn som konverterar den.

`Server.cfg` har också en inställning `RecordDemos`, av som standard. Räkna med ungefär
70 till 80 MB per timme för en liten match; storleken för en full server med 100 spelare har inte mätts.

En demo innehåller namn och online-ID:n för alla på servern: behandla den som personuppgifter
([Begränsningar, uppdateringar och villkor](limits.md#personal-data)).

Nästa steg: [Konvertera demos](converting.md).
