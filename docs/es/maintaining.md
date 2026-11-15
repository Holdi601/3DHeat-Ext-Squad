---
title: Mantenimiento de estas páginas
nav_order: 91
lang: es
source: maintaining.md
source_hash: "b0b7836a5545"
nav_exclude: true
search_exclude: true
---
# Mantenimiento de estas páginas {#maintaining-these-docs}

Una lista de comprobación para cada versión, para que las páginas nunca se queden atrás del código.

1. **Regenerar la referencia.** `python tools/gen_docs_reference.py` reescribe
   [Referencia de comandos](../cli-reference.md) a partir del propio `--help` del programa y de sus
   columnas de salida. `python tools/gen_docs_reference.py --check` termina con código 1 cuando la
   página confirmada está desactualizada.
2. **Listar lo que cambió.** `git log v<VERSION>..HEAD --oneline`, donde `<VERSION>` es la última
   versión publicada (el archivo `VERSION` en la publicación). Dale a cada función nueva, opción y
   columna de salida un lugar en una página, y una fila en la sección **Docs** de
   [`CHANGELOG.md`](https://github.com/Holdi601/3DHeat-Ext-Squad/blob/main/CHANGELOG.md).
3. **Revisión independiente.** Alguien que no escribió las páginas lee el README y cada página
   cambiada, con las imágenes incluidas, tres veces: como principiante que nunca ha usado una
   terminal, como un niño de 8 años y como experto que comprueba cada opción con `--help`. Los
   ejemplos usan solo nombres y números inventados.
4. **Corregir** todo lo que encuentre la revisión.
5. **Traducciones.** Cada página traducida registra el hash de la página en inglés de la que se
   hizo. Vuelve a traducir las páginas cuyo original en inglés cambió, y después revisa cada idioma:
   texto claro, etiquetas de los diagramas correctas, las mismas palabras que la interfaz traducida
   del visor 3DHeat.
6. **Ejecutar las pruebas** (`pytest`).
7. **Publicar** solo con el visto bueno del propietario.

## Traducciones: los comandos {#translations-the-commands}

El sitio está traducido a los 40 idiomas del visor 3DHeat: el inglés en `docs/`, cada otro idioma en
`docs/<lang>/` con los mismos nombres de archivo. `tools/docs_i18n.py` lleva la contabilidad:

```bash
python tools/docs_i18n.py hashes             # tras cualquier cambio en inglés: registrar el hash de cada página
python tools/docs_i18n.py svg-strings        # tras cualquier cambio en una imagen: las etiquetas a traducir
python tools/docs_i18n.py status             # por idioma: al día, desactualizadas, páginas que faltan
python tools/docs_i18n.py todo --lang de     # las páginas en alemán a (re)traducir
python tools/docs_i18n.py svg-build --lang de    # imágenes en alemán desde docs/assets/i18n/svg/de.json
python tools/docs_i18n.py finish --lang de   # sellar las páginas en alemán con su hash en inglés
python tools/docs_i18n.py check              # termina con código 1 cuando los hashes o etiquetas están desactualizados
```

Traduce solo lo que lista `todo`: mantén el Markdown, los enlaces, el código y los nombres de archivos
y columnas tal como están, traduce los títulos y las descripciones de las imágenes, y usa las palabras
propias del visor 3DHeat para sus botones y paneles (su `src/i18n/locales/<lang>/`). Las páginas de
referencia generadas y las imágenes de terminal se quedan en inglés. En el sitio, una traducción
desactualizada lo indica y enlaza la página en inglés; una que falta recurre al inglés. El menú de
idiomas del encabezado y la redirección de la página de inicio según el idioma del navegador vienen de
`docs/_includes/`.
