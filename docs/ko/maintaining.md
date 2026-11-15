---
title: 문서 관리
nav_order: 91
lang: "ko"
source: maintaining.md
source_hash: "b0b7836a5545"
nav_exclude: true
search_exclude: true
---
# 문서 관리 {#maintaining-these-docs}

릴리스마다 따르는 체크리스트입니다. 코드가 바뀌어도 페이지가 뒤처지지 않도록 합니다.

1. **참조를 다시 만드세요.** `python tools/gen_docs_reference.py`를 실행하면 프로그램 자체의 `--help`와 출력 열을 바탕으로 [명령 참조](../cli-reference.md)를 다시 씁니다. `python tools/gen_docs_reference.py --check`는 커밋된 페이지가 오래되었으면 1로 끝납니다.
2. **바뀐 것을 나열하세요.** `git log v<VERSION>..HEAD --oneline`을 실행합니다. 여기서 `<VERSION>`은 마지막으로 릴리스된 버전입니다(릴리스 때의 `VERSION` 파일). 새 기능, 옵션, 출력 열마다 페이지에 자리를 주고, [`CHANGELOG.md`](https://github.com/Holdi601/3DHeat-Ext-Squad/blob/main/CHANGELOG.md)의 **Docs** 항목에 한 줄을 추가하세요.
3. **독립적으로 검토하세요.** 페이지를 쓰지 않은 사람이 README와 바뀐 모든 페이지를, 그림까지 포함해 세 번 읽습니다. 터미널을 한 번도 써 본 적 없는 초보자로, 여덟 살 어린이로, 그리고 모든 옵션을 `--help`와 대조하는 전문가로 읽습니다. 예시는 지어낸 이름과 숫자만 씁니다.
4. **검토에서 나온 것은 모두 고치세요.**
5. **번역.** 번역된 페이지마다, 그것을 만든 영문 페이지의 해시를 기록합니다. 영문 원본이 바뀐 페이지는 다시 번역하고, 각 언어를 검토하세요. 글이 분명한지, 그림 라벨이 맞는지, 뷰어 자체의 번역된 인터페이스와 같은 단어를 쓰는지 확인합니다.
6. **테스트를 실행하세요** (`pytest`).
7. **푸시는 소유자의 허락을 받은 뒤에만** 하세요.

## 번역: 명령 {#translations-the-commands}

이 사이트는 3DHeat 뷰어의 40개 언어로 번역됩니다. 영문은 `docs/`에, 다른 언어는 같은 파일 이름으로 `docs/<lang>/`에 있습니다. `tools/docs_i18n.py`가 이 관리 작업을 합니다:

```bash
python tools/docs_i18n.py hashes             # 영문이 바뀔 때마다: 각 페이지의 해시를 기록
python tools/docs_i18n.py svg-strings        # 그림이 바뀔 때마다: 번역할 라벨 목록
python tools/docs_i18n.py status             # 언어별: 최신, 오래됨, 없는 페이지
python tools/docs_i18n.py todo --lang de     # 독일어로 (다시) 번역할 페이지
python tools/docs_i18n.py svg-build --lang de    # docs/assets/i18n/svg/de.json으로 독일어 그림 만들기
python tools/docs_i18n.py finish --lang de   # 독일어 페이지에 영문 해시를 찍기
python tools/docs_i18n.py check              # 해시나 라벨이 오래되었으면 1로 끝남
```

`todo`가 나열한 것만 번역하세요. Markdown, 링크, 코드, 파일 이름과 열 이름은 그대로 두고, 제목과 그림 설명은 번역하세요. 버튼과 패널 이름은 뷰어 자체의 말(`src/i18n/locales/<lang>/`)을 쓰세요. 자동 생성된 참조 페이지와 터미널 그림은 영어로 둡니다. 사이트에서 오래된 번역은 그 사실을 알리고 영문 페이지로 연결합니다. 없는 번역은 영어 페이지로 대신합니다. 머리글의 언어 메뉴와 홈 페이지의 브라우저 언어 자동 이동은 `docs/_includes/`에서 가져옵니다.
