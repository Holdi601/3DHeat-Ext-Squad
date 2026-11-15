---
title: 표
nav_order: 4
lang: ko
source: output-table.md
source_hash: "0f3cfed1c108"
nav_exclude: true
search_exclude: true
---
# 표: `<demo>.parquet` {#the-table-parquet}

샘플이나 이벤트 하나에 한 줄입니다. 서버가 액터의 이동을 복제할 때마다 샘플이 하나씩 생기며, 움직이는 동안 초당 최대 8번입니다(데모의 녹화 속도).

![가상 데모 표의 첫 줄들](../assets/img/table.svg)

## 열 {#columns}

| 열 | 뜻 |
|---|---|
| `time` | 녹화가 시작된 뒤의 초 |
| `x`, `y`, `z` | Unreal 단위(센티미터)의 위치, Z가 위 |
| `dirX`, `dirY`, `dirZ` | 보병이 보는 방향: 몸의 요(yaw)와 시점의 피치를 합친 단위 벡터 (차량은 수평) |
| `yaw`, `pitch` | 같은 값을 도 단위로; `pitch`는 지평선에서 위로, 보병에게만 해당 |
| `health` | 그 순간 보병, 봇 또는 차량의 체력. 서버가 보낸 경우에만 있습니다 (부상당한 보병의 체력은 0 아래로 떨어집니다) |
| `speed` | 복제된 속도, cm/s |
| `player` | 플레이어 이름. 봇은 `bot <id>`. 주인이 없는 차량이나 설치물은 클래스. 차량 무기의 발사라면 그 차량에 앉은 플레이어 |
| `team`, `faction` | Squad의 팀 번호(1, 2)와 진영 구성, **그 순간의 값**: 플레이어는 편을 바꿀 수 있습니다 |
| `squad` | 분대 번호. 분대에 속하지 않으면 -1 |
| `event` | 이 행이 무엇인지 (아래 참고) |
| `pawn` | 보병 블루프린트(봇은 `SQSquidBot`), 차량, 또는 `fire`의 경우 무기 |
| `seat` | 포탑이나 승객 좌석의 경우, 그 좌석 자체의 폰 |
| `detail` | `fire`의 경우 발사를 일으킨 무기 호출, `hit`의 경우 피해 종류, `removed`의 경우 채널이 닫힌 이유(`Destroyed`, `Dormancy`...) |
| `entity` | 이 행이 다루는 액터(그 네트 GUID). 보조 파일 행의 `entity`와 같습니다 |
| `match` | 데모의 이름 |

## 이벤트 {#events}

| `event` | 해당 행의 대상 | 내용 |
|---|---|---|
| `position` | 보행 중인 보병 또는 봇 | 이동 샘플 |
| `vehicle` | 지상 차량이나 헬리콥터에 탄 보병 | 차량 위치에서의 샘플 |
| `wounded`, `revived`, `death` | 보병과 봇 | 일어난 곳 |
| `spawn`, `damaged`, `destroyed`, `removed` | 차량, 설치물, 거치 진지, 상자, 헬리콥터 | 그것들이 있던 곳 |
| `seat` | 플레이어 | 좌석에 앉음 |
| `fire` | 사수 | 발사: 발사된 곳, 방향은 `yaw`/`pitch`/`dirX..Z` |
| `hit` | 차량 | 차량 명중: 어디에 |

이벤트를 읽는 방법은 [데모를 읽는 방법](how-it-works.md#how-the-events-are-read)에 있습니다.

## 뷰어에서 {#in-the-viewer}

Parquet 바닥글에는 `heat3d` 키 아래에 읽는 방법이 적혀 있습니다. Z가 위, 축 뒤집기 없음, 단위 배율 1이므로 뷰어는 열을 따로 연결할 필요가 없습니다. 표는 히트맵 탭에서 여세요. 뷰어의 [데이터 넣기](https://holdi601.github.io/3DHeat/getting-data-in.html)와 [열 연결](https://holdi601.github.io/3DHeat/column-mapping.html)을 보세요.
