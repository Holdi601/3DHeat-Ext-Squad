---
title: "Ottelun asiakirja ja sivutiedostot"
nav_order: 5
lang: fi
source: output-match.md
source_hash: "715bd3417e47"
nav_exclude: true
search_exclude: true
---
# Ottelun asiakirja ja sivutiedostot {#the-match-document-and-sidecars}

Taulukon rinnalla jokainen demo saa tiedoston `<demo>.match.json` ja kaksi sivutiedostoa,
`<demo>.entities.parquet` ja `<demo>.packets.parquet`. Katselin lukee ottelun asiakirjan
Ottelu-välilehdellään.

## Ottelun asiakirja {#the-match-document}

`<demo>.match.json` (ottelun asiakirja) sisältää ylimmällä tasollaan kentät `map`, `layer`, `level_path`,
`game_version`, `engine_version`, `recorded_unix`, `duration_s`, `teams`, `squads`, `game_state`, `actors`,
`players`, `rows`, `events`, `not_read`, `file`, `header`, `chunks`, `stream`, `shots` ja `selfCheck`
(koko luettelo: [Komentoviite](../cli-reference.md)). Lyhyesti: kartta ja kenttä, pelin ja moottorin versiot,
tallennusaika, pituus, ja:

- **joukkueet**: numero, puoli ja kaikki, mitä niiden tila replikoi (lippuja, saatavuuksia, komentaja),
  sitä mukaa kun se muuttui;
- **joukkueiden ryhmät**: numero, joukkue, nimi, perustaja, johtaja, jäsenet;
- **pelin tila**: palvelimen nimi ja asetukset, pelimuoto, ottelun tila ja tunnus, kartta- ja kenttäkierrot,
  äänestykset, ajastimet, päivän viesti;
- **toimijat**: jokainen ajoneuvo, siirrettävä tukikohta, asema, ammuslaatikko ja helikopteri – luokka, missä
  ja milloin se syntyi, milloin se poistui, kenen se oli ja sen replikoitu tila (terveys, rakennustila, istuimet...);
- **rivi jokaiselle pelaajalle**: näytteet jalan ja ajoneuvoissa, kuljettu matka, pelatut sotilasluokat,
  käytetyt ajoneuvot, joukkueen vaihdot, otetut istuimet sekä kaikki, mitä pelaajatila replikoi (ping, taso,
  rooli, nykyinen istuin...); ja rivi jokaiselle botille;
- **tapahtumat** laskettuina, **ominaisuuslaskenta** (kuinka usein kunkin luokan ominaisuuksia lähetettiin) ja
  **etäkutsulaskenta**, laukaukset ja osumat, mitä **ei** luettu, sekä lukijan diagnostiikka;
- **tiedosto ja otsikko**: jokainen infolohkon ja demo-otsikon kenttä, osien taulukko, net field -vientitaulukot
  (`net_field_exports`), kanavien sulkemisen syyt ja objekteille löydetyt luokat, joita viennit eivät nimeä
  (`stream.class_resolution`);
