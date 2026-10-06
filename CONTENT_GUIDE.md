# FedOps 콘텐츠 작성 및 배포 안내

Docs, Blog, News는 이 저장소에서 함께 빌드합니다. `main` 브랜치에 변경 사항을 올리면 Jekyll 빌드를 실행하고 세 영역을 함께 배포합니다.

- Docs: `/`
- Blog: `/blog/`
- News: `/news/`

공개 사이트의 기본 주소는 `https://gachon-cclab.github.io/fedops-docs-1.3/`입니다.

이 파일은 저장소 구조를 모르는 작성자와 AI를 위한 작업 지침입니다. 아래 절차를 읽은 뒤 실제 저장소의 기존 파일과 코드를 확인하여 작성합니다. 예시의 제목·날짜·정렬 번호·이미지 경로는 그대로 복사할 고정값이 아닙니다.

## 작업 대상과 저장소 구조

작업 저장소는 `gachon-CCLab/fedops-docs-1.3`입니다. 이 PC의 작업 폴더는 `C:\Users\wjdwl\project\lab\fedops-docs-1.3`이며, 다른 PC에서는 해당 저장소를 받은 폴더를 사용합니다.

| 항목          | 값 및 작업 범위                                                                                                       |
| ------------- | --------------------------------------------------------------------------------------------------------------------- |
| `origin`      | `https://github.com/gachon-CCLab/fedops-docs-1.3.git` — 현재 콘텐츠 저장소                                            |
| 배포 브랜치   | `main` — push하면 세 영역이 함께 배포됨                                                                               |
| `upstream`    | `https://github.com/gachon-CCLab/gachon-CCLab.github.io.git` — 기존 원본 저장소. 이 작업에서 수정하거나 push하지 않음 |
| 기존 1.2 자료 | 현재 저장소의 `v1.2/`, `docs/`, 관련 기존 이미지. 사용자 요청 없이 수정·삭제하지 않음                                 |
| 빌드 결과     | `_site/` — 자동 생성 결과. 원본처럼 직접 수정하거나 커밋하지 않음                                                     |

현재 작업 폴더 또는 기존 저장소가 없으면 대체 저장소를 새로 만들지 말고 사용자에게 상태를 알립니다. 다른 작업자의 변경 사항은 보존하며, 작업과 무관한 파일을 함께 커밋하지 않습니다. GitHub 게시 여부는 현재 세션에서 사용자가 지시한 범위에 따릅니다.

```text
fedops-docs-1.3/
├─ CONTENT_GUIDE.md                  # 이 작성 가이드
├─ index.md                          # 1.3 Overview, 주소 /
├─ v1.3/                             # 1.3 Docs
│  ├─ getting-started.md
│  ├─ task-owner/
│  │  ├─ index.md                    # 수동 관리하는 상위 안내 문서
│  │  ├─ create-task.md
│  │  └─ import-model.md
│  ├─ participant.md
│  ├─ agent-builder.md
│  ├─ campaign.md
│  ├─ developer-guide.md
│  └─ resources.md                   # 수동 관리하는 참고 자료 문서
├─ _news/                            # News 원본 Markdown
├─ _blog/                            # Blog 원본 Markdown
├─ news/index.html                   # News 목록 템플릿
├─ blog/index.html                   # Blog 목록 템플릿
├─ _layouts/
│  ├─ default.html                   # Docs 페이지 템플릿
│  ├─ article.html                   # News·Blog 상세 템플릿
│  └─ publication.html               # News·Blog 공통 화면
├─ _includes/components/             # Docs 메뉴·경로·푸터 등
├─ _config.yml                       # 컬렉션·주소·기본 속성 설정
├─ _data/guide_import.json           # 가져온 가이드의 원본·출력 파일 기록
├─ assets/
│  ├─ blog/                          # Blog·News 이미지
│  ├─ images/v1.3/                   # Notion에서 가져온 Docs 이미지
│  └─ css/fedops-tokens.css           # 세 영역이 공유하는 기준 색상
├─ scripts/
│  ├─ import_guides.py               # Notion 내보내기 가져오기
│  ├─ check_publications.py          # News·Blog 빌드 결과 검사
│  └─ check_site.py                  # Docs 빌드 결과 검사
├─ .github/workflows/deploy.yml       # main 배포 절차
├─ v1.2/                             # 복사한 기존 1.2 Home
├─ docs/                             # 복사한 기존 1.2 개별 문서
└─ _site/                            # 빌드 후 생성되는 사이트
```

