---
title: "Dokument meczu i pliki towarzyszące"
nav_order: 5
lang: pl
source: output-match.md
source_hash: "715bd3417e47"
nav_exclude: true
search_exclude: true
---
# Dokument meczu i pliki towarzyszące {#the-match-document-and-sidecars}

Obok tabeli każde demo dostaje `<demo>.match.json` i dwa pliki towarzyszące,
`<demo>.entities.parquet` i `<demo>.packets.parquet`. Przeglądarka czyta dokument meczu
w swojej karcie Mecz.

## Dokument meczu {#the-match-document}

`<demo>.match.json` (dokument meczu) zawiera na najwyższym poziomie `map`, `layer`, `level_path`, `game_version`, `engine_version`, `recorded_unix`, `duration_s`, `teams`, `squads`, `game_state`, `actors`, `players`, `rows`, `events`, `not_read`, `file`, `header`, `chunks`, `stream`, `shots` i `selfCheck` (pełna lista: [Opis poleceń](../cli-reference.md)). Słownie: mapa i warstwa, wersje gry i silnika, czas nagrania, długość oraz:

- **drużyny**: numer, frakcja i wszystko, co ich stan replikował (bilety, dostępności, dowódca), w miarę zmian;
- **sekcje**: numer, drużyna, nazwa, twórca, dowódca, członkowie;
- **stan gry**: nazwa serwera i ustawienia, tryb gry, stan meczu i jego identyfikator, rotacje map i poziomów, głosowania, zegary, komunikat dnia;
- **aktorzy**: każdy pojazd, element rozstawiany, stanowisko, skrzynia z amunicją i helikopter - klasa, miejsce i czas pojawienia się, kiedy zniknął, czyj był oraz jego replikowany stan (zdrowie, stan budowy, miejsca...);
- **wiersz dla każdego gracza**: próbki pieszo i w pojazdach, przebyty dystans, grane klasy żołnierzy, użyte pojazdy, zmiany drużyny, zajęte miejsca oraz wszystko, co replikował stan gracza (ping, poziom, rola, aktualne miejsce...); oraz wiersz dla każdego bota;
- **zdarzenia** policzone, **spis właściwości** (jak często wysyłano właściwości każdej klasy) i **spis zdalnych wywołań**, strzały i trafienia, to, czego **nie odczytano**, oraz diagnostykę czytnika;
- **plik i nagłówek**: każde pole bloku informacyjnego i nagłówka dema, tabelę fragmentów, tabele eksportu pól sieciowych (`net_field_exports`), powody zamknięcia kanałów oraz klasy znalezione dla obiektów, których eksporty nie nazywają (`stream.class_resolution`);
- **samosprawdzenie** (`selfCheck.completeness`, zob. [Kompletność](#completeness)).

Identyfikatory online (Steam, EOS) są celowo pominięte.

Szybki podgląd przekonwertowanego dema:

```bash
python -c "import json; d = json.load(open('out/<map>/<demo>.match.json')); print(d['map'], d['layer'], d['duration_s'], len(d['players']))"
```

## Kompletność {#completeness}

Ten czytnik stosuje zasadę, której trzymają się wszystkie konwertery 3DHeat: odczytaj to, co da się odczytać teraz, resztę zachowaj w całości i powiedz, ile z każdego rodzaju zostało zachowane ([Konwertery zachowują wszystko](https://github.com/Holdi601/3DHeat/blob/main/docs/converters.md)). Każdy dokument meczu ma `selfCheck.completeness`: dla każdego typu elementu napotkanego w demie liczbę `seen` (widziane), `decoded` (odczytane), `partial` (odczytane po części i zachowane w całości), `raw` (zachowane tylko w całości) oraz `lost` (musi być 0). Typy są liczone tam, gdzie czytnik je napotyka: `file.info`, `chunk.<kind>`, `frame`, `packet`, `bunch`, `open`, `close`, `export.field`, `export.guid`, `external`, `property:<class>`, `rpc:<class>`, `block:<object>`, `subobject.*`.

W prawdziwych odczytanych demach `lost` wynosi 0: ich elementów jest od setek tysięcy do milionów; około połowa odczytuje się w całości, reszta częściowo albo jako surowe dane.

**Odczytane** (do tabeli i dokumentu meczu):

- blok informacyjny, nagłówek dema (każde pole; dwa nieznane końcowe bajty są zachowane jako hex), tabela fragmentów;
- każda ramka, pakiet i wiązka (rozbite w całości na to, co niosą), każdy otwarty aktor (z miejscem pojawienia się, obrotem, skalą i prędkością) i każdy zamknięty (z powodem: `Destroyed`, `Dormancy`...);
- każda replikowana właściwość, o ile jej bity na to pozwalają ([Dekodowanie właściwości](how-it-works.md#decoding-properties)), pozycje z `FRepMovement` i z komponentu ruchu helikopterów, ofiary, zdrowie pojazdów, miejsca;
- każde zdalne wywołanie po nazwie, z jego parametrami, gdy demo eksportuje grupę funkcji: strzały (`fire`) i trafienia w pojazdy (`hit`) do tabeli;
- tabele eksportu pól sieciowych i identyfikatory net GUID (ich liczba; ścieżki są w pliku towarzyszącym entities).

**Zachowane surowe** (w całości, z tym, co odczytano, obok):

- `<demo>.entities.parquet`, kolumny `time`, `type` (`<class>.<property>`, `<class>.<call>` albo nazwa obiektu), `name` (klasa aktora), `entity` (net GUID aktora, jako `entity` tabeli), `kind`, `object` (podobiekt), `channel`, `handle`, `group` (ścieżka klasy grupy eksportu), `decoded` (JSON), `bits` i `payload` (bity, od najniższego, dopełnione do pełnych bajtów):
  - każda aktualizacja właściwości (`kind` `property`), także ruch, z tym, co odczytano; surowo tylko tam, gdzie nic nie da się odczytać (nienazwane uchwyty, struktury, np. `RotationReplicatedMovement` wież, oraz właściwości zostawione jako bity);
  - każde zdalne wywołanie i pole niestandardowej delty (`rpc`), parametry odczytane, gdy grupa funkcji została wyeksportowana; surowo tam, gdzie nie (`RepInventory`, `PlayerStateData`);
  - każda treść bloku obiektu, którego klasy nie dało się znaleźć (`block`: `Buoyancy`, `GameplayTasksComponent`, `AmmoRackComponent`...), z odczytanym nagłówkiem;
  - każdy kanał aktora otwarty i zamknięty (`open`, `close`), każdy podobiekt usunięty lub zniszczony;
  - kontekst potrzebny późniejszemu dekoderowi, by odczytać sam plik: każde pole eksportu sieciowego (`export.field`: ścieżka grupy, uchwyt, nazwa właściwości, suma kontrolna) i każdy wyeksportowany net GUID (`export.guid`: jego ścieżka, obiekt nadrzędny i flagi), w chwili, w której strumień je przekazał.
- `<demo>.packets.parquet`, kolumny `time`, `type`, `name`, `channel`, `offset` (w pliku), `decoded`, `bits`, `payload`: blok informacyjny, blok nagłówka, każdy blok punktu kontrolnego (punkt kontrolny to stan każdego aktora w danej chwili, którego strumień od początku też dostarcza), każdy blok zdarzeń oraz każda ramka, pakiet lub wiązka, która się nie odczytuje (jedna wiązka na demo: otwierająca wiązka spectatora nagrywającego), w całości.

Wiersze entities są pogrupowane według `kind`, `type` i `entity`, każda grupa w kolejności czasu; sortuj po `time`, by uzyskać kolejność strumienia.

**Niedostępne:**

- to, czego serwer nie nagrywa w demie: wejścia klientów, to, co widział gracz;
- efekty po stronie klienta: znaczniki trafień, dźwięki, tekst tablicy zabójstw (serwer wysyła wywołania, nie ich wyświetlanie);
- odszyfrowane identyfikatory online: zachowane tylko jako bity (zob. [Dane osobowe](limits.md#personal-data)).
