---
title: Snimanje dema
nav_order: 2
lang: "hr"
source: recording.md
source_hash: "5139aa7d896f"
nav_exclude: true
search_exclude: true
---
# Snimanje dema {#recording-a-demo}

Squad demoi se snimaju **na serveru**, a ne u klijentu igre.

1. U serverskoj datoteci `Admins.cfg` dajte grupi administratora dopuštenje `demos`.
2. U konzoli igre pokrenite `AdminDemoRec <name>` kad počne meč.
   Administrator to mora upisati u samoj igri; jedno izvješće kaže da RCON to ne prihvaća.
3. Odigrajte meč, zatim pokrenite `AdminDemoStop`.
4. Demo se zapisuje u `<server>/SquadGame/Saved/Demos/<name>.replay`.
   Kopirajte ga sa servera na računalo na kojem ga pretvarate.

`Server.cfg` ima i postavku `RecordDemos`, isključenu prema zadanim postavkama. Za mali meč očekujte
otprilike 70 do 80 MB po satu; veličina za puni server sa 100 igrača nije izmjerena.

Demo sadrži imena i mrežne ID-jeve svih na serveru: postupajte s njim kao s osobnim podacima
([Ograničenja, ažuriranja i uvjeti](limits.md#personal-data)).

Dalje: [Pretvaranje dema](converting.md).