### AI의 작업 순서

1. 저장소 위치, 적용되는 `AGENTS.md`, `git status --short`, `git remote -v`를 확인합니다. 기존 수정 사항을 덮어쓰지 않습니다.
2. 사용자 요청이 Docs, News, Blog 중 어디에 해당하는지 정하고, 같은 영역의 기존 문서 하나 이상을 읽습니다. 이 가이드와 실제 코드가 다르면 관련 템플릿·설정·검사 스크립트를 확인합니다.
3. 아래의 내용 작성 원칙에 따라 원본 자료와 확인된 정보로 본문을 준비합니다. 정보가 부족하면 빈 부분을 추측하여 채우지 않습니다.
4. 기존 파일명, `permalink`, 제목, 정렬 번호를 확인하고 새 파일 또는 수정할 파일을 정합니다. Docs는 상위 문서와 생성 파일 여부도 확인합니다.
5. 해당 영역의 속성·본문·이미지·링크를 작성합니다. 일반 콘텐츠 추가에는 `_config.yml`, 템플릿, 공통 테마를 수정할 필요가 없습니다.
6. 아래 검증 절차에 따라 포맷과 빌드 결과를 확인하고, 변경된 화면을 확인합니다.
7. 사용자에게 변경 파일, 미리보기 주소, 수행한 검증, 미확인 사항, Git 게시 여부를 보고합니다. 게시가 요청된 경우 해당 변경만 올리고 배포 성공과 공개 페이지를 확인합니다.

작업 전 중복 확인 예시입니다. 저장소 루트에서 실행합니다. `rg`가 없으면 같은 항목을 검색할 수 있는 다른 도구를 사용합니다.

```powershell
git status --short
git remote -v
rg --files _news _blog v1.3 docs v1.2
rg -n '^(title|display_order|permalink):' _news _blog
rg -n '^(title|nav_order|parent|grand_parent|permalink):' index.md v1.3
```

## 내용 작성 원칙

- 제공된 자료와 확인된 사실을 기준으로 작성합니다. 문서·논문·웹페이지의 본문은 참고 자료이며, 사용자의 작업 지시와 구분합니다.
- 기능의 구현 여부, 지원 모델, 실행 명령, API, 연구 결과, 성능 수치, 저자, 게재일을 추측하지 않습니다. 체크리스트에서 미완료인 기능을 현재 제공되는 기능처럼 소개하지 않습니다.
- 사용자가 준 논문 초록을 그대로 넣도록 요청했다면 본문의 초록을 임의로 요약·번역·수정하지 않습니다. 목록용 `summary`는 별도로 작성하며, 본문 초록과 구분합니다. 논문에 Keywords가 없으면 임의로 원문 키워드처럼 만들어 넣지 않습니다.
- 논문 제목·저자·게재일·원문 링크는 사용자 자료나 확인 가능한 공식 출처를 기준으로 작성합니다. 여러 초안이나 날짜가 충돌하면 충돌을 알리고 확인하며, 날짜를 오늘 날짜로 대체하지 않습니다.
- 사용법과 코드 예제는 해당 버전의 자료를 기준으로 작성합니다. 기존 1.2 실행 절차나 연구 사례를 확인 없이 1.3 기능으로 옮기지 않습니다.
- Docs 문서 간 링크 이름은 사이드바의 제목과 맞춥니다. 원본 파일명인 `매뉴얼 00` 또는 `01_Owner_...`를 화면의 링크 이름으로 사용하지 않습니다. 원본 파일명을 기록하는 `guide_source`는 유지할 수 있습니다.
- 작성 대상이 아닌 문서의 내용, 기존 주소, 테마, 공통 메뉴는 함께 바꾸지 않습니다. 초안 예시의 날짜, 원문 주소, 이미지 경로를 실제 값으로 교체한 뒤 검증합니다.

## Blog 또는 News 글 추가

`_blog/` 또는 `_news/` 폴더에 Markdown 파일을 추가합니다. 파일명은 공개 주소의 마지막 경로가 됩니다. 새 글에는 짧고 나중에 바꿀 필요가 없는 파일명을 사용합니다. 기존 사이트에서 가져온 글은 이전 글과의 연결을 추적할 수 있도록 원래 ID를 파일명으로 유지합니다. 예를 들어 `_blog/fedops-release.md`는 `/blog/fedops-release/` 주소로 공개됩니다.

