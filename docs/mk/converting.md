---
title: Претворање демоа
nav_order: 3
lang: mk
source: converting.md
source_hash: "e8c77423085b"
nav_exclude: true
search_exclude: true
---
# Претворање демоа {#converting-demos}

```text
heat3d-squad-demo <demos or folders> -o <folder> [--flat] [--json]
python -m heat3d_ext_squad ...          the same, without installing
```

## Чекор по чекор {#step-by-step}

Нови сте со командната линија? Прво прочитајте [Пред да започнете](before-you-start.md).

1. Инсталирајте еднаш: `git clone https://github.com/Holdi601/3DHeat-Ext-Squad`,
   отворете терминал во таа папка, пуштете `python -m pip install -e .`
   (Python 3.10 или понов; носи со себе pyarrow и numpy).
2. Ставете ги `.replay` датотеките во папка, или именувајте ги една по една.
3. Пуштете `heat3d-squad-demo <folder> -o out`.
4. Треба да видите по една линија за секое демо: неговиот слој, играчите и редовите, и каде
   отишла табелата. Секое демо станува четири одделни датотеки во `out/<map>/` (не
   контејнер `.3dheat`); вчитајте го `.parquet` во прегледувачот 3DHeat.

![Извршување на синтетичко демо](../assets/img/run.svg)

Сликата прикажува извршување на демо што го градат тестовите (`tests/test_stream.py`),
а не вистински меч.

## Опции {#options}

| Опција | Стандардно | Што прави |
|---|---|---|
| `demos` (едно или повеќе) | - | `.replay` датотеки, или папки што ги содржат |
| `-o`, `--out` | задолжително | папката во која се пишува; секое демо оди во `<out>/<map>/` |
| `--flat` | исклучено | пишува директно во папката, без папката `<map>/` |
| `--json` | исклучено | печати по една линија JSON за секое демо на stdout (за програми што ја повикуваат командата): `demo`, `ok`, `parquet`, `match`, `sidecars`, `lost`, `rows`, `players`, `layer`, `recorded_unix`; демо што не успеало печати `demo`, `ok: false` и `error` наместо тоа |
| `--version` | - | ја печати верзијата и запира |

Секоја опција, како што ја печати програмата: [Упатство за команди](../cli-reference.md).

Папката на мапата е името на мапата земено од патеката на нивото што ја именува демото
(`/Game/Maps/<Map>/Gameplay_Layers/<Layer>` дава `<Map>`).

Излезен статус: 0 кога сите демоа се претворени; 1 кога било кое не успеало (останатите
сепак се запишани) или кога не е пронајдена ниту една `.replay` датотека.

## Што се добива {#what-comes-out}

| Датотека | Што содржи |
|---|---|
| `<demo>.parquet` | табелата: позиции и настани, по еден ред ([Табелата](output-table.md)) |
| `<demo>.match.json` | документот за мечот ([Документот за мечот](output-match.md)) |
| `<demo>.entities.parquet` | придружна датотека: секое ажурирање на својство и секое оддалечено повикување, целосно |
| `<demo>.packets.parquet` | придружна датотека: деловите (chunks) на датотеката и сè што не се прочитало, целосно |

Табелата и документот за мечот се истиот пар што го пишува алатката 3DHeat CS2.
Прегледувачот ја отвора табелата директно, а придружните датотеки ги изоставува кога се вчитува цела
папка.

## Примери {#examples}

```bash
heat3d-squad-demo D:\SquadDemos -o out                 # every demo in a folder
heat3d-squad-demo one.replay two.replay -o out --flat  # straight into out/
heat3d-squad-demo D:\SquadDemos -o out --json          # one JSON line per demo
```

`D:\SquadDemos` е пример за папка на дискот D: користете своја.
