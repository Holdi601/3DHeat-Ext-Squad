---
title: "Taflan"
nav_order: 4
lang: "is"
source: output-table.md
source_hash: "0f3cfed1c108"
nav_exclude: true
search_exclude: true
---
# Taflan: `<demo>.parquet` {#the-table-parquet}

Ein röð fyrir hvert sýni eða atburð. Sýni er tekið í hvert sinn sem þjónninn
afritaði hreyfingu leikaðilans, allt að 8 sinnum á sekúndu (upptökutíðni demo-sins)
meðan hann hreyfist.

![Fyrstu raðir í töflu gervidemo](../assets/img/table.svg)

## Dálkar {#columns}

| Dálkur | Hvað það er |
|---|---|
| `time` | sekúndur frá upphafi upptöku |
| `x`, `y`, `z` | staðsetning í Unreal-einingum (sentímetrum), Z upp |
| `dirX`, `dirY`, `dirZ` | hvert hermaður lítur: sveigja (yaw) líkamans og halli (pitch) sjónarinnar, sem einingarvigur (ökutækis: lárétt) |
| `yaw`, `pitch` | það sama í gráðum; `pitch` upp frá sjóndeildarhring, aðeins hermenn |
| `health` | heilsa hermanns, bots eða ökutækis á þeirri stundu, þar sem þjónninn sendi hana (hjá hermanni fer hún niður fyrir 0 meðan hann er særður) |
| `speed` | afritaður hraði, cm/s |
| `player` | nafn leikmanns; `bot <id>` fyrir bot; fyrir ökutæki eða hlut sem enginn á, flokkur þess (class); fyrir skot úr vopni ökutækis, leikmaðurinn sem situr í því ökutæki |
| `team`, `faction` | liðsnúmer Squad (1, 2) og fylkingaruppsetning þess, **á þeirri stundu**: leikmenn geta skipt um lið |
| `squad` | sveitarnúmerið, -1 þegar ekki í sveit |
| `event` | hvað röðin er (hér að neðan) |
| `pawn` | hermannateikningin (blueprint) (`SQSquidBot` fyrir bot), ökutækið, eða fyrir `fire` vopnið |
| `seat` | fyrir virki eða farþegasæti, eigið pawn sætisins |
| `detail` | fyrir `fire` kall vopnsins sem setti skotið, fyrir `hit` skaðategundin, fyrir `removed` hvers vegna rásin lokaðist (`Destroyed`, `Dormancy`...) |
| `entity` | leikaðilinn sem röðin snýst um (net GUID hans): `entity` í röðum hliðarskránna |
| `match` | nafn demo-sins |

## Atburðir {#events}

| `event` | Á röð hjá | Hvað |
|---|---|---|
| `position` | hermanni eða bot fótgangandi | hreyfisýni |
| `vehicle` | hermanni í landökutæki eða þyrlu | sýni á staðsetningu ökutækisins |
| `wounded`, `revived`, `death` | hermenn og bots | hvar það gerðist |
| `spawn`, `damaged`, `destroyed`, `removed` | ökutæki, uppsett mannvirki, skotstæði, kassar, þyrlur | hvar þau voru |
| `seat` | leikmaður | tók sæti |
| `fire` | skotmaðurinn | skot: hvaðan það fór, stefna þess sem `yaw`/`pitch`/`dirX..Z` |
| `hit` | ökutækið | högg á ökutæki: hvar |

Hvernig atburðir eru lesnir er í [Hvernig demo er lesið](how-it-works.md#how-the-events-are-read).

## Í skoðaranum {#in-the-viewer}

Parquet-fótur skrárinnar geymir leiðbeiningar um lestur undir lyklinum `heat3d`: Z upp,
enginn ás speglaður, einingakvarði 1, svo skoðarinn þarf enga dálkaúthlutun. Hladdu
töfluna í flipanum Hitakort; sjá
[Að koma gögnum inn](https://holdi601.github.io/3DHeat/getting-data-in.html)
og [Dálkaúthlutun](https://holdi601.github.io/3DHeat/column-mapping.html) í skoðaranum.