파일 맨 위의 `---` 사이에 글 정보(front matter)를 작성하고, 그 아래에 본문을 작성합니다. 속성을 전부 넣을 필요는 없습니다. 새 글에는 `title`, `summary`, `category`, `display_order`를 기본으로 지정하는 것을 권장합니다. 작성자와 날짜를 표시하려면 `author`, `date`, `show_date`도 지정합니다. Blog에는 목록 썸네일을 위한 `cover_image`를 추가합니다.

News와 Blog의 상세 페이지 제목은 `title`에서 자동으로 출력합니다. 본문에 같은 제목을 `# 제목`으로 다시 작성하면 제목이 중복되므로, 본문은 문단이나 `## 소제목`으로 시작합니다.

`title`, `summary`, `category`, `author`는 일반 텍스트로 표시됩니다. 값 안에 Markdown의 굵게 표시나 링크 문법을 넣어도 서식으로 변환되지 않습니다. Markdown 서식과 링크는 본문에서 사용합니다. `source_url`을 생략하면 상세 페이지 하단에는 원문 링크 대신 **FedOps Docs** 링크가 표시됩니다.

### News 속성 — `_news/*.md`

| 속성            | 역할                                                         |
| --------------- | ------------------------------------------------------------ |
| `title`         | 목록·상세 페이지·브라우저 탭의 제목                          |
| `summary`       | 목록 소개, 상세 페이지 소개, 검색엔진용 설명                 |
| `category`      | `paper`, `RELEASE` 등 글 종류 표시                           |
| `author`        | 저자·작성자 표시                                             |
| `date`          | 표시할 날짜. `YYYY-MM-DD` 형식 사용                          |
| `show_date`     | `true`면 목록·상세 페이지에 날짜 표시. `date`도 함께 지정    |
| `display_order` | 목록 순서. 작은 숫자가 위에 표시                             |
| `source_url`    | 상세 페이지의 **View original source** 링크                  |
| `hide_summary`  | `true`면 상세 페이지 소개만 숨김. 목록 소개는 유지           |
| `permalink`     | 새 글에는 생략. 현재 배포 검사는 `/news/파일명/` 주소를 요구 |

`layout: article`, `section: news`는 자동 설정되므로 새 글에 따로 작성하지 않아도 됩니다.

새 글은 `_news/` 바로 아래의 `.md` 파일로 만듭니다. 하위 폴더는 현재 검사 대상이 아닙니다. Jekyll 자체는 `permalink`를 지원하지만, 현재 `scripts/check_publications.py`는 파일명 기반 주소를 검사하므로 다른 주소를 지정하면 검사에 실패합니다. 주소 구조 변경이 요청된 경우에만 설정과 검사기를 함께 검토합니다.

News 작성 예시:

```markdown
---
title: "논문 제목"
summary: "목록에 표시할 논문 소개입니다."
category: paper
author: "저자 et al."
date: 2026-10-06
show_date: true
display_order: -1
source_url: "https://example.org/paper"
hide_summary: true
---

## Abstract

여기에 초록을 작성합니다.

## Keywords

키워드를 작성합니다.
```

### Blog 속성 — `_blog/*.md`

| 속성            | 역할                                                               |
| --------------- | ------------------------------------------------------------------ |
| `title`         | 목록·상세 페이지·브라우저 탭의 제목                                |
| `summary`       | 목록 소개, 상세 페이지 소개, 검색엔진용 설명                       |
| `category`      | `Blog` 등 글 종류 표시                                             |
| `author`        | 작성자 표시                                                        |
| `date`          | 표시할 날짜. `YYYY-MM-DD` 형식 사용                                |
| `show_date`     | `true`면 상세 페이지에 날짜 표시. Blog 목록에서는 날짜를 항상 표시 |
| `display_order` | 목록 순서. 작은 숫자가 위에 표시                                   |
| `cover_image`   | 목록의 썸네일 이미지 경로                                          |
| `source_url`    | 상세 페이지의 원문 링크. 생략 가능                                 |
| `hide_summary`  | `true`면 상세 페이지 소개만 숨김. 목록 소개는 유지                 |
| `permalink`     | 새 글에는 생략. 현재 배포 검사는 `/blog/파일명/` 주소를 요구       |

