---
title: Konverter demoer
nav_order: 3
lang: da
source: converting.md
source_hash: "e8c77423085b"
nav_exclude: true
search_exclude: true
---
# Konverter demoer {#converting-demos}

```text
heat3d-squad-demo <demos or folders> -o <folder> [--flat] [--json]
python -m heat3d_ext_squad ...          det samme, uden at installere
```

## Trin for trin {#step-by-step}

Ny til kommandolinjen? Læs [Før du går i gang](before-you-start.md) først.

1. Installer én gang: `git clone https://github.com/Holdi601/3DHeat-Ext-Squad`,
   åbn en terminal i den mappe, kør `python -m pip install -e .`
   (Python 3.10 eller nyere; det henter pyarrow og numpy med sig).
2. Læg `.replay`-filerne i en mappe, eller angiv dem én for én.
3. Kør `heat3d-squad-demo <folder> -o out`.
4. Du bør se én linje pr. demo: dens lag, spillere og rækker, og hvor
   tabellen blev gemt. Hver demo bliver til fire løse filer i `out/<map>/` (ikke
   en `.3dheat`-container); indlæs `.parquet`-filen i 3DHeat-vieweren.

![En kørsel på en syntetisk demo](../assets/img/run.svg)

Billedet viser en kørsel på en demo, som testene bygger (`tests/test_stream.py`),
ikke på en rigtig kamp.

## Valgmuligheder {#options}

| Valgmulighed | Standard | Gør |
|---|---|---|
| `demos` (en eller flere) | - | `.replay`-filer, eller mapper, der indeholder dem |
| `-o`, `--out` | påkrævet | mappen der skrives til; hver demo havner i `<out>/<map>/` |
| `--flat` | fra | skriv direkte i mappen, uden mappen `<map>/` |
| `--json` | fra | udskriv én JSON-linje pr. demo på stdout (til programmer, der kalder kommandoen): `demo`, `ok`, `parquet`, `match`, `sidecars`, `lost`, `rows`, `players`, `layer`, `recorded_unix`; en demo der fejlede udskriver `demo`, `ok: false` og `error` i stedet |
| `--version` | - | udskriv versionen og stop |

Hver valgmulighed, som programmet udskriver den: [Kommandoreference](../cli-reference.md).

Kortmappen er kortets navn, taget fra banestien, som demoen angiver
(`/Game/Maps/<Map>/Gameplay_Layers/<Layer>` giver `<Map>`).

Exit-status: 0, når hver demo blev konverteret; 1, når en af dem fejlede (de andre
bliver stadig skrevet), eller når der ikke blev fundet nogen `.replay`-fil.

## Hvad der kommer ud {#what-comes-out}

| Fil | Hvad den indeholder |
|---|---|
| `<demo>.parquet` | tabellen: positioner og hændelser, én række hver ([Tabellen](output-table.md)) |
| `<demo>.match.json` | kampdokumentet ([Kampdokumentet](output-match.md)) |
| `<demo>.entities.parquet` | sidecar: hver egenskabsopdatering og hvert fjernkald, helt |
| `<demo>.packets.parquet` | sidecar: filens bidder og alt, der ikke blev læst, helt |

Tabellen og kampdokumentet er det samme par, som 3DHeat CS2-værktøjet skriver.
Vieweren åbner tabellen direkte og springer sidecarene over, når en hel
mappe indlæses.

## Eksempler {#examples}

```bash
heat3d-squad-demo D:\SquadDemos -o out                 # every demo in a folder
heat3d-squad-demo one.replay two.replay -o out --flat  # straight into out/
heat3d-squad-demo D:\SquadDemos -o out --json          # one JSON line per demo
```

`D:\SquadDemos` er en eksempelmappe på drev D: brug din egen.
