---
title: "Mängu dokument ja lisafailid"
nav_order: 5
lang: "et"
source: output-match.md
source_hash: "715bd3417e47"
nav_exclude: true
search_exclude: true
---
# Mängu dokument ja lisafailid {#the-match-document-and-sidecars}

Tabeli kõrval saab iga demo `<demo>.match.json` ja kaks lisafaili,
`<demo>.entities.parquet` ja `<demo>.packets.parquet`. Vaataja loeb mängu dokumenti
oma Matš-vahelehel.

## Mängu dokument {#the-match-document}

`<demo>.match.json` (mängu dokument) sisaldab oma ülemisel tasemel `map`, `layer`, `level_path`, `game_version`, `engine_version`, `recorded_unix`, `duration_s`, `teams`, `squads`, `game_state`, `actors`, `players`, `rows`, `events`, `not_read`, `file`, `header`, `chunks`, `stream`, `shots` ja `selfCheck` (täielik loend: [Käsu viide](../cli-reference.md)). Sõnades: kaart ja tase, mängu ja mootori versioonid, salvestamise aeg, kestus ning:

- **meeskonnad**: number, vorm ja kõik, mida nende olek replitseeris (piletid, saadavused, komandör), nagu see muutus;
- **squadid**: number, meeskond, nimi, looja, juht, liikmed;
- **mängu olek**: serveri nimi ja seaded, mänguliik, mängu olek ja id, kaardi- ja tasemerotatsioonid, hääletused, taimerid, päeva teade;
- **actorid**: iga sõiduk, paigaldatav, emplacement, laskemoonakast ja helikopter - klass, kus ja millal see tekkis, millal see läks, kelle see oli, ning tema replitseeritud olek (tervis, ehitusseisund, istmed...);
- **rida iga mängija kohta**: proovid jalgsi ja sõidukites, läbitud vahemaa, mängitud sõduriklassid, kasutatud sõidukid, meeskonnavahetused, võetud istmed ning kõik, mida mängija olek replitseeris (ping, tase, roll, praegune istmed...); ja rida iga boti kohta;
- **sündmused** loendatuna, **omaduste loendus** (kui sageli iga klassi omadusi saadeti) ja **kaugkäskude loendus**, lasud ja tabamused, mis **ei loetud**, ning lugeja diagnostika;
- **fail ja päis**: iga infoploki ja demo päise väli, tükitabel, võrgu-väljade eksporditabelid (`net_field_exports`), kanalite sulgemise põhjused ja klassid, mis leiti objektidele, mida eksportid ei nimeta (`stream.class_resolution`);
- **enesekontroll** (`selfCheck.completeness`, vt [Täielikkus](#completeness)).

Online-ID-d (Steam, EOS) on tahtlikult välja jäetud.

Kiire vaade teisendatud demole:

```bash
python -c "import json; d = json.load(open('out/<map>/<demo>.match.json')); print(d['map'], d['layer'], d['duration_s'], len(d['players']))"
```

## Täielikkus {#completeness}

See lugeja järgib reeglit, mida jagavad kõik 3DHeati konverterid: loe nüüd see, mis on loetav, hoia ülejäänu tervena ja ütle, kui palju igat liiki on loetud ([Konverterid hoiavad kõike](https://github.com/Holdi601/3DHeat/blob/main/docs/converters.md)). Igal mängu dokumendil on `selfCheck.completeness`: iga demos kohatud üksuste liigi kohta, mitu oli `seen`, `decoded`, `partial` (osaliselt dekodeeritud ja tervena hoitud), `raw` (ainult tervena hoitud) ja `lost` (peab olema 0). Liigid loetakse seal, kus lugeja neid kohtab: `file.info`, `chunk.<kind>`, `frame`, `packet`, `bunch`, `open`, `close`, `export.field`, `export.guid`, `external`, `property:<class>`, `rpc:<class>`, `block:<object>`, `subobject.*`.

Loetud päris demodel on `lost` 0: nende üksused käivad sadadest tuhandetest miljoniteni; umbes pool dekodeerub täielikult, ülejäänud on osalised või toorandmed.

**Loetud** (tabelisse ja mängu dokumenti):

- infoplokk, demo päis (iga väli; kaks lõpubaiti, mida ei tuntud, hoitakse heksina) ja tükitabel;
- iga kaader, pakett ja bunch (jagatud tervena selle, mida nad kannavad), iga avatud actor (koos spawni asukoha, pöörde, suuruse ja kiirusega) ja iga suletud actor (koos põhjusega: `Destroyed`, `Dormancy`...);
- iga replitseeritud omadus, nii kaugele, kui tema bitid ütlevad ([Omaduste dekodeerimine](how-it-works.md#decoding-properties)), asukohad `FRepMovement`'ist ja helikopterite liikumiskomponendist, surmad, sõidukite tervis, istmed;
- iga kaugkäsk nime järgi, koos parameetritega, kui demo eksportis funktsiooni rühma: lasud (`fire`) ja sõidukite tabamused (`hit`) tabelisse;
- võrgu-väljade eksporditabelid ja võrgu GUID-id (nende arv; teed on lisafailis entities).

**Hoitud toorelt** (tervena, koos sellest loetuga kõrval):

- `<demo>.entities.parquet`, veerud `time`, `type` (`<class>.<property>`, `<class>.<call>` või objekti nimi), `name` (actori klass), `entity` (actori net GUID, nagu tabeli `entity`), `kind`, `object` (alamobjekt), `channel`, `handle`, `group` (eksportrühma klassi tee), `decoded` (JSON), `bits` ja `payload` (bitid, madalaimast algades, täisbaitideni täidetud):
  - iga omaduse uuendus (`kind` `property`), liikumine kaasa arvatud, koos dekodeeritud osaga; toorelt ainult seal, kus muud ei ole (nimetamata handle'id, struktuurid nagu pöörlemiste `RotationReplicatedMovement`, ja omadused, mis on jäetud bittidena);
  - iga kaugkäsk ja custom-delta väli (`rpc`), parameetrid dekodeeritud, kui funktsiooni rühm eksporditi; toorelt, kui mitte (`RepInventory`, `PlayerStateData`);
  - iga sisuplokk objektilt, mille klassi ei leitud (`block`: `Buoyancy`, `GameplayTasksComponent`, `AmmoRackComponent`...), päis dekodeeritud;
  - iga actorikanal, mis avati ja suleti (`open`, `close`), iga alamobjekt, mis kustutati või hävitati;
  - kontekst, mida hilisem dekooder vajab, et faili üksi lugeda: iga võrgu-välja eksport (`export.field`: rühma tee, handle, omaduse nimi, kontrollsumma) ja iga eksporditud net GUID (`export.guid`: tema tee, omanik ja lipud), sel ajal, kui voog need andis.
- `<demo>.packets.parquet`, veerud `time`, `type`, `name`, `channel`, `offset` (failis), `decoded`, `bits` ja `payload`: infoplokk, päise tükk, iga kontrollpunkti tükk (kontrollpunkt on iga actori seisund tema ajal, mida algusest peale hoidev voog samuti sisaldab), iga sündmuse tükk ja iga kaader, pakett või bunch, mida ei loeta (üks bunch demo kohta: registreerija enda pealtvaataja avamisbunch), tervena.

Entities-read on grupeeritud `kind`, `type` ja `entity` järgi, igaüks ajajärjekorras; sorteeri `time` järgi voo järjekorra saamiseks.

**Pole saadaval:**

- mida serveri demo ei salvesta: klientide sisendid, mida mängija nägi;
- kliendipoolsed efektid: tabamismärgid, helid, tapmiste loendi tekst (server saadab käsud, mitte nende kuvamist);
- dekodeeritud online-ID-d: hoitud ainult bittidena (vt [Isikuandmed](limits.md#personal-data)).
