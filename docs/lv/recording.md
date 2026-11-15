---
title: Demo ierakstīšana
nav_order: 2
lang: "lv"
source: recording.md
source_hash: "5139aa7d896f"
nav_exclude: true
search_exclude: true
---
# Demo ierakstīšana {#recording-a-demo}

Squad demo tiek ierakstīti **serverī**, nevis ar spēles klientu.

1. Servera `Admins.cfg` failā dod administratora grupai atļauju `demos`.
2. Spēles konsolē, kad mačs sākas, palaidiet `AdminDemoRec <name>`.
   Administratoram šo jāieraksta pašā spēlē; viens ziņojums vēsta, ka RCON to nepieņem.
3. Nospēlējiet maču, tad palaidiet `AdminDemoStop`.
4. Demo tiek saglabāts `<server>/SquadGame/Saved/Demos/<name>.replay`.
   Nokopējiet to no servera uz datoru, kurā to konvertēsiet.

`Server.cfg` ir arī iestatījums `RecordDemos`, pēc noklusējuma izslēgts. Mazam
maču sagaidiet apmēram 70 līdz 80 MB stundā; pilna 100 spēlētāju servera izmērs nav izmērīts.

Demo satur visu servera spēlētāju vārdus un tiešsaistes ID: traktējiet to kā personas datus
([Ierobežojumi, atjauninājumi un noteikumi](limits.md#personal-data)).

Tālāk: [Demo konvertēšana](converting.md).
