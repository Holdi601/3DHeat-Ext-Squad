---
title: "Maintenir ces documents"
nav_order: 91
lang: "fr"
source: maintaining.md
source_hash: "b0b7836a5545"
nav_exclude: true
search_exclude: true
---
# Maintenir ces documents {#maintaining-these-docs}

Une liste de contrôle pour chaque version, pour que les pages ne soient jamais en retard sur le code.

1. **Régénérer la référence.** `python tools/gen_docs_reference.py` réécrit
   [Référence des commandes](../cli-reference.md) à partir du `--help` du programme et des colonnes de sortie.
   `python tools/gen_docs_reference.py --check` quitte avec 1 quand la page validée n'est plus à jour.
2. **Lister ce qui a changé.** `git log v<VERSION>..HEAD --oneline`, où
   `<VERSION>` est la dernière version publiée (le fichier `VERSION` à la publication). Donnez à chaque
   nouvelle fonction, option et colonne de sortie une place dans une page, et une ligne dans la section **Docs** de
   [`CHANGELOG.md`](https://github.com/Holdi601/3DHeat-Ext-Squad/blob/main/CHANGELOG.md).
3. **Relecture indépendante.** Une personne qui n'a pas écrit les pages relit le
   README et chaque page modifiée, images comprises, trois fois : en débutante qui n'a jamais
   utilisé de terminal, en enfant de huit ans, et en experte qui vérifie chaque option par rapport à `--help`. Les exemples
   n'utilisent que des noms et des chiffres inventés.
4. **Corriger** tout ce que la relecture trouve.
5. **Traductions.** Chaque page traduite enregistre l'empreinte de la page anglaise dont elle est issue.
   Retraduisez les pages dont la source anglaise a changé, puis relisez chaque langue : texte clair, libellés
   corrects des schémas, mêmes mots que l'interface traduite du visualiseur.
6. **Lancer les tests** (`pytest`).
7. **Publier** seulement après le feu vert du propriétaire.

## Traductions : les commandes {#translations-the-commands}

Le site est traduit dans les 40 langues du visualiseur 3DHeat : l'anglais dans `docs/`, chaque autre
langue dans `docs/<langue>/` avec les mêmes noms de fichiers. `tools/docs_i18n.py` tient les comptes :

```bash
python tools/docs_i18n.py hashes             # après tout changement anglais : enregistrer l'empreinte de chaque page
python tools/docs_i18n.py svg-strings        # après tout changement d'image : les libellés à traduire
python tools/docs_i18n.py status             # par langue : à jour, périmées, pages manquantes
python tools/docs_i18n.py todo --lang de     # les pages allemandes à (re)traduire
python tools/docs_i18n.py svg-build --lang de    # images allemandes à partir de docs/assets/i18n/svg/de.json
python tools/docs_i18n.py finish --lang de   # marquer les pages allemandes avec l'empreinte de leur source anglaise
python tools/docs_i18n.py check              # quitte avec 1 quand les empreintes ou les libellés sont périmés
```

Ne traduisez que ce que `todo` liste : gardez le Markdown, les liens, le code, les noms de fichiers et de colonnes tels quels ;
traduisez les titres et les descriptions d'images, et utilisez les mots propres à l'interface du visualiseur 3DHeat pour ses boutons
et panneaux (son `src/i18n/locales/<langue>/`). Les pages de référence générées et les images de terminal restent
en anglais. Sur le site, une traduction périmée l'indique et renvoie vers la page anglaise ; une traduction
manquante revient à l'anglais. Le menu de langue de l'en-tête et la redirection de la page d'accueil selon la langue du navigateur
viennent de `docs/_includes/`.