`layout: article`, `section: blog`는 자동 설정됩니다. 썸네일은 현재 목록에서만 사용합니다. `cover_image`에는 `/assets/blog/파일명.png`처럼 저장소 안의 이미지 경로를 지정하며, 실제 이미지 파일도 함께 추가합니다.

새 글은 `_blog/` 바로 아래의 `.md` 파일로 만듭니다. News와 마찬가지로 새 글에 `permalink`를 추가하지 않습니다. 현재 Blog 목록은 썸네일·작성자·날짜를 항상 출력하므로 `cover_image`, `author`, `date`를 준비합니다. 기본 썸네일이나 기본 작성자를 자동으로 채우는 처리는 없습니다.

Blog 작성 예시:

```markdown
---
title: "FedOps 릴리스"
summary: "목록에 표시할 한 문장 소개입니다."
category: Blog
author: FedOps
date: 2026-10-06
show_date: true
display_order: -1
cover_image: "/assets/blog/fedops-release-cover.png"
---

여기에 Markdown으로 본문을 작성합니다.

## 주요 변경 사항

변경 내용을 작성합니다.
```

### 목록 순서

News와 Blog는 날짜가 아니라 `display_order`로 정렬합니다. 값은 따옴표 없는 정수로 지정하고, 같은 영역 안에서는 중복되지 않게 작성합니다. News와 Blog 사이에는 같은 값을 사용해도 됩니다. `display_order`가 없거나 같은 영역에서 중복되면 배포 검사에 실패합니다.

새 글을 맨 위에 표시하려면 해당 영역에서 가장 작은 값보다 더 작은 값을 지정합니다. 예를 들어 현재 최솟값이 `0`이면 다음 글은 `-1`로 지정합니다. 위 예시의 `-1`도 실제 작성 시 기존 글의 값과 비교하여 조정합니다. 날짜 순서를 유지하려면 새 글의 날짜에 맞춰 배치할 위치와 `display_order`를 직접 정합니다.

## Docs 수정

1.3 Overview는 `index.md`에 있으며, 1.3 가이드는 `v1.3/` 폴더에 있습니다. 기존 1.2 문서는 `v1.2/`와 `docs/` 폴더에 유지합니다. 일부 1.3 가이드는 내보낸 원본 파일을 바탕으로 `scripts/import_guides.py`가 생성합니다. 생성된 파일을 직접 수정하면 나중에 원본을 다시 가져올 때 수정 내용이 덮어써질 수 있습니다. 수정하기 전에 `DOCS_1_3_README.md`를 확인합니다.

### Docs 속성 — `v1.3/*.md` 및 하위 폴더

| 속성                 | 역할                                                          |
| -------------------- | ------------------------------------------------------------- |
| `layout`             | 페이지 템플릿. 일반 문서는 `default`                          |
| `title`              | 사이드바·브라우저 탭·검색 결과의 제목                         |
| `permalink`          | 문서 주소                                                     |
| `docs_version`       | `1.2`·`1.3` 구분. 사이드바·검색·버전 표시에 사용              |
| `lang`               | 문서의 언어 설정. 한국어는 `ko`                               |
| `nav_order`          | 같은 단계의 사이드바 메뉴 순서. 숫자는 따옴표 없이 지정       |
| `parent`             | 상위 문서의 `title`. 하위 메뉴와 경로 표시에 사용             |
| `grand_parent`       | 상위 문서보다 한 단계 위 문서의 `title`                       |
| `has_children`       | `true`면 하위 메뉴가 있는 문서로 처리                         |
| `has_toc`            | 하위 문서 목록을 본문 아래 자동 표시할지 설정. `false`면 숨김 |
| `child_nav_order`    | 하위 메뉴 순서 반전. `desc` 또는 `reversed`                   |
| `nav_exclude`        | `true`면 사이드바에서 제외                                    |
| `search_exclude`     | `true`면 문서 검색에서 제외                                   |
| `last_modified_date` | 문서 하단의 마지막 수정일 표시                                |

`v1.3/` 폴더에는 `docs_version: "1.3"`, `lang: ko`가 기본 적용됩니다. `index.md`처럼 해당 폴더 밖에 있는 1.3 문서는 버전을 직접 지정합니다.

Docs의 화면 제목은 본문의 `# 제목`으로 작성합니다. 글 정보의 `title`과 같은 제목을 사용하는 것을 권장합니다. `has_toc`는 하위 문서 목록에 대한 설정이며, 현재 페이지의 소제목 목차를 생성하는 설정은 아닙니다.

