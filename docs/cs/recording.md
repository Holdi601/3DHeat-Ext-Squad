---
title: "Nahrávání dema"
nav_order: 2
lang: cs
source: recording.md
source_hash: "5139aa7d896f"
nav_exclude: true
search_exclude: true
---
# Nahrávání dema {#recording-a-demo}

Dema Squadu se nahrávají **na serveru**, ne klientem hry.

1. V souboru `Admins.cfg` na serveru dejte skupině administrátora oprávnění `demos`.
2. V konzoli hry spusťte `AdminDemoRec <name>`, když zápas začne.
   Musí to napsat administrátor přímo ve hře; podle jednoho hlášení RCON tento příkaz nepřijme.
3. Dohrajte zápas a spusťte `AdminDemoStop`.
4. Demo se zapíše do `<server>/SquadGame/Saved/Demos/<name>.replay`.
   Zkopírujte ho ze serveru na počítač, na kterém ho převedete.

Soubor `Server.cfg` má také nastavení `RecordDemos`, ve výchozím stavu vypnuté. U malého
zápasu počítejte zhruba s 70 až 80 MB za hodinu; velikost pro plný 100hráčový server
nebyla změřena.

Demo obsahuje jména a online ID všech na serveru: zacházejte s ním jako s osobními údaji
([Omezení, aktualizace a podmínky](limits.md#personal-data)).

Dále: [Převod dem](converting.md).
