---
layout: default
title: "문제 해결 · 알려진 문제"
parent: "참고 자료"
grand_parent: "FedOps 튜토리얼"
nav_order: 1
permalink: /v1.3/tutorial/reference/troubleshooting/
docs_version: "1.3"
lang: ko
---

# 문제 해결 · 알려진 문제
{: .no_toc }

{: .note }
> 2026년 9월 28일, 10월 6일, 10월 11일에 Intel Mac + Docker Desktop 환경에서, 10월 19일에 Mac(Owner) + Windows 노트북(Client) 두 계정으로 이전 데이터(위스콘신 유방암)를 써서 따라 하며 확인한 내용입니다. FedOps·Studio 쪽 문제라 데이터가 바뀌어도 그대로일 것으로 보지만, Heart Disease 로는 아직 다시 확인하지 못했습니다. Agent Studio 가 업데이트되면 달라질 수 있습니다.

## 알려진 문제 (FedOps 쪽 수정 대기)

### 🔴 빌드한 Agent 의 API 에서 Tool 예측 실패

- **증상:** `test_agent.py --sample 0` → `[실패: TOOL_UNAVAILABLE] Tool AI smoke test failed` (로그에 `Readme file does not exist: README.md`)
- **범위:** Agent Builder 의 Generate Response(모델 활용 1장)는 정상, API 의 `/health`·`/info` 도 정상. 빌드된 Agent 를 API 로 부를 때 Tool 단계만 실패
- **원인:** Studio 가 Agent 빌드 스냅샷을 만들 때 `README.md` 를 빼고 복사하는데, Task 패키지 설정이 README 를 요구함
- **현재:** FedOps 쪽 수정 대기(2026-10-06, 2026-10-11 에도 재현). **우회:** Build 할 때마다 Workspace 의 `README.md` 를 `~/fedops-workspace/accounts/*/.local-data/agents/builds/<agentId>/r1/components/tool-0/project/` 에 복사. 이렇게 하면 모델 활용 2~3장이 끝까지 동작함을 확인했습니다

### 🟠 첫 API 호출이 10분 가까이 걸림

- 빌드 후 첫 호출 때 Tool 실행 환경(약 2 GB)을 새로 설치합니다. 2026-10-11 실측 570초(그중 Tool 509초), 두 번째부터 43초
- 이 사이 요청을 겹치거나 PC 가 잠들면 환경이 깨져 `No module named 'torch._tensor'` 가 나거나, Agent API 가 응답을 멈추고 Studio 컨테이너가 멈춘 사례가 있습니다
- Docker 나 Studio 를 다시 켜도 비슷합니다. 2026-10-13 재시작 직후에는 Tool 없이 LLM 만 부르는 첫 호출도 300초 안에 끝나지 않았고, 그 뒤 호출은 40~50초였습니다
- **대처:** 첫 호출은 타임아웃을 900초로, 요청은 하나만, 그동안 PC 가 잠들지 않게. Studio 가 멈춰서 `docker stop` 도 안 되면 Docker Desktop 을 재시작합니다

### 🟡 오래된 Docker 에서 Studio 재시작 실패

- **증상:** `Could not replace existing container` 또는 `unknown flag: --timeout`
- **대처:** Docker Desktop 업데이트. 당장은 `docker stop fedops-agent-studio` 로 멈춘 뒤 `fedops run agent-studio`

### 🟡 Intel Mac 에서 `pip install fedops` 실패

- **증상:** `Failed building wheel for llvmlite`
- **대처:** `pip install --no-deps fedops`

### 🟢 Finish Client Session 을 눌러도 화면이 그대로

- 첫 클릭에서 세션은 이미 끝났습니다. 다시 누르면 500 이 날 수 있는데 무시하고 다음 단계로 넘어가면 됩니다
- 2026-10-20 Mac(Owner) 에서는 **첫 클릭에서 바로 500**(브라우저 콘솔에만 표시)이 났습니다. 캐페인은 이미 끝났고 결과·Global Model 에는 영향이 없었습니다. 여러 번 누르지 말고 다음 단계로 넘어갑니다
- 버튼이 아예 없고 `✓ Client session ended` 가 보이면 세션이 자동으로 끝난 것입니다(2026-10-19 Windows 노트북). 누를 것이 없습니다

