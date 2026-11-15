---
title: Kampdokumentet og sidecarene
nav_order: 5
lang: "da"
source: output-match.md
source_hash: "715bd3417e47"
nav_exclude: true
search_exclude: true
---
# Kampdokumentet og sidecarene {#the-match-document-and-sidecars}

Ved siden af tabellen får hver demo `<demo>.match.json` og to sidecars,
`<demo>.entities.parquet` og `<demo>.packets.parquet`. Fremviseren læser
kampdokumentet i sin Kamp-fane.

## Kampdokumentet {#the-match-document}

`<demo>.match.json` (kampdokumentet) holder på sit øverste niveau `map`, `layer`, `level_path`, `game_version`, `engine_version`, `recorded_unix`, `duration_s`, `teams`, `squads`, `game_state`, `actors`, `players`, `rows`, `events`, `not_read`, `file`, `header`, `chunks`, `stream`, `shots` og `selfCheck` (den fulde liste: [Kommandoreference](../cli-reference.md)). Med ord: kortet og banelaget, spillets og motorens versioner, optagelsestidspunktet, længden, og:

- **holdene**: nummer, fraktion og alt, hvad deres tilstand replikerede (billetter, tilgængelighed, chef) efterhånden som det ændrede sig;
- **squads**: nummer, hold, navn, opretter, leder, medlemmer;
- **spiltilstanden**: serverens navn og indstillinger, spiltilstand, kampens tilstand og id, rotation af kort og baner, afstemninger, timere, dagens besked;
- **aktørerne**: hvert køretøj, deployable, emplacement, ammunitionskasse og helikopter - klasse, hvor og hvornår det spawnede, hvornår det forsvandt, hvis det var, og dets replikerede tilstand (helbred, byggetilstand, sæder...);
- **en linje for hver spiller**: prøver til fods og i køretøjer, tilbagelagt afstand, soldatklasser spillet, køretøjer brugt, holdskift, sæder taget, og alt, spillertilstanden replikerede (ping, niveau, rolle, aktuelt sæde...); og en linje for hver bot;
- **hændelserne** talt, **egenskabstællingen** (hvor ofte hver klasses egenskaber blev sendt) og **remote call-tællingen**, skud og træf, hvad der **ikke** blev læst, og læserens diagnostik;
- **filen og headeren**: hvert felt i infoblokken og demo-headeren, bidde-tabellen, netfelt-eksporttabellerne (`net_field_exports`), kanalernes lukkeårsager, og klasserne fundet for objekter, som eksporterne ikke navngiver (`stream.class_resolution`);
- **selvkontrollen** (`selfCheck.completeness`, se [Fuldstændighed](#completeness)).

Online-id'er (Steam, EOS) er udeladt med vilje.

Et hurtigt kig på en konverteret demo:

```bash
python -c "import json; d = json.load(open('out/<map>/<demo>.match.json')); print(d['map'], d['layer'], d['duration_s'], len(d['players']))"
```

## Fuldstændighed {#completeness}

Denne læser følger den regel, alle 3DHeat-konvertere deler: afkod det, der kan læses nu, gem resten helt, og sig, hvor meget af hver slags den fik ([Konvertere gemmer alt](https://github.com/Holdi601/3DHeat/blob/main/docs/converters.md)). Hvert kampdokument har `selfCheck.completeness`: for hver type element, der mødes i demoen, hvor mange der blev `seen`, `decoded`, `partial` (afkodet delvist og gemt helt), `raw` (kun gemt helt) og `lost` (skal være 0). Typerne tælles, hvor læseren møder dem: `file.info`, `chunk.<kind>`, `frame`, `packet`, `bunch`, `open`, `close`, `export.field`, `export.guid`, `external`, `property:<class>`, `rpc:<class>`, `block:<object>`, `subobject.*`.

På de rigtige demoer, der er læst, er `lost` 0: deres elementer løber fra hundredtusinder til millioner; cirka halvdelen afkodes helt, resten er delvise eller rå.

**Læst** (ind i tabellen og kampdokumentet):

- infoblokken, demo-headeren (hvert felt; to afsluttende bytes, der ikke er kendt, gemmes som hex), bidde-tabellen;
- hver frame, pakke og bunch (opdelt helt i det, de bærer), hver aktør åbnet (med dens spawn-position, rotation, skala og hastighed) og lukket (med årsag: `Destroyed`, `Dormancy`...);
- hver replikeret egenskab, så langt dens bits siger ([Afkodning af egenskaber](how-it-works.md#decoding-properties)), positioner fra `FRepMovement` og fra helikoptrenes bevægelseskomponent, dødsfaldene, køretøjernes helbred, sæder;
- hvert remote call med navn, med dets parametre, hvor demoen eksporterer funktionens gruppe: skud (`fire`) og køretøjstræf (`hit`) ind i tabellen;
- netfelt-eksporttabellerne og net-GUID'erne (deres antal; stierne er i entitets-sidecaren).

**Gemt rå** (helt, med det, der læses af det, ved siden af):

- `<demo>.entities.parquet`, kolonnerne `time`, `type` (`<class>.<property>`, `<class>.<call>`, eller objektets navn), `name` (aktørens klasse), `entity` (aktørens net-GUID, som tabellens `entity`), `kind`, `object` (underobjektet), `channel`, `handle`, `group` (eksportgruppens klassesti), `decoded` (JSON), `bits` og `payload` (bitsene, laveste først, udfyldt til hele bytes):
  - hver egenskabsopdatering (`kind` `property`), bevægelsen inklusive, med det, der afkodes; rå kun hvor intet afkodes (ikke-navngivne handles, strukturer som `RotationReplicatedMovement` for tårne, og egenskaber, der står tilbage som bits);
  - hvert remote call og custom-delta-felt (`rpc`), parametrene afkodet, hvor funktionens gruppe blev eksporteret; rå, hvor den ikke blev (`RepInventory`, `PlayerStateData`);
  - hver indholdsblok af et objekt, hvis klasse ikke kunne findes (`block`: `Buoyancy`, `GameplayTasksComponent`, `AmmoRackComponent`...), med dens header afkodet;
  - hver aktørkanal åbnet og lukket (`open`, `close`), hvert underobjekt slettet eller ødelagt;
  - den kontekst, en senere afkoder har brug for for at læse filen alene: hvert netfelt-eksport (`export.field`: gruppesti, handle, egenskabsnavn, checksum) og hvert eksporteret net-GUID (`export.guid`: dets sti, outer og flag), på det tidspunkt streamen gav dem.
- `<demo>.packets.parquet`, kolonnerne `time`, `type`, `name`, `channel`, `offset` (i filen), `decoded`, `bits`, `payload`: infoblokken, headerbidden, hver checkpoint-bid (et checkpoint er tilstanden for hver aktør på dets tidspunkt, som streamen fra starten også holder), hver hændelsesbid, og hver frame, pakke eller bunch, der ikke læses (én bunch pr. demo: optagerens egen tilskuers åbnende bunch), helt.

Entitets-rækkerne er grupperet efter `kind`, `type` og `entity`, hver i tidsrækkefølge; sortér efter `time` for streamens rækkefølge.

**Ikke tilgængeligt:**

- det, en serverdemo ikke optager: klienters input, hvad en spiller så;
- klientsidede effekter: trefmarkører, lyde, dræbningsfeedens tekst (serveren sender kaldene, ikke deres visning);
- online-id'er afkodet: gemt kun som bits (se [Personlige data](limits.md#personal-data)).
