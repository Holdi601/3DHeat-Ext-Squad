---
title: Kampdokumentet og sidefilene
nav_order: 5
lang: no
source: output-match.md
source_hash: "715bd3417e47"
nav_exclude: true
search_exclude: true
---
# Kampdokumentet og sidefilene {#the-match-document-and-sidecars}

Ved siden av tabellen får hver demo `<demo>.match.json` og to sidefiler,
`<demo>.entities.parquet` og `<demo>.packets.parquet`. Visningsprogrammet leser
kampdokumentet i sin Kamp-fane.

## Kampdokumentet {#the-match-document}

`<demo>.match.json` (kampdokumentet) holder på toppnivå `map`, `layer`, `level_path`, `game_version`, `engine_version`, `recorded_unix`, `duration_s`, `teams`, `squads`, `game_state`, `actors`, `players`, `rows`, `events`, `not_read`, `file`, `header`, `chunks`, `stream`, `shots` og `selfCheck` (hele listen: [Kommandoreferanse](../cli-reference.md)). Med ord: kartet og laget, spillversjonen og motorversjonen, opptakstidspunktet, lengden, og:

- **lagene**: nummer, fraksjon og alt deres tilstand replikerte (billetter, tilgjengelighet, sjef) etter hvert som den endret seg;
- **troppene**: nummer, lag, navn, skaper, leder, medlemmer;
- **spillsituasjonen**: serverens navn og innstillinger, spillmodus, kampstatus og id, kart- og banerotasjoner, avstemninger, tidtakere, dagens melding;
- **aktørene**: hvert kjøretøy, utplasserbart objekt, stilling, ammunisjonskasse og helikopter - klasse, hvor og når det ble spawnet, når det forsvant, hvems det var, og dets replikerte tilstand (helse, byggestatus, seter...);
- **en linje for hver spiller**: prøver til fots og i kjøretøy, tilbakelagt distanse, spilte soldatklasser, brukte kjøretøy, lagbytter, tatte seter, og alt spillertilstanden replikerte (ping, nivå, rolle, nåværende sete...); og en linje for hver bot;
- **hendelsene** talt, **egenskapstellingen** (hvor ofte hver klasses egenskaper ble sendt) og **fjernkalltellingen**, skuddene og treffene, det som **ikke** ble lest, og leserens diagnostikk;
- **filen og headeren**: hvert felt i infoblokken og demoheaderen, bittabellen, eksporttabellene for nettfelt (`net_field_exports`), kanalenes lukkeårsaker, og klassene funnet for objekter eksportene ikke navngir (`stream.class_resolution`);
- **selvkontrollen** (`selfCheck.completeness`, se [Fullstendighet](#completeness)).

Online-id-er (Steam, EOS) er utelatt med vilje.

Et raskt blikk på en konvertert demo:

```bash
python -c "import json; d = json.load(open('out/<map>/<demo>.match.json')); print(d['map'], d['layer'], d['duration_s'], len(d['players']))"
```

## Fullstendighet {#completeness}

Denne leseren følger regelen alle 3DHeat-konvertere deler: dekod det som kan leses nå, behold resten hel, og si hvor mye av hver type den gjorde ([Konvertere beholder alt](https://github.com/Holdi601/3DHeat/blob/main/docs/converters.md)). Hvert kampdokument har `selfCheck.completeness`: per type element møtt i demoen, hvor mange som var `seen`, `decoded`, `partial` (dekodet delvis og holdt hel), `raw` (bare holdt hel) og `lost` (må være 0). Typene telles der leseren møter dem: `file.info`, `chunk.<kind>`, `frame`, `packet`, `bunch`, `open`, `close`, `export.field`, `export.guid`, `external`, `property:<class>`, `rpc:<class>`, `block:<object>`, `subobject.*`.

På de virkelige demoene som ble lest, er `lost` 0: deres elementer går fra hundretusener til millioner; omtrent halvparten dekodes fullt, resten er delvise eller rå.

**Lest** (inn i tabellen og kampdokumentet):

- infoblokken, demoheaderen (hvert felt; to avsluttende byte som ikke er kjent holdes som hex), bittabellen;
- hver ramme, pakke og bunch (delt helt i det de bærer), hver aktør som ble åpnet (med dens spawn-posisjon, rotasjon, skala og hastighet) og lukket (med hvorfor: `Destroyed`, `Dormancy`...);
- hver replikert egenskap, så langt bitene sier ([Dekoding av egenskaper](how-it-works.md#decoding-properties)), posisjoner fra `FRepMovement` og fra helikoptrenes bevegelseskomponent, drapene, kjøretøyenes helse, seter;
- hvert fjernkall med navn, med parameterne der demoen eksporterer funksjonens gruppe: skudd (`fire`) og kjøretøytreff (`hit`) inn i tabellen;
- eksporttabellene for nettfelt og nett-GUID-ene (antallet; stiene er i sidefilen for entiteter).

**Holdt rå** (hel, med det som leses av den ved siden av):

- `<demo>.entities.parquet`, kolonnene `time`, `type` (`<class>.<property>`, `<class>.<call>`, eller objektets navn), `name` (aktørens klasse), `entity` (aktørens nett-GUID, som tabellens `entity`), `kind`, `object` (underobjektet), `channel`, `handle`, `group` (klassestien til eksportgruppen), `decoded` (JSON), `bits` og `payload` (bitene, lavest først, utfylt til hele byte):
  - hver egenskapsoppdatering (`kind` `property`), bevegelsen inkludert, med det som dekodes; rå bare der ingenting dekodes (ukjente håndtak, strukturer som `RotationReplicatedMovement` for tårn, og egenskaper som er igjen som bit);
  - hvert fjernkall og egendefinert delta-felt (`rpc`), parameterne dekodet der funksjonens gruppe ble eksportert; rå der ikke (`RepInventory`, `PlayerStateData`);
  - hver innholdsblokk til et objekt hvis klasse ikke kunne finnes (`block`: `Buoyancy`, `GameplayTasksComponent`, `AmmoRackComponent`...), med headeren dekodet;
  - hver aktørkanal som ble åpnet og lukket (`open`, `close`), hvert underobjekt som ble slettet eller ødelagt;
  - konteksten en senere dekoder trenger for å lese filen alene: hvert eksporterte nettfelt (`export.field`: gruppesti, håndtak, egenskapsnavn, sjekksum) og hver eksporterte nett-GUID (`export.guid`: dens sti, ytre og flagg), slik strømmen ga dem på tidspunktet.
- `<demo>.packets.parquet`, kolonnene `time`, `type`, `name`, `channel`, `offset` (i filen), `decoded`, `bits` og `payload`: infoblokken, headerbiten, hver sjekkpunkt-bit (et sjekkpunkt er tilstanden til hver aktør på sitt tidspunkt, som strømmen fra starten også holder), hver hendelsesbit, og hver ramme, pakke eller bunch som ikke leses (én bunch per demo: opptakerens egen tilskuers åpningsbunch), hel.

Radene i entitetene er gruppert etter `kind`, `type` og `entity`, hver i tidsrekkefølge; sorter etter `time` for strømmens rekkefølge.

**Ikke tilgjengelig:**

- det en serverdemo ikke tar opp: klienters inndata, det en spiller så;
- effekter på klientsiden: treffmarkører, lyder, drapsloggens tekst (serveren sender kallene, ikke deres visning);
- online-ID-er dekodet: holdt bare som bit (se [Personopplysninger](limits.md#personal-data)).
