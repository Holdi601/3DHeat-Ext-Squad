---
title: An tábla
nav_order: 4
lang: ga
source: output-table.md
source_hash: "0f3cfed1c108"
nav_exclude: true
search_exclude: true
---
# An tábla: `<demo>.parquet` {#the-table-parquet}

Sraith amháin in aghaidh an tsampla nó an imeachta. Tógtar sampla aon uair a rinne an
freastalaí gluaiseacht an aisteora a mhacasamhlú, suas le 8 n-uaire in aghaidh an tsoicind (ráta taifeadta an demo)
fad a ghluaiseann sé.

![Chéad sraitheanna tábla demo sintéisigh](../assets/img/table.svg)

## Colúin {#columns}

| Colún | Cad é |
|---|---|
| `time` | soicindí ó thosaigh an taifeadadh |
| `x`, `y`, `z` | suíomh in aonaid Unreal (ceintiméadair), Z suas |
| `dirX`, `dirY`, `dirZ` | cá bhféachann saighdiúir: gluaiseacht chasta (yaw) an choirp agus pitch an radhairc, mar veicteoir aonaid (do ghluaisteán: cothrom) |
| `yaw`, `pitch` | an rud céanna i gcéimeanna; `pitch` suas ón léaslíne, saighdiúirí amháin |
| `health` | sláinte an tsaighdiúra, an bhota nó an ghluaisteáin ag an nóiméad sin, nuair a sheol an freastalaí í (titeann sláinte saighdiúra faoi bhun 0 agus é créachtaithe) |
| `speed` | an luas macasamhlaithe, cm/s |
| `player` | ainm an imreora; `bot <id>` do bhot; do ghluaisteán nó d'earra imlonnaithe nach bhfuil úinéir air, a aicme; do lámhaigh ó arm gluaisteáin, an t-imreoir atá ina shuí ar an ngluaisteán sin |
| `team`, `faction` | uimhir fhoireann Squad (1, 2) agus a socrú faction, **ag an nóiméad sin**: is féidir le himreoirí taobh a athrú |
| `squad` | uimhir na scuaide, -1 nuair nach bhfuil sé in aon cheann |
| `event` | cad é an tsraith (thíos) |
| `pawn` | blueprint an tsaighdiúra (`SQSquidBot` do bhot), an gluaisteán, nó do `fire` an t-arm |
| `seat` | do thuirléad nó d'suíochán paisinéara, pawn an tsuíocháin féin |
| `detail` | do `fire` glao an airm a chuir an lámhaigh, do `hit` an cineál damáiste, do `removed` cén fáth ar dhúnadh an cainéal (`Destroyed`, `Dormancy`...) |
| `entity` | an t-aisteoir a bhfuil an tsraith faoi (a net GUID): `entity` sraitheanna na dtaobhchomhad |
| `match` | ainm an demo |

## Imeachtaí {#events}

| `event` | Ar shraith | Cad |
|---|---|---|
| `position` | saighdiúir nó bot ar shiúl na gcos | sampla gluaiseachta |
| `vehicle` | saighdiúir i ngluaisteán talún nó i héileacaptar | sampla ag suíomh an ghluaisteáin |
| `wounded`, `revived`, `death` | saighdiúirí agus botanna | an áit inar tharla sé |
| `spawn`, `damaged`, `destroyed`, `removed` | gluaisteáin, earraí imlonnaithe, bunacha, cásanna, héileacaptair | an áit a raibh siad |
| `seat` | imreoir | ghlac suíochán |
| `fire` | an lámhachóir | lámhaigh: an áit ar fhág sí, a treo mar `yaw`/`pitch`/`dirX..Z` |
| `hit` | an gluaisteán | buille ar ghluaisteán: an áit |

Tá an chaoi a léitear na himeachtaí in [Conas a léitear demo](how-it-works.md#how-the-events-are-read).

## Sa lucht féachana {#in-the-viewer}

Tá treoracha léitheoireachta i bhfuiseog an Parquet faoin eochair `heat3d`: Z suas,
aon ais scáthánaithe, scála aonaid 1, mar sin ní theastaíonn mapáil colúin ón lucht féachana. Lódáil
an tábla sa chluaisín Léarscáil teasa; féach [Sonraí a thabhairt isteach](https://holdi601.github.io/3DHeat/getting-data-in.html)
agus [Mapáil colún](https://holdi601.github.io/3DHeat/column-mapping.html) an lucht féachana.
