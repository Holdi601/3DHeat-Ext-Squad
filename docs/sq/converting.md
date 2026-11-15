---
title: "Konvertimi i demove"
nav_order: 3
lang: sq
source: converting.md
source_hash: "e8c77423085b"
nav_exclude: true
search_exclude: true
---
# Konvertimi i demove {#converting-demos}

```text
heat3d-squad-demo <demos or folders> -o <folder> [--flat] [--json]
python -m heat3d_ext_squad ...          the same, without installing
```

## Hap pas hapi {#step-by-step}

Je i ri me vijën e komandës? Lexo së pari [Para se të fillosh](before-you-start.md).

1. Instalo një herë: `git clone https://github.com/Holdi601/3DHeat-Ext-Squad`,
   hap një terminal në atë dosje, ekzekuto `python -m pip install -e .`
   (Python 3.10 ose më i ri; sjell pyarrow dhe numpy).
2. Vendos skedarët `.replay` në një dosje, ose emërtoji një nga një.
3. Ekzekuto `heat3d-squad-demo <folder> -o out`.
4. Duhet të shohësh një rresht për çdo demo: shtresën, lojtarët dhe rreshtat e saj, dhe ku
   shkoi tabela. Çdo demo bëhet katër skedarë të veçantë në `out/<map>/` (jo një
   kontejner `.3dheat`); ngarko `.parquet` në shikuesin 3DHeat.

![Një ekzekutim mbi një demo sintetike](../assets/img/run.svg)

Fotoja tregon një ekzekutim mbi një demo që e ndërtojnë testet (`tests/test_stream.py`),
jo një ndeshje të vërtetë.

## Opsionet {#options}

| Opsioni | Parazgjedhja | Çfarë bën |
|---|---|---|
| `demos` (një ose më shumë) | - | skedarë `.replay`, ose dosje që i përmbajnë |
| `-o`, `--out` | i detyrueshëm | dosja ku shkruhet; çdo demo shkon te `<out>/<map>/` |
| `--flat` | off | shkruan drejt në dosje, pa dosjen `<map>/` |
| `--json` | off | shtyp një rresht JSON për çdo demo në stdout (për programet që e thërrasin komandën): `demo`, `ok`, `parquet`, `match`, `sidecars`, `lost`, `rows`, `players`, `layer`, `recorded_unix`; një demo që dështoi shtyp në vend të tyre `demo`, `ok: false` dhe `error` |
| `--version` | - | shtyp versionin dhe ndalon |

Çdo opsion, ashtu siç e shtyp programi: [Referenca e komandave](../cli-reference.md).

Dosja e hartës është emri i hartës i marrë nga shtegu i nivelit që emërton demo
(`/Game/Maps/<Map>/Gameplay_Layers/<Layer>` jep `<Map>`).

Kodi i daljes: 0 kur çdo demo u konvertua; 1 kur ndonjë dështoi (të tjerat shkruhen prapë)
ose kur nuk u gjet asnjë skedar `.replay`.

## Çfarë del {#what-comes-out}

| Skedari | Çfarë përmban |
|---|---|
| `<demo>.parquet` | tabela: pozicionet dhe ngjarjet, nga një rresht secila ([Tabela](output-table.md)) |
| `<demo>.match.json` | dokumenti i ndeshjes ([Dokumenti i ndeshjes](output-match.md)) |
| `<demo>.entities.parquet` | skedar ndihmës: çdo përditësim vetie dhe çdo thirrje në distancë, e plotë |
| `<demo>.packets.parquet` | skedar ndihmës: copat e skedarit dhe çdo gjë që nuk u lexua, e plotë |

Tabela dhe dokumenti i ndeshjes janë i njëjti çift që e shkruan mjeti 3DHeat CS2.
Shikuesi e hap tabelën drejtpërdrejt dhe i lë jashtë skedarët ndihmës kur ngarkohet një
dosje e tërë.

## Shembuj {#examples}

```bash
heat3d-squad-demo D:\SquadDemos -o out                 # every demo in a folder
heat3d-squad-demo one.replay two.replay -o out --flat  # straight into out/
heat3d-squad-demo D:\SquadDemos -o out --json          # one JSON line per demo
```

`D:\SquadDemos` është një dosje shembull në diskun D: përdor të tënden.
