---
title: "Demo konvertavimas"
nav_order: 3
lang: lt
source: converting.md
source_hash: "e8c77423085b"
nav_exclude: true
search_exclude: true
---
# Demo konvertavimas {#converting-demos}

```text
heat3d-squad-demo <demos or folders> -o <folder> [--flat] [--json]
python -m heat3d_ext_squad ...          the same, without installing
```

## Žingsnis po žingsnio {#step-by-step}

Nesate įpratę prie komandinės eilutės? Pirmiausia perskaitykite [Prieš pradedant](before-you-start.md).

1. Įdiekite vieną kartą: `git clone https://github.com/Holdi601/3DHeat-Ext-Squad`,
   atidarykite terminalą tame aplanke, vykdykite `python -m pip install -e .`
   (Python 3.10 ar naujesnė; kartu įdiegiama pyarrow ir numpy).
2. Įdėkite `.replay` failus į aplanką arba nurodykite juos po vieno.
3. Vykdykite `heat3d-squad-demo <folder> -o out`.
4. Turėtumėte matyti po vieną eilutę kiekvienam demo: jo sluoksnį, žaidėjus ir eilutes bei kur
   įrašyta lentelė. Kiekvienas demo tampa keturiais atskirais failais `out/<map>/` aplanke (ne
   `.3dheat` konteineriu); įkelkite `.parquet` 3DHeat žiūryklėje.

![Paleidimas su sintetiniu demo](../assets/img/run.svg)

Paveikslėlyje parodytas paleidimas su demo, kurį sukuria testai (`tests/test_stream.py`),
o ne tikros rungtynės.

## Parinktys {#options}

| Parinktis | Numatyta | Ką daro |
|---|---|---|
| `demos` (viena ar daugiau) | - | `.replay` failai arba juos turintys aplankai |
| `-o`, `--out` | privaloma | aplankas, į kurį rašyti; kiekvienas demo įrašomas į `<out>/<map>/` |
| `--flat` | išjungta | rašyti tiesiai į aplanką, be `<map>/` aplanko |
| `--json` | išjungta | spausdinti po vieną JSON eilutę kiekvienam demo į standartinį išvestį (programoms, kurios kviečia šią komandą): `demo`, `ok`, `parquet`, `match`, `sidecars`, `lost`, `rows`, `players`, `layer`, `recorded_unix`; demo, kuris nepavyko, spausdina `demo`, `ok: false` ir `error` |
| `--version` | - | parodyti versiją ir sustoti |

Kiekviena parinktis, kaip ją rodo programa: [Komandų nuoroda](../cli-reference.md).

Žemėlapio aplankas – tai žemėlapio pavadinimas, paimtas iš lygio kelio, kurį nurodo demo
(`/Game/Maps/<Map>/Gameplay_Layers/<Layer>` duoda `<Map>`).

Išeities kodas: 0, kai kiekvienas demo konvertuotas; 1, kai nepavyko bent vienas (kiti vis tiek
įrašomi) arba kai nerasta nė vieno `.replay` failo.

## Kas išeina {#what-comes-out}

| Failas | Ką jame yra |
|---|---|
| `<demo>.parquet` | lentelė: pozicijos ir įvykiai, po vieną eilutę ([Lentelė](output-table.md)) |
| `<demo>.match.json` | rungtynių dokumentas ([Rungtynių dokumentas](output-match.md)) |
| `<demo>.entities.parquet` | papildomas failas: kiekvienas savybių atnaujinimas ir nuotolinis kvietimas, visi |
| `<demo>.packets.parquet` | papildomas failas: failo dalys ir viskas, ko nepavyko nuskaityti, visa |

Lentelė ir rungtynių dokumentas yra ta pati pora, kurią rašo 3DHeat CS2 įrankis.
Žiūryklė atidaro lentelę tiesiogiai, o kai įkeliamas visas aplankas, papildomų failų neįtraukia.

## Pavyzdžiai {#examples}

```bash
heat3d-squad-demo D:\SquadDemos -o out                 # visi demo aplanke
heat3d-squad-demo one.replay two.replay -o out --flat  # tiesiai į out/
heat3d-squad-demo D:\SquadDemos -o out --json          # po vieną JSON eilutę kiekvienam demo
```

`D:\SquadDemos` – pavyzdinis aplankas diske D: naudokite savo.
