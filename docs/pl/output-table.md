---
title: "Tabela"
nav_order: 4
lang: "pl"
source: output-table.md
source_hash: "0f3cfed1c108"
nav_exclude: true
search_exclude: true
---
# Tabela: `<demo>.parquet` {#the-table-parquet}

Jeden wiersz na próbkę lub zdarzenie. Próbka jest pobierana zawsze, gdy serwer replikował
ruch aktora, do 8 razy na sekundę (tempo nagrywania dema), gdy aktor się porusza.

![Pierwsze wiersze tabeli syntetycznego dema](../assets/img/table.svg)

## Kolumny {#columns}

| Kolumna | Co to jest |
|---|---|
| `time` | sekundy od rozpoczęcia nagrania |
| `x`, `y`, `z` | pozycja w jednostkach Unreal (centymetrach), Z w górę |
| `dirX`, `dirY`, `dirZ` | dokąd patrzy żołnierz: obrót ciała w poziomie (yaw) i pochylenie widoku jako wektor jednostkowy (pojazd: poziomo) |
| `yaw`, `pitch` | to samo w stopniach; `pitch` to kąt w górę od horyzontu, tylko dla żołnierzy |
| `health` | zdrowie żołnierza, bota albo pojazdu w tym momencie, o ile serwer je wysłał (zdrowie żołnierza schodzi poniżej 0, gdy jest ranny) |
| `speed` | replikowana prędkość, cm/s |
| `player` | nazwa gracza; `bot <id>` dla bota; dla pojazdu albo elementu rozstawianego, którego nikt nie posiada, jego klasa; dla strzału z broni pojazdu gracz siedzący w tym pojeździe |
| `team`, `faction` | numer drużyny w Squad (1, 2) i jej ustawienie frakcji, **w tym momencie**: gracze mogą zmieniać strony |
| `squad` | numer sekcji, -1 gdy gracz nie jest w sekcji |
| `event` | czym jest wiersz (poniżej) |
| `pawn` | pawn żołnierza (`SQSquidBot` dla bota), pojazd, a dla `fire` broń |
| `seat` | dla miejsca w wieżyczce lub pasażerskiego miejsca: własny pawn tego miejsca |
| `detail` | dla `fire` wywołanie broni, które umieściło strzał; dla `hit` rodzaj obrażeń; dla `removed` powód zamknięcia kanału (`Destroyed`, `Dormancy`...) |
| `entity` | aktor, którego dotyczy wiersz (jego net GUID): `entity` wierszy plików towarzyszących |
| `match` | nazwa dema |

## Zdarzenia {#events}

| `event` | Na wierszu | Co to |
|---|---|---|
| `position` | żołnierz lub bot pieszo | próbka ruchu |
| `vehicle` | żołnierz w pojeździe lądowym albo helikopterze | próbka w pozycji pojazdu |
| `wounded`, `revived`, `death` | żołnierze i boty | gdzie to się stało |
| `spawn`, `damaged`, `destroyed`, `removed` | pojazdy, elementy rozstawiane, stanowiska, skrzynie z amunicją, helikoptery | gdzie były |
| `seat` | gracz | zajął miejsce |
| `fire` | strzelec | strzał: skąd poleciał, jego kierunek jako `yaw`/`pitch`/`dirX..Z` |
| `hit` | pojazd | trafienie w pojazd: gdzie |

Jak odczytuje się zdarzenia, opisano w [Jak czytane jest demo](how-it-works.md#how-the-events-are-read).

## W przeglądarce {#in-the-viewer}

Stopka pliku Parquet niesie instrukcje odczytu pod kluczem `heat3d`: Z w górę,
żadna oś nie jest odbita lustrzanie, skala jednostkowa 1, więc przeglądarka nie potrzebuje
mapowania kolumn. Wczytaj tabelę w karcie Mapa cieplna; zobacz
[Wczytywanie danych](https://holdi601.github.io/3DHeat/getting-data-in.html)
i [Mapowanie kolumn](https://holdi601.github.io/3DHeat/column-mapping.html) w dokumentacji przeglądarki.
