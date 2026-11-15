---
title: Mantenir aquesta documentació
nav_order: 91
lang: ca
source: maintaining.md
source_hash: "b0b7836a5545"
nav_exclude: true
search_exclude: true
---
# Mantenir aquesta documentació {#maintaining-these-docs}

Una llista de comprovació per a cada publicació, perquè les pàgines no es quedin mai
enrere respecte del codi.

1. **Regenerar la referència.** `python tools/gen_docs_reference.py` reescriu
   [Referència de l'ordre](../cli-reference.md) a partir del propi `--help` del programa
   i de les columnes de sortida. `python tools/gen_docs_reference.py --check` surt amb
   codi 1 quan la pàgina confirmada està obsoleta.
2. **Llistar què ha canviat.** `git log v<VERSION>..HEAD --oneline`, on
   `<VERSION>` és l'última versió publicada (el fitxer `VERSION` en el moment de la publicació).
   Doni a cada nova funcionalitat, opció i columna de sortida un lloc en una pàgina, i
   una fila a la secció **Docs** de [`CHANGELOG.md`](https://github.com/Holdi601/3DHeat-Ext-Squad/blob/main/CHANGELOG.md).
3. **Revisió independent.** Algú que no ha escrit les pàgines llegeix el README i cada
   pàgina modificada, les imatges incloses, tres vegades: com un principiant que mai
   no ha utilitzat una terminal, com un nen de 8 anys, i com un expert que comprova
   cada opció amb `--help`. Els exemples només utilitzen noms i números inventats.
4. **Corregir** tot el que trobi la revisió.
5. **Traduccions.** Cada pàgina traduïda registra el hash de la pàgina anglesa de la qual
   va sortir. Torni a traduir les pàgines el text anglès de les quals ha canviat,
   i després revisi cada idioma: text clar, etiquetes correctes als diagrames, les
   mateixes paraules que la interfície traduïda del visualitzador de 3DHeat.
6. **Executar les proves** (`pytest`).
7. **Publicar** només amb el vistiplau del propietari.

## Traduccions: les ordres {#translations-the-commands}

El lloc es tradueix als 40 idiomes del visualitzador de 3DHeat: l'anglès a `docs/`, cada altre
idioma a `docs/<lang>/` amb els mateixos noms de fitxer. `tools/docs_i18n.py` fa la
comptabilitat:

```bash
python tools/docs_i18n.py hashes             # després de qualsevol canvi en anglès: registra el hash de cada pàgina
python tools/docs_i18n.py svg-strings        # després de qualsevol canvi en una imatge: les etiquetes per traduir
python tools/docs_i18n.py status             # per idioma: al dia, obsoletes, pàgines que falten
python tools/docs_i18n.py todo --lang de     # les pàgines en alemany per (re)traduir
python tools/docs_i18n.py svg-build --lang de    # les imatges en alemany a partir de docs/assets/i18n/svg/de.json
python tools/docs_i18n.py finish --lang de   # marca les pàgines en alemany amb el hash de l'anglès
python tools/docs_i18n.py check              # surt amb codi 1 quan els hashes o les etiquetes estan obsolets
```

Tradueixi només el que llisti `todo`: mantingui el Markdown, els enllaços, el codi, els noms de fitxer
i de columna tal com estan, tradueixi els títols i les descripcions de les imatges, i utilitzi
les paraules pròpies del visualitzador de 3DHeat per als seus botons i panells (el seu
`src/i18n/locales/<lang>/`). Les pàgines de referència generades i les imatges de terminal
es mantenen en anglès. Al lloc, una traducció obsoleta ho indica i enllaça la pàgina
anglesa; una que falta torna a l'anglès. El menú d'idioma de la capçalera i la
redirecció de la pàgina d'inici segons l'idioma del navegador venen de `docs/_includes/`.
