---
title: It-tabella
nav_order: 4
lang: mt
source: output-table.md
source_hash: "0f3cfed1c108"
nav_exclude: true
search_exclude: true
---
# It-tabella: `<demo>.parquet` {#the-table-parquet}

Ringiela waħda għal kull kampjun jew avveniment. Kampjun jittieħed kull meta s-server
irrepika l-moviment tal-attur, sa 8 darbiet fis-sekonda (ir-rata ta' rrekordjar tad-demo)
waqt li jiċċaqlaq.

![L-ewwel ringieli tat-tabella ta' demo sintetika](../assets/img/table.svg)

## Kolonni {#columns}

| Kolonna | X'inhi |
|---|---|
| `time` | sekondi minn meta bdiet ir-reġistrazzjoni |
| `x`, `y`, `z` | pożizzjoni f'unitajiet ta' Unreal (ċentimetri), Z 'il fuq |
| `dirX`, `dirY`, `dirZ` | fejn iħares suldat: il-yaw tal-ġisem u l-pitch tal-vista, bħala vettur unitarju (dak ta' vettura: orizzontali) |
| `yaw`, `pitch` | l-istess f'gradi; `pitch` 'il fuq mill-orizzont, suldati biss |
| `health` | is-saħħa tas-suldat, tal-bot jew tal-vettura f'dak il-mument, fejn is-server bagħtha (ta' suldat tinżel taħt 0 waqt li jkun midrub) |
| `speed` | l-veloċità rreplikata, cm/s |
| `player` | l-isem tal-plejer; `bot <id>` għal bot; għal vettura jew deployable li ħadd ma għandu, il-klassi tagħha; għal sparatura mill-arma ta' vettura, il-plejer bilqiegħda fuq dik il-vettura |
| `team`, `faction` | in-numru tat-tim ta' Squad (1, 2) u s-setup tal-fazzjoni tiegħu, **f'dak il-mument**: il-plejers jistgħu jbiddlu naħa |
| `squad` | in-numru tal-iskwadra, -1 meta mhux f'waħda |
| `event` | x'inhi r-ringiela (hawn taħt) |
| `pawn` | il-blueprint tas-suldat (`SQSquidBot` għal bot), il-vettura, jew għal `fire` l-arma |
| `seat` | għal turret jew sit tal-passiġġieri, il-pawn proprju tas-sit |
| `detail` | għal `fire` is-sejħa tal-arma li poġġiet l-isparatura, għal `hit` it-tip ta' dannu, għal `removed` għaliex il-channel magħluq (`Destroyed`, `Dormancy`...) |
| `entity` | l-attur li dwaru hi r-ringiela (in-net GUID tiegħu): l-`entity` tar-ringieli tas-sidecars |
| `match` | l-isem tad-demo |

## Avvenimenti {#events}

| `event` | Fuq ir-ringiela ta' | X'inhu |
|---|---|---|
| `position` | suldat jew bot a piedi | kampjun ta' moviment |
| `vehicle` | suldat f'vettura tal-art jew elikopter | kampjun fil-pożizzjoni tal-vettura |
| `wounded`, `revived`, `death` | suldati u bots | fejn ġara |
| `spawn`, `damaged`, `destroyed`, `removed` | vetturi, deployables, emplacements, crates, elikopters | fejn kienu |
| `seat` | plejer | ħa sit |
| `fire` | ix-shooter | sparatura: minn fejn ħarġet, id-direzzjoni tagħha bħala `yaw`/`pitch`/`dirX..Z` |
| `hit` | il-vettura | daqqa fuq vettura: fejn |

Kif jinqraw l-avvenimenti hu f'[Kif tinqara demo](how-it-works.md#how-the-events-are-read).

## Fil-viewer {#in-the-viewer}

Il-footer tal-Parquet iġorr struzzjonijiet tal-qari taħt iċ-ċavetta `heat3d`: Z 'il fuq,
ebda assi mirja, skala tal-unità 1, għalhekk il-viewer m'għandu bżonn ebda mappjar tal-kolonni. Tgħabbi
t-tabella fit-tab Heatmap; ara
[Kif iddaħħal id-dejta](https://holdi601.github.io/3DHeat/getting-data-in.html)
u [Mappjar tal-kolonni](https://holdi601.github.io/3DHeat/column-mapping.html) tal-viewer.
