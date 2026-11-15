---
title: "Snimanje demoa"
nav_order: 2
lang: "bs"
source: recording.md
source_hash: "5139aa7d896f"
nav_exclude: true
search_exclude: true
---
# Snimanje demoa {#recording-a-demo}

Squad demoi se snimaju **na serveru**, a ne u klijentu igre.

1. U serverskoj datoteci `Admins.cfg` daj grupi administratora dozvolu
   `demos`.
2. U konzoli igre pokreni `AdminDemoRec <name>` kad meč počne.
   Administrator ovo mora upisati u samoj igri; jedan izvještaj kaže da RCON
   to ne prihvata.
3. Odigraj meč, pa pokreni `AdminDemoStop`.
4. Demo se piše u `<server>/SquadGame/Saved/Demos/<name>.replay`.
   Kopiraj ga sa servera na računar koji ga pretvara.

`Server.cfg` ima i postavku `RecordDemos`, koja je zadano isključena. Računaj otprilike
70 do 80 MB po satu za mali meč; veličina za pun server sa 100 igrača
nije mjerena.

Demo sadrži imena i online ID-ove svih na serveru: tretiraj ga kao lične
podatke ([Ograničenja, ažuriranja i uvjeti](limits.md#personal-data)).

Dalje: [Pretvaranje demoa](converting.md).
