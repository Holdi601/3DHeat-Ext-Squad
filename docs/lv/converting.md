---
title: Demo konvertēšana
nav_order: 3
lang: "lv"
source: converting.md
source_hash: "e8c77423085b"
nav_exclude: true
search_exclude: true
---
# Demo konvertēšana {#converting-demos}

```text
heat3d-squad-demo <demos or folders> -o <folder> [--flat] [--json]
python -m heat3d_ext_squad ...          tas pats, bez uzstādīšanas
```

## Soli pa solim {#step-by-step}

Nekad neesat strādājis ar komandrindu? Vispirms izlasiet [Pirms sākat](before-you-start.md).

1. Uzstādiet vienreiz: `git clone https://github.com/Holdi601/3DHeat-Ext-Squad`,
   atveriet termināli šajā mapē un palaidiet `python -m pip install -e .`
   (Python 3.10 vai jaunāks; tas atnes pyarrow un numpy).
2. Ievietojiet `.replay` failus mapē vai nosauciet tos vienu pēc otra.
3. Palaidiet `heat3d-squad-demo <folder> -o out`.
4. Redzēsiet pa vienai rindai katram demo: tā slāni, spēlētājus un rindas un to, kur
   tabula ir saglabāta. Katrs demo kļūst par četriem atsevišķiem failiem mapē `out/<map>/` (nevis
   `.3dheat` konteineris); ielādējiet `.parquet` 3DHeat skatītājā.

![Palaišana uz sintētiska demo](../assets/img/run.svg)

Attēlā redzama palaišana uz demo, ko testi izveido (`tests/test_stream.py`),
nevis uz īstas spēles.

## Iespējas {#options}

| Iespēja | Noklusējums | Ko dara |
|---|---|---|
| `demos` (viens vai vairāki) | - | `.replay` faili vai mapes, kurās tie atrodas |
| `-o`, `--out` | obligāta | mape, kurā rakstīt; katrs demo ieies mapē `<out>/<map>/` |
| `--flat` | izslēgts | raksta tieši mapē, bez mapes `<map>/` |
| `--json` | izslēgts | izdrukā vienu JSON rindu katram demo standarta izvadā (programmām, kas izsauc šo komandu): `demo`, `ok`, `parquet`, `match`, `sidecars`, `lost`, `rows`, `players`, `layer`, `recorded_unix`; demo, kas neizdevās, drukā `demo`, `ok: false` un `error` |
| `--version` | - | izdrukā versiju un apstājas |

Visas iespējas, kā tās izdrukā programma: [Komandu atsauce](../cli-reference.md).

Kartes mape ir kartes nosaukums, kas paņemts no līmeņa ceļa, ko demo nosauc
(`/Game/Maps/<Map>/Gameplay_Layers/<Layer>` dod `<Map>`).

Izejas statuss: 0, ja katrs demo ir konvertēts; 1, ja kāds neizdevās (pārējie
tomēr tiek saglabāti) vai ja nav atrasts neviens `.replay` fails.

## Kas tiek izveidots {#what-comes-out}

| Fails | Ko tajā ir |
|---|---|
| `<demo>.parquet` | tabula: pozīcijas un notikumi, pa vienai rindai katrs ([Tabula](output-table.md)) |
| `<demo>.match.json` | mača dokuments ([Mača dokuments](output-match.md)) |
| `<demo>.entities.parquet` | papildfails: katrs īpašību atjauninājums un attālais izsaukums, pilnībā |
| `<demo>.packets.parquet` | papildfails: faila fragmenti un viss, kas nebija nolasāms, pilnībā |

Tabula un mača dokuments ir tie paši faili, ko raksta 3DHeat CS2 rīks.
Skatītājs atver tabulu tieši un atstāj papildfailus neielādētus, kad ielādē veselu mapi.

## Piemēri {#examples}

```bash
heat3d-squad-demo D:\SquadDemos -o out                 # visi demo mapē
heat3d-squad-demo one.replay two.replay -o out --flat  # tieši mapē out/
heat3d-squad-demo D:\SquadDemos -o out --json          # viena JSON rinda katram demo
```

`D:\SquadDemos` ir piemēra mape diskā D: izmanto savu.
