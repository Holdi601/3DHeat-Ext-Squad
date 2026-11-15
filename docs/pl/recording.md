---
title: "Nagrywanie dema"
nav_order: 2
lang: pl
source: recording.md
source_hash: "5139aa7d896f"
nav_exclude: true
search_exclude: true
---
# Nagrywanie dema {#recording-a-demo}

Dema Squad nagrywa się **na serwerze**, a nie w kliencie gry.

1. W pliku `Admins.cfg` serwera daj grupie administratora uprawnienie `demos`.
2. W konsoli gry wpisz `AdminDemoRec <name>`, gdy zaczyna się mecz.
   Administrator musi wpisać to w samej grze; jedno zgłoszenie mówi, że RCON tego nie przyjmuje.
3. Zagraj mecz, potem wpisz `AdminDemoStop`.
4. Demo zapisuje się w `<server>/SquadGame/Saved/Demos/<name>.replay`.
   Skopiuj je z serwera na komputer, na którym będziesz je konwertować.

`Server.cfg` ma też ustawienie `RecordDemos`, domyślnie wyłączone. Przy małym meczu
spodziewaj się około 70 do 80 MB na godzinę; rozmiar dla pełnego serwera na 100 graczy
nie został zmierzony.

Demo zawiera nazwy i identyfikatory online wszystkich graczy na serwerze: traktuj je jak dane osobowe
([Ograniczenia, aktualizacje i warunki](limits.md#personal-data)).

Dalej: [Konwersja dem](converting.md).
