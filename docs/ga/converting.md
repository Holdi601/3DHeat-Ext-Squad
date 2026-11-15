---
title: Demos a thiontú
nav_order: 3
lang: ga
source: converting.md
source_hash: "e8c77423085b"
nav_exclude: true
search_exclude: true
---
# Demos a thiontú {#converting-demos}

```text
heat3d-squad-demo <demos or folders> -o <folder> [--flat] [--json]
python -m heat3d_ext_squad ...          the same, without installing
```

## Céim ar chéim {#step-by-step}

An bhfuil tú nua leis an líne ordaithe? Léigh [Sula dtosaíonn tú](before-you-start.md) ar dtús.

1. Suiteáil uair amháin: `git clone https://github.com/Holdi601/3DHeat-Ext-Squad`,
   oscail teirminéal sa fhillteán sin, rith `python -m pip install -e .`
   (Python 3.10 nó níos nuaí; tugann sé pyarrow agus numpy leis).
2. Cuir na comhaid `.replay` i bhfillteán, nó ainmnigh iad ceann ar cheann.
3. Rith `heat3d-squad-demo <folder> -o out`.
4. Ba chóir duit líne amháin a fheiceáil in aghaidh an demo: a layer, na himreoirí agus na sraitheanna, agus an áit
   ar chuaigh an tábla. Éiríonn gach demo ina cheithre chomhad scaoilte in `out/<map>/` (ní
   coimeádán `.3dheat`); lódáil an `.parquet` sa lucht féachana 3DHeat.

![Rith ar demo sintéiseach](../assets/img/run.svg)

Léiríonn an pictiúr rith ar demo a thógann na tástálacha (`tests/test_stream.py`),
ní cluiche fíor.

## Roghanna {#options}

| Rogha | Réamhshocrú | Cad a dhéanann sí |
|---|---|---|
| `demos` (ceann amháin nó níos mó) | - | comhaid `.replay`, nó fillteáin ina bhfuil siad |
| `-o`, `--out` | riachtanach | an fillteán le scríobh ann; téann gach demo isteach in `<out>/<map>/` |
| `--flat` | as | scríobh go díreach isteach sa fhillteán, gan an fillteán `<map>/` |
| `--json` | as | priontáil líne JSON amháin in aghaidh an demo ar stdout (do chláir a ghlaonn an t-ordú): `demo`, `ok`, `parquet`, `match`, `sidecars`, `lost`, `rows`, `players`, `layer`, `recorded_unix`; priontálann demo a theip `demo`, `ok: false` agus `error` ina ionad |
| `--version` | - | priontáil an leagan agus stop |

Gach rogha, mar a phriontálann an clár í: [Tagairt orduithe](../cli-reference.md).

Is é ainm na léarscáile ainm an fhillteáin léarscáile, tógtha ón gcosán leibhéil a ainmníonn an demo
(`/Game/Maps/<Map>/Gameplay_Layers/<Layer>` a thugann `<Map>`).

Stádas scoir: 0 nuair a tiontaíodh gach demo; 1 nuair a theip ar aon cheann (scríobhtar na cinn eile
fós) nó nuair nach bhfuarthas aon chomhad `.replay`.

## Cad a thagann amach {#what-comes-out}

| Comhad | Cad atá ann |
|---|---|
| `<demo>.parquet` | an tábla: suíomhanna agus imeachtaí, ceann in aghaidh na sraithe ([An tábla](output-table.md)) |
| `<demo>.match.json` | doiciméad an chluiche ([Doiciméad an chluiche agus na taobhchomhaid](output-match.md)) |
| `<demo>.entities.parquet` | taobhchomhad: gach nuashonrú airí agus gach glao cianda, iomlán |
| `<demo>.packets.parquet` | taobhchomhad: codanna an chomhaid agus gach rud nár léadh, iomlán |

Is é an péire céanna an tábla agus doiciméad an chluiche a scríobhann uirlis CS2 3DHeat.
Osclaíonn an lucht féachana an tábla go díreach agus fágann sé na taobhchomhaid ar lár nuair a
lódáiltear fillteán iomlán.

## Samplaí {#examples}

```bash
heat3d-squad-demo D:\SquadDemos -o out                 # every demo in a folder
heat3d-squad-demo one.replay two.replay -o out --flat  # straight into out/
heat3d-squad-demo D:\SquadDemos -o out --json          # one JSON line per demo
```

Is fillteán samplach ar dhiosca D é `D:\SquadDemos`: úsáid ceann de do chuid féin.