### 🟠 Sync 도중 Docker 가 멈춤 (메모리 부족)

- **증상:** Python 환경 Sync 나 `fedops run agent-studio --repair-host` 도중 Studio 와 `docker` 명령이 응답하지 않음. 그 뒤 Local Train 이 `No module named 'torch._utils'` 로 실패
- **원인(추정):** Mac 메모리 부족. 2026-10-20 16 GB Mac 에서 두 번 격었고, 둘 다 남은 메모리가 100 MB 안팎이었습니다
- **대처:** 브라우저 탭·Notion 등 무거운 앱을 닫고 Docker Desktop 을 다시 켭니다(Studio 로그인이 풀리므로 다시 로그인). torch 가 깨졌으면 Python Environments 에서 Default 환경을 **Delete** 후 다시 Sync 합니다(Owner 트랙 3장)

### 🟢 서버를 켜자 준비 점검이 `Check required` 로 돌아감

- 새 캠페인 서버가 켜지면 Owner·Client 모두 점검이 풀립니다. Start Client 전에 **Check Participation Readiness** 를 다시 누릅니다(Client 트랙 3·4장)
- Start Client 첫 클릭이 `[Errno 2] … task-binding.tmp` 로 실패하면 **Refresh** 후 다시 누릅니다

### 🟢 Agent Builder 에서 `handson-heart changed after selection`

- Global Model v1 을 처음 Prepare 할 때 나옵니다(이전 실습에서 매번). 모델은 이미 받아졌으니 새로고침하고 Tool AI 를 다시 고르면 `Global Model v1 · Ready` 로 바뀌어 있습니다. Save 안 한 Base LLM 선택은 사라지므로, Tool AI 를 먼저 고르고 Base LLM 을 나중에 고릅니다

### 🟢 Serving API 에서 `Port 24400 is already assigned to another Agent.`

- 다른 Agent 가 이미 그 포트로 Serving 중입니다. 화면은 쓰고 있는 포트도 기본값으로 보여 줍니다. 포트를 `24401` 처럼 다음 번호로 바꿔 다시 Enable 합니다

### 🟢 Agents 화면의 Delete 가 눌리지 않음

- 그 Agent 의 Serving API 가 켜져 있으면 Delete 버튼이 잠깁니다(화면에 이유가 나오지 않습니다). **Serving API** 탭 → **Disable API** 를 먼저 누릅니다

### 🟢 같은 이름으로 Agent 를 다시 만들 수 없음 (`An Agent draft with this name already exists.`)

- Agents 화면에서 Agent 를 지워도 **Agent Builder 의 초안(draft)** 은 따로 남습니다. Agent Builder 에서 그 초안을 열고 위쪽 **Delete** 로 지운 뒤 다시 만듭니다

### 🟢 Open folder / Open Data Folder 를 눌러도 Finder 가 안 열림

- `The host folder opener refused the connection` — Docker 재시작 등으로 Studio 가 다시 떴을 때 폴더를 여는 호스트 프로그램이 같이 뜨지 않은 것입니다. 터미널에서 `fedops run agent-studio --repair-host` (Studio 는 재시작되지 않습니다)

### 🟢 Demo UI 가 뜨지 않음 (`Unable to evaluate type annotation 'int | None'`)

- Python 3.9 로 실행했습니다. Python 3.10 이상으로 `pip install -r requirements.txt` 후 다시 실행합니다

### 🟢 `prepare_data.py` 가 `클래스마다 3행 이상이어야 …` 로 멈춤

- `--hospitals` 에 `switzerland` 를 넣었습니다. 스위스 병원 데이터는 심장병 없는 환자가 1명뿐이라 FedOps 참여 조건을 채우지 못합니다. 다른 병원을 고릅니다

### ⚠️ FL 서버 live log 에 AWS 접근 키 ID 가 찍힘

- Server Management 의 live log 위쪽 DEBUG 줄에 서버의 AWS 접근 키 ID 와 요청 서명이 보입니다(비밀 키는 아님). live log 화면을 캡처해 공유하지 마세요. FedOps 쪽에 전달할 결함입니다

## 자주 묻는 것

<details markdown="1">
<summary>Studio 와 Console 중 어디서 무엇을 하나요?</summary>