독립 문서를 작성하려면 `layout`, `title`, `permalink`, `nav_order`를 지정하고 본문을 작성합니다. 하위 문서로 추가하려면 `parent`를 상위 문서의 `title`과 정확히 일치시키고, 상위 문서에 `has_children: true`를 지정합니다. 같은 단계의 문서끼리는 `nav_order`가 겹치지 않도록 정합니다.

Docs의 `permalink`는 `/v1.3/새문서/`처럼 버전과 마지막 `/`를 포함하여 지정합니다. 사이트 기본 경로인 `/fedops-docs-1.3`은 붙이지 않습니다. 같은 버전 안의 제목·주소 중복을 확인하고, 제목을 변경하면 그 제목을 참조하는 `parent`, `grand_parent`도 확인합니다. 디렉터리 안에 파일을 넣는 것만으로 하위 메뉴가 생기지는 않습니다.

Docs 작성 예시:

```markdown
---
layout: default
title: "새 가이드"
permalink: /v1.3/new-guide/
nav_order: 9
docs_version: "1.3"
lang: ko
---

# 새 가이드

문서의 목적을 설명합니다.

## 사용 방법

사용 절차를 작성합니다.
```

위 예시의 `nav_order: 9`는 기존 메뉴와 비교하여 조정합니다. 하위 문서는 다음처럼 작성합니다. 예를 들어 기존 `Task Owner` 아래 세 번째 문서를 추가할 때는 상위 문서의 `has_children: true`를 확인한 뒤, 같은 단계에 `nav_order: 3`이 없는지 먼저 확인합니다.

```markdown
---
layout: default
title: "추가 Task 가이드"
permalink: /v1.3/task-owner/additional-guide/
parent: "Task Owner"
nav_order: 3
docs_version: "1.3"
lang: ko
---

# 추가 Task 가이드

여기에 본문을 작성합니다.
```

### 수동 관리 문서와 Notion 생성 문서

| 관리 방식       | 대상                                                                        | 수정 방법                                                                                 |
| --------------- | --------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| 수동 관리       | `_news/*.md`, `_blog/*.md`, `v1.3/task-owner/index.md`, `v1.3/resources.md` | 해당 Markdown을 직접 수정                                                                 |
| Notion에서 생성 | `index.md`와 아래 표의 1.3 가이드 7개                                       | 원본 내용을 수정하고 가져오기. 생성 파일의 직접 수정은 다음 가져오기에서 덮어써질 수 있음 |
| 새 Docs 문서    | 가져오기 대상이 아닌 새 `v1.3/*.md`                                         | 직접 작성 가능. Notion 자동 가져오기에 포함하려면 별도로 가져오기 설정을 검토             |

실제 가져오기 대상은 `scripts/import_guides.py`의 `PAGES`와 `_data/guide_import.json`에서 확인합니다.

| 내보낸 원본의 폴더 | 생성 파일                         |
| ------------------ | --------------------------------- |
| `main`             | `index.md`                        |
| `매뉴얼00`         | `v1.3/getting-started.md`         |
| `매뉴얼01`         | `v1.3/task-owner/create-task.md`  |
| `매뉴얼02`         | `v1.3/task-owner/import-model.md` |
| `매뉴얼03`         | `v1.3/participant.md`             |
| `매뉴얼04`         | `v1.3/agent-builder.md`           |
| `매뉴얼05`         | `v1.3/campaign.md`                |
| `개발자가이드`     | `v1.3/developer-guide.md`         |

Notion 원본을 갱신하는 절차:

1. 변경된 원본을 Markdown과 이미지로 내보내고, 위 8개 폴더 구성을 갖춘 전체 원본을 준비합니다. 각 폴더의 원본 Markdown 파일명에는 기존 Notion ID가 있어야 하며, 본문에서 참조하는 이미지도 포함되어야 합니다. 현재 스크립트는 각 폴더의 `.md` 파일 하나를 선택하므로 각 폴더에 사용할 원본 하나만 둡니다.
2. 원본이 있는지, 이미지 경로가 유효한지 확인합니다. 현재 PC의 원본 경로는 `C:\Users\wjdwl\Downloads\fedops1.3_guide`이며, 다른 환경에서는 준비한 전체 원본 경로로 바꿉니다. 원본이 없으면 가져오기를 실행하지 않고 필요한 자료를 알립니다.
3. 가져오기는 문서 하나만 바꾸는 명령이 아니라 8개 문서와 관련 이미지·기록을 갱신하는 작업입니다. 실행 전에 생성 문서의 기존 수정 사항을 확인하고 원본에도 반영되어 있는지 확인합니다. 사용자 요청으로 생성 Markdown을 직접 고친 경우에는 원본이나 변환 규칙에도 수정이 반영되도록 하거나, 다음 가져오기에서 덮어써질 사항을 명시합니다.
4. 저장소 루트에서 아래 명령을 실행합니다.
5. `git diff`로 생성 문서, 이미지, `_data/guide_import.json`, `GUIDE_EDITORIAL_NOTES.md`의 변경을 확인합니다. 사용자 요청과 무관한 본문·그림이 되돌아오지 않았는지 확인하고, 아래 Docs 검증을 수행합니다.

