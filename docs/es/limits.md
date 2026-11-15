---
title: Límites, actualizaciones y condiciones
nav_order: 7
lang: es
source: limits.md
source_hash: "ef3802087acc"
nav_exclude: true
search_exclude: true
---
# Límites, actualizaciones y condiciones {#limits-updates-and-terms}

## No se lee {#not-read}

- **Quién mató a quién, y el daño a los soldados por impacto.** Estos datos viajan en los resultados de impacto de las llamadas remotas de las armas y de los estados de los jugadores (`HitResultsZeroBased`, `MulticastOnImpact.Hit`), cuya estructura no se lee; se guardan completos en el auxiliar de entidades. Solo se decodifica la salud de las víctimas.
- **El equipo del bot.** El estado de un bot lleva un número que puede ser su equipo; no está confirmado, no se usa.
- **Hacia dónde mira un soldado de lado**, más allá del giro del cuerpo.

## Actualizaciones del juego {#game-updates}

El lector depende del formato de repetición del motor y de un puñado de nombres de clases y propiedades de Squad. No depende de disposiciones de propiedades que no puede ver: la repetición las nombra por sí misma.

**Qué puede romperse con una actualización de Squad:**

- **Una actualización del motor.** Squad pasó a UE 5.7 con la v10.4, y esto no está probado allí. La actualización puede cambiar la cabecera de bunch, los datos de aparición o `FRepMovement`. Están controlados por versión en el código donde se conoce el cambio. Los pasos desconocidos (`ENG_PARTIAL_CUSTOM_EXPORTS`, el bit final de movimiento) se fijan a lo que hace la v10.3.1.
- **Replicación Iris.** Si Squad pasara a Iris, el flujo dentro de los fragmentos sería nuevo y este lector no lo leería. Squad v10.3.1 usa el sistema clásico (funciona con ReplicationGraph).
- **Clases o propiedades renombradas.** Si Squad renombra sus clases de jugador, equipo o escuadra, o sus propiedades, faltarían nombres o equipos, pero no posiciones.
- **Qué pasa si falla.** Cuando cambia el formato, el lector falla de forma visible, con errores de flujo o de movimiento en los diagnósticos. No produce posiciones incorrectas en silencio: `FRepMovement` solo se acepta cuando sus bits cuadran exactamente.

## Datos personales {#personal-data}

Una demo contiene los nombres e identificadores en línea de todas las personas del servidor. La tabla y el documento de la partida llevan nombres, no identificadores. Los auxiliares guardan los bits de cada propiedad, así que contienen los identificadores tal como los contiene la demo (sin decodificar). Trátalos todos como a la propia demo.

## Licencia y fuentes {#licence-and-sources}

MIT; ver [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-Squad/blob/main/LICENSE). Todo esto se escribió para este paquete. No se incluye ni se enlaza código de terceros: las únicas dependencias son pyarrow (Apache-2.0) y numpy (BSD-3-Clause).

Los datos sobre el formato proceden de estas fuentes:

- **Unreal.Core** en [FortniteReplayDecompressor](https://github.com/Shiqan/FortniteReplayDecompressor) (MIT). Describe la disposición genérica de las repeticiones de Unreal: el bloque de información, los fragmentos, las tramas, los bunches y las tablas de exportación de campos de red.
- **[squad-replay](https://github.com/Codycody31/squad-replay)** (MPL-2.0). Se leyó su analizador para la disposición tal como la escribe Squad v10.3.1, para las comprobaciones de versión, y para saber qué clases de Squad llevan los datos de las plantillas. Sus demos de prueba publicadas y sus recuentos de instantáneas se usaron como comprobación cruzada independiente. No se copió ni tradujo nada de su código: este lector está estructurado de otra forma (un archivo de bits en Python sobre paquetes completos, bunches parciales unidos bit a bit, propiedades despachadas por nombre), y se encontraron en las propias demos dos cosas que ese proyecto no hace: el tercer indicador de bunch parcial y el bit final de movimiento.

Squad es una marca de Offworld Industries. Este paquete lee archivos que escribe un servidor de Squad; no toca el juego, su código ni sus archivos. La política de licencias y administración de servidores de Offworld no dice nada sobre grabar o analizar demos. El EULA de Squad prohíbe la ingeniería inversa del propio juego, que este paquete no hace.
