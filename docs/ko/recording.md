---
title: 데모 녹화하기
nav_order: 2
lang: "ko"
source: recording.md
source_hash: "5139aa7d896f"
nav_exclude: true
search_exclude: true
---
# 데모 녹화하기 {#recording-a-demo}

Squad 데모는 게임 클라이언트가 아니라 **서버에서** 녹화합니다.

1. 서버의 `Admins.cfg`에서 관리자 그룹에 `demos` 권한을 주세요.
2. 매치가 시작되면 게임의 콘솔에서 `AdminDemoRec <name>`을 실행하세요. 관리자가 게임 안에서 직접 입력해야 합니다. 한 보고에 따르면 RCON으로는 받아들여지지 않습니다.
3. 매치를 한 뒤 `AdminDemoStop`을 실행하세요.
4. 데모는 `<server>/SquadGame/Saved/Demos/<name>.replay`에 저장됩니다. 이것을 서버에서 변환할 컴퓨터로 복사하세요.

`Server.cfg`에도 `RecordDemos` 설정이 있으며, 기본값은 꺼짐입니다. 작은 매치는 한 시간에 약 70에서 80MB가 됩니다. 100명이 들어가는 서버의 크기는 아직 재 보지 않았습니다.

데모에는 서버에 있던 모든 사람의 이름과 온라인 ID가 들어 있습니다. 이것을 개인 정보로 다루세요([한계, 업데이트, 약관](limits.md#personal-data)).

다음 단계: [데모 변환하기](converting.md).
