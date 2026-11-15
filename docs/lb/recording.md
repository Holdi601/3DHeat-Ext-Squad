---
title: "Eng Demo ophuelen"
nav_order: 2
lang: "lb"
source: recording.md
source_hash: "5139aa7d896f"
nav_exclude: true
search_exclude: true
---
# Eng Demo ophuelen {#recording-a-demo}

Squad-Demoe ginn **um Server** opgeholl, net vum Spillclient.

1. An der `Admins.cfg` vum Server der Grupp vum Admin d'`demos`-Recht
   ginn.
2. An der Konsol vum Spill `AdminDemoRec <name>` ausféieren, wann de Match ufänkt.
   Een Admin muss dat am Spill selwer tippen; ee Bericht seet, RCON
   akzeptéiert et net.
3. De Match spillen, dann `AdminDemoStop` ausféieren.
4. D'Demo gëtt op `<server>/SquadGame/Saved/Demos/<name>.replay` geschriwwen.
   Kopéiert se vum Server op de Rechner, deen se konvertéiert.

D'`Server.cfg` huet och eng `RecordDemos`-Astellung, standardméisseg aus. Rechent mat ongeféier
70 bis 80 MB pro Stonn fir e klenge Match; d'Gréisst fir e vollen
Server mat 100 Spiller ass net gemooss ginn.

Eng Demo hält d'Nimm an Online-IDen vun allen um Server: behandelt se als
perséinlech Daten ([Grenzen, Updates a Bedingungen](limits.md#personal-data)).

Als Nächst: [Demoe konvertéieren](converting.md).
