---
title: "Канвертаванне дэма"
nav_order: 3
lang: "be"
source: converting.md
source_hash: "e8c77423085b"
nav_exclude: true
search_exclude: true
---
# Канвертаванне дэма {#converting-demos}

```text
heat3d-squad-demo <demos or folders> -o <folder> [--flat] [--json]
python -m heat3d_ext_squad ...          the same, without installing
```

## Крок за крокам {#step-by-step}

Упершыню ў камандным радку? Спачатку прачытайце [Перад пачаткам](before-you-start.md).

1. Усталюйце адзін раз: `git clone https://github.com/Holdi601/3DHeat-Ext-Squad`,
   адкрыйце тэрмінал у гэтай папцы, выканайце `python -m pip install -e .`
   (Python 3.10 або навейшы; ён прыносіць pyarrow і numpy).
2. Пакладзіце файлы `.replay` у папку або назавіце іх па адным.
3. Выканайце `heat3d-squad-demo <folder> -o out`.
4. Вы ўбачыце па радку на кожнае дэма: яго пласт, гульцоў і радкі, і куды
   пайшла табліца. Кожнае дэма становіцца чатырма асобнымі файламі ў `out/<map>/` (не
   кантэйнер `.3dheat`); загрузіце `.parquet` у праглядальнік 3DHeat.

![Запуск на сінтэтычным дэма](../assets/img/run.svg)

Малюнак паказвае запуск на дэма, якое будуюць тэсты (`tests/test_stream.py`),
а не рэальны матч.

## Опцыі {#options}

| Опцыя | Па змаўчанні | Што робіць |
|---|---|---|
| `demos` (адно або болей) | - | файлы `.replay` або папкі з імі |
| `-o`, `--out` | абавязкова | папка, у якую пішуць; кожнае дэма трапляе ў `<out>/<map>/` |
| `--flat` | выключана | пісаць наўпрост у папку, без папкі `<map>/` |
| `--json` | выключана | друкаваць адзін радок JSON на кожнае дэма ў stdout (для праграм, што выклікаюць каманду): `demo`, `ok`, `parquet`, `match`, `sidecars`, `lost`, `rows`, `players`, `layer`, `recorded_unix`; дэма, якое не ўдалося, замест гэтага друкуе `demo`, `ok: false` і `error` |
| `--version` | - | надрукаваць версію і спыніцца |

Кожная опцыя, як яе друкуе праграма: [Даведнік каманд](../cli-reference.md).

Папка карты — гэта назва карты з шляху ўзроўню, які называе дэма
(`/Game/Maps/<Map>/Gameplay_Layers/<Layer>` дае `<Map>`).

Статус выхаду: 0, калі ўсе дэма сканвертаваны; 1, калі якое-небудзь не ўдалося (астатнія
усё роўна запісаны) або калі не знойдзена ніводнага файла `.replay`.

## Што атрымліваецца {#what-comes-out}

| Файл | Што ў ім |
|---|---|
| `<demo>.parquet` | табліца: пазіцыі і падзеі, па радку на кожную ([Табліца](output-table.md)) |
| `<demo>.match.json` | дакумент матча ([Дакумент матча](output-match.md)) |
| `<demo>.entities.parquet` | дапаможны файл: кожнае абнаўленне ўласцівасці і кожны выклік па сетцы, цалкам |
| `<demo>.packets.parquet` | дапаможны файл: часткі файла і ўсё, што не прачыталася, цалкам |

Табліца і дакумент матча — тая самая пара, што піша інструмент 3DHeat CS2.
Праглядальнік адкрывае табліцу наўпрост і пропускае дапаможныя файлы, калі
загружаецца ўся папка.

## Прыклады {#examples}

```bash
heat3d-squad-demo D:\SquadDemos -o out                 # every demo in a folder
heat3d-squad-demo one.replay two.replay -o out --flat  # straight into out/
heat3d-squad-demo D:\SquadDemos -o out --json          # one JSON line per demo
```

`D:\SquadDemos` — прыклад папкі на дыску D: бярыце сваю.
