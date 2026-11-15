---
title: Antes de empezar
nav_order: 1.5
lang: es
source: before-you-start.md
source_hash: "ca4b6281fdfc"
nav_exclude: true
search_exclude: true
---
# Antes de empezar {#before-you-start}

¿Nuevo en la línea de comandos? Esta página te lleva de cero a una primera ejecución.
Tarda unos diez minutos, una sola vez.

## 1. Instalar Python {#install-python}

Esta herramienta necesita **Python 3.10 o posterior**.

- **Windows:** descarga Python desde [python.org/downloads](https://www.python.org/downloads/)
  y ejecuta el instalador. En su primera pantalla marca **Add python.exe to PATH**
  y haz clic en **Install Now**.
- **macOS y Linux:** Python 3 suele estar ya instalado. Donde estas páginas dicen
  `python`, escribe `python3`.

## 2. Conseguir esta herramienta {#get-this-tool}

Abre [github.com/Holdi601/3DHeat-Ext-Squad](https://github.com/Holdi601/3DHeat-Ext-Squad), haz clic en
el botón verde **Code** y después en **Download ZIP**, y descomprímelo en una carpeta
de tu elección. Si usas git: `git clone https://github.com/Holdi601/3DHeat-Ext-Squad`.

## 3. Abrir una terminal en esa carpeta {#open-a-terminal-in-that-folder}

Una terminal es una ventana donde escribes comandos.

- **Windows:** abre la carpeta en el Explorador, haz clic en la barra de direcciones,
  escribe `powershell` y pulsa Intro. Se abre una ventana azul o negra, ya dentro de
  esa carpeta.
- **macOS:** abre **Terminal**, escribe `cd ` (con un espacio), arrastra la carpeta a
  la ventana y pulsa Intro.

`cd` significa "cambiar de carpeta": `cd C:\Tools\3DHeat-Ext-Squad` va a esa carpeta.

## 4. Instalar la herramienta {#install-the-tool}

Escribe esto y pulsa Intro:

```bash
python -m pip install -e .
```

Al final deberías ver: `Successfully installed heat3d-ext-squad-demo-...`.

## 5. Ejecutarla {#run-it}

```bash
heat3d-squad-demo --version
```

Deberías ver algo como:

```text
heat3d-squad-demo 0.1.0
```

Siguiente: [Grabar una demo](recording.md), y después [Convertir demos](converting.md).

## Cómo leer los comandos de estas páginas {#how-to-read-the-commands-on-these-pages}

| Lo que ves | Significa |
|---|---|
| `<folder>` | un marcador: escribe tu propio valor, sin los `< >` |
| `[--force]` | opcional: déjalo fuera, o escríbelo como se muestra |
| `a\|b` | una elección: escribe `a` o `b` |
| `# a note` | un comentario para ti: no lo escribas |
| `"C:\My Files\x"` | pon entre comillas una ruta que tenga espacios |
| `D:\Demos` | un ejemplo de carpeta de Windows: usa la tuya |

## Cuando algo sale mal {#when-something-goes-wrong}

| El mensaje | Qué hacer |
|---|---|
| `'python' is not recognized` | Python no está instalado, o no se marcó la casilla PATH: instálalo de nuevo y márcala (o escribe `py` en lugar de `python`). |
| `'heat3d-squad-demo' is not recognized` | Repite el paso 4 en la carpeta de la herramienta, o escribe `python -m heat3d_ext_squad` en lugar de `heat3d-squad-demo`: hace lo mismo. |
| `No module named heat3d_ext_squad` | No estás en la carpeta de la herramienta, o el paso 4 falló: entra con `cd` y repite el paso 4. |
| `No module named pip` | Ejecuta `python -m ensurepip` y después el paso 4. |
| cualquier otra cosa | Lee la última línea del mensaje y abre un issue en GitHub con ella. |

Cada comando termina también con un **código de salida**: 0 significa que funcionó. Para verlo,
escribe `echo $LASTEXITCODE` en PowerShell o `echo $?` en macOS y Linux.
