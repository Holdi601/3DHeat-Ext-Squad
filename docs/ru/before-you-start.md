---
title: С чего начать
nav_order: 1.5
lang: ru
source: before-you-start.md
source_hash: "ca4b6281fdfc"
nav_exclude: true
search_exclude: true
---
# С чего начать {#before-you-start}

Впервые в командной строке? Эта страница проведёт вас от нуля до первого запуска.
Это займёт около десяти минут, один раз.

## 1. Установите Python {#install-python}

Этому инструменту нужен **Python 3.10 или новее**.

- **Windows:** скачайте Python на [python.org/downloads](https://www.python.org/downloads/)
  и запустите установщик. На его первом экране отметьте **Add python.exe to PATH**,
  затем нажмите **Install Now**.
- **macOS и Linux:** Python 3 обычно уже есть. Там, где на этих страницах написано
  `python`, введите `python3`.

## 2. Получите этот инструмент {#get-this-tool}

Откройте [github.com/Holdi601/3DHeat-Ext-Squad](https://github.com/Holdi601/3DHeat-Ext-Squad),
нажмите зелёную кнопку **Code**, затем **Download ZIP**, и распакуйте архив в папку по
вашему выбору. Если вы пользуетесь git: `git clone https://github.com/Holdi601/3DHeat-Ext-Squad`.

## 3. Откройте терминал в этой папке {#open-a-terminal-in-that-folder}

Терминал — это окно, в котором вы вводите команды.

- **Windows:** откройте папку в Проводнике, щёлкните в адресной строке, введите
  `powershell` и нажмите Enter. Откроется синее или чёрное окно, уже в этой папке.
- **macOS:** откройте **Terminal**, введите `cd ` (с пробелом), перетащите папку в окно
  и нажмите Enter.

`cd` означает «сменить папку»: `cd C:\Tools\3DHeat-Ext-Squad` переходит в эту папку.

## 4. Установите инструмент {#install-the-tool}

Введите это и нажмите Enter:

```bash
python -m pip install -e .
```

В конце вы должны увидеть: `Successfully installed heat3d-ext-squad-demo-...`.

## 5. Запустите его {#run-it}

```bash
heat3d-squad-demo --version
```

Вы должны увидеть что-то вроде:

```text
heat3d-squad-demo 0.1.0
```

Дальше: [Запись демо](recording.md), затем [Преобразование демо](converting.md).

## Как читать команды на этих страницах {#how-to-read-the-commands-on-these-pages}

| Вы видите | Это значит |
|---|---|
| `<folder>` | заполнитель: вместо него введите своё значение, без угловых скобок `< >` |
| `[--force]` | необязательно: можно не вводить, или ввести как показано |
| `a\|b` | выбор: введите `a` или `b` |
| `# a note` | комментарий для вас: его не вводите |
| `"C:\My Files\x"` | путь с пробелами берите в кавычки |
| `D:\Demos` | пример папки Windows: используйте свою |

## Если что-то пошло не так {#when-something-goes-wrong}

| Сообщение | Что делать |
|---|---|
| `'python' is not recognized` | Python не установлен или не была отмечена галочка PATH: установите его снова и отметьте её (или введите `py` вместо `python`). |
| `'heat3d-squad-demo' is not recognized` | Повторите шаг 4 в папке инструмента или введите `python -m heat3d_ext_squad` вместо `heat3d-squad-demo`: это то же самое. |
| `No module named heat3d_ext_squad` | Вы не в папке инструмента или шаг 4 не выполнился: выполните `cd` в эту папку и повторите шаг 4. |
| `No module named pip` | Выполните `python -m ensurepip`, затем шаг 4. |
| всё остальное | Прочитайте последнюю строку сообщения и откройте задачу (issue) на GitHub с этой строкой. |

Каждая команда также завершается **кодом выхода**: 0 означает, что всё получилось.
Чтобы его увидеть, введите `echo $LASTEXITCODE` в PowerShell или `echo $?` в macOS и Linux.