**FedOps Console**(Web 홈페이지의 Open Console): Task 만들기, Registry 게시, 연합학습 서버·캠페인, 참여 승인, 모니터링. **Studio**: 코드·데이터, 로컬 학습·검사, 연합학습 참여, Agent 빌드·API. 두 곳 모두 같은 계정으로 따로 로그인해야 합니다.

</details>

<details markdown="1">
<summary>내 데이터가 어딘가로 올라가나요?</summary>

아니요. 데이터는 `~/fedops-workspace/.../.local-data/` 에만 있고, Registry 에는 코드·모델·README, 연합학습 중에는 모델 파라미터만 오갑니다.

</details>

<details markdown="1">
<summary>왜 정확도가 0.8 도 안 되나요?</summary>

이 데이터의 원래 수준입니다. 1980년대 병원 기록 10개 항목만으로 심장병을 맞히는 문제라 두 병원을 모아 학습해도 0.8 안팎입니다. 이 튜토리얼은 정확도가 아니라 FedOps 로 연합학습을 끝까지 돌려 보는 것이 목적입니다.

</details>

<details markdown="1">
<summary>병원을 더 넣어 볼 수 있나요?</summary>

`python prepare_data.py --hospitals hungarian,cleveland,va` 로 VA 병원 데이터(130행)를 더 만들 수 있습니다. 세 번째 계정이 이 파일로 참여하고, 6장의 Clients per round 를 3 으로 둡니다. 다만 VA 병원은 심장병이 78% 로 치우쳐 있어, 시뮬레이션에서는 Owner 기준 성능이 오히려 떨어지는 경우가 많았습니다. non-IID 가 연합학습에 어떤 영향을 주는지 보는 실험으로는 좋습니다.

</details>

<details markdown="1">
<summary>Task 를 비공개로 게시할 수 있나요?</summary>

현재는 없습니다. Registry 게시는 Public 전환을 포함합니다. 실습 후 원치 않으면 Console 에서 Task 를 삭제하세요.

</details>

<details markdown="1">
<summary>연합학습을 혼자 해도 되나요?</summary>

됩니다. Clients per round 를 1 로 두면 내 PC 하나로 라운드가 돌아갑니다(실제로 확인함).

</details>

<details markdown="1">
<summary>Agent 답변의 숫자가 모델 결과와 다르면?</summary>

Harness 의 Instructions 에 "Tool 수치를 그대로 인용" 규칙이 들어갔는지, Temperature 가 낮은지(0.2) 확인하고 다시 Build 하세요. 정답은 항상 `toolResult.result` 의 값입니다.

</details>

<details markdown="1">
<summary>실습을 끝내고 정리하려면?</summary>

1. Console Server Management → **Pause** (서버 자원 반납)
2. 공개를 원치 않으면 Task actions → **Delete task**
3. Studio → Agents → Serving API **Disable API** (Agent 를 지우려면 그 뒤 Delete, Agent Builder 초안도 Delete)
4. Demo UI 를 껐는지(터미널에서 Ctrl+C) 확인
5. `fedops stop agent-studio`

</details>

<details markdown="1">
<summary>Client 가 받은 코드를 고쳐도 되나요?</summary>

안 됩니다. Client 의 코드는 Owner 가 게시한 Release 와 같아야 참여 준비 점검을 통과하고, 다른 참여자와 파라미터를 합칠 수 있습니다. 코드에 문제가 있으면 Owner 에게 알려 새 Release 를 게시하게 합니다.

</details>

<details markdown="1">
<summary>Client 는 참여가 끝나면 무엇을 정리하나요?</summary>

1. 연합학습 화면에서 **Finish Client Session** 을 한 번 누른다(버튼이 없고 `✓ Client session ended` 가 보이면 이미 끝난 것)
2. 더 참여하지 않을 Task 라면 **Leave**
3. `fedops stop agent-studio`

내 데이터는 `~/fedops-workspace/` 아래 Task 전용 데이터 폴더에 그대로 남아 있습니다. 필요 없으면 직접 지웁니다.

</details>

## 도움 요청

막히면 다음 정보를 모아 CCL 연구실에 문의하세요: 어느 단계인지, 화면의 오류 문구, OS·Docker 버전(`docker version`), Studio 로그(`docker logs --tail 100 fedops-agent-studio`).
