---
title: Beperkingen, updates en voorwaarden
nav_order: 7
lang: "nl"
source: limits.md
source_hash: "8a9c7c448411"
nav_exclude: true
search_exclude: true
---
# Beperkingen, updates en voorwaarden {#limits-updates-and-terms}

## Niet gelezen {#not-read}

- **Wie wie doodde, en schade aan soldaten per treffer.** Deze reizen mee in de trefferresultaten van de remote calls van de wapens en spelerstatussen (`HitResultsZeroBased`, `MulticastOnImpact.Hit`), waarvan de structuur niet gelezen wordt; ze worden volledig bewaard in het bijbestand entities. Alleen de gezondheid van de slachtoffers wordt gedecodeerd.
- **Het team van de bot.** De status van een bot bevat een getal dat zijn team kan zijn; niet bevestigd, niet gebruikt.
- **Waar een soldaat zijwaarts kijkt**, voorbij de gier van het lichaam.

## Spelupdates {#game-updates}

De lezer hangt af van het replicatieformaat van de engine en een handvol klasse- en eigenschapsnamen van Squad. Hij hangt niet af van eigenschapsindelingen die hij niet kan zien: die benoemt de replay zelf.

**Wat er kan breken met een Squad-update:**

- **Een engine-upgrade.** Squad is met v10.4 naar UE 5.7 gegaan, en dat is daar niet getest. De upgrade kan de bunch-header, de spawngegevens of `FRepMovement` veranderen. Die zijn in de code versie-afhankelijk gemaakt waar de stap bekend is. Onbekende stappen (`ENG_PARTIAL_CUSTOM_EXPORTS`, het slotbit van de beweging) zijn vastgezet op wat v10.3.1 doet.
- **Iris-replicatie.** Als Squad naar Iris is overgestapt, zou de stream in de chunks nieuw zijn en zou deze lezer hem niet lezen. Squad v10.3.1 gebruikt het klassieke systeem (het draait op ReplicationGraph).
- **Hernoemde klassen of eigenschappen.** Als Squad zijn spelers-, team- of squadklassen of hun eigenschappen heeft hernoemd, zouden namen of teams ontbreken, maar posities niet.
- **Wat er gebeurt bij een fout.** Wanneer het formaat verandert, faalt de lezer hardop met streamfouten of bewegingsfouten in de diagnose. Hij levert niet stilletjes foute posities op: `FRepMovement` wordt alleen geaccepteerd wanneer de bits exact kloppen.

## Persoonsgegevens {#personal-data}

Een demo bevat de namen en online-id's van iedereen op de server. De tabel en het wedstrijddocument bevatten namen, geen id's. De bijbestanden bewaren alle bits van elke eigenschap, dus ze bevatten de id's zoals de demo ze heeft (niet gedecodeerd). Behandel ze allemaal als de demo zelf.

## Licentie en bronnen {#licence-and-sources}

MIT; zie [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-Squad/blob/main/LICENSE). Alles hier is geschreven voor dit pakket. Er is geen code van derden opgenomen of gekoppeld: de enige afhankelijkheden zijn pyarrow (Apache-2.0) en numpy (BSD-3-Clause).

Feiten over het formaat komen uit deze bronnen:

- **Unreal.Core** in [FortniteReplayDecompressor](https://github.com/Shiqan/FortniteReplayDecompressor) (MIT). Die beschrijft de algemene indeling van Unreal-replays: het infoblok, de chunks, frames, bunches en netveld-exports.
- **[squad-replay](https://github.com/Codycody31/squad-replay)** (MPL-2.0). De parser ervan is gelezen voor de indeling zoals Squad v10.3.1 die schrijft, voor de versiecontroles, en voor welke Squad-klassen de ledenlijsten dragen. Zijn gepubliceerde testdemo's en aantallen in snapshots zijn gebruikt als onafhankelijke controle. Geen van zijn code is gekopieerd of vertaald: deze lezer is anders opgebouwd (een bitarchief in Python over hele pakketten, gedeeltelijke bunches bit voor bit samengevoegd, eigenschappen gekozen op naam), en twee dingen die die parser niet doet, zijn hier op de demo's zelf gevonden: de derde vlag van gedeeltelijke bunches en het slotbit van de beweging.

Dit pakket leest de demobestanden die een Squad-server schrijft; het raakt het spel, de code en de archieven niet aan, en niets uit het spel zit erin of wordt verder verspreid. Wat het schrijft, blijft op je eigen machine.

3DHeat is niet verbonden aan en niet goedgekeurd door Offworld Industries. Squad en bijbehorende namen en handelsmerken zijn van hun eigenaars.

Rechthebbenden: open een issue op <https://github.com/Holdi601/3DHeat-Ext-Squad/issues> - we reageren snel en verwijderen alles op verzoek.
