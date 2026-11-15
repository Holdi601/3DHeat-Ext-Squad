---
title: "Dokumenti i ndeshjes dhe skedarët anësorë"
nav_order: 5
lang: "sq"
source: output-match.md
source_hash: "715bd3417e47"
nav_exclude: true
search_exclude: true
---
# Dokumenti i ndeshjes dhe skedarët anësorë {#the-match-document-and-sidecars}

Përveç tabelës, çdo demo merr `<demo>.match.json` dhe dy skedarë anësorë,
`<demo>.entities.parquet` dhe `<demo>.packets.parquet`. Shikuesi e lexon
dokumentin e ndeshjes te skeda Ndeshja.

## Dokumenti i ndeshjes {#the-match-document}

`<demo>.match.json` (dokumenti i ndeshjes) mban në nivelin e sipërm `map`, `layer`, `level_path`, `game_version`, `engine_version`, `recorded_unix`, `duration_s`, `teams`, `squads`, `game_state`, `actors`, `players`, `rows`, `events`, `not_read`, `file`, `header`, `chunks`, `stream`, `shots` dhe `selfCheck` (lista e plotë: [Referenca e komandave](../cli-reference.md)). Me fjalë: hartën dhe shtresën, versionet e lojës dhe të motorit, kohën e regjistrimit, gjatësinë, dhe:

