---
title: 시작하기 전에
nav_order: 1.5
lang: ko
source: before-you-start.md
source_hash: "ca4b6281fdfc"
nav_exclude: true
search_exclude: true
---
# 시작하기 전에 {#before-you-start}

명령줄이 처음입니까? 이 페이지는 아무것도 없는 상태에서 첫 실행까지 안내합니다.
한 번만 하면 되고, 약 10분 걸립니다.

## 1. Python 설치 {#install-python}

이 도구는 **Python 3.10 이상**이 필요합니다.

- **Windows:** [python.org/downloads](https://www.python.org/downloads/)에서 Python을 내려받고 설치 프로그램을 실행하세요. 첫 화면에서 **Add python.exe to PATH**를 체크한 다음 **Install Now**를 누르세요.
- **macOS와 Linux:** Python 3가 이미 설치되어 있는 경우가 많습니다. 이 페이지에 `python`이라고 나오는 곳에는 `python3`을 입력하세요.

## 2. 이 도구 받기 {#get-this-tool}

[github.com/Holdi601/3DHeat-Ext-Squad](https://github.com/Holdi601/3DHeat-Ext-Squad)를 여세요. 초록색 **Code** 버튼을 누르고 **Download ZIP**을 선택한 뒤, 원하는 폴더에 압축을 푸세요. git을 쓴다면: `git clone https://github.com/Holdi601/3DHeat-Ext-Squad`.

## 3. 그 폴더에서 터미널 열기 {#open-a-terminal-in-that-folder}

터미널은 명령을 입력하는 창입니다.

- **Windows:** 탐색기에서 폴더를 연 다음, 주소창을 클릭하고 `powershell`을 입력한 뒤 Enter를 누르세요. 파란색 또는 검은색 창이 열리는데, 이미 그 폴더에 들어가 있습니다.
- **macOS:** **터미널**을 열고 `cd `(뒤에 빈칸 하나)를 입력한 다음, 폴더를 창으로 끌어다 놓고 Enter를 누르세요.

`cd`는 "폴더 바꾸기"라는 뜻입니다. `cd C:\Tools\3DHeat-Ext-Squad`는 그 폴더로 이동합니다.

## 4. 도구 설치 {#install-the-tool}

다음을 입력하고 Enter를 누르세요:

```bash
python -m pip install -e .
```

끝에 이런 줄이 보여야 합니다: `Successfully installed heat3d-ext-squad-demo-...`.

## 5. 실행 {#run-it}

```bash
heat3d-squad-demo --version
```

다음과 비슷한 줄이 보여야 합니다:

```text
heat3d-squad-demo 0.1.0
```

다음 단계: [데모 녹화하기](recording.md), 그다음 [데모 변환하기](converting.md).

## 이 페이지의 명령 읽는 법 {#how-to-read-the-commands-on-these-pages}

| 보이는 것 | 뜻 |
|---|---|
| `<folder>` | 자리 표시자입니다. `< >` 없이 본인의 값을 입력하세요 |
| `[--force]` | 선택 사항입니다. 생략하거나 보이는 그대로 입력하세요 |
| `a\|b` | 선택지입니다. `a` 또는 `b`를 입력하세요 |
| `# a note` | 설명입니다. 입력하지 마세요 |
| `"C:\My Files\x"` | 공백이 있는 경로는 따옴표로 감싸세요 |
| `D:\Demos` | Windows 폴더 예시입니다. 본인의 폴더를 쓰세요 |

## 문제가 생겼을 때 {#when-something-goes-wrong}

| 메시지 | 할 일 |
|---|---|
| `'python' is not recognized` | Python이 설치되지 않았거나 PATH 항목을 체크하지 않은 것입니다. 다시 설치하면서 체크하세요 (또는 `python` 대신 `py`를 입력하세요). |
| `'heat3d-squad-demo' is not recognized` | 이 도구의 폴더에서 4단계를 다시 실행하거나, `heat3d-squad-demo` 대신 `python -m heat3d_ext_squad`를 입력하세요. 같은 일을 합니다. |
| `No module named heat3d_ext_squad` | 도구의 폴더에 있지 않거나 4단계가 실패한 것입니다. 그 폴더로 `cd`한 뒤 4단계를 실행하세요. |
| `No module named pip` | `python -m ensurepip`를 실행한 뒤 4단계를 하세요. |
| 그 밖의 경우 | 메시지의 마지막 줄을 읽고, 그 줄을 붙여 GitHub에 이슈를 올리세요. |

모든 명령은 마지막에 **종료 상태**를 남깁니다. 0이면 성공입니다. 확인하려면 PowerShell에서는 `echo $LASTEXITCODE`, macOS와 Linux에서는 `echo $?`를 입력하세요.
