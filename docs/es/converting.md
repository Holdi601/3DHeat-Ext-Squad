---
title: Convertir demos
nav_order: 3
lang: es
source: converting.md
source_hash: "e8c77423085b"
nav_exclude: true
search_exclude: true
---
# Convertir demos {#converting-demos}

```text
heat3d-squad-demo <demos or folders> -o <folder> [--flat] [--json]
python -m heat3d_ext_squad ...          lo mismo, sin instalar
```

## Paso a paso {#step-by-step}

¿Nuevo en la línea de comandos? Lee primero [Antes de empezar](before-you-start.md).

1. Instala una vez: `git clone https://github.com/Holdi601/3DHeat-Ext-Squad`,
   abre una terminal en esa carpeta y ejecuta `python -m pip install -e .`
   (Python 3.10 o posterior; trae pyarrow y numpy).
2. Pon los archivos `.replay` en una carpeta, o nómbralos uno a uno.
3. Ejecuta `heat3d-squad-demo <folder> -o out`.
4. Verás una línea por demo: su capa, jugadores y filas, y dónde se guardó la tabla.
   Cada demo se convierte en cuatro archivos sueltos en `out/<map>/` (no en un
   contenedor `.3dheat`); carga el `.parquet` en el visor 3DHeat.

![Una ejecución sobre una demo sintética](../assets/img/run.svg)

La imagen muestra una ejecución sobre una demo que construyen los tests (`tests/test_stream.py`),
no una partida real.

## Opciones {#options}

| Opción | Por defecto | Qué hace |
|---|---|---|
| `demos` (una o más) | - | archivos `.replay`, o carpetas que los contienen |
| `-o`, `--out` | obligatoria | la carpeta donde escribir; cada demo va a `<out>/<map>/` |
| `--flat` | desactivada | escribe directamente en la carpeta, sin la carpeta `<map>/` |
| `--json` | desactivada | imprime una línea de JSON por demo en la salida estándar (para programas que llaman al comando): `demo`, `ok`, `parquet`, `match`, `sidecars`, `lost`, `rows`, `players`, `layer`, `recorded_unix`; una demo que falló imprime `demo`, `ok: false` y `error` en su lugar |
| `--version` | - | muestra la versión y se detiene |

Cada opción, tal como la muestra el programa: [Referencia de comandos](../cli-reference.md).

La carpeta del mapa es el nombre del mapa tomado de la ruta del nivel que nombra la demo
(`/Game/Maps/<Map>/Gameplay_Layers/<Layer>` da `<Map>`).

Estado de salida: 0 cuando todas las demos se convirtieron; 1 cuando alguna falló (las demás
se escriben igualmente) o cuando no se encontró ningún archivo `.replay`.

## Qué sale {#what-comes-out}

| Archivo | Qué contiene |
|---|---|
| `<demo>.parquet` | la tabla: posiciones y eventos, una fila cada uno ([La tabla](output-table.md)) |
| `<demo>.match.json` | el documento de la partida ([El documento de la partida](output-match.md)) |
| `<demo>.entities.parquet` | auxiliar: cada actualización de propiedad y cada llamada remota, completas |
| `<demo>.packets.parquet` | auxiliar: los fragmentos del archivo y lo que no se pudo leer, completo |

La tabla y el documento de la partida son el mismo par que escribe la herramienta CS2 de 3DHeat.
El visor abre la tabla directamente y deja fuera los auxiliares cuando se carga una carpeta entera.

## Ejemplos {#examples}

```bash
heat3d-squad-demo D:\SquadDemos -o out                 # cada demo de una carpeta
heat3d-squad-demo one.replay two.replay -o out --flat  # directamente en out/
heat3d-squad-demo D:\SquadDemos -o out --json          # una línea JSON por demo
```

`D:\SquadDemos` es una carpeta de ejemplo en la unidad D: usa la tuya.