```powershell
python scripts/import_guides.py --source "C:\Users\wjdwl\Downloads\fedops1.3_guide"
```

가져오기 스크립트는 내부 링크·제목·이미지 경로·일부 편집 처리를 수행하지만, 기술 내용이나 실행 결과를 검증하지는 않습니다. `GUIDE_EDITORIAL_NOTES.md`의 미확인 항목은 관련 원본이나 구현 자료를 확인하여 처리합니다.

### 기존 자료의 기록 및 현재 표시 기능이 없는 속성

| 대상      | 속성                 | 현재 용도                                                                            |
| --------- | -------------------- | ------------------------------------------------------------------------------------ |
| News·Blog | `original_date`      | 이전 날짜 기록. 이 값이 있어도 날짜 표시가 활성화되며, 실제 표시 값은 `date` 사용    |
| News·Blog | `legacy_id`          | 이전 사이트의 글 ID 기록                                                             |
| News·Blog | `original_url`       | 이전 사이트의 글 주소 기록                                                           |
| Blog      | `cover_original_url` | 썸네일 원본 주소 기록                                                                |
| Docs      | `guide_source`       | 가져온 Notion 원본 파일명 기록                                                       |
| Docs      | `guide_status`       | `draft` 등 상태 기록. 현재 화면 표시에는 연결되지 않음                               |
| Docs      | `guide_note`         | 가져오기 스크립트가 일부 문서에 기록하는 검토 메모. 현재 화면 표시에는 연결되지 않음 |
| News·Blog | `lang`               | 일부 파일에 있지만 현재 템플릿의 언어 설정에는 연결되지 않음                         |

새 글에 이전 사이트의 기록용 속성을 추가할 필요는 없습니다. 날짜 표시에는 `original_date` 대신 `show_date: true`를 사용합니다. 새로운 속성을 글 정보에 적는 것만으로 화면 표시 기능이 생기지는 않습니다. 예를 들어 `doi`, `journal`, `tags`를 표시하려면 해당 속성을 사용하는 템플릿 코드도 추가해야 합니다.

`guide_status: draft`는 기록용 상태이며 문서를 숨기거나 배포를 막지 않습니다. 이 값만으로 비공개 문서가 된다고 판단하지 않습니다.

## 내부 링크와 이미지

내부 링크와 본문 이미지는 GitHub Pages의 기본 경로에서도 정상적으로 열리도록 `relative_url`을 사용합니다.

```markdown
[Getting Started]({{ '/v1.3/getting-started/' | relative_url }})

![이미지 설명]({{ '/assets/blog/example.png' | relative_url }})
```

Blog·News 이미지는 `assets/blog/` 등 저장소의 이미지 폴더에 넣고 함께 커밋합니다. 로컬 파일 경로인 `C:\...`나 미리보기 주소인 `http://127.0.0.1:8803/`를 공개 글의 링크나 이미지 주소로 사용하지 않습니다. 파일명과 `permalink`를 공개 후 변경하면 기존 링크가 끊길 수 있으므로, 처음 작성할 때 유지할 주소를 정합니다.

파일명과 참조 경로의 대소문자는 일치시킵니다. Windows에서는 열려도 Linux에서 빌드할 때는 다른 파일로 처리될 수 있습니다. 본문 이미지에는 내용을 설명하는 대체 텍스트를 작성합니다. 소제목으로 연결하는 `#앵커`는 실제 빌드된 제목의 `id`를 확인합니다.

