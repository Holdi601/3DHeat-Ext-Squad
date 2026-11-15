---
title: 매치 문서와 보조 파일
nav_order: 5
lang: ko
source: output-match.md
source_hash: "715bd3417e47"
nav_exclude: true
search_exclude: true
---
# 매치 문서와 보조 파일 {#the-match-document-and-sidecars}

표 옆에 데모마다 `<demo>.match.json`과 보조 파일 두 개, `<demo>.entities.parquet`와 `<demo>.packets.parquet`가 생깁니다. 뷰어는 매치 문서를 매치 탭에서 읽습니다.

## 매치 문서 {#the-match-document}

`<demo>.match.json`(매치 문서)은 최상위에 `map`, `layer`, `level_path`, `game_version`, `engine_version`, `recorded_unix`, `duration_s`, `teams`, `squads`, `game_state`, `actors`, `players`, `rows`, `events`, `not_read`, `file`, `header`, `chunks`, `stream`, `shots`, `selfCheck`를 담습니다(전체 목록: [명령 참조](../cli-reference.md)). 말로 풀면 다음과 같습니다. 맵과 레이어, 게임과 엔진 버전, 녹화 시각, 길이, 그리고:

- **팀**: 번호, 진영, 그리고 팀 상태가 복제한 모든 것(티켓, 가용성, 지휘관)을 바뀐 순서대로;
- **분대**: 번호, 팀, 이름, 만든 사람, 리더, 구성원;
- **게임 상태**: 서버 이름과 설정, 게임 모드, 매치 상태와 ID, 맵과 레이어 순환, 투표, 타이머, 오늘의 공지;
- **액터**: 모든 차량, 설치물, 거치 진지, 탄약 상자, 헬리콥터. 각각 클래스, 생성된 곳과 때, 사라진 때, 소유자, 복제된 상태(체력, 건설 상태, 좌석...);
- **플레이어마다 한 줄**: 보행과 탑승 중의 샘플, 걸은 거리, 플레이한 보병 클래스, 사용한 차량, 팀 변경, 앉은 좌석, 그리고 플레이어 상태가 복제한 모든 것(핑, 레벨, 역할, 현재 좌석...). 봇마다 한 줄;
- **이벤트** 집계, **속성 목록**(클래스별 속성이 얼마나 자주 전송되었는지), **원격 호출 목록**, 발사와 명중, **읽지 않은** 것, 그리고 리더의 진단 정보;
- **파일과 헤더**: 정보 블록과 데모 헤더의 모든 필드, 청크 표, 네트 필드 내보내기 표(`net_field_exports`), 채널이 닫힌 이유, 내보내기가 이름을 주지 않은 객체에 대해 찾은 클래스(`stream.class_resolution`);
- **자체 검사**(`selfCheck.completeness`, [완전성](#completeness) 참고).

온라인 ID(Steam, EOS)는 일부러 빼 두었습니다.

변환한 데모를 간단히 보는 예:

```bash
python -c "import json; d = json.load(open('out/<map>/<demo>.match.json')); print(d['map'], d['layer'], d['duration_s'], len(d['players']))"
```

## 완전성 {#completeness}

이 리더는 모든 3DHeat 변환기가 공유하는 원칙을 따릅니다. 지금 읽을 수 있는 것은 해석하고, 나머지는 통째로 보관하며, 종류별로 얼마나 해석했는지 밝힙니다([변환기는 모든 것을 보관합니다](https://github.com/Holdi601/3DHeat/blob/main/docs/converters.md)). 매치 문서마다 `selfCheck.completeness`가 있습니다. 데모에서 만난 항목 종류마다, `seen`(본 개수), `decoded`(완전히 해석한 개수), `partial`(일부만 해석하고 통째로 보관한 개수), `raw`(통째로만 보관한 개수), `lost`(반드시 0이어야 함)를 셉니다. 항목 종류는 리더가 만나는 곳에서 셉니다: `file.info`, `chunk.<kind>`, `frame`, `packet`, `bunch`, `open`, `close`, `export.field`, `export.guid`, `external`, `property:<class>`, `rpc:<class>`, `block:<object>`, `subobject.*`.

실제 데모를 읽었을 때 `lost`는 0입니다. 항목은 수십만에서 수백만 개에 이르고, 약 절반은 완전히 해석되며 나머지는 일부만 해석되거나 통째로 보관됩니다.

**읽는 것**(표와 매치 문서에 들어갑니다):

- 정보 블록, 데모 헤더(모든 필드. 아직 모르는 끝의 두 바이트는 16진수로 보관), 청크 표;
- 모든 프레임, 패킷, 번치(담긴 내용으로 통째로 나눔), 열린 모든 액터(생성 위치, 회전, 크기, 속도 포함)와 닫힌 모든 액터(이유: `Destroyed`, `Dormancy`...);
- 비트가 말하는 만큼의 모든 복제 속성([속성 해석](how-it-works.md#decoding-properties)), `FRepMovement`와 헬리콥터 이동 컴포넌트의 위치, 사상자, 차량의 체력, 좌석;
- 내보내기가 함수의 그룹을 준 경우 매개변수와 함께, 이름으로 된 모든 원격 호출: 발사(`fire`)와 차량 명중(`hit`)은 표에 들어갑니다;
- 네트 필드 내보내기 표와 네트 GUID(개수. 경로는 보조 파일의 엔티티에 있습니다).

**원본 그대로 보관하는 것**(통째로, 읽은 내용을 옆에 함께 둡니다):

- `<demo>.entities.parquet`, 열: `time`, `type`(`<class>.<property>`, `<class>.<call>`, 또는 객체의 이름), `name`(액터의 클래스), `entity`(액터의 네트 GUID, 표의 `entity`와 같음), `kind`, `object`(하위 객체), `channel`, `handle`, `group`(내보내기 그룹의 클래스 경로), `decoded`(JSON), `bits`와 `payload`(비트, 가장 낮은 것부터, 바이트 단위로 채움):
  - 모든 속성 갱신(`kind`가 `property`), 이동 포함, 해석한 내용과 함께. 아무것도 해석되지 않는 경우에만 원본으로 둠(이름 없는 핸들, 포탑의 `RotationReplicatedMovement` 같은 구조, 비트로 남은 속성);
  - 모든 원격 호출과 커스텀 델타 필드(`rpc`). 함수의 그룹이 내보내졌으면 매개변수를 해석하고, 아니면 원본으로 둠(`RepInventory`, `PlayerStateData`);
  - 클래스를 찾지 못한 객체의 모든 콘텐츠 블록(`block`: `Buoyancy`, `GameplayTasksComponent`, `AmmoRackComponent`...). 헤더는 해석함;
  - 열고 닫힌 모든 액터 채널(`open`, `close`), 삭제되거나 파괴된 모든 하위 객체;
  - 나중에 파일만으로 읽는 디코더가 필요로 하는 맥락: 스트림이 준 시점의 모든 네트 필드 내보내기(`export.field`: 그룹 경로, 핸들, 속성 이름, 체크섬)와 모든 내보낸 네트 GUID(`export.guid`: 경로, 외부 객체, 플래그).
- `<demo>.packets.parquet`, 열: `time`, `type`, `name`, `channel`, `offset`(파일 안 위치), `decoded`, `bits`, `payload`. 정보 블록, 헤더 청크, 모든 체크포인트 청크(체크포인트는 그 시점의 모든 액터 상태입니다. 처음부터의 스트림도 이것을 담고 있습니다), 모든 이벤트 청크, 그리고 읽히지 않는 모든 프레임, 패킷, 번치(데모마다 한 번치: 기록자 자신의 관전자의 시작 번치)를 통째로 담습니다.

엔티티 행은 `kind`, `type`, `entity`별로 묶이며, 각 묶음은 시간 순서입니다. 스트림의 순서대로 보려면 `time`으로 정렬하세요.

**제공하지 않는 것:**

- 서버 데모가 기록하지 않는 것: 클라이언트의 입력, 플레이어가 본 화면;
- 클라이언트 쪽 효과: 적중 표시, 소리, 킬 피드의 글자(서버는 호출을 보내고, 화면 표시는 보내지 않습니다);
- 해석된 온라인 ID: 비트로만 보관합니다([개인 정보](limits.md#personal-data) 참고).
