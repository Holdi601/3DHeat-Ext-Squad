---
title: "Падтрымка гэтай дакументацыі"
nav_order: 91
lang: be
source: maintaining.md
source_hash: "b0b7836a5545"
nav_exclude: true
search_exclude: true
---
# Падтрымка гэтай дакументацыі {#maintaining-these-docs}

Спіс для кожнага выпуску, каб старонкі ніколі не адсталі ад кода.

1. **Стварыце даведнік нанова.** `python tools/gen_docs_reference.py` перапісвае
   [Даведнік каманд](../cli-reference.md) з уласнага `--help` праграмы і
   слупкоў вываду. `python tools/gen_docs_reference.py --check` завяршаецца з кодам 1, калі
   захаваная старонка састарэла.
2. **Пералічыце, што змянілася.** `git log v<VERSION>..HEAD --oneline`, дзе
   `<VERSION>` — апошняя выпушчаная версія (файл `VERSION` на момант выпуску).
   Дайце кожнай новай магчымасці, опцыі і слупку вываду месца на старонцы і
   радок у раздзеле **Docs** файла [`CHANGELOG.md`](https://github.com/Holdi601/3DHeat-Ext-Squad/blob/main/CHANGELOG.md).
3. **Незалежная праверка.** Той, хто не пісаў старонкі, чытае
   README і кожную змененую старонку, разам з малюнкамі, тройчы: як
   пачатковец, які ніколі не карыстаўся тэрміналам, як 8-гадовае дзіця і як эксперт,
   які правярае кожную опцыю па `--help`. У прыкладах толькі выдуманыя імёны
   і лічбы.
4. **Выпраўце** усё, што знайшла праверка.
5. **Пераклады.** Кожная перакладзеная старонка запісвае хэш англійскай старонкі,
   з якой яна зроблена. Перакладзіце нанова старонкі, чый англійскі зыходнік змяніўся,
   потым праверце кожную мову: зразумелы тэкст, правільныя подпісы на схемах, тыя самыя
   словы, што ў перакладзеным інтэрфейсе праглядальніка.
6. **Запусціце тэсты** (`pytest`).
7. **Адпраўляйце (push)** толькі пасля дазволу ўладальніка.

## Пераклады: каманды {#translations-the-commands}

Сайт перакладзены на 40 моў праглядальніка 3DHeat: англійская ў `docs/`, кожная іншая
мова ў `docs/<lang>/` з тымі ж назвамі файлаў. `tools/docs_i18n.py` вядзе ўлік:

```bash
python tools/docs_i18n.py hashes             # after any English change: record each page's hash
python tools/docs_i18n.py svg-strings        # after any picture change: the labels to translate
python tools/docs_i18n.py status             # per language: current, outdated, missing pages
python tools/docs_i18n.py todo --lang de     # the German pages to (re)translate
python tools/docs_i18n.py svg-build --lang de    # German pictures from docs/assets/i18n/svg/de.json
python tools/docs_i18n.py finish --lang de   # stamp the German pages with their English hash
python tools/docs_i18n.py check              # exit 1 when hashes or labels are stale
```

Перакладайце толькі тое, што паказвае `todo`: Markdown, спасылкі, код, назвы файлаў і слупкоў
пакідайце як ёсць, перакладайце загалоўкі і апісанні малюнкаў, а для кнопак
і панэляў выкарыстоўвайце ўласныя словы праглядальніка 3DHeat (яго `src/i18n/locales/<lang>/`). Створаныя даведачныя старонкі і малюнкі тэрмінала застаюцца
англійскімі. На сайце састарэлы пераклад кажа пра гэта і дае спасылку на англійскую старонку; адсутны
пераходзіць на англійскую. Моўнае меню ў загалоўку і перанакіраванне на галоўнай старонцы
па мове браўзера бяруцца з `docs/_includes/`.
