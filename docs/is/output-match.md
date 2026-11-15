---
title: "Leikskjalið og hliðarskrár"
nav_order: 5
lang: is
source: output-match.md
source_hash: "715bd3417e47"
nav_exclude: true
search_exclude: true
---
# Leikskjalið og hliðarskrár {#the-match-document-and-sidecars}

Auk töflunnar fær hvert demo `<demo>.match.json` og tvær hliðarskrár,
`<demo>.entities.parquet` og `<demo>.packets.parquet`. Skoðarinn les
leikskjalið í flipanum Leikur.

## Leikskjalið {#the-match-document}

`<demo>.match.json` (leikskjalið) geymir á efsta stigi `map`, `layer`, `level_path`, `game_version`, `engine_version`, `recorded_unix`, `duration_s`, `teams`, `squads`, `game_state`, `actors`, `players`, `rows`, `events`, `not_read`, `file`, `header`, `chunks`, `stream`, `shots` og `selfCheck` (heildarlistinn: [Skipanayfirlit](../cli-reference.md)). Í orðum: kortið og lagið, útgáfur leiks og vélar, upptökutíminn, lengdin, og:

- **liðin**: númer, fylking og allt sem staða þeirra afritaði (miðar, tiltækileiki, foringi) eftir því sem það breyttist;
- **sveitirnar**: númer, lið, nafn, stofnandi, foringi, meðlimir;
- **leikstaðan**: nafn þjóns og stillingar, leikhamur, leikstaða og auðkenni, kortaraðir og laga, atkvæðagreiðslur, tímamælar, skilaboð dagsins;
- **leikaðilarnir**: sérhvert ökutæki, uppsett mannvirki, skotstæði, skotfærakassi og þyrla - flokkur, hvar og hvenær það birtist, hvenær það hvarf, hvers það er, og afrituð staða þess (heilsa, byggingarstaða, sæti...);
- **lína fyrir hvern leikmann**: sýni fótgangandi og í ökutækjum, gengin vegalengd, hermannaflokkar sem spilaðir voru, ökutæki sem notuð voru, liðaskipti, sæti sem tekin voru, og allt sem leikmannsstaðan afritaði (ping, stig, hlutverk, núverandi sæti...); og lína fyrir hvern bot;
- **atburðirnir** taldir, **eigindatalningin** (hversu oft eigindir hvers flokks voru sendar) og **fjarkallatalningin**, skotin og höggin, það sem var **ekki** lesið, og greiningarupplýsingar lesarans;
- **skráin og hausinn**: sérhver reitur upplýsingablokkarinnar og haus demo-sins, bútatafla, net field export töflurnar (`net_field_exports`), lokunarástæður rásanna, og flokkarnir sem fundust fyrir hluti sem exports nefna ekki (`stream.class_resolution`);
- **sjálfsskoðunin** (`selfCheck.completeness`, sjá [Heilleiki](#completeness)).

Nettengd auðkenni (Steam, EOS) eru viljandi útilokuð.

Fljótleg skoðun á umbreyttu demo:

```bash
python -c "import json; d = json.load(open('out/<map>/<demo>.match.json')); print(d['map'], d['layer'], d['duration_s'], len(d['players']))"
```

## Heilleiki {#completeness}

Þessi lesari fylgir reglunni sem allir 3DHeat-umbreytar deila: afkóða það sem lesa má núna, geyma afganginn í heild, og segja hversu mikið af hverri tegund var gert ([Umbreytar geyma allt](https://github.com/Holdi601/3DHeat/blob/main/docs/converters.md)). Hvert leikskjal hefur `selfCheck.completeness`: fyrir hverja tegund atriða sem mætt var í demo-inu, hversu mörg voru `seen`, `decoded`, `partial` (afkóðuð að hluta og geymd í heild), `raw` (aðeins geymd í heild) og `lost` (verður að vera 0). Tegundirnar eru taldar þar sem lesarinn mætir þeim: `file.info`, `chunk.<kind>`, `frame`, `packet`, `bunch`, `open`, `close`, `export.field`, `export.guid`, `external`, `property:<class>`, `rpc:<class>`, `block:<object>`, `subobject.*`.

Í raunverulegu demo-unum sem lesin voru er `lost` 0: atriðin skipta hundruðum þúsunda upp í milljónir; um helmingur afkóðast að fullu, hinn hlutinn er að hluta eða hrár.

**Lesið** (inn í töfluna og leikskjalið):

- upplýsingablokkin, haus demo-sins (sérhver reitur; tveir síðustu bætin sem ekki eru þekkt eru geymd sem hex), bútataflan;
- sérhver rammi, pakki og bunch (skipt í heild í það sem þeir bera), sérhver leikaðili opnaður (með spawn-staðsetningu, snúningi, kvarða og hraða) og lokaður (með ástæðu: `Destroyed`, `Dormancy`...);
- sérhver afrituð eigind, að því marki sem bitar hennar segja til um ([Afkóðun eiginda](how-it-works.md#decoding-properties)), staðsetningar úr `FRepMovement` og úr hreyfihlutum þyrlnanna, mannfallið, heilsa ökutækja, sæti;
- sérhvert fjarkall með nafni, með færibreytum þess þar sem demo-ið flytur út hóp fallsins: skot (`fire`) og högg á ökutæki (`hit`) inn í töfluna;
- net field export töflurnar og net GUID-in (fjöldi þeirra; slóðirnar eru í entities-hliðarskránni).

**Geymt hrátt** (í heild, með því sem lesið er úr því við hliðina):

- `<demo>.entities.parquet`, dálkar `time`, `type` (`<class>.<property>`, `<class>.<call>`, eða nafn hlutarins), `name` (flokkur leikaðilans), `entity` (net GUID leikaðilans, eins og `entity` töflunnar), `kind`, `object` (undirhluturinn), `channel`, `handle`, `group` (flokkaslóð export-hópsins), `decoded` (JSON), `bits` og `payload` (bitarnir, lægsti fyrst, fylltir upp í heil bæti):
  - sérhver eigindauppfærsla (`kind` `property`), hreyfingin meðtalin, með því sem er afkóðað; hrá aðeins þar sem ekkert er afkóðað (ónefnd handföng, gerðir eins og `RotationReplicatedMovement` virkja, og eigindir skildar eftir sem bitar);
  - sérhvert fjarkall og custom-delta reitur (`rpc`), færibreytur afkóðaðar þar sem hópur fallsins var fluttur út; hráar þar sem ekki (`RepInventory`, `PlayerStateData`);
  - sérhver efnisblokk hlutar þar sem flokkurinn fannst ekki (`block`: `Buoyancy`, `GameplayTasksComponent`, `AmmoRackComponent`...), með haus hans afkóðaðan;
  - sérhver leikaðilarás opnuð og lokuð (`open`, `close`), sérhver undirhlutur eyddur eða eyðilagður;
  - samhengið sem síðari afkóðari þarf til að lesa skrána einn: sérhver net field export (`export.field`: hópslóð, handfang, eigindarnafn, prófsumma) og sérhver útfluttur net GUID (`export.guid`: slóð hans, outer og flags), á þeim tíma sem straumurinn gaf þá.
- `<demo>.packets.parquet`, dálkar `time`, `type`, `name`, `channel`, `offset` (í skránni), `decoded`, `bits`, `payload`: upplýsingablokkin, haus-bútur, sérhver checkpoint-bútur (checkpoint er staða hvers leikaðila á þeim tíma, sem straumurinn frá upphafi geymir líka), sérhver atburðabútur, og sérhver rammi, pakki eða bunch sem les ekki (einn bunch í hverju demo: opnunarbunch áhorfandans sem tekur upp), í heild.

Entities-raðirnar eru flokkaðar eftir `kind`, `type` og `entity`, hver í tímaröð; raðaðu eftir `time` til að fá röð straumsins.

**Ekki tiltækt:**

- það sem þjónsdemo skráir ekki: inntak biðlara, það sem leikmaður sá;
- áhrif á biðlarahliðinni: höggmerki, hljóð, texti dráparununnar (þjónninn sendir kallið, ekki birtingu þess);
- afkóðuð nettengd auðkenni: aðeins geymd sem bitar (sjá [Persónuupplýsingar](limits.md#personal-data)).
