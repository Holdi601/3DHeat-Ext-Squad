---
title: Dokument meča i prateće datoteke
nav_order: 5
lang: hr
source: output-match.md
source_hash: "715bd3417e47"
nav_exclude: true
search_exclude: true
---
# Dokument meča i prateće datoteke {#the-match-document-and-sidecars}

Uz tablicu, svaki demo dobije `<demo>.match.json` i dvije prateće datoteke,
`<demo>.entities.parquet` i `<demo>.packets.parquet`. Preglednik čita dokument meča
na svojoj kartici Meč.

## Dokument meča {#the-match-document}

`<demo>.match.json` (dokument meča) na vrhu sadrži `map`, `layer`, `level_path`, `game_version`, `engine_version`, `recorded_unix`, `duration_s`, `teams`, `squads`, `game_state`, `actors`, `players`, `rows`, `events`, `not_read`, `file`, `header`, `chunks`, `stream`, `shots` i `selfCheck` (cijeli popis: [Referenca naredbi](../cli-reference.md)). Ukratko: karta i razina, verzije igre i motora, vrijeme snimanja, trajanje i:

- **timovi**: broj, frakcija i sve što je njihovo stanje replicirao (karte, dostupnost, zapovjednik) kako se mijenjalo;
- **odredi**: broj, tim, ime, tko ga je stvorio, vođa, članovi;
- **stanje igre**: ime servera i postavke, način igre, stanje i ID meča, rotacije karata i razina, glasovanja, tajmeri, poruka dana;
- **akteri**: svako vozilo, postavljeni objekt, utvrda, sanduk s municijom i helikopter - klasa, gdje i kad se pojavio, kad je nestao, čiji je bio i njegovo replicirano stanje (zdravlje, stanje gradnje, sjedala...);
- **redak za svakog igrača**: uzorci pješice i u vozilima, prijeđena udaljenost, klase vojnika koje je igrao, korištena vozila, promjene tima, zauzeta sjedala i sve što je stanje igrača replicirao (ping, razina, uloga, trenutno sjedalo...); te redak za svakog bota;
- **događaji** prebrojeni, **popis svojstava** (koliko su se puta slala svojstva svake klase) i **popis udaljenih poziva**, hici i pogoci, što **nije** pročitano, te dijagnostika čitača;
- **datoteka i zaglavlje**: svako polje informacijskog bloka i zaglavlja dema, tablica dijelova, tablice izvoza mrežnih polja (`net_field_exports`), razlozi zatvaranja kanala i klase pronađene za objekte koje izvozi ne imenuju (`stream.class_resolution`);
- **samoprovjera** (`selfCheck.completeness`, vidi [Potpunost](#completeness)).

Mrežni ID-jevi (Steam, EOS) namjerno su izostavljeni.

Brzi pogled na pretvoreni demo:

```bash
python -c "import json; d = json.load(open('out/<map>/<demo>.match.json')); print(d['map'], d['layer'], d['duration_s'], len(d['players']))"
```

## Potpunost {#completeness}

Ovaj čitač slijedi pravilo koje dijele svi 3DHeat pretvarači: pročitati ono što se može pročitati odmah, ostatak sačuvati cijelim i reći koliko se čega pročitalo ([Pretvarači čuvaju sve](https://github.com/Holdi601/3DHeat/blob/main/docs/converters.md)). Svaki dokument meča ima `selfCheck.completeness`: za svaku vrstu stavke nađene u demou, koliko ih je `seen` (viđeno), `decoded` (dekodirano), `partial` (djelomično dekodirano i sačuvano cijelo), `raw` (samo sačuvano cijelo) i `lost` (mora biti 0). Vrste se broje tamo gdje ih čitač nađe: `file.info`, `chunk.<kind>`, `frame`, `packet`, `bunch`, `open`, `close`, `export.field`, `export.guid`, `external`, `property:<class>`, `rpc:<class>`, `block:<object>`, `subobject.*`.

Na pročitanim pravim demoima `lost` je 0: stavki ima od stotina tisuća do milijuna; otprilike polovica se dekodira potpuno, ostatak je djelomično ili sirovo.

**Pročitano** (u tablicu i dokument meča):

- informacijski blok, zaglavlje dema (svako polje; dva završna bajta koja nisu poznata sačuvana su kao heks), tablica dijelova;
- svaki okvir, paket i snop (rastavljen cijeli na ono što nosi), svaki otvoreni akter (s položajem pojave, rotacijom, skalom i brzinom) i zatvoreni (s razlogom: `Destroyed`, `Dormancy`...);
- svako replicirano svojstvo, koliko god njegovi bitovi govore ([Dekodiranje svojstava](how-it-works.md#decoding-properties)), položaji iz `FRepMovement` i iz komponente kretanja helikoptera, ubojstva, zdravlje vozila, sjedala;
- svaki udaljeni poziv po imenu, s parametrima tamo gdje demo izvozi grupu funkcije: hici (`fire`) i pogoci u vozila (`hit`) u tablicu;
- tablice izvoza mrežnih polja i mrežni GUID-ovi (njihov broj; putanje su u pratećoj datoteci entiteta).

**Sačuvano sirovo** (cijelo, uz ono što je pročitano):

- `<demo>.entities.parquet`, stupci `time`, `type` (`<class>.<property>`, `<class>.<call>` ili ime objekta), `name` (klasa aktera), `entity` (mrežni GUID aktera, kao `entity` u tablici), `kind`, `object` (podobjekt), `channel`, `handle`, `group` (putanja klase grupe izvoza), `decoded` (JSON), `bits` i `payload` (bitovi, najniži prvi, dopunjeni do cijelih bajtova):
  - svaka promjena svojstva (`kind` `property`), uključujući kretanje, s onim što je dekodirano; sirovo samo tamo gdje nema dekodiranja (nepoznate ručke, strukture kao `RotationReplicatedMovement` topova i svojstva ostavljena kao bitovi);
  - svaki udaljeni poziv i polje delta-a po mjeri (`rpc`), parametri dekodirani tamo gdje je grupa funkcije izvezena; sirovo tamo gdje nije (`RepInventory`, `PlayerStateData`);
  - svaki sadržajni blok objekta čija se klasa nije mogla pronaći (`block`: `Buoyancy`, `GameplayTasksComponent`, `AmmoRackComponent`...), sa zaglavljem dekodiranim;
  - svaki kanal aktera otvoren i zatvoren (`open`, `close`), svaki podobjekt obrisan ili uništen;
  - kontekst koji kasniji dekoder treba da bi sam pročitao datoteku: svako mrežno polje izvoza (`export.field`: putanja grupe, ručka, ime svojstva, kontrolni zbroj) i svaki izvezeni mrežni GUID (`export.guid`: njegova putanja, vanjski objekt i zastavice), u trenutku kad ih je tok dao.
- `<demo>.packets.parquet`, stupci `time`, `type`, `name`, `channel`, `offset` (u datoteci), `decoded`, `bits` i `payload`: informacijski blok, zaglavlje, svaki dio kontrolne točke (kontrolna točka je stanje svakog aktera u svom trenutku, koje tok od početka također sadrži), svaki dio događaja, i svaki okvir, paket ili snop koji se ne može pročitati (jedan snop po demou: početni snop spektatora snimatelja), cijelo.

Redci entiteta grupirani su po `kind`, `type` i `entity`, svaki po vremenu; za redoslijed toka sortirajte po `time`.

**Nije dostupno:**

- što server demo ne snima: ulazi klijenata, što je igrač vidio;
- učinci na strani klijenta: oznake pogodaka, zvukovi, tekst popisa ubojstava (server šalje pozive, ne njihov prikaz);
- dekodirani online ID-jevi: sačuvani samo kao bitovi (vidi [Osobni podaci](limits.md#personal-data)).
