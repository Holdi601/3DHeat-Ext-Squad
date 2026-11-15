---
title: La tabla
nav_order: 4
lang: es
source: output-table.md
source_hash: "0f3cfed1c108"
nav_exclude: true
search_exclude: true
---
# La tabla: `<demo>.parquet` {#the-table-parquet}

Una fila por muestra o evento. Se toma una muestra cada vez que el servidor replicó el movimiento
del actor, hasta 8 veces por segundo (la frecuencia de grabación de la demo) mientras se mueve.

![Las primeras filas de la tabla de una demo sintética](../assets/img/table.svg)

## Columnas {#columns}

| Columna | Qué es |
|---|---|
| `time` | segundos desde que empezó la grabación |
| `x`, `y`, `z` | posición en unidades de Unreal (centímetros), Z hacia arriba |
| `dirX`, `dirY`, `dirZ` | hacia dónde mira un soldado: el giro del cuerpo y el cabeceo de la vista, como vector unitario (en un vehículo: horizontal) |
| `yaw`, `pitch` | lo mismo en grados; `pitch` hacia arriba desde el horizonte, solo soldados |
| `health` | la salud del soldado, del bot o del vehículo en ese momento, cuando el servidor la envió (la de un soldado baja de 0 cuando está herido) |
| `speed` | la velocidad replicada, cm/s |
| `player` | el nombre del jugador; `bot <id>` para un bot; para un vehículo o elemento desplegable que nadie posee, su clase; para un disparo desde el arma de un vehículo, el jugador sentado en ese vehículo |
| `team`, `faction` | el número de equipo de Squad (1, 2) y su configuración de facción, **en ese momento**: los jugadores pueden cambiar de bando |
| `squad` | el número de escuadra, -1 cuando no está en una |
| `event` | qué es la fila (abajo) |
| `pawn` | el blueprint del soldado (`SQSquidBot` para un bot), el vehículo, o para `fire` el arma |
| `seat` | para un asiento de torreta o de pasajero, el propio pawn del asiento |
| `detail` | para `fire`, la llamada del arma que colocó el disparo; para `hit`, el tipo de daño; para `removed`, por qué se cerró el canal (`Destroyed`, `Dormancy`...) |
| `entity` | el actor al que se refiere la fila (su GUID de red): la `entity` de las filas de los auxiliares |
| `match` | el nombre de la demo |

## Eventos {#events}

| `event` | En la fila de | Qué es |
|---|---|---|
| `position` | un soldado o bot a pie | una muestra de movimiento |
| `vehicle` | un soldado en un vehículo terrestre o helicóptero | una muestra en la posición del vehículo |
| `wounded`, `revived`, `death` | soldados y bots | dónde ocurrió |
| `spawn`, `damaged`, `destroyed`, `removed` | vehículos, elementos desplegables, emplazamientos, cajas, helicópteros | dónde estaban |
| `seat` | un jugador | ocupó un asiento |
| `fire` | el tirador | un disparo: por dónde salió, su dirección como `yaw`/`pitch`/`dirX..Z` |
| `hit` | el vehículo | un impacto en el vehículo: dónde |

Cómo se leen los eventos está en [Cómo se lee una demo](how-it-works.md#how-the-events-are-read).

## En el visor {#in-the-viewer}

El pie del Parquet lleva instrucciones de lectura bajo la clave `heat3d`: Z hacia arriba,
ningún eje invertido, escala unitaria 1, así que el visor no necesita asignación de columnas. Carga
la tabla en la pestaña Mapa de calor; ver [Cómo cargar datos](https://holdi601.github.io/3DHeat/getting-data-in.html)
y [Asignación de columnas](https://holdi601.github.io/3DHeat/column-mapping.html) del visor.