- **skuadrat**: numrin, fraksionin dhe çdo gjë që gjendja e tyre replikoi (biletat, disponueshmëritë, komandanti) ashtu si ndryshoi;
- **togat**: numrin, skuadrën, emrin, krijuesin, drejtuesin, anëtarët;
- **gjendjen e lojës**: emrin dhe cilësimet e serverit, mënyrën e lojës, gjendjen dhe id-në e ndeshjes, rotacionet e hartave dhe shtresave, votat, kohëmatësit, mesazhin e ditës;
- **aktorët**: çdo automjet, objekt të vendosur, pozicion, arkë municioni dhe helikopter - klasën, ku dhe kur u shfaq, kur iku, të kujt ishte, dhe gjendjen e tij të replikuar (shëndetin, gjendjen e ndërtimit, ndenjëset...);
- **një rresht për çdo lojtar**: mostrat në këmbë dhe në automjete, largësinë e ecur, klasat e ushtarëve të luajtura, automjetet e përdorura, ndërrimet e skuadrës, ndenjëset e zëna, dhe çdo gjë që gjendja e lojtarit replikoi (ping, nivel, rol, ndenjësen aktuale...); dhe një rresht për çdo bot;
- **ngjarjet** të numëruara, **regjistrimin e vetive** (sa herë u dërguan vetitë e çdo klase) dhe **regjistrimin e thirrjeve në distancë**, të shtënat dhe goditjet, çfarë **nuk** u lexua, dhe diagnostikimet e lexuesit;
- **skedarin dhe kokën**: çdo fushë të bllokut të informacionit dhe të kokës së demos, tabelën e copave, tabelat e eksportit të fushave të rrjetit (`net_field_exports`), arsyet e mbylljes së kanaleve, dhe klasat e gjetura për objektet që eksportet nuk i emërtojnë (`stream.class_resolution`);
- **vetëkontrollin** (`selfCheck.completeness`, shih [Plotësia](#completeness)).

ID-të online (Steam, EOS) lihen jashtë me qëllim.

Një vështrim i shpejtë mbi një demo të konvertuar:

```bash
python -c "import json; d = json.load(open('out/<map>/<demo>.match.json')); print(d['map'], d['layer'], d['duration_s'], len(d['players']))"
```

## Plotësia {#completeness}

Ky lexues ndjek rregullin që e ndajnë të gjithë konvertuesit 3DHeat: dekodo çfarë mund të lexohet tani, ruaje pjesën tjetër të plotë, dhe thuaj sa nga çdo lloj u bë ([Converters keep everything](https://github.com/Holdi601/3DHeat/blob/main/docs/converters.md)). Çdo dokument ndeshjeje ka `selfCheck.completeness`: për çdo lloj sendi të takuar në demo, sa ishin `seen` (parë), `decoded` (dekoduar), `partial` (dekoduar pjesërisht dhe ruajtur i plotë), `raw` (ruajtur vetëm i plotë) dhe `lost` (humbur, duhet të jetë 0). Llojet numërohen aty ku lexuesi i takon: `file.info`, `chunk.<kind>`, `frame`, `packet`, `bunch`, `open`, `close`, `export.field`, `export.guid`, `external`, `property:<class>`, `rpc:<class>`, `block:<object>`, `subobject.*`.

Në demot e vërteta të lexuara, `lost` është 0: sendet e tyre shkojnë nga qindra mijëra në miliona; rreth gjysma dekodohen plotësisht, pjesa tjetër është e pjesshme ose raw.

**Lexuar** (në tabelë dhe në dokumentin e ndeshjes):

- blloku i informacionit, koka e demos (çdo fushë; dy bajte të fundit të panjohura ruhen si hex), tabela e copave;
- çdo frame, paketë dhe bunch (ndarë i plotë në çfarë mbajnë), çdo aktor i hapur (me vendin, rrotullimin, shkallën dhe shpejtësinë e shfaqjes) dhe i mbyllur (me arsyen: `Destroyed`, `Dormancy`...);
- çdo veti e replikuar, aq sa thonë bitet e saj ([Dekodimi i vetive](how-it-works.md#decoding-properties)), pozicionet nga `FRepMovement` dhe nga komponenti i lëvizjes së helikopterëve, viktimat, shëndeti i automjeteve, ndenjëset;
- çdo thirrje në distancë me emër, me parametrat e saj aty ku demo eksporton grupin e funksionit: të shtënat (`fire`) dhe goditjet mbi automjete (`hit`) në tabelë;
- tabelat e eksportit të fushave të rrjetit dhe net GUID-et (numri i tyre; shtigjet janë në skedarin anësor entities).

**Ruajtur raw** (i plotë, me atë që lexohet prej tij pranë tij):

- `<demo>.entities.parquet`, kolonat `time`, `type` (`<class>.<property>`, `<class>.<call>`, ose emri i objektit), `name` (klasa e aktorit), `entity` (net GUID-i i aktorit, si `entity` i tabelës), `kind`, `object` (nënobjekti), `channel`, `handle`, `group` (shtegu i klasës i grupit të eksportit), `decoded` (JSON), `bits` dhe `payload` (bitet, më të vegjlit së pari, të plotësuara në bajte të plotë):
  - çdo përditësim vetie (`kind` `property`), edhe lëvizja, me atë që dekodohet; raw vetëm aty ku s'dekodohet asgjë (handle pa emër, struktura si `RotationReplicatedMovement` e frëngjive, dhe veti të lëna si bite);
  - çdo thirrje në distancë dhe fushë custom-delta (`rpc`), parametrat e dekoduar aty ku grupi i funksionit u eksportua; raw aty ku jo (`RepInventory`, `PlayerStateData`);
  - çdo bllok përmbajtjeje i një objekti të cilit nuk iu gjet dot klasa (`block`: `Buoyancy`, `GameplayTasksComponent`, `AmmoRackComponent`...), me kokën e dekoduar;
  - çdo kanal aktori i hapur dhe i mbyllur (`open`, `close`), çdo nënobjekt i fshirë ose i shkatërruar;
  - konteksti që i duhet një dekoderi të mëvonshëm për ta lexuar skedarin vetëm: çdo eksport fushe rrjeti (`export.field`: shtegu i grupit, handle, emri i vetisë, checksum) dhe çdo net GUID i eksportuar (`export.guid`: shtegu, outer dhe flamujt), në kohën kur i dha rrjedha.
- `<demo>.packets.parquet`, kolonat `time`, `type`, `name`, `channel`, `offset` (në skedar), `decoded`, `bits`, `payload`: blloku i informacionit, copa e kokës, çdo copë checkpoint (një checkpoint është gjendja e çdo aktori në kohën e tij, që e mban edhe rrjedha nga fillimi), çdo copë ngjarjesh, dhe çdo frame, paketë ose bunch që nuk lexohet (një bunch për demo: bunch-i i hapjes së spektatorit të vetë regjistruesit), e plotë.

Rreshtat e entities janë grupuar sipas `kind`, `type` dhe `entity`, secili sipas kohës; rendit sipas `time` për rendin e rrjedhës.

**Jo të disponueshme:**

- çfarë një demo serveri nuk regjistron: inputet e klientëve, çfarë pa një lojtar;
- efektet nga ana e klientit: shenjat e goditjeve, tingujt, teksti i kill feed-it (serveri dërgon thirrjet, jo shfaqjen e tyre);
- ID-të online të dekoduara: ruhen vetëm si bite (shih [Të dhënat personale](limits.md#personal-data)).
