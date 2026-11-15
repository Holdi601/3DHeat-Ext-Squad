---
title: "Nahrávanie dema"
nav_order: 2
lang: "sk"
source: recording.md
source_hash: "5139aa7d896f"
nav_exclude: true
search_exclude: true
---
# Nahrávanie dema {#recording-a-demo}

Dema Squad sa nahrávajú **na serveri**, nie klientom hry.

1. V súbore `Admins.cfg` na serveri dajte skupine administrátora oprávnenie `demos`.
2. V konzole hry spustite `AdminDemoRec <name>`, keď sa zápas začne.
   Tento príkaz musí napísať administrátor priamo v hre; podľa jednej správy ho RCON neprijme.
3. Odohrajte zápas a potom spustite `AdminDemoStop`.
4. Demo sa zapíše do `<server>/SquadGame/Saved/Demos/<name>.replay`.
   Skopírujte ho zo servera na počítač, na ktorom ho budete prevádzať.

`Server.cfg` má aj nastavenie `RecordDemos`, predvolene vypnuté. Pri malom zápase čakajte
približne 70 až 80 MB za hodinu; veľkosť pre plný server so 100 hráčmi nebola zmeraná.

Demo obsahuje mená a online identifikátory všetkých na serveri: zaobchádzajte s ním ako s osobnými údajmi
([Obmedzenia, aktualizácie a podmienky](limits.md#personal-data)).

Ďalej: [Prevod dem](converting.md).
