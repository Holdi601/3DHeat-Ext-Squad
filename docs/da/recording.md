---
title: Optag en demo
nav_order: 2
lang: da
source: recording.md
source_hash: "5139aa7d896f"
nav_exclude: true
search_exclude: true
---
# Optag en demo {#recording-a-demo}

Squad-demoer optages **på serveren**, ikke af spilklienten.

1. I serverens `Admins.cfg` giver du admingruppen tilladelsen `demos`.
2. I spillets konsol kører du `AdminDemoRec <name>`, når kampen starter.
   En admin skal skrive dette i selve spillet; en rapport siger, at RCON
   ikke accepterer det.
3. Spil kampen, og kør derefter `AdminDemoStop`.
4. Demoen skrives til `<server>/SquadGame/Saved/Demos/<name>.replay`.
   Kopiér den fra serveren til den maskine, der konverterer den.

`Server.cfg` har også en indstilling `RecordDemos`, som er slået fra som standard. Regn med
cirka 70 til 80 MB i timen for en lille kamp; størrelsen for en fuld server med 100 spillere
er ikke målt.

En demo indeholder navnene og online-id'erne på alle på serveren: behandl den som
personlige data ([Begrænsninger, opdateringer og vilkår](limits.md#personal-data)).

Næste: [Konverter demoer](converting.md).
