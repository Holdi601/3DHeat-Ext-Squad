---
title: 데모 변환하기
nav_order: 3
lang: "ko"
source: converting.md
source_hash: "e8c77423085b"
nav_exclude: true
search_exclude: true
---
# 데모 변환하기 {#converting-demos}

```text
heat3d-squad-demo <demos or folders> -o <folder> [--flat] [--json]
python -m heat3d_ext_squad ...          설치 없이 같은 동작
```

## 단계별 안내 {#step-by-step}

명령줄이 처음입니까? 먼저 [시작하기 전에](before-you-start.md)를 읽으세요.

1. 한 번만 설치하세요: `git clone https://github.com/Holdi601/3DHeat-Ext-Squad`, 그 폴더에서 터미널을 열고 `python -m pip install -e .`를 실행합니다.
   (Python 3.10 이상이 필요하며, pyarrow와 numpy도 함께 설치됩니다.)
2. `.replay` 파일을 한 폴더에 모으거나, 파일 이름을 하나씩 지정하세요.
3. `heat3d-squad-demo <folder> -o out`을 실행하세요.
4. 데모마다 한 줄씩 출력됩니다. 레이어, 플레이어 수, 행 수, 그리고 표를 어디에 저장했는지 보여 줍니다. 각 데모는 `out/<map>/` 폴더 안의 독립된 파일 네 개가 됩니다 (`.3dheat` 컨테이너가 아닙니다). `.parquet` 파일을 3DHeat 뷰어에 불러오세요.

![테스트가 만든 가상 데모를 실행한 모습](../assets/img/run.svg)

그림은 실제 매치가 아니라, 테스트(`tests/test_stream.py`)가 만든 데모를 실행한 모습입니다.

## 옵션 {#options}

| 옵션 | 기본값 | 하는 일 |
|---|---|---|
| `demos` (하나 이상) | - | `.replay` 파일, 또는 그 파일이 들어 있는 폴더 |
| `-o`, `--out` | 필수 | 쓸 폴더입니다. 각 데모는 `<out>/<map>/`에 들어갑니다 |
| `--flat` | 꺼짐 | `<map>/` 폴더 없이 지정한 폴더에 바로 씁니다 |
| `--json` | 꺼짐 | 데모마다 JSON 한 줄을 표준 출력에 씁니다 (이 명령을 호출하는 프로그램용). 항목은 `demo`, `ok`, `parquet`, `match`, `sidecars`, `lost`, `rows`, `players`, `layer`, `recorded_unix`입니다. 실패한 데모는 `demo`, `ok: false`, `error`를 씁니다 |
| `--version` | - | 버전을 출력하고 끝냅니다 |

프로그램이 출력하는 모든 옵션: [명령 참조](../cli-reference.md).

맵 폴더 이름은 데모가 지정한 레벨 경로에서 가져옵니다. (`/Game/Maps/<Map>/Gameplay_Layers/<Layer>`이면 `<Map>`이 폴더 이름이 됩니다.)

종료 상태: 모든 데모가 변환되면 0, 하나라도 실패하거나(나머지는 그래도 저장됩니다) `.replay` 파일을 찾지 못하면 1입니다.

## 결과 파일 {#what-comes-out}

| 파일 | 내용 |
|---|---|
| `<demo>.parquet` | 표: 위치와 이벤트, 한 줄에 하나씩 ([표 설명](output-table.md)) |
| `<demo>.match.json` | 매치 문서 ([매치 문서 설명](output-match.md)) |
| `<demo>.entities.parquet` | 보조 파일: 모든 속성 갱신과 원격 호출을 빠짐없이 담습니다 |
| `<demo>.packets.parquet` | 보조 파일: 파일의 조각들과, 읽지 못한 모든 내용을 빠짐없이 담습니다 |

표와 매치 문서는 3DHeat CS2 도구가 쓰는 것과 같은 한 쌍입니다. 뷰어는 표를 바로 열며, 폴더 전체를 불러올 때는 보조 파일을 제외합니다.

## 예시 {#examples}

```bash
heat3d-squad-demo D:\SquadDemos -o out                 # 폴더의 모든 데모
heat3d-squad-demo one.replay two.replay -o out --flat  # out/ 안에 바로 저장
heat3d-squad-demo D:\SquadDemos -o out --json          # 데모마다 JSON 한 줄
```

`D:\SquadDemos`는 D 드라이브의 예시 폴더입니다. 본인의 폴더를 쓰세요.
