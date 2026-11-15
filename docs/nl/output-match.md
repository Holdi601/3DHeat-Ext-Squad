---
title: Het wedstrijddocument en de bijbestanden
nav_order: 5
lang: "nl"
source: output-match.md
source_hash: "715bd3417e47"
nav_exclude: true
search_exclude: true
---
# Het wedstrijddocument en de bijbestanden {#the-match-document-and-sidecars}

Naast de tabel krijgt elke demo `<demo>.match.json` en twee bijbestanden,
`<demo>.entities.parquet` en `<demo>.packets.parquet`. De viewer leest het wedstrijddocument in zijn
tabblad Match.

## Het wedstrijddocument {#the-match-document}

`<demo>.match.json` (het wedstrijddocument) bevat op het hoogste niveau `map`, `layer`, `level_path`, `game_version`, `engine_version`, `recorded_unix`, `duration_s`, `teams`, `squads`, `game_state`, `actors`, `players`, `rows`, `events`, `not_read`, `file`, `header`, `chunks`, `stream`, `shots` en `selfCheck` (de volledige lijst: [Commandoreferentie](../cli-reference.md)). In woorden: de kaart en de laag, de versies van het spel en de engine, de opnametijd, de lengte, en:

- **de teams**: nummer, factie en alles wat hun status repliceerde (tickets, beschikbaarheden, commandant) zoals het veranderde;
- **de squads**: nummer, team, naam, oprichter, leider, leden;
- **de spelstatus**: servernaam en instellingen, spelmodus, wedstrijdstatus en -id, rotaties van kaarten en lagen, stemmingen, timers, de boodschap van de dag;
- **de actors**: elk voertuig, elke opstelling, stelling, munitiekrat en helikopter - klasse, waar en wanneer het verscheen, wanneer het verdween, van wie het was, en zijn gerepliceerde status (gezondheid, bouwstatus, stoelen...);
- **een regel per speler**: monsters te voet en in voertuigen, afgelegde afstand, gespeelde soldatenklassen, gebruikte voertuigen, teamwissels, ingenomen stoelen, en alles wat de spelerstatus repliceerde (ping, level, rol, huidige stoel...); en een regel per bot;
- **de gebeurtenissen** geteld, de **eigenschapsinventaris** (hoe vaak de eigenschappen van elke klasse werden verstuurd) en de **inventaris van remote calls**, de schoten en treffers, wat **niet** gelezen werd, en de diagnose van de lezer;
- **het bestand en de header**: elk veld van het infoblok en de demo-header, de chunk-tabel, de netveld-exporttabellen (`net_field_exports`), de sluitredenen van de kanalen, en de klassen die gevonden zijn voor objecten die de exports niet benoemen (`stream.class_resolution`);
- **de zelfcontrole** (`selfCheck.completeness`, zie [Volledigheid](#completeness)).

Online-id's (Steam, EOS) zijn er bewust uitgelaten.

Een snelle blik op een omgezette demo:

```bash
python -c "import json; d = json.load(open('out/<map>/<demo>.match.json')); print(d['map'], d['layer'], d['duration_s'], len(d['players']))"
```

## Volledigheid {#completeness}

Deze lezer volgt de regel die alle 3DHeat-converters delen: decodeer wat nu gelezen kan worden, bewaar de rest volledig, en zeg hoeveel van elke soort er is gedecodeerd ([Converters bewaren alles](https://github.com/Holdi601/3DHeat/blob/main/docs/converters.md)). Elk wedstrijddocument heeft `selfCheck.completeness`: per soort item in de demo, hoeveel er `seen` (gezien), `decoded` (gedecodeerd), `partial` (deels gedecodeerd en volledig bewaard), `raw` (alleen volledig bewaard) en `lost` (moet 0 zijn) waren. De soorten worden geteld waar de lezer ze tegenkomt: `file.info`, `chunk.<kind>`, `frame`, `packet`, `bunch`, `open`, `close`, `export.field`, `export.guid`, `external`, `property:<class>`, `rpc:<class>`, `block:<object>`, `subobject.*`.

Bij de gelezen echte demo's is `lost` 0: hun items lopen van honderdduizenden tot miljoenen; ongeveer de helft wordt volledig gedecodeerd, de rest is deels of ruw.

**Gelezen** (in de tabel en het wedstrijddocument):

- het infoblok, de demo-header (elk veld; twee slotbytes die niet bekend zijn, worden als hex bewaard), de chunk-tabel;
- elk frame, elk pakket en elke bunch (volledig gesplitst in wat ze dragen), elke actor die geopend werd (met zijn startpositie, rotatie, schaal en snelheid) en gesloten (met de reden: `Destroyed`, `Dormancy`...);
- elke gerepliceerde eigenschap, voor zover de bits zeggen wat ze zijn ([Eigenschappen decoderen](how-it-works.md#decoding-properties)), posities uit `FRepMovement` en uit de bewegingscomponent van de helikopters, de slachtoffers, de gezondheid van voertuigen, stoelen;
- elke remote call bij naam, met zijn parameters waar de demo de groep van de functie exporteert: schoten (`fire`) en treffers op voertuigen (`hit`) in de tabel;
- de netveld-exporttabellen en de net-GUID's (hun aantal; de paden staan in het bijbestand entities).

**Ruw bewaard** (volledig, met wat ervan gelezen is ernaast):

- `<demo>.entities.parquet`, kolommen `time`, `type` (`<class>.<property>`, `<class>.<call>`, of de naam van het object), `name` (de klasse van de actor), `entity` (de net-GUID van de actor, als de `entity` van de tabel), `kind`, `object` (het subobject), `channel`, `handle`, `group` (het klassepad van de exportgroep), `decoded` (JSON), `bits` en `payload` (de bits, het laagste eerst, opgevuld tot hele bytes):
  - elke eigenschapsupdate (`kind` `property`), de beweging inbegrepen, met wat gedecodeerd is; ruw alleen waar niets gedecodeerd is (naamloze handles, structuren zoals `RotationReplicatedMovement` van torens, en eigenschappen die als bits zijn gebleven);
  - elke remote call en elk custom-delta-veld (`rpc`), de parameters gedecodeerd waar de groep van de functie is geëxporteerd; ruw waar niet (`RepInventory`, `PlayerStateData`);
  - elk contentblok van een object waarvan de klasse niet gevonden kon worden (`block`: `Buoyancy`, `GameplayTasksComponent`, `AmmoRackComponent`...), met zijn header gedecodeerd;
  - elk actorkanaal dat geopend en gesloten werd (`open`, `close`), elk subobject dat verwijderd of vernietigd werd;
  - de context die een latere decoder nodig heeft om het bestand alleen te lezen: elk netveld-export (`export.field`: groepspad, handle, eigenschapsnaam, checksum) en elke geëxporteerde net-GUID (`export.guid`: zijn pad, outer en vlaggen), op het moment dat de stream ze gaf.
- `<demo>.packets.parquet`, kolommen `time`, `type`, `name`, `channel`, `offset` (in het bestand), `decoded`, `bits` en `payload`: het infoblok, het headerchunk, elk checkpointchunk (een checkpoint is de toestand van elke actor op zijn tijdstip, die de stream vanaf het begin ook bevat), elk gebeurtenischunk, en elk frame, pakket of bunch dat niet gelezen kan worden (één bunch per demo: de openingsbunch van de eigen spectator van de opnemer), volledig.

De rijen van entities zijn gegroepeerd op `kind`, `type` en `entity`, elk in tijdvolgorde; sorteer op `time` voor de volgorde van de stream.

**Niet beschikbaar:**

- wat een serverdemo niet opneemt: invoer van clients, wat een speler zag;
- effecten aan clientzijde: trefferindicatoren, geluiden, de tekst van de killfeed (de server stuurt de calls, niet hun weergave);
- online-id's gedecodeerd: alleen als bits bewaard (zie [Persoonsgegevens](limits.md#personal-data)).
