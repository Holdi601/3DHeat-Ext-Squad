---
title: Одржување на оваа документација
nav_order: 91
lang: mk
source: maintaining.md
source_hash: "b0b7836a5545"
nav_exclude: true
search_exclude: true
---
# Одржување на оваа документација {#maintaining-these-docs}

Список за проверка за секое издание, за страниците никогаш да не заостанат зад кодот.

1. **Повторно генерирајте го упатството.** `python tools/gen_docs_reference.py` го препишува
   [Упатство за команди](../cli-reference.md) од сопствениот `--help` на програмата и
   од излезните колони. `python tools/gen_docs_reference.py --check` излегува со 1 кога
   зачуваната страница е застарена.
2. **Наведете што се променило.** `git log v<VERSION>..HEAD --oneline`, каде
   `<VERSION>` е последната објавена верзија (датотеката `VERSION` при издавањето).
   Дајте на секоја нова функција, опција и излезна колона место на некоја страница, и
   ред во делот **Docs** од [`CHANGELOG.md`](https://github.com/Holdi601/3DHeat-Ext-Squad/blob/main/CHANGELOG.md).
3. **Независен преглед.** Некој што не ги пишувал страниците ги чита
   README и секоја променета страница, вклучително и сликите, три пати: како
   почетник што никогаш не користел терминал, како 8-годишно дете и како експерт
   што секоја опција ја проверува според `--help`. Примерите користат само измислени имиња и
   броеви.
4. **Поправете** сè што ќе најде прегледот.
5. **Преводи.** Секоја преведена страница ја запишува хеш-вредноста на англиската страница
   од која е направена. Преведете повторно ги страниците чиј англиски извор се променил,
   потоа прегледајте го секој јазик: јасен текст, точни ознаки на дијаграмите, истите
   зборови како во преведениот интерфејс на прегледувачот.
6. **Пуштете ги тестовите** (`pytest`).
7. **Објавете** дури по одобрение од сопственикот.

## Преводи: командите {#translations-the-commands}

Страницата е преведена на 40-те јазика на прегледувачот 3DHeat: англиски во `docs/`, секој друг
јазик во `docs/<lang>/` со исти имиња на датотеки. `tools/docs_i18n.py` ја води евиденцијата:

```bash
python tools/docs_i18n.py hashes             # after any English change: record each page's hash
python tools/docs_i18n.py svg-strings        # after any picture change: the labels to translate
python tools/docs_i18n.py status             # per language: current, outdated, missing pages
python tools/docs_i18n.py todo --lang de     # the German pages to (re)translate
python tools/docs_i18n.py svg-build --lang de    # German pictures from docs/assets/i18n/svg/de.json
python tools/docs_i18n.py finish --lang de   # stamp the German pages with their English hash
python tools/docs_i18n.py check              # exit 1 when hashes or labels are stale
```

Преведувајте само што наведува `todo`: Markdown, врските, кодот, имињата на датотеки и колони
оставете ги како што се, преведете наслови и описи на слики, и користете ги
сопствените зборови на прегледувачот 3DHeat за неговите копчиња и панели (неговиот `src/i18n/locales/<lang>/`). Генерираните страници за упатства и сликите од терминал остануваат на
англиски. На страницата, застарен превод тоа го кажува и ја поврзува англиската страница; недостасувачки
се враќа на англиски. Јазичното мени во заглавието и пренасочувањето на почетната страница
според јазикот на прелистувачот доаѓаат од `docs/_includes/`.