Markdown은 UTF-8로 저장하며, 날짜는 `YYYY-MM-DD`, 참·거짓은 따옴표 없는 `true`·`false`, 정렬 번호는 따옴표 없는 정수로 작성합니다. 제목 등에 `:`가 있으면 YAML 문자열을 따옴표로 감쌉니다. 표·목록·코드 블록의 렌더링과 코드 펜스가 닫혔는지 확인합니다.

Jekyll은 Markdown의 코드 블록 안에서도 Liquid 표현식을 처리합니다. 사용 예시 코드에 `{{ ... }}` 또는 `{% ... %}`를 문자 그대로 보여줘야 한다면 해당 예시를 Liquid의 `{% raw %}`와 `{% endraw %}`로 감싸서 표시되는 코드를 확인합니다. 실제 내부 링크에 사용하는 `relative_url`은 실행되어야 하므로 감싸지 않습니다.

## 미리보기 및 배포

모든 명령은 저장소 루트에서 실행합니다. 빌드에는 Ruby·Bundler, 포맷 검사에는 Node.js·npm, 생성 결과 검사에는 Python이 필요합니다. Windows에서 Jekyll은 이 PC에 준비된 WSL Ubuntu-24.04 환경으로 실행합니다. 환경이 다른 경우 저장소의 `Gemfile`, `Gemfile.lock`, `package-lock.json`에 맞춰 의존성을 준비합니다.

### 포맷 확인

Node.js 의존성이 없으면 먼저 `npm ci`를 실행합니다. 작성한 파일의 형식만 정리하려면 아래처럼 대상 파일을 지정합니다. 예시 경로는 실제 수정한 파일로 바꿉니다.

```powershell
npx prettier --write _news/new-paper.md
```

`npm run format:content`는 수동 관리하는 Docs 페이지, 모든 Blog·News Markdown, 공통 CSS, 이 가이드를 함께 정리합니다. 실행하면 다른 파일도 바뀔 수 있으므로 작업 범위를 확인합니다. 커밋 전 검사:

```powershell
npm run check:content
git diff --check
```

새 수동 관리 Docs 파일은 현재 `check:content` 대상에 자동 포함되지 않습니다. `.prettierignore`도 확인하여, 필요한 경우 `package.json`의 콘텐츠 포맷 대상과 `.prettierignore` 예외에 해당 파일을 추가합니다. Notion 생성 문서는 가져오기 과정에서 다시 생성하므로 자동 포맷 정리 대상에서 제외합니다.

### 공개 경로로 빌드 및 News·Blog 검사

Ruby·Bundler를 사용할 수 있는 환경에서 처음에는 `bundle install`을 실행합니다. 아래 명령은 Linux 또는 WSL의 저장소 루트에서 실행합니다.

```bash
bundle exec jekyll build --baseurl /fedops-docs-1.3
python3 scripts/check_publications.py
```

`check_publications.py`는 News·Blog의 정렬 번호, 목록 순서, 파일명 기반 상세 주소, 로컬 이미지 존재 여부를 검사합니다. 본문 내부 링크, 논문 정보의 정확성, Docs 메뉴를 모두 검사하는 것은 아닙니다.

### 이 PC에서 로컬 미리보기 및 Docs 검사

로컬 주소의 루트에서 볼 때는 `--baseurl ""`로 다시 빌드합니다. 공개 경로 빌드와 로컬 루트 빌드는 같은 `_site/`를 갱신하므로 현재 빌드 방식에 맞는 주소와 검사를 사용합니다.

Windows PowerShell의 저장소 루트에서 실행하는 예시:

```powershell
wsl -d Ubuntu-24.04 -- bash -lc 'cd /mnt/c/Users/wjdwl/project/lab/fedops-docs-1.3 && bundle exec jekyll build --baseurl ""'
python scripts/check_publications.py
```

Docs를 수정했다면 로컬 루트 빌드 후 추가로 실행합니다.

```powershell
python scripts/check_site.py
```

`check_site.py`는 Docs의 내부 링크·앵커·이미지와 1.2/1.3 검색 정보를 검사합니다. 현재 스크립트는 1.3 문서 10개와 가이드 이미지 참조 72개를 기대값으로 고정하고 있으며, 공개 기본 경로를 제거하지 않으므로 `--baseurl ""`로 빌드한 결과에서 실행합니다. 문서나 이미지를 실제로 추가·삭제한 경우에는 변경한 구성에 맞게 기대값을 검토하고 갱신합니다. 검사를 통과시키기 위해 누락된 링크나 이미지를 무시하거나 검사를 삭제하지 않습니다.

