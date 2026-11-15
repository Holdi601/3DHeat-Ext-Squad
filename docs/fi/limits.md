---
title: "Rajoitukset, päivitykset ja ehdot"
nav_order: 7
lang: fi
source: limits.md
source_hash: "ef3802087acc"
nav_exclude: true
search_exclude: true
---
# Rajoitukset, päivitykset ja ehdot {#limits-updates-and-terms}

## Ei luettu {#not-read}

- **Kuka tappoi kenet, ja vahinko sotilaille osumittain.** Nämä kulkevat aseiden ja pelaajatilojen
  etäkutsujen osumatuloksissa (`HitResultsZeroBased`, `MulticastOnImpact.Hit`), joiden rakennetta ei
  lueta; ne säilytetään kokonaisina sivutiedostossa entities. Vain uhrien terveys puretaan.
- **Botin joukkue.** Botin tilassa on luku, joka saattaa olla sen joukkue; ei vahvistettu, ei käytetty.
- **Missä sotilas katsoo sivulle** rungon kääntymän ylittäen.

## Pelipäivitykset {#game-updates}

Lukija riippuu moottorin tallennusmuodosta ja muutamasta Squadin luokan ja ominaisuuden nimestä.
Se ei riipu ominaisuuksien asetteluista, joita se ei näe: toisto nimeää ne itse.

**Mikä voi rikkoutua Squad-päivityksessä:**

- **Moottoripäivitys.** Squad siirtyi UE 5.7:ään versiossa v10.4, eikä tätä ole testattu siinä. Päivitys
  voi muuttaa niputtimen otsikkoa, synnyt-dataa tai `FRepMovementia`. Nämä ovat koodissa versiosidonnaisia
  siellä, missä askel tunnetaan. Tuntemattomat askeleet (`ENG_PARTIAL_CUSTOM_EXPORTS`, lopullinen
  liikebitti) on lukittu siihen, mitä v10.3.1 tekee.
- **Iris-replikointi.** Jos Squad siirtyisi Iris-järjestelmään, nippujen sisäinen striimi olisi uusi, eikä tämä
  lukija lukisi sitä. Squad v10.3.1 käyttää klassista järjestelmää (se ajaa ReplicationGraphia).
- **Uudelleennimetyt luokat tai ominaisuudet.** Jos Squad nimeäisi uudelleen pelaaja-, joukkue- tai
  ryhmäluokkansa tai niiden ominaisuudet, nimet tai joukkueet katoaisivat, mutta sijainnit eivät.
- **Mitä tapahtuu virheessä.** Kun formaatti muuttuu, lukija pettää äänekkäästi striimivirheillä tai
  liikevirheillä diagnostiikassa. Se ei tuota hiljaa vääriä sijainteja: `FRepMovement` hyväksytään vain,
  kun sen bitit täsmäävät tarkasti.

## Henkilötiedot {#personal-data}

Demo sisältää kaikkien palvelimella olevien nimet ja verkkotunnukset. Taulukko ja ottelun asiakirja
kantavat nimiä, eivät tunnuksia. Sivutiedostot säilyttävät jokaisen ominaisuuden bitit, joten ne
sisältävät tunnukset siinä muodossa kuin demo ne sisältää (ei purettuina). Käsittele kaikkia niitä kuten
itse demoa.

## Lisenssi ja lähteet {#licence-and-sources}

MIT; katso [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-Squad/blob/main/LICENSE). Kaikki tässä on
kirjoitettu tätä pakettia varten. Mitään kolmannen osapuolen koodia ei sisälly tai linkitetä: ainoat
riippuvuudet ovat pyarrow (Apache-2.0) ja numpy (BSD-3-Clause).

Tiedot formaatista tulevat näistä lähteistä:

- **Unreal.Core** kohdassa [FortniteReplayDecompressor](https://github.com/Shiqan/FortniteReplayDecompressor)
  (MIT). Se kuvaa yleisen Unreal-toiston asettelun: infolohkon, osat, kehykset, niput ja net field -viennit.
- **[squad-replay](https://github.com/Codycody31/squad-replay)** (MPL-2.0). Sen jäsentäjää luettiin asettelun
  osalta sellaisena kuin Squad v10.3.1 sen kirjoittaa, versiotarkistusten osalta ja sen osalta, mitkä Squad-luokat
  kantavat joukkuetietoja. Sen julkaistuja testidemoja ja laskentatietoja käytettiin itsenäisenä
  ristitarkistuksena. Mitään sen koodia ei kopioitu tai käännetty: tämä lukija on rakennettu eri tavalla
  (Python-bittiarkisto kokonaisille paketeille, osittaiset nipput yhdistetään bitti kerrallaan, ominaisuudet
  lähetetään nimen mukaan), ja kaksi asiaa, joita se ei tee, löydettiin täällä demoista itsestään: kolmas
  osittaisen nipun lippu ja lopullinen liikebitti.

Squad on Offworld Industriesin tavaramerkki. Tämä paketti lukee tiedostoja, joita Squad-palvelin kirjoittaa;
se ei koske peliin, sen koodiin tai arkistoihin. Offworldin palvelimien lisensointi- ja hallintakäytäntö ei
sano mitään demojen tallentamisesta tai analysoinnista. Squadin käyttöehdot kieltävät pelin itsensä
käänteissuunnittelun, mitä tämä ei tee.
