# FedOps 1.3 문서 작업 안내

기존 Jekyll / Just the Docs 구조를 재사용합니다. 배포 저장소는 `gachon-CCLab/fedops-docs-1.3`이며 `main` 브랜치를 GitHub Pages로 배포합니다.

## 문서 구성

- `/`: 1.3 Overview
- `/v1.3/`: Getting Started, Task Owner, Participant, Agent Builder, Campaign, Developer Guide, Resources
- `/v1.2/`: 기존 Home
- `/docs/...`: 기존 문서 URL과 본문 유지

사이드바와 검색 결과는 현재 문서 버전별로 나뉩니다. 1.3 가이드는 작성 중 표시를 유지합니다.

## Notion 내용 갱신

원본 폴더 구성(main, 매뉴얼00~05, 개발자가이드)을 유지한 Markdown 내보내기를 준비하고 저장소에서 실행합니다.

```powershell
python scripts/import_guides.py --source "C:\Users\wjdwl\Downloads\fedops1.3_guide"
```

8개 가이드와 이미지를 다시 생성합니다. 생성 문서를 직접 수정하면 다음 이관 때 덮어쓰므로 본문 수정은 원본에 반영합니다. Task Owner 안내 페이지와 Resources는 수동 관리합니다. 원본 파일 해시와 이관 개수는 `_data/guide_import.json`에 기록됩니다.

이미지 경로, 문서 간 링크, 표 줄바꿈, 중첩 코드 펜스를 웹에 맞게 변환합니다. 개발자 가이드의 긴 MNIST/Baseline 예제는 접어서 표시합니다. 기술 내용의 타당성이나 실제 FedOps 실행 결과를 검증한 것은 아닙니다.

## 로컬 빌드와 확인

이 PC에는 WSL Ubuntu-24.04의 Ruby/Bundler로 빌드 환경을 준비했습니다. Bundler 라이브러리는 `/tmp/fedops-docs-bundle`에 있어 삭제된 경우 `bundle install`을 다시 실행합니다.

```bash
cd /mnt/c/Users/wjdwl/project/lab/fedops-docs-1.3
bundle install
bundle exec jekyll build --baseurl ""
```

Windows에서 미리보기 서버:

```powershell
python -m http.server 8803 --bind 127.0.0.1 --directory _site
```

주소: http://127.0.0.1:8803 . 원본 수정 후 다시 빌드하고 브라우저를 새로고침합니다.

빌드된 페이지의 내부 링크와 이미지 확인:

```powershell
python scripts/check_site.py
```

## 공개 전 내용 확인

`GUIDE_EDITORIAL_NOTES.md`에 원본의 편집 메모와 검토 항목을 모았습니다. Manual 02 보완, Manual 01 Web Draft 정의, Manual 05 서버 생성 순서, Main과 Manual 04의 Tool AI 최소 개수 차이를 확인해야 합니다. 원문을 임의로 확정하지 않았습니다.

현재 1.3을 기본 화면으로 만들었으므로 공개 시 기존 첫 화면도 바뀝니다. 기존 개별 문서 URL은 보존됩니다. 공개 주소는 https://gachon-cclab.github.io/fedops-docs-1.3/ 입니다.
