---
title: "Konwersja dem"
nav_order: 3
lang: pl
source: converting.md
source_hash: "e8c77423085b"
nav_exclude: true
search_exclude: true
---
# Konwersja dem {#converting-demos}

```text
heat3d-squad-demo <demos or folders> -o <folder> [--flat] [--json]
python -m heat3d_ext_squad ...          to samo, bez instalowania
```

## Krok po kroku {#step-by-step}

Nigdy nie używałeś wiersza poleceń? Najpierw przeczytaj [Zanim zaczniesz](before-you-start.md).

1. Zainstaluj raz: `git clone https://github.com/Holdi601/3DHeat-Ext-Squad`,
   otwórz terminal w tym folderze i uruchom `python -m pip install -e .`
   (Python 3.10 lub nowszy; instaluje też pyarrow i numpy).
2. Włóż pliki `.replay` do jednego folderu albo podaj je po kolei.
3. Uruchom `heat3d-squad-demo <folder> -o out`.
4. Zobaczysz jedną linię na każde demo: jego warstwę, graczy i wiersze oraz to, gdzie zapisano tabelę. Każde demo staje się czterema luźnymi plikami w `out/<map>/` (nie kontenerem `.3dheat`); wczytaj `.parquet` w przeglądarce 3DHeat.

![Uruchomienie na syntetycznym demie](../assets/img/run.svg)

Obrazek pokazuje uruchomienie na demie, które budują testy (`tests/test_stream.py`),
a nie na prawdziwym meczu.

## Opcje {#options}

| Opcja | Domyślnie | Co robi |
|---|---|---|
| `demos` (jedno lub więcej) | - | pliki `.replay` albo foldery, w których one leżą |
| `-o`, `--out` | wymagane | folder docelowy; każde demo trafia do `<out>/<map>/` |
| `--flat` | wyłączone | zapisuje prosto do folderu, bez podfolderu `<map>/` |
| `--json` | wyłączone | wypisuje na standardowe wyjście jedną linię JSON na demo (dla programów, które wywołują to polecenie): `demo`, `ok`, `parquet`, `match`, `sidecars`, `lost`, `rows`, `players`, `layer`, `recorded_unix`; demo, które się nie udało, wypisuje `demo`, `ok: false` i `error` |
| `--version` | - | wypisuje wersję i kończy działanie |

Każda opcja, tak jak ją wypisuje program: [Opis poleceń](../cli-reference.md).

Nazwa folderu mapy to nazwa mapy wzięta ze ścieżki poziomu, którą podaje demo
(`/Game/Maps/<Map>/Gameplay_Layers/<Layer>` daje `<Map>`).

Kod wyjścia: 0, gdy każde demo zostało przekonwertowane; 1, gdy któreś się nie udało
(pozostałe i tak są zapisane) albo gdy nie znaleziono żadnego pliku `.replay`.

## Co powstaje {#what-comes-out}

| Plik | Co zawiera |
|---|---|
| `<demo>.parquet` | tabela: pozycje i zdarzenia, po jednym wierszu każde ([Tabela](output-table.md)) |
| `<demo>.match.json` | dokument meczu ([Dokument meczu](output-match.md)) |
| `<demo>.entities.parquet` | plik towarzyszący: każda aktualizacja właściwości i każde zdalne wywołanie, w całości |
| `<demo>.packets.parquet` | plik towarzyszący: fragmenty pliku i wszystko, czego nie udało się odczytać, w całości |

Tabela i dokument meczu to ta sama para, którą zapisuje narzędzie 3DHeat CS2.
Przeglądarka otwiera tabelę bezpośrednio, a pliki towarzyszące pomija, gdy wczytuje cały folder.

## Przykłady {#examples}

```bash
heat3d-squad-demo D:\SquadDemos -o out                 # każde demo w folderze
heat3d-squad-demo one.replay two.replay -o out --flat  # prosto do out/
heat3d-squad-demo D:\SquadDemos -o out --json          # jedna linia JSON na demo
```

`D:\SquadDemos` to przykładowy folder na dysku D: użyj własnego.