- **itsetarkistus** (`selfCheck.completeness`, ks. [Täydellisyys](#completeness)).

Verkkotunnukset (Steam, EOS) on jätetty pois tarkoituksella.

Pikainen katsaus muunnettuun demoon:

```bash
python -c "import json; d = json.load(open('out/<map>/<demo>.match.json')); print(d['map'], d['layer'], d['duration_s'], len(d['players']))"
```

## Täydellisyys {#completeness}

Tämä lukija noudattaa kaikkien 3DHeat-muuntimien yhteistä sääntöä: lue, mikä voidaan lukea heti, säilytä loput
kokonaisina ja kerro, kuinka paljon kutakin lajia on ([Muuntimet säilyttävät kaiken](https://github.com/Holdi601/3DHeat/blob/main/docs/converters.md)).
Jokaisella ottelun asiakirjalla on `selfCheck.completeness`: jokaista demossa kohdattua kohdetyyppiä kohden,
kuinka monta oli `seen` (nähty), `decoded` (purettu), `partial` (purettu osittain ja säilytetty kokonaisena),
`raw` (vain säilytetty kokonaisena) ja `lost` (pitää olla 0). Tyypit lasketaan siellä, missä lukija ne kohtaa:
`file.info`, `chunk.<kind>`, `frame`, `packet`, `bunch`, `open`, `close`, `export.field`, `export.guid`, `external`,
`property:<class>`, `rpc:<class>`, `block:<object>`, `subobject.*`.

Luetuissa oikeissa demoissa `lost` on 0: niiden kohteita on sadoista tuhansista miljooniin; noin puolet purkautuu
kokonaan, loput ovat osittaisia tai raakoja.

**Luettu** (taulukkoon ja ottelun asiakirjaan):

- infolohko, demo-otsikko (jokainen kenttä; kaksi lopussa olevaa tuntematonta tavua säilytetään heksadesimaalina) ja
  osien taulukko;
- jokainen kehys, paketti ja nippu (jaettu kokonaisena siihen, mitä ne kantavat), jokainen avattu toimija
  (synnyttyään sijainnilla, kiertymällä, skaalalla ja nopeudella) ja suljettu toimija (syy: `Destroyed`, `Dormancy`...);
- jokainen replikoitu ominaisuus niin pitkälle kuin sen bitit kertovat ([Ominaisuuksien purkaminen](how-it-works.md#decoding-properties)),
  sijainnit `FRepMovementista` ja helikoptereiden liikekomponentista, kuolemat, ajoneuvojen terveys, istuimet;
- jokainen etäkutsu nimeltään, parametreineen silloin, kun demo vie funktion ryhmän: laukaukset (`fire`) ja
  ajoneuvojen osumat (`hit`) taulukkoon;
- net field -vientitaulukot ja net GUIDit (niiden määrä; polut ovat sivutiedostossa entities).

**Säilytetty raakana** (kokonaisena, ja siitä luettu näkyy sen rinnalla):

- `<demo>.entities.parquet`, sarakkeet `time`, `type` (`<class>.<property>`, `<class>.<call>` tai objektin nimi),
  `name` (toimijan luokka), `entity` (toimijan net GUID, kuten taulukon `entity`), `kind`, `object` (alaobjekti),
  `channel`, `handle`, `group` (vientiryhmän luokkapolku), `decoded` (JSON), `bits` ja `payload` (bitit, alimmasta
  ylöspäin, täytettynä kokonaisiin tavuihin):
  - jokainen ominaisuuspäivitys (`kind` `property`), liike mukaan lukien, sekä purettu tieto; raakana vain siellä,
    missä ei mitään voi purkaa (nimettömät kahvat, rakenteet kuten turrettien `RotationReplicatedMovement`, ja
    ominaisuudet, jotka jäävät biteiksi);
  - jokainen etäkutsu ja mukautettu delta-kenttä (`rpc`), parametrit purettuina siellä, missä funktion ryhmä vietiin;
    raakana muualla (`RepInventory`, `PlayerStateData`);
  - jokainen sisältölohko objektista, jonka luokkaa ei löytynyt (`block`: `Buoyancy`, `GameplayTasksComponent`,
    `AmmoRackComponent`...), otsikkonsa purettuna;
  - jokainen toimijakanava, joka avattiin ja suljettiin (`open`, `close`), jokainen alaobjekti, joka poistettiin tai tuhottiin;
  - kontekstin, jonka myöhempi purkaja tarvitsee lukeakseen tiedoston yksin: jokainen net field -vienti
    (`export.field`: ryhmän polku, kahva, ominaisuuden nimi, tarkistussumma) ja jokainen viety net GUID
    (`export.guid`: sen polku, ulompi objekti ja liput), siinä ajassa, jolloin striimi ne antoi.
- `<demo>.packets.parquet`, sarakkeet `time`, `type`, `name`, `channel`, `offset` (tiedostossa), `decoded`, `bits` ja
  `payload`: infolohko, otsikko-osa, jokainen tarkistuspiste-osa (tarkistuspiste on jokaisen toimijan tila sen
  hetkellä, minkä striimi alusta alkaen myös pitää), jokainen tapahtuma-osa sekä jokainen kehys, paketti tai nippu,
  joka ei lue (demossa yksi nippu: tallentajan oman katsojatoimijan avaava nippu), kokonaisena.

Entities-rivit ryhmitellään lajin `kind`, `type` ja `entity` mukaan, kukin aikajärjestyksessä; järjestä `time`-sarakkeen
mukaan saadaksesi striimin järjestyksen.

**Ei saatavilla:**

- mitä palvelindemo ei tallenna: asiakkaiden syötteet, mitä pelaaja näki;
- asiakaspuolen vaikutukset: osumamerkit, äänet, tappolokin teksti (palvelin lähettää kutsut, ei niiden näyttöä);
- verkkotunnukset purettuina: säilytetään vain bitteinä (ks. [Henkilötiedot](limits.md#personal-data)).
