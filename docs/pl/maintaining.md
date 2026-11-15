---
title: "Utrzymanie tych stron"
nav_order: 91
lang: pl
source: maintaining.md
source_hash: "b0b7836a5545"
nav_exclude: true
search_exclude: true
---
# Utrzymanie tych stron {#maintaining-these-docs}

Lista kontrolna przy każdym wydaniu, żeby strony nigdy nie zostawały w tyle za kodem.

1. **Wygeneruj ponownie opis poleceń.** `python tools/gen_docs_reference.py` przepisuje
   [Opis poleceń](../cli-reference.md) na podstawie własnej pomocy programu (`--help`) i kolumn wyjścia.
   `python tools/gen_docs_reference.py --check` kończy się kodem 1, gdy zapisana strona jest nieaktualna.
2. **Wypisz, co się zmieniło.** `git log v<VERSION>..HEAD --oneline`, gdzie `<VERSION>` to ostatnia wydana wersja
   (plik `VERSION` z wydania). Każda nowa funkcja, opcja i kolumna wyjścia ma mieć miejsce na stronie
   i wiersz w sekcji **Docs** pliku [`CHANGELOG.md`](https://github.com/Holdi601/3DHeat-Ext-Squad/blob/main/CHANGELOG.md).
3. **Niezależny przegląd.** Ktoś, kto nie pisał stron, czyta README i każdą zmienioną stronę, łącznie z obrazkami,
   trzy razy: jako początkujący, który nigdy nie używał terminala, jako ośmiolatek i jako ekspert,
   który sprawdza każdą opcję z `--help`. Przykłady używają wyłącznie zmyślonych nazw i liczb.
4. **Popraw** wszystko, co wypadnie w przeglądzie.
5. **Tłumaczenia.** Każda przetłumaczona strona zapisuje skrót (hash) angielskiej strony, z której powstała.
   Przetłumacz ponownie strony, których angielskie źródło się zmieniło, a potem przejrzyj każdy język: czytelny tekst,
   poprawne etykiety na schematach, te same słowa co w przetłumaczonym interfejsie przeglądarki 3DHeat.
6. **Uruchom testy** (`pytest`).
7. **Wypchnij** dopiero po zielonym świetle od właściciela.

## Tłumaczenia: polecenia {#translations-the-commands}

Strona jest tłumaczona na 40 języków interfejsu przeglądarki 3DHeat: angielski w `docs/`, każdy inny język w `docs/<lang>/`
z tymi samymi nazwami plików. `tools/docs_i18n.py` prowadzi ewidencję:

```bash
python tools/docs_i18n.py hashes             # po każdej zmianie w angielskim: zapisz skrót każdej strony
python tools/docs_i18n.py svg-strings        # po każdej zmianie obrazka: etykiety do przetłumaczenia
python tools/docs_i18n.py status             # dla każdego języka: aktualne, nieaktualne, brakujące strony
python tools/docs_i18n.py todo --lang de     # niemieckie strony do (ponownego) przetłumaczenia
python tools/docs_i18n.py svg-build --lang de    # niemieckie obrazki z docs/assets/i18n/svg/de.json
python tools/docs_i18n.py finish --lang de   # oznacz niemieckie strony skrótem angielskiej strony
python tools/docs_i18n.py check              # kończy się kodem 1, gdy skróty lub etykiety są nieaktualne
```

Tłumacz tylko to, co wypisuje `todo`: zachowaj Markdown, linki, kod, nazwy plików i kolumn; przetłumacz tytuły i opisy obrazków,
a w przyciskach i panelach używaj słów z własnego interfejsu przeglądarki 3DHeat (`src/i18n/locales/<lang>/`).
Wygenerowane strony z opisem poleceń i obrazki z terminala zostają po angielsku. Na stronie nieaktualne tłumaczenie to mówi
i odsyła do angielskiej strony; brakujące tłumaczenie przechodzi na angielski. Menu języków w nagłówku i przekierowanie
na stronie głównej według języka przeglądarki pochodzą z `docs/_includes/`.
