---
title: "Převod dem"
nav_order: 3
lang: "cs"
source: converting.md
source_hash: "e8c77423085b"
nav_exclude: true
search_exclude: true
---
# Převod dem {#converting-demos}

```text
heat3d-squad-demo <demos or folders> -o <folder> [--flat] [--json]
python -m heat3d_ext_squad ...          the same, without installing
```

## Krok za krokem {#step-by-step}

Nikdy jste nepracovali s příkazovým řádkem? Nejdřív si přečtěte [Než začnete](before-you-start.md).

1. Nainstalujte jednou: `git clone https://github.com/Holdi601/3DHeat-Ext-Squad`,
   otevřete terminál v této složce a spusťte `python -m pip install -e .`
   (Python 3.10 nebo novější; přinese s sebou pyarrow a numpy).
2. Dejte soubory `.replay` do složky, nebo je pojmenujte jeden po druhém.
3. Spusťte `heat3d-squad-demo <folder> -o out`.
4. Uvidíte jeden řádek na každé demo: jeho vrstvu, hráče a řádky a kam se tabulka uložila.
   Každé demo se promění ve čtyři volné soubory v `out/<map>/` (ne v kontejner
   `.3dheat`); `.parquet` načtěte v prohlížeči 3DHeat.

![Běh na syntetickém demu](../assets/img/run.svg)

Obrázek ukazuje běh na demu, které vytvářejí testy (`tests/test_stream.py`),
ne na skutečném zápasu.

## Možnosti {#options}

| Možnost | Výchozí | Co dělá |
|---|---|---|
| `demos` (jedno nebo více) | - | soubory `.replay`, nebo složky, které je obsahují |
| `-o`, `--out` | povinné | složka, do které se zapisuje; každé demo jde do `<out>/<map>/` |
| `--flat` | vypnuto | zapisuje rovnou do složky, bez podsložky `<map>/` |
| `--json` | vypnuto | vypíše na standardní výstup jeden řádek JSON na demo (pro programy, které tento příkaz volají): `demo`, `ok`, `parquet`, `match`, `sidecars`, `lost`, `rows`, `players`, `layer`, `recorded_unix`; demo, které selhalo, vypíše `demo`, `ok: false` a `error` |
| `--version` | - | vypíše verzi a skončí |

Každá možnost tak, jak ji program vypisuje: [Přehled příkazů](../cli-reference.md).

Složka mapy je název mapy převzatý z cesty k úrovni, kterou demo uvádí
(`/Game/Maps/<Map>/Gameplay_Layers/<Layer>` dá `<Map>`).

Stavový kód: 0, když se převedla všechna dema; 1, když některé selhalo (ostatní
se přesto zapíší), nebo když nebyl nalezen žádný soubor `.replay`.

## Co vznikne {#what-comes-out}

| Soubor | Co obsahuje |
|---|---|
| `<demo>.parquet` | tabulka: pozice a události, jeden řádek na každou ([Tabulka](output-table.md)) |
| `<demo>.match.json` | dokument zápasu ([Dokument zápasu](output-match.md)) |
| `<demo>.entities.parquet` | doplňková data: každá aktualizace vlastnosti a každé vzdálené volání, celé |
| `<demo>.packets.parquet` | doplňková data: části souboru a vše, co se nepřečetlo, celé |

Tabulka a dokument zápasu jsou stejná dvojice, kterou zapisuje nástroj 3DHeat CS2.
Prohlížeč otevře tabulku přímo a při načtení celé složky doplňková data vynechá.

## Příklady {#examples}

```bash
heat3d-squad-demo D:\SquadDemos -o out                 # every demo in a folder
heat3d-squad-demo one.replay two.replay -o out --flat  # straight into out/
heat3d-squad-demo D:\SquadDemos -o out --json          # one JSON line per demo
```

`D:\SquadDemos` je příklad složky na jednotce D: použijte vlastní.
