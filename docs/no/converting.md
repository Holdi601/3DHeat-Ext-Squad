---
title: Konverter demoer
nav_order: 3
lang: no
source: converting.md
source_hash: "e8c77423085b"
nav_exclude: true
search_exclude: true
---
# Konverter demoer {#converting-demos}

```text
heat3d-squad-demo <demos or folders> -o <folder> [--flat] [--json]
python -m heat3d_ext_squad ...          the same, without installing
```

## Steg for steg {#step-by-step}

Ny til kommandolinjen? Les [Før du begynner](before-you-start.md) først.

1. Installer én gang: `git clone https://github.com/Holdi601/3DHeat-Ext-Squad`,
   åpne en terminal i den mappen, kjør `python -m pip install -e .`
   (Python 3.10 eller nyere; det henter pyarrow og numpy).
2. Legg `.replay`-filene i en mappe, eller nevn dem én for én.
3. Kjør `heat3d-squad-demo <folder> -o out`.
4. Du bør se én linje per demo: laget, spillerne og radene, og hvor
   tabellen ble skrevet. Hver demo blir til fire løse filer i `out/<map>/` (ikke en
   `.3dheat`-beholder); last inn `.parquet` i 3DHeat-visningsprogrammet.

![En kjøring på en syntetisk demo](../assets/img/run.svg)

Bildet viser en kjøring på en demo som testene lager (`tests/test_stream.py`),
ikke en ekte kamp.

## Alternativer {#options}

| Alternativ | Standard | Gjør |
|---|---|---|
| `demos` (en eller flere) | - | `.replay`-filer, eller mapper som holder dem |
| `-o`, `--out` | påkrevd | mappen å skrive til; hver demo havner i `<out>/<map>/` |
| `--flat` | av | skriv rett inn i mappen, uten `<map>/`-mappen |
| `--json` | av | skriv én JSON-linje per demo til stdout (for programmer som kaller kommandoen): `demo`, `ok`, `parquet`, `match`, `sidecars`, `lost`, `rows`, `players`, `layer`, `recorded_unix`; en demo som mislyktes skriver `demo`, `ok: false` og `error` i stedet |
| `--version` | - | skriv ut versjonen og stopp |

Alle alternativene, slik programmet skriver dem ut: [Kommandoreferanse](../cli-reference.md).

Kartmappen er kartets navn, hentet fra nivåstien demoen oppgir
(`/Game/Maps/<Map>/Gameplay_Layers/<Layer>` gir `<Map>`).

Avslutningsstatus: 0 når alle demoene ble konvertert; 1 når noen mislyktes (de andre
skrives likevel) eller når ingen `.replay`-fil ble funnet.

## Hva som kommer ut {#what-comes-out}

| Fil | Hva den inneholder |
|---|---|
| `<demo>.parquet` | tabellen: posisjoner og hendelser, én rad hver ([Tabellen](output-table.md)) |
| `<demo>.match.json` | kampdokumentet ([Kampdokumentet](output-match.md)) |
| `<demo>.entities.parquet` | sidefil: hver egenskapsoppdatering og hvert fjernkall, helt |
| `<demo>.packets.parquet` | sidefil: filens biter og alt som ikke ble lest, helt |

Tabellen og kampdokumentet er samme par som 3DHeat CS2-verktøyet skriver.
Visningsprogrammet åpner tabellen direkte og hopper over sidefilene når en
hel mappe lastes inn.

## Eksempler {#examples}

```bash
heat3d-squad-demo D:\SquadDemos -o out                 # every demo in a folder
heat3d-squad-demo one.replay two.replay -o out --flat  # straight into out/
heat3d-squad-demo D:\SquadDemos -o out --json          # one JSON line per demo
```

`D:\SquadDemos` er en eksempelmappe på stasjon D: bruk din egen.
