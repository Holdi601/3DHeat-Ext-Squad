---
title: Id-dokument tal-partita u s-sidecars
nav_order: 5
lang: mt
source: output-match.md
source_hash: "715bd3417e47"
nav_exclude: true
search_exclude: true
---
# Id-dokument tal-partita u s-sidecars {#the-match-document-and-sidecars}

Minbarra t-tabella, kull demo tikseb `<demo>.match.json` u żewġ sidecars,
`<demo>.entities.parquet` u `<demo>.packets.parquet`. Il-viewer jaqra
id-dokument tal-partita fit-tab Match tiegħu.

## Id-dokument tal-partita {#the-match-document}

`<demo>.match.json` (id-dokument tal-partita) iżomm fil-livell ta' fuq `map`, `layer`, `level_path`, `game_version`, `engine_version`, `recorded_unix`, `duration_s`, `teams`, `squads`, `game_state`, `actors`, `players`, `rows`, `events`, `not_read`, `file`, `header`, `chunks`, `stream`, `shots` u `selfCheck` (il-lista sħiħa: [Referenza tal-kmandi](../cli-reference.md)). Bil-kliem: il-mappa u s-saff, il-verżjonijiet tal-logħba u tal-magna, il-ħin tar-rekordjar, it-tul, u:

- **it-timijiet**: numru, fazzjoni u dak kollu li l-istat tagħhom irrepika (biljetti, disponibbiltajiet, kmandant) kif inbidel;
- **l-iskwadri**: numru, tim, isem, il-ħalliq, il-mexxej, il-membri;
- **l-istat tal-logħba**: isem u settings tas-server, modalità tal-logħba, stat u id tal-partita, rotazzjonijiet tal-mapep u tas-saffi, voti, timers, il-messaġġ tal-ġurnata;
- **l-atturi**: kull vettura, deployable, emplacement, crate tal-munizzjon u elikopter - klassi, fejn u meta ħarġet, meta marret, ta' min hi, u l-istat irreplikat tagħha (saħħa, build state, sits...);
- **linja għal kull plejer**: kampjuni a piedi u fil-vetturi, distanza mixja, klassijiet ta' suldati mlaqqba, vetturi użati, bidliet ta' tim, sits meħuda, u dak kollu li l-player state irrepika (ping, livell, rwol, sit kurrenti...); u linja għal kull bot;
- **l-avvenimenti** magħduda, iċ-**census tal-proprjetajiet** (kemm-il darba nbagħtu l-proprjetajiet ta' kull klassi) u ċ-**census tas-sejħiet remoti**, l-isparaturi u d-daqqiet, dak li **ma** nqarax, u d-dijanjostika tal-qarrej;
- **il-fajl u l-header**: kull qasam tal-info block u tal-header tad-demo, it-tabella tal-chunks, it-tabelli tal-net field export (`net_field_exports`), ir-raġunijiet tal-għeluq tal-channels, u l-klassijiet misjuba għal oġġetti li l-exports ma jsemmux (`stream.class_resolution`);
- **is-self-check** (`selfCheck.completeness`, ara [Kompletezza](#completeness)).

L-online ids (Steam, EOS) jitħallew barra apposta.

Ħarsa mgħaġġla lejn demo kkonvertita:

```bash
python -c "import json; d = json.load(open('out/<map>/<demo>.match.json')); print(d['map'], d['layer'], d['duration_s'], len(d['players']))"
```

## Kompletezza {#completeness}

Dan il-qarrej isegwi r-regola li jaqsmu l-konvertituri kollha ta' 3DHeat: iddekodifika dak li jista' jinqara issa, żomm il-bqija sħiħ, u għid kemm għamel minn kull tip ([Il-konvertituri jżommu kollox](https://github.com/Holdi601/3DHeat/blob/main/docs/converters.md)). Kull dokument tal-partita għandu `selfCheck.completeness`: għal kull tip ta' oġġett li ltaqa' miegħu fid-demo, kemm kienu `seen`, `decoded`, `partial` (iddekodifikati parzjalment u miżmuma sħaħ), `raw` (miżmuma sħaħ biss) u `lost` (għandu jkun 0). It-tipi jingħaddu fejn il-qarrej jiltaqa' magħhom: `file.info`, `chunk.<kind>`, `frame`, `packet`, `bunch`, `open`, `close`, `export.field`, `export.guid`, `external`, `property:<class>`, `rpc:<class>`, `block:<object>`, `subobject.*`.

Fuq id-demos veri li nqraw, `lost` huwa 0: l-oġġetti tagħhom jvarjaw minn mijiet ta' eluf sa miljuni; madwar nofs jiddekodifikaw bis-sħiħ, il-bqija huma parzjali jew raw.

**Moqri** (fit-tabella u fid-dokument tal-partita):

- l-info block, il-header tad-demo (kull qasam; żewġ bytes fl-aħħar mhux magħrufa jinżammu bħala hex), it-tabella tal-chunks;
- kull frame, packet u bunch (maqsum sħiħ f'dak li jġorru), kull attur miftuħ (bil-lokazzjoni tal-ispawn, rotazzjoni, skala u veloċità tiegħu) u magħluq (u għaliex: `Destroyed`, `Dormancy`...);
- kull proprjetà rreplikata, safejn jgħidu l-bits tagħha ([Id-dekodifikar tal-proprjetajiet](how-it-works.md#decoding-properties)), pożizzjonijiet minn `FRepMovement` u mill-komponent tal-moviment tal-elikopters, il-vittmi, is-saħħa tal-vetturi, is-sits;
- kull sejħa remota b'isimha, bil-parametri tagħha fejn id-demo tesporta l-grupp tal-funzjoni: sparaturi (`fire`) u daqqiet fuq vetturi (`hit`) fit-tabella;
- it-tabelli tal-net field export u n-net GUIDs (l-għadd tagħhom; il-paths huma fis-sidecar tal-entities).

**Miżmum raw** (sħiħ, b'dak li nqara minnu ħdejh):

- `<demo>.entities.parquet`, kolonni `time`, `type` (`<class>.<property>`, `<class>.<call>`, jew l-isem tal-oġġett), `name` (il-klassi tal-attur), `entity` (in-net GUID tal-attur, bħall-`entity` tat-tabella), `kind`, `object` (is-subobject), `channel`, `handle`, `group` (il-path tal-klassi tal-export group), `decoded` (JSON), `bits` u `payload` (il-bits, l-iżgħar l-ewwel, imħaxxa għal bytes sħaħ):
  - kull aġġornament ta' proprjetà (`kind` `property`), il-moviment inkluż, b'dak li huwa ddekodifikat; raw biss fejn xejn mhu (handles bla isem, strutturi bħal `RotationReplicatedMovement` ta' turrets, u proprjetajiet li fadal bħala bits);
  - kull sejħa remota u qasam custom-delta (`rpc`), il-parametri ddekodifikati fejn il-grupp tal-funzjoni ġie esportat; raw fejn le (`RepInventory`, `PlayerStateData`);
  - kull content block ta' oġġett li l-klassi tiegħu ma nstabitx (`block`: `Buoyancy`, `GameplayTasksComponent`, `AmmoRackComponent`...), bl-header tiegħu ddekodifikat;
  - kull actor channel miftuħ u magħluq (`open`, `close`), kull subobject imħassar jew meqrud;
  - il-kuntest li dekoder aktar tard għandu bżonn biex jaqra l-fajl waħdu: kull net field export (`export.field`: path tal-grupp, handle, isem tal-proprjetà, checksum) u kull net GUID esportat (`export.guid`: il-path, l-outer u l-flags tiegħu), fil-ħin li taha l-istream.
- `<demo>.packets.parquet`, kolonni `time`, `type`, `name`, `channel`, `offset` (fil-fajl), `decoded`, `bits`, `payload`: l-info block, il-header chunk, kull checkpoint chunk (checkpoint huwa l-istat ta' kull attur fil-ħin tiegħu, li l-istream mill-bidu jżomm ukoll), kull event chunk, u kull frame, packet jew bunch li ma jinqarax (bunch wieħed għal kull demo: il-bunch tal-ftuħ tal-ispettatur tar-recorder nnifsu), sħiħ.

Ir-ringieli tal-entities huma miġbura skont `kind`, `type` u `entity`, kull waħda f'ordni tal-ħin; ordna skont `time` għall-ordni tal-istream.

**Mhux disponibbli:**

- dak li demo ta' server ma tirrekordjax: l-inputs tal-klijenti, dak li ra plejer;
- effetti min-naħa tal-klijent: hit markers, ħsejjes, it-test tal-kill feed (is-server jibgħat is-sejħiet, mhux il-wiri tagħhom);
- online IDs iddekodifikati: miżmuma bħala bits biss (ara [Dejta personali](limits.md#personal-data)).
