---
title: Ta opp en demo
nav_order: 2
lang: no
source: recording.md
source_hash: "5139aa7d896f"
nav_exclude: true
search_exclude: true
---
# Ta opp en demo {#recording-a-demo}

Squad-demoer tas opp **på serveren**, ikke av spillklienten.

1. I serverens `Admins.cfg`, gi admin-gruppen tillatelsen `demos`.
2. I spillets konsoll, kjør `AdminDemoRec <name>` når kampen starter.
   En admin må skrive dette i selve spillet; én rapport sier at RCON ikke godtar det.
3. Spill kampen, kjør deretter `AdminDemoStop`.
4. Demoen skrives til `<server>/SquadGame/Saved/Demos/<name>.replay`.
   Kopier den fra serveren til maskinen som konverterer den.

`Server.cfg` har også en innstilling `RecordDemos`, av som standard. Regn med omtrent
70 til 80 MB per time for en liten kamp; størrelsen for en full server med 100 spillere
er ikke målt.

En demo holder navnene og nettidentiteten til alle på serveren: behandle den som
personopplysninger ([Begrensninger, oppdateringer og vilkår](limits.md#personal-data)).

Neste: [Konverter demoer](converting.md).
