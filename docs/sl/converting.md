---
title: "Pretvarjanje posnetkov"
nav_order: 3
lang: sl
source: converting.md
source_hash: "e8c77423085b"
nav_exclude: true
search_exclude: true
---
# Pretvarjanje posnetkov {#converting-demos}

```text
heat3d-squad-demo <posnetki ali mape> -o <mapa> [--flat] [--json]
python -m heat3d_ext_squad ...          isto, brez namestitve
```

## Korak za korakom {#step-by-step}

Še nisi vajen ukazne vrstice? Najprej preberi [Preden začneš](before-you-start.md).

1. Namesti enkrat: `git clone https://github.com/Holdi601/3DHeat-Ext-Squad`,
   odpri terminal v tej mapi in zaženi `python -m pip install -e .`
   (Python 3.10 ali novejši; prinese pyarrow in numpy).
2. Datoteke `.replay` daj v mapo ali jih navedi eno za drugo.
3. Zaženi `heat3d-squad-demo <mapa> -o out`.
4. Za vsak posnetek se izpiše ena vrstica: njegova plast, igralci in vrstice ter
   kam je šla tabela. Vsak posnetek postane štiri ločene datoteke v `out/<zemljevid>/`
   (ne vsebnik `.3dheat`); v pregledovalniku 3DHeat naloži `.parquet`.

![Zagon na sintetičnem posnetku](../assets/img/run.svg)

Slika prikazuje zagon na posnetku, ki ga ustvarijo testi (`tests/test_stream.py`),
ne na pravi tekmi.

## Možnosti {#options}

| Možnost | Privzeto | Naredi |
|---|---|---|
| `demos` (ena ali več) | - | datoteke `.replay` ali mape, ki jih vsebujejo |
| `-o`, `--out` | obvezno | mapa, v katero se zapisuje; vsak posnetek gre v `<out>/<zemljevid>/` |
| `--flat` | izklopljeno | zapiše neposredno v mapo, brez mape `<zemljevid>/` |
| `--json` | izklopljeno | na standardni izhod izpiše po eno vrstico JSON na posnetek (za programe, ki kličejo ukaz): `demo`, `ok`, `parquet`, `match`, `sidecars`, `lost`, `rows`, `players`, `layer`, `recorded_unix`; posnetek, ki ni uspel, izpiše `demo`, `ok: false` in `error` |
| `--version` | - | izpiše različico in se ustavi |

Vsaka možnost, kot jo izpiše program: [Priročnik ukazov](../cli-reference.md).

Mapa zemljevida je ime zemljevida, vzeto iz poti do ravni, ki jo navaja posnetek
(`/Game/Maps/<Zemljevid>/Gameplay_Layers/<Plast>` daje `<Zemljevid>`).

Izhodna koda: 0, ko so bili vsi posnetki pretvorjeni; 1, ko katerikoli ni uspel
(ostali so vseeno zapisani) ali ko ni bila najdena nobena datoteka `.replay`.

## Kaj nastane {#what-comes-out}

| Datoteka | Vsebina |
|---|---|
| `<posnetek>.parquet` | tabela: položaji in dogodki, po ena vrstica vsak ([Tabela](output-table.md)) |
| `<posnetek>.match.json` | dokument tekme ([Dokument tekme](output-match.md)) |
| `<posnetek>.entities.parquet` | spremljevalna datoteka: vsaka posodobitev lastnosti in oddaljeni klic, v celoti |
| `<posnetek>.packets.parquet` | spremljevalna datoteka: deli datoteke in vse, kar se ni prebralo, v celoti |

Tabela in dokument tekme sta isti par, ki ga zapisuje orodje 3DHeat CS2.
Pregledovalnik odpre tabelo neposredno in pri nalaganju cele mape spremljevalnih
datotek izpusti.

## Primeri {#examples}

```bash
heat3d-squad-demo D:\SquadDemos -o out                 # vsi posnetki v mapi
heat3d-squad-demo one.replay two.replay -o out --flat  # neposredno v out/
heat3d-squad-demo D:\SquadDemos -o out --json          # po ena vrstica JSON na posnetek
```

`D:\SquadDemos` je primer mape na disku D: uporabi svojo.
