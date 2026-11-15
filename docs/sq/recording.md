---
title: "Regjistrimi i një demoje"
nav_order: 2
lang: "sq"
source: recording.md
source_hash: "5139aa7d896f"
nav_exclude: true
search_exclude: true
---
# Regjistrimi i një demoje {#recording-a-demo}

Demot e Squad regjistrohen **në server**, jo nga klienti i lojës.

1. Në `Admins.cfg` të serverit, jepi grupit të adminit lejen `demos`.
2. Në konsolën e lojës, ekzekuto `AdminDemoRec <name>` kur fillon ndeshja.
   Një admin duhet ta shkruajë këtë brenda vetë lojës; një raport thotë se RCON
   nuk e pranon.
3. Luaj ndeshjen, pastaj ekzekuto `AdminDemoStop`.
4. Demo shkruhet te `<server>/SquadGame/Saved/Demos/<name>.replay`.
   Kopjoje nga serveri te kompjuteri që e konverton.

`Server.cfg` ka edhe një cilësim `RecordDemos`, të çaktivizuar si parazgjedhje. Prit
afërsisht 70 deri 80 MB në orë për një ndeshje të vogël; madhësia për një server të plotë
me 100 lojtarë nuk është matur.

Një demo përmban emrat dhe ID-të online të të gjithëve në server: trajtoje si
të dhëna personale ([Kufizimet, përditësimet dhe kushtet](limits.md#personal-data)).

Më pas: [Konvertimi i demove](converting.md).
