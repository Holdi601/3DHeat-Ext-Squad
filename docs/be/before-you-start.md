---
title: "Перад пачаткам"
nav_order: 1.5
lang: be
source: before-you-start.md
source_hash: "ca4b6281fdfc"
nav_exclude: true
search_exclude: true
---
# Перад пачаткам {#before-you-start}

Упершыню ў камандным радку? Гэтая старонка правядзе вас ад нуля да першага
запуску. Гэта займае каля дзесяці хвілін, і толькі адзін раз.

## 1. Усталюйце Python {#install-python}

Для гэтага інструмента патрэбны **Python 3.10 або навейшы**.

- **Windows:** спампуйце Python з [python.org/downloads](https://www.python.org/downloads/)
  і запусціце ўсталёўшчык. На першым экране адзначце **Add python.exe to PATH**,
  потым націсніце **Install Now**.
- **macOS і Linux:** Python 3 часта ўжо ёсць. Дзе на гэтых старонках напісана
  `python`, друкуйце `python3`.

## 2. Атрымайце гэты інструмент {#get-this-tool}

Адкрыйце [github.com/Holdi601/3DHeat-Ext-Squad](https://github.com/Holdi601/3DHeat-Ext-Squad), націсніце зялёную
кнопку **Code**, потым **Download ZIP** і распакуйце архіў у любую
папку. Калі вы карыстаецеся git: `git clone https://github.com/Holdi601/3DHeat-Ext-Squad`.

## 3. Адкрыйце тэрмінал у гэтай папцы {#open-a-terminal-in-that-folder}

Тэрмінал — гэта акно, у якім друкуюць каманды.

- **Windows:** адкрыйце папку ў Правадыру, пстрыкніце ў адрасным радку, увядзіце
  `powershell` і націсніце Enter. Адкрыецца сіняе або чорнае акно, ужо ў гэтай
  папцы.
- **macOS:** адкрыйце **Terminal**, увядзіце `cd ` (з прабелам), перацягніце папку ў
  акно і націсніце Enter.

`cd` значыць «змяніць папку»: `cd C:\Tools\3DHeat-Ext-Squad` пераходзіць у гэтую папку.

## 4. Усталюйце інструмент {#install-the-tool}

Увядзіце гэта і націсніце Enter:

```bash
python -m pip install -e .
```

У канцы вы ўбачыце: `Successfully installed heat3d-ext-squad-demo-...`.

## 5. Запусціце яго {#run-it}

```bash
heat3d-squad-demo --version
```

Вы ўбачыце нешта накшталт:

```text
heat3d-squad-demo 0.1.0
```

Далей: [Запіс дэма](recording.md), потым [Канвертаванне дэма](converting.md).

## Як чытаць каманды на гэтых старонках {#how-to-read-the-commands-on-these-pages}

| Вы бачыце | Што гэта значыць |
|---|---|
| `<folder>` | запаўняльнік: увядзіце сваё значэнне замест яго, без `< >` |
| `[--force]` | неабавязкова: прапусціце або ўвядзіце, як паказана |
| `a\|b` | выбар: увядзіце `a` або `b` |
| `# a note` | каментар для вас: не друкуйце яго |
| `"C:\My Files\x"` | шлях з прабеламі бярыце ў двукоссі |
| `D:\Demos` | прыклад папкі ў Windows: бярыце сваю |

## Калі нешта пайшло не так {#when-something-goes-wrong}

| Паведамленне | Што рабіць |
|---|---|
| `'python' is not recognized` | Python не ўсталяваны, або не адзначылі PATH: усталюйце яго зноў і адзначце (або друкуйце `py` замест `python`). |
| `'heat3d-squad-demo' is not recognized` | Паўтарыце крок 4 у папцы інструмента, або друкуйце `python -m heat3d_ext_squad` замест `heat3d-squad-demo`: гэта тое самае. |
| `No module named heat3d_ext_squad` | Вы не ў папцы інструмента, або крок 4 не ўдаўся: перайдзіце туды праз `cd` і выканайце крок 4. |
| `No module named pip` | Выканайце `python -m ensurepip`, потым крок 4. |
| што заўгодна іншае | Прачытайце апошні радок паведамлення, потым адкрыйце issue на GitHub з ім. |

Кожная каманда таксама заканчваецца **статусам выхаду**: 0 значыць, што ўсё атрымалася. Каб убачыць яго,
увядзіце `echo $LASTEXITCODE` у PowerShell або `echo $?` на macOS і Linux.
