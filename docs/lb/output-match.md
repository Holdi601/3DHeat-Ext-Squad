---
title: "D'Match-Dokument a Niewendateien"
nav_order: 5
lang: "lb"
source: output-match.md
source_hash: "715bd3417e47"
nav_exclude: true
search_exclude: true
---
# D'Match-Dokument a Niewendateien {#the-match-document-and-sidecars}

Niewent der Tabell kritt all Demo en `<demo>.match.json` an zwou Niewendateien,
`<demo>.entities.parquet` an `<demo>.packets.parquet`. De Viewer liest d'Match-Dokument
a sengem Match-Tab.

## D'Match-Dokument {#the-match-document}

`<demo>.match.json` (d'Match-Dokument) hält um ieweschten Niveau `map`, `layer`, `level_path`, `game_version`, `engine_version`, `recorded_unix`, `duration_s`, `teams`, `squads`, `game_state`, `actors`, `players`, `rows`, `events`, `not_read`, `file`, `header`, `chunks`, `stream`, `shots` an `selfCheck` (déi voll Lëscht: [Kommando-Referenz](../cli-reference.md)). A Wierder: d'Map an de Layer, d'Spill- an Engine-Versiounen, d'Opnamzäit, d'Längt, an:

- **d'Teams**: Nummer, Fraktioun an alles, wat hire State replizéiert huet (Tickets, Verfügbarkeeten, Commander), wéi et sech geännert huet;
- **d'Squads**: Nummer, Team, Numm, Ersteller, Leader, Memberen;
- **de Spillstand**: Servernumm an Astellungen, Spillmodus, Match-State an -ID, Map- a Layer-Rotatiounen, Ofstëmmungen, Timer, d'Message vum Dag;
- **d'Akteuren**: all Gefier, Deployable, Emplacement, Munitiounskëscht an Helikopter - Klass, wou a wéini et erschafft gouf, wéini et fort war, wiem et gehéiert, a säi replizéierte State (Gesondheet, Build-State, Sëtzer...);
- **eng Zeil fir all Spiller**: Echantillonen zu Fouss an a Gefierer, gelaafe Distanz, gespillt Zaldotenklassen, benotzt Gefierer, Teamwiessel, geholl Sëtzer, an alles, wat de Player-State replizéiert huet (Ping, Level, Roll, aktuelle Sëtz...); an eng Zeil fir all Bot;
- **d'Evenementer** gezielt, de **Property-Zensus** (wéi dacks d'Properties vun all Klass geschéckt goufen) an den **Remote-Call-Zensus**, d'Schëss an Treffer, wat **net** gelies gouf, an d'Diagnose vum Reader;
- **d'Datei an den Header**: all Feld vum Info-Block an vum Demo-Header, d'Chunk-Tabell, d'Net-Field-Export-Tabellen (`net_field_exports`), d'Zouginn-Grënn vun de Kanäl, an d'Klassen, déi fir Objeten fonnt goufen, déi d'Exports net nennen (`stream.class_resolution`);
- **de Selbstcheck** (`selfCheck.completeness`, kuckt [Vollstännegkeet](#completeness)).

Online-IDen (Steam, EOS) ginn absichtlech ausgelooss.

E séiere Bléck op eng konvertéiert Demo:

```bash
python -c "import json; d = json.load(open('out/<map>/<demo>.match.json')); print(d['map'], d['layer'], d['duration_s'], len(d['players']))"
```

## Vollstännegkeet {#completeness}

Dëse Reader follegt der Regel, déi all 3DHeat-Konverteren deelen: dekodéieren, wat elo ka gelies ginn, de Rescht komplett halen, a soen, wéi vill vun all Zort gemaach gouf ([Konverteren halen alles](https://github.com/Holdi601/3DHeat/blob/main/docs/converters.md)). All Match-Dokument huet `selfCheck.completeness`: pro Zort vun Element, dat an der Demo begéint gouf, wéi vill `seen` (gesinn), `decoded` (dekodéiert), `partial` (deelweis dekodéiert a komplett gehalen), `raw` (nëmmen komplett gehalen) an `lost` (verluer; muss 0 sinn) waren. D'Zorte ginn do gezielt, wou de Reader se begéint: `file.info`, `chunk.<kind>`, `frame`, `packet`, `bunch`, `open`, `close`, `export.field`, `export.guid`, `external`, `property:<class>`, `rpc:<class>`, `block:<object>`, `subobject.*`.

Bei de richtegen Demoen, déi gelies goufen, ass `lost` 0: hir Elementer ginn vun Honnertdausende bis zu Millioune; ongeféier d'Halschent dekodéiert voll, de Rescht ass partial oder raw.

**Gelies** (an d'Tabell an d'Match-Dokument):

- den Info-Block, den Demo-Header (all Feld; zwee hannescht Bytes, déi net bekannt sinn, ginn als Hex gehalen), d'Chunk-Tabell;
- all Frame, Packet a Bunch (ganz opgedeelt an dat, wat se droen), all Akteur, deen opgemaach gouf (mat senger Spawn-Plaz, Rotatioun, Skala a Geschwindegkeet) a zougemaach gouf (mat dem Grond: `Destroyed`, `Dormancy`...);
- all replizéiert Property, sou wäit seng Bits soen, wat et ass ([Properties dekodéieren](how-it-works.md#decoding-properties)), Positioune vun `FRepMovement` an vum Beweegungskomponent vun den Helikopteren, d'Verloschter, d'Gesondheet vun de Gefierer, d'Sëtzer;
- all Remote-Call mam Numm, mat sengen Parameteren, wou d'Demo d'Grupp vun der Funktioun exportéiert: Schëss (`fire`) an Treffer um Gefier (`hit`) an d'Tabell;
- d'Net-Field-Export-Tabellen an d'Net-GUIDen (hir Unzuel; d'Weeër sinn an der Entities-Niewendatei).

**Komplett gehalen** (ganz, mat deem, wat dovun gelies gëtt, niewendrun):

- `<demo>.entities.parquet`, Kolonnen `time`, `type` (`<class>.<property>`, `<class>.<call>`, oder den Numm vum Objet), `name` (d'Klass vum Akteur), `entity` (de Net-GUID vum Akteur, wéi den `entity` vun der Tabell), `kind`, `object` (dat Subobjet), `channel`, `handle`, `group` (de Klassewee vun der Export-Grupp), `decoded` (JSON), `bits` an `payload` (d'Bits, déi niddregst zuerst, op ganz Bytes opgefëllt):
  - all Property-Update (`kind` `property`), d'Beweegung abegraff, mat deem, wat dekodéiert ass; nëmmen do raw, wou näischt dekodéiert ass (onbenannt Handles, Strukturen wéi `RotationReplicatedMovement` vun Tierm, a Properties, déi als Bits bleiwen);
  - all Remote-Call a Custom-Delta-Feld (`rpc`), d'Parameter dekodéiert, wou d'Grupp vun der Funktioun exportéiert gouf; raw, wou net (`RepInventory`, `PlayerStateData`);
  - all Inhaltsblock vun engem Objet, deem seng Klass net fonnt gouf (`block`: `Buoyancy`, `GameplayTasksComponent`, `AmmoRackComponent`...), mat sengem Header dekodéiert;
  - all Akteur-Kanal, deen opgemaach a zougemaach gouf (`open`, `close`), all Subobjet, dat geläscht oder zerstéiert gouf;
  - de Kontext, deen e spéidere Dekoder brauch, fir d'Datei eleng ze liesen: all Net-Field-Export (`export.field`: Gruppewee, Handle, Property-Numm, Checksumm) an all exportéierte Net-GUID (`export.guid`: säi Wee, Outer a Flags), zu der Zäit, wou de Stream se ginn huet.
- `<demo>.packets.parquet`, Kolonnen `time`, `type`, `name`, `channel`, `offset` (an der Datei), `decoded`, `bits`, `payload`: den Info-Block, de Header-Chunk, all Checkpoint-Chunk (e Checkpoint ass de State vun allen Akteuren zu senger Zäit, deen de Stream vum Ufank un och hält), all Event-Chunk, an all Frame, Packet oder Bunch, deen sech net liese léisst (ee Bunch pro Demo: den Opmaachs-Bunch vum Zuschauer vum Recorder selwer), ganz.

D'Entities-Zeilen si no `kind`, `type` an `entity` gruppéiert, jidd no Zäit gerangéiert; sortéiert no `time` fir d'Reihenfolleg vum Stream.

**Net verfügbar:**

- wat eng Server-Demo net ophëlt: d'Inputen vun de Clienten, wat e Spiller gesinn huet;
- Effekter um Client: Hit-Markeren, Téin, den Text vum Kill-Feed (de Server schéckt d'Calls, net hir Usiicht);
- dekodéiert Online-IDen: nëmmen als Bits gehalen (kuckt [Perséinlech Daten](limits.md#personal-data)).
