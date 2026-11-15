---
title: "Rungtynių dokumentas ir papildomi failai"
nav_order: 5
lang: lt
source: output-match.md
source_hash: "715bd3417e47"
nav_exclude: true
search_exclude: true
---
# Rungtynių dokumentas ir papildomi failai {#the-match-document-and-sidecars}

Šalia lentelės kiekvienas demo gauna `<demo>.match.json` ir du papildomus failus,
`<demo>.entities.parquet` ir `<demo>.packets.parquet`. Žiūryklė rungtynių dokumentą skaito
savo Rungtynės skirtuke.

## Rungtynių dokumentas {#the-match-document}

`<demo>.match.json` (rungtynių dokumentas) savo viršutiniame lygyje turi `map`, `layer`, `level_path`, `game_version`, `engine_version`, `recorded_unix`, `duration_s`, `teams`, `squads`, `game_state`, `actors`, `players`, `rows`, `events`, `not_read`, `file`, `header`, `chunks`, `stream`, `shots` ir `selfCheck` (pilnas sąrašas: [Komandų nuoroda](../cli-reference.md)). Žodžiais: žemėlapis ir lygis, žaidimo ir variklio versijos, įrašymo laikas, trukmė ir:

- **komandos**: numeris, frakcija ir viskas, ką jų būsena replikavo (bilietai, galimybės, vadas), kaip tai keitėsi;
- **būriai**: numeris, komanda, pavadinimas, kūrėjas, vadovas, nariai;
- **žaidimo būsena**: serverio pavadinimas ir nustatymai, žaidimo režimas, rungtynių būsena ir ID, žemėlapių ir lygių rotacijos, balsavimai, laikmačiai, dienos pranešimas;
- **veikėjai**: kiekviena transporto priemonė, įrenginys, įtvirtinimas, šaudmenų dėžė ir sraigtasparnis – klasė, kur ir kada atsirado, kada dingo, kieno buvo, ir jo replikuota būsena (sveikata, statybos būsena, sėdynės...);
- **po eilutę kiekvienam žaidėjui**: matavimai pėsčiomis ir transporto priemonėse, nueitas atstumas, kareivių klasės, naudotos transporto priemonės, komandų pakeitimai, užimtos sėdynės ir viskas, ką replikavo žaidėjo būsena (ping, lygis, vaidmuo, dabartinė sėdynė...); ir po eilutę kiekvienam botui;
- **įvykiai** suskaičiuoti, **savybių surašymas** (kiek kartų buvo siunčiamos kiekvienos klasės savybės) ir **nuotolinių kvietimų surašymas**, šūviai ir pataikymai, kas **nebuvo** nuskaityta, ir skaitytuvo diagnostika;
- **failas ir antraštė**: kiekvienas informacijos bloko ir demo antraštės laukas, dalių lentelė, tinklo lauko eksporto lentelės (`net_field_exports`), kanalų uždarymo priežastys ir klasės, rastos objektams, kurių eksportai nevardija (`stream.class_resolution`);
- **savitikra** (`selfCheck.completeness`, žr. [Pilnumas](#completeness)).

Interneto ID (Steam, EOS) tyčia neįtraukiami.

Greitas pažvelgimas į konvertuotą demo:

```bash
python -c "import json; d = json.load(open('out/<map>/<demo>.match.json')); print(d['map'], d['layer'], d['duration_s'], len(d['players']))"
```

## Pilnumas {#completeness}

Šis skaitytuvas laikosi taisyklės, kurią visi 3DHeat konvertuotojai: iškart dekoduoti tai, ką galima perskaityti, o likusį išsaugoti visą ir pasakyti, kiek kiekvieno tipo jo perskaitė ([Konvertuotojai išsaugo viską](https://github.com/Holdi601/3DHeat/blob/main/docs/converters.md)). Kiekvienas rungtynių dokumentas turi `selfCheck.completeness`: kiekvienam demo sutiktų elementų tipui – kiek buvo `seen`, `decoded`, `partial` (iš dalies dekoduoti ir išsaugoti visi), `raw` (tik išsaugoti visi) ir `lost` (turi būti 0). Tipai skaičiuojami ten, kur skaitytuvas juos sutinka: `file.info`, `chunk.<kind>`, `frame`, `packet`, `bunch`, `open`, `close`, `export.field`, `export.guid`, `external`, `property:<class>`, `rpc:<class>`, `block:<object>`, `subobject.*`.

Perskaitytuose tikruose demo `lost` yra 0: jų elementų yra nuo šimtų tūkstančių iki milijonų; apie pusė dekoduojami visiškai, likusieji – iš dalies ar žali.

**Perskaityta** (į lentelę ir rungtynių dokumentą):

- informacijos blokas, demo antraštė (kiekvienas laukas; du nežinomi galiniai baitai išsaugomi šešioliktainiu kodu), dalių lentelė;
- kiekvienas kadras, paketas ir bunch'as (visi, suskaidyti į tai, ką jie neša), kiekvienas atidarytas veikėjas (su atsiradimo vieta, sukimu, mastelio ir greičio duomenimis) ir uždarytas (su priežastimi: `Destroyed`, `Dormancy`...);
- kiekviena replikuojama savybė, kiek tai nurodo jos bitai ([Savybių dekodavimas](how-it-works.md#decoding-properties)), pozicijos iš `FRepMovement` ir iš sraigtasparnių judėjimo komponento, žuvimai, transporto priemonių sveikata, sėdynės;
- kiekvienas nuotolinis kvietimas pagal pavadinimą, su parametrais, kai demo eksportuoja funkcijos grupę: šūviai (`fire`) ir transporto priemonių pataikymai (`hit`) – į lentelę;
- tinklo lauko eksporto lentelės ir tinklo GUID (jų skaičius; keliai – papildomame veikėjų faile).

**Išsaugota žalia** (visa, kartu su tuo, kas perskaityta, šalia):

- `<demo>.entities.parquet`, stulpeliai `time`, `type` (`<class>.<property>`, `<class>.<call>` arba objekto vardas), `name` (veikėjo klasė), `entity` (veikėjo tinklo GUID, kaip lentelės `entity`), `kind`, `object` (subobjektas), `channel`, `handle`, `group` (eksporto grupės klasės kelias), `decoded` (JSON), `bits` ir `payload` (bitai, nuo mažiausio, užpildyti iki pilnų baitų):
  - kiekvienas savybės atnaujinimas (`kind` `property`), įskaitant judėjimą, su tuo, kas dekoduota; žalias tik ten, kur nieko nedekoduota (nepavadinti rankenėlės, struktūros, pavyzdžiui, bokštelių `RotationReplicatedMovement`, ir savybės, paliktos kaip bitai);
  - kiekvienas nuotolinis kvietimas ir pasirinktinis delta laukas (`rpc`), parametrai dekoduoti, kai funkcijos grupė buvo eksportuota; žalias, kai ne (`RepInventory`, `PlayerStateData`);
  - kiekvienas turinio blokas objekto, kurio klasės nepavyko rasti (`block`: `Buoyancy`, `GameplayTasksComponent`, `AmmoRackComponent`...), su dekoduota antraște;
  - kiekvienas veikėjo kanalas, kuris atidarytas ir uždarytas (`open`, `close`), kiekvienas subobjektas, ištrintas ar sunaikintas;
  - kontekstas, kurio vėlesniam dekoderiui reikia, kad perskaitytų vieną failą: kiekvienas tinklo lauko eksportas (`export.field`: grupės kelias, rankenėlė, savybės pavadinimas, kontrolinė suma) ir kiekvienas eksportuotas tinklo GUID (`export.guid`: jo kelias, išorinis ir žymės), tuo metu, kai srautas juos pateikė.
- `<demo>.packets.parquet`, stulpeliai `time`, `type`, `name`, `channel`, `offset` (faile), `decoded`, `bits`, `payload`: informacijos blokas, antraštės dalis, kiekviena kontrolinio taško dalis (kontrolinis taškas – tai kiekvieno veikėjo būsena jo metu, kurią turi ir srautas nuo pradžios), kiekviena įvykių dalis ir kiekvienas kadras, paketas ar bunch'as, kurio neperskaityta (vienas bunch kiekviename demo: paties įrašytojo stebėtojo atidarymo bunch'as), visa.

Veikėjų eilutės sugrupuotos pagal `kind`, `type` ir `entity`, kiekviena laiko tvarka; rikiuokite pagal `time`, kad gautumėte srauto tvarką.

**Nepasiekiama:**

- ko serverio demo neįrašo: klientų įvestys, ką matė žaidėjas;
- kliento pusės efektai: pataikymo žymekliai, garsai, žudynių sąrašo tekstas (serveris siunčia kvietimus, o ne jų rodymą);
- dekoduojami interneto ID: išsaugomi tik bitais (žr. [Asmens duomenys](limits.md#personal-data)).
