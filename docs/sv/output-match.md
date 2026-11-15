---
title: Matchdokumentet och sidofilerna
nav_order: 5
lang: "sv"
source: output-match.md
source_hash: "715bd3417e47"
nav_exclude: true
search_exclude: true
---
# Matchdokumentet och sidofilerna {#the-match-document-and-sidecars}

Bredvid tabellen får varje demo `<demo>.match.json` och två sidofiler,
`<demo>.entities.parquet` och `<demo>.packets.parquet`. Visaren läser matchdokumentet i sin Match-flik.

## Matchdokumentet {#the-match-document}

`<demo>.match.json` (matchdokumentet) innehåller på sin översta nivå `map`, `layer`, `level_path`, `game_version`, `engine_version`, `recorded_unix`, `duration_s`, `teams`, `squads`, `game_state`, `actors`, `players`, `rows`, `events`, `not_read`, `file`, `header`, `chunks`, `stream`, `shots` och `selfCheck` (hela listan: [Kommandoreferens](../cli-reference.md)). Med ord: kartan och lagret, spelets och motorns versioner, inspelningstiden, längden, och:

- **lagen**: nummer, fraktion och allt deras tillstånd replikerade (biljetter, tillgänglighet, befälhavare) när det ändrades;
- **truppar**: nummer, lag, namn, skapare, ledare, medlemmar;
- **spelläget**: serverns namn och inställningar, spelläge, matchstatus och id, karto- och lagerrotationer, röstningar, timers, dagens meddelande;
- **aktörerna**: varje fordon, utplacerad sak, bunker, ammunitionslåda och helikopter - klass, var och när den uppkom, när den försvann, vems den var, och dess replikerade tillstånd (hälsa, byggtillstånd, platser...);
- **en rad för varje spelare**: prov till fots och i fordon, tillryggalagd sträcka, soldatklasser som spelats, fordon som använts, lagbyten, platser som tagits, och allt spelarens tillstånd replikerat (ping, nivå, roll, nuvarande plats...); och en rad för varje bot;
- **händelserna** räknade, **egenskapsräkningen** (hur ofta varje klass egenskaper skickades) och **fjärranropsräkningen**, skotten och träffarna, vad som **inte** lästes, och läsarens diagnostik;
- **filen och huvudet**: varje fält i infoblocket och demohuvudet, delartabellen, nätfältens exporttabeller (`net_field_exports`), kanalernas stängningsorsaker, och klasserna som hittats för objekt som exporterna inte namnger (`stream.class_resolution`);
- **självkontrollen** (`selfCheck.completeness`, se [Fullständighet](#completeness)).

Online-ID:n (Steam, EOS) utelämnas med avsikt.

En snabb titt på en konverterad demo:

```bash
python -c "import json; d = json.load(open('out/<map>/<demo>.match.json')); print(d['map'], d['layer'], d['duration_s'], len(d['players']))"
```

## Fullständighet {#completeness}

Den här läsaren följer regeln alla 3DHeat-konverterare delar: avkoda det som kan läsas nu, spara resten hela, och säg hur mycket av varje sort den gjorde ([Konverterare behåller allt](https://github.com/Holdi601/3DHeat/blob/main/docs/converters.md)). Varje matchdokument har `selfCheck.completeness`: per sort post som mötts i demon, hur många som `seen` (sedda), `decoded` (avkodade), `partial` (delvis avkodade och sparade hela), `raw` (bara sparade hela) och `lost` (måste vara 0). Typerna räknas där läsaren möter dem: `file.info`, `chunk.<kind>`, `frame`, `packet`, `bunch`, `open`, `close`, `export.field`, `export.guid`, `external`, `property:<class>`, `rpc:<class>`, `block:<object>`, `subobject.*`.

På de riktiga demos som lästs är `lost` 0: deras poster går från hundratusentals till miljoner; ungefär hälften avkodas helt, resten är delvis eller rå.

**Läses** (in i tabellen och matchdokumentet):

- infoblocket, demohuvudet (varje fält; två avslutande bytes som inte är kända sparas som hex), delartabellen;
- varje bildruta, paket och bunt (delas hela i det de bär), varje aktör som öppnats (med dess uppkomstplats, rotation, skala och hastighet) och stängts (med varför: `Destroyed`, `Dormancy`...);
- varje replikerad egenskap, så långt dess bitar säger ([Avkoda egenskaper](how-it-works.md#decoding-properties)), positioner från `FRepMovement` och från helikoptrarnas rörelsekomponent, dödsfallen, fordonens hälsa, platser;
- varje fjärranrop med namn, med dess parametrar där demon exporterar funktionens grupp: skott (`fire`) och fordonsträffar (`hit`) in i tabellen;
- nätfältens exporttabeller och nätverks-GUID:erna (deras antal; vägarna finns i sidofilen för entiteter).

**Sparas rå** (hela, med det som lästs av dem bredvid):

- `<demo>.entities.parquet`, kolumnerna `time`, `type` (`<class>.<property>`, `<class>.<call>`, eller objektets namn), `name` (aktörens klass), `entity` (aktörens nätverks-GUID, som tabellens `entity`), `kind`, `object` (underobjektet), `channel`, `handle`, `group` (exportgruppens klassväg), `decoded` (JSON), `bits` och `payload` (bitarna, lägsta först, utfyllda till hela byte):
  - varje egenskapsuppdatering (`kind` `property`), rörelsen inkluderad, med det som avkodats; rå bara där inget avkodats (namnlösa handtag, strukturer såsom `RotationReplicatedMovement` för torn, och egenskaper kvar som bitar);
  - varje fjärranrop och anpassat deltafält (`rpc`), parametrarna avkodade där funktionens grupp exporterades; rå där inte (`RepInventory`, `PlayerStateData`);
  - varje innehållsblock för ett objekt vars klass inte kunde hittas (`block`: `Buoyancy`, `GameplayTasksComponent`, `AmmoRackComponent`...), med dess huvud avkodat;
  - varje aktörskanal som öppnats och stängts (`open`, `close`), varje underobjekt som tagits bort eller förstörts;
  - sammanhanget en senare avkodare behöver för att läsa filen ensam: varje nätfältexport (`export.field`: grupp-sökväg, handtag, egenskapsnamn, kontrollsumma) och varje exporterat nätverks-GUID (`export.guid`: dess sökväg, yttre objekt och flaggor), vid den tid strömmen gav dem.
- `<demo>.packets.parquet`, kolumnerna `time`, `type`, `name`, `channel`, `offset` (i filen), `decoded`, `bits` och `payload`: infoblocket, huvuddelen, varje kontrollpunktsdel (en kontrollpunkt är varje aktörs tillstånd vid sin tid, vilket strömmen från början också har), varje händelsedel, och varje bildruta, paket eller bunt som inte går att läsa (en bunt per demo: den inspelande spelarens egna åskådaraktörs inledande bunt), hela.

Posterna i entities-filen grupperas efter `kind`, `type` och `entity`, var och en i tidsordning; sortera på `time` för strömmens ordning.

**Inte tillgängligt:**

- det en serverdemo inte spelar in: klienters indata, vad en spelare såg;
- effekter på klientsidan: träffmarkörer, ljud, dödsloggens text (servern skickar anropen, inte deras visning);
- avkodade online-ID:n: sparade bara som bitar (se [Personuppgifter](limits.md#personal-data)).
