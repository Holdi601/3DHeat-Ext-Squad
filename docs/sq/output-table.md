---
title: "Tabela"
nav_order: 4
lang: sq
source: output-table.md
source_hash: "0f3cfed1c108"
nav_exclude: true
search_exclude: true
---
# Tabela: `<demo>.parquet` {#the-table-parquet}

Një rresht për çdo mostër ose ngjarje. Një mostër merret sa herë që serveri e ka
replikuar lëvizjen e aktorit, deri 8 herë në sekondë (shpejtësia e regjistrimit të demos)
ndërsa lëviz.

![Rreshtat e parë të tabelës së një demoje sintetike](../assets/img/table.svg)

## Kolonat {#columns}

| Kolona | Çfarë është |
|---|---|
| `time` | sekonda që nga fillimi i regjistrimit |
| `x`, `y`, `z` | pozicioni në njësi Unreal (centimetra), Z lart |
| `dirX`, `dirY`, `dirZ` | ku shikon një ushtar: kthesa e trupit (yaw) dhe pjerrësia e shikimit (pitch), si vektor njësi (për një automjet: horizontal) |
| `yaw`, `pitch` | e njëjta në gradë; `pitch` lart nga horizonti, vetëm për ushtarët |
| `health` | shëndeti i ushtarit, i botit ose i automjetit në atë çast, aty ku e dërgoi serveri (ai i ushtarit bie nën 0 kur është i plagosur) |
| `speed` | shpejtësia e replikuar, cm/s |
| `player` | emri i lojtarit; `bot <id>` për një bot; për një automjet ose një objekt të vendosur që s'e ka askush, klasa e tij; për një të shtënë nga arma e një automjeti, lojtari që është ulur në atë automjet |
| `team`, `faction` | numri i skuadrës së Squad (1, 2) dhe konfigurimi i fraksionit të saj, **në atë çast**: lojtarët mund të ndërrojnë anë |
| `squad` | numri i togës, -1 kur nuk është në asnjërën |
| `event` | çfarë është rreshti (më poshtë) |
| `pawn` | skema e ushtarit (`SQSquidBot` për një bot), automjeti, ose për `fire` arma |
| `seat` | për një frëngji ose ndenjëse pasagjeri, pawn-i i vetë ndenjëses |
| `detail` | për `fire` thirrja e armës që e vendosi të shtënën, për `hit` lloji i dëmit, për `removed` pse u mbyll kanali (`Destroyed`, `Dormancy`...) |
| `entity` | aktori për të cilin flet rreshti (net GUID-i i tij): `entity` i rreshtave të skedarëve ndihmës |
| `match` | emri i demos |

## Ngjarjet {#events}

| `event` | Në rreshtin e | Çfarë |
|---|---|---|
| `position` | një ushtari ose boti në këmbë | një mostër lëvizjeje |
| `vehicle` | një ushtari në një automjet tokësor ose helikopter | një mostër në pozicionin e automjetit |
| `wounded`, `revived`, `death` | ushtarëve dhe botëve | ku ndodhi |
| `spawn`, `damaged`, `destroyed`, `removed` | automjeteve, objekteve të vendosura, pozicioneve, arkave, helikopterëve | ku ishin |
| `seat` | një lojtari | zuri një ndenjëse |
| `fire` | gjuajtësit | një e shtënë: ku doli, drejtimi i saj si `yaw`/`pitch`/`dirX..Z` |
| `hit` | automjetit | një goditje mbi automjet: ku |

Si lexohen ngjarjet është te [Si lexohet një demo](how-it-works.md#how-the-events-are-read).

## Në shikues {#in-the-viewer}

Fundi i Parquet mban udhëzime leximi nën çelësin `heat3d`: Z lart,
asnjë bosht i pasqyruar, shkallë njësie 1, kështu që shikuesi s'ka nevojë për lidhje
kolonash. Ngarkoje tabelën te skeda Harta e nxehtësisë; shih
[Getting data in](https://holdi601.github.io/3DHeat/getting-data-in.html)
dhe [Column mapping](https://holdi601.github.io/3DHeat/column-mapping.html) të shikuesit.