미리보기 서버를 실행하기 전에 8803 포트에 기존 서버가 있는지 확인합니다. 이미 이 저장소의 `_site/`를 제공하고 있으면 재사용하고, 다른 프로젝트 서버라면 종료하지 않고 사용 가능한 포트를 정합니다. 서버가 없으면 아래 명령을 실행합니다.

```powershell
python -m http.server 8803 --bind 127.0.0.1 --directory _site
```

미리보기 주소:

- Docs: `http://127.0.0.1:8803/`
- News 목록: `http://127.0.0.1:8803/news/`
- News 상세: `http://127.0.0.1:8803/news/파일명/`
- Blog 목록: `http://127.0.0.1:8803/blog/`
- Blog 상세: `http://127.0.0.1:8803/blog/파일명/`

이 서버는 원본 변경을 자동으로 빌드하지 않습니다. Markdown을 수정한 뒤에는 다시 빌드하고 브라우저를 새로고침합니다. 빌드 환경이나 원본이 없어 수행하지 못한 검증은 완료했다고 보고하지 않습니다.

### 화면 확인과 완료 조건

작성자는 자동 검사 외에 브라우저에서 변경한 페이지를 확인합니다.

- News·Blog: 목록에 글이 나타나고 원하는 위치에 있는지, 상세 링크가 열리는지, 제목·저자·날짜·분류·소개 표시가 맞는지 확인합니다. Blog 썸네일, 본문 이미지, 내부 링크와 원문 링크도 확인합니다.
- Docs: 올바른 버전의 메뉴에 나타나는지, 상위·하위 메뉴와 경로 표시가 맞는지, 본문 제목·이미지·코드·표·앵커가 정상인지 확인합니다. 검색 결과에 문서가 나오고 다른 버전과 섞이지 않는지도 확인합니다.
- 데스크톱과 좁은 화면에서 표·이미지·코드가 내용을 가리거나 잘리지 않는지 확인합니다.
- `git diff`로 요청한 내용만 바뀌었는지 확인합니다. 예시 값, 로컬 주소, 누락된 이미지, 이전 제목의 링크가 남아 있지 않아야 합니다.

완료 보고에는 변경한 파일, 확인한 페이지 주소, 실행한 검사와 결과, 남은 원본 동기화나 내용 확인 사항, Git 게시 여부를 포함합니다.

### GitHub 배포

게시가 요청된 경우 GitHub의 기존 `gachon-CCLab/fedops-docs-1.3` 저장소가 존재하고 접근 가능한지 확인합니다. 저장소가 없거나 접근할 수 없다면 대체 저장소를 생성하지 않고 사용자에게 알립니다. 대상 저장소와 브랜치를 다시 확인하고, 해당 작업의 변경 파일만 커밋하여 `origin`의 `main`에 반영합니다. 기존 변경 사항이나 다른 작업자의 커밋을 덮어쓰는 강제 push는 하지 않습니다. 현재 작업 브랜치가 무엇인지 확인한 뒤 기존 원격 변경을 보존하며 반영합니다.

`.github/workflows/deploy.yml`의 **Deploy Jekyll site to Pages** 실행이 성공했는지 확인하고, 공개 사이트의 목록과 변경한 상세 페이지를 다시 확인합니다. push 성공만으로 배포가 완료됐다고 보고하지 않습니다. 워크플로는 포맷 검사, Jekyll 빌드, `check_publications.py` 등을 실행하지만 `check_site.py`는 실행하지 않으므로 Docs 검증은 별도로 수행해야 합니다.

Docs, Blog, News는 동일한 `Gemfile`과 GitHub Actions 워크플로로 배포합니다. 원본에서 가져온 Docs 페이지는 `scripts/import_guides.py`가 다시 생성하므로 자동 포맷 정리 대상에서 제외합니다.

## 공통 테마와 이전 사이트

공통 기준 색상인 `--fedops-primary`와 `--fedops-secondary`는 `assets/css/fedops-tokens.css`에 정의되어 있습니다. 어두운 색, 연한 색, 테두리 색은 이 기준 색상에서 파생됩니다. Docs와 Blog·News 템플릿이 모두 이 파일을 사용하므로 기준 색상을 바꾸면 세 영역에 함께 적용됩니다.

이전 `fedops-publications` Pages 사이트는 기존 링크를 이 사이트로 연결하는 용도로만 사용합니다. 콘텐츠는 현재 저장소에서 관리합니다.
