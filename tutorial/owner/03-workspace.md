---
layout: default
title: "3. Workspace 에 코드와 데이터 넣기"
parent: "Task Owner 트랙"
grand_parent: "FedOps 튜토리얼"
nav_order: 3
permalink: /v1.3/tutorial/owner/workspace/
docs_version: "1.3"
lang: ko
---

# 3. Workspace 에 코드와 데이터 넣기
{: .no_toc }

{: .note }
> 📍 **지금 어디:** Task Owner 3/7 — ① 설계 → ② Task 만들기 → **③ Workspace** → ④ 학습·게시 → ⑤ 승인 → ⑥ 캠페인 → ⑦ 결과<br> 화면: **Agent Studio** (+ Finder) · 다음: 첫 모델을 학습하고 Registry 에 게시한다

{: .important }
> 🎯 **이 단계에서 하는 일:** 2장에서 만든 빈 Task 를 Studio 에서 열고(**Workspace**), 1장의 일반 학습 코드를 FedOps 가 정한 모양으로 옮긴 **완성본 코드**를 넣습니다. 그리고 Owner 자신의 데이터(헝가리 병원)를 둡니다. 이 코드는 4장에서 게시되면 **모든 Client 의 PC 에 그대로 배포되어 실행됩니다.** 그래서 Owner 의 코드가 곧 연합학습 전체의 약속입니다.

1. TOC
{:toc}

## 왜 코드를 정해진 모양으로 옮기나

1장의 `train_centralized.py` 는 내가 실행하는 스크립트였습니다. 연합학습에서는 **내 코드를 내가 실행하지 않습니다.**

| 누가 | 내 코드의 무엇을 부르나 |
| --- | --- |
| 집계 서버 | 모델을 만드는 함수 (파라미터 모양을 알아야 합칠 수 있음) |
| 각 Client 의 Studio | 데이터를 읽는 함수, 학습 함수, 평가 함수 |
| Agent (모델 활용 트랙) | 예측 함수 |

남이 내 코드를 부르려면 **이름과 인자가 약속되어 있어야** 합니다. 그래서 FedOps 는 이름·인자가 고정된 함수에 내 코드를 넣는 방식을 씁니다. 템플릿 코드에서 두 표시를 보세요.

| 표시 | 뜻 |
| --- | --- |
| `# FEDOPS CONTRACT` | 이름·인자·기본값을 **바꿀 수 없는** 함수. FedOps 가 코드 안을 들여다보지 않고 그대로 부른다 (예: `build_model`, 학습 함수) |
| `# USER IMPLEMENTATION` | 내 마음대로 쓰는 부분 (예: `TabularMLP` 클래스의 층 구성) |

함수 **안의 구현**은 자유입니다. 이 튜토리얼에서는 변환이 끝난 완성본(`template/federated-task/`)을 그대로 씁니다.

## 1) Studio 에서 Workspace 열기

**① Workspace 화면**

![Studio Workspace 화면의 New Federated Task 버튼]({{ '/tutorial/images/ho3-01.png' | relative_url }})

1. Studio 왼쪽 메뉴에서 **Workspace** 를 고른 뒤, 오른쪽 위 **+ New Federated Task** 를 누릅니다.

**② Start a Federated Task Workspace 창**

![My Web Draft 에서 handson-heart 선택]({{ '/tutorial/images/ho3-02.png' | relative_url }})

1. **My Web Draft** 탭을 고릅니다.
2. **FedOps Web Draft** 목록에서 방금 만든 `handson-heart` 를 고릅니다.
3. **Open Draft in Workspace** 를 누릅니다.

**③ 열린 Workspace**

![열린 handson-heart Workspace]({{ '/tutorial/images/ho3-03.png' | relative_url }})

`handson-heart` Workspace 가 열립니다. 아직 Python 환경은 `missing` 입니다.

> Workspace 이름이 나중에 **Tool id** 가 됩니다. `handson-heart` 라면 Tool id 는 `local:handson-heart` 입니다.

{: .highlight }
> **1번 탭(Python Environments)은 아직 누르지 마세요.** 다음 단계에서 의존성 파일이 바뀌므로, 템플릿을 넣은 다음에 Sync 해야 한 번에 끝납니다.

### ⚙️ 옵션 해설 — Workspace 를 여는 세 가지 출처

Start a Federated Task Workspace 창의 탭은 "어디서 시작하느냐"입니다.

| 탭 | 무엇 | 누가 |
| --- | --- | --- |
| **My Web Draft** | 내가 Console 에서 만든 Task (아직 게시 전) | **Owner — 이 튜토리얼** |
| **Joined Registry Task** | 남의 Task 에 참여 승인을 받은 것 | Client ([Client 트랙 2장]({{ '/v1.3/tutorial/client/workspace/' | relative_url }})) |
| (그 밖의 탭) | 기존 코드를 가져오는 경로 | 이 튜토리얼에서는 쓰지 않음 |

## 2) 템플릿 파일 넣기 (Finder)

템플릿 폴더의 파일을 Workspace 폴더로 **끌어다 놓습니다.** 두 Finder 창을 나란히 두고 하면 편합니다.

**① Workspace 폴더 열기**

![Studio Workspace 의 Open folder 버튼]({{ '/tutorial/images/ho3-12.png' | relative_url }})

1. Studio Workspace 위쪽의 **Open folder** 를 누릅니다. Finder 에 Workspace 폴더(`handson-heart`)가 열립니다.

![Finder 에 열린 Workspace 폴더]({{ '/tutorial/images/f-open.png' | relative_url }})

위처럼 Workspace 폴더가 열리면, Finder 에서 **새 창(⌘N)** 을 열고 내려받은 가이드의 `FedOps-hands-on-guide/template/federated-task` 폴더로 갑니다. 두 창을 왼쪽(템플릿)·오른쪽(Workspace)으로 나란히 둡니다.

{: .warning }
> **`federated_task` 폴더를 통째로 끌어다 놓지 마세요.** Finder 는 같은 이름의 폴더를 **통째로 바꿔** 버려서 FedOps 가 관리하는 파일(`main.py`, `federated_learning/` 등)이 사라집니다. 아래 ㉠~㉤ 처럼 **파일만** 골라 같은 이름의 하위 폴더에 넣습니다.

각 그림에서 **1** = 왼쪽 창에서 고를 파일, **2** = 오른쪽 창의 놓을 곳입니다. 같은 이름의 파일이 있다는 창이 뜨면 **대치** 를 누릅니다.

**㉠ `README.md`, `requirements.txt` → Workspace 맨 위**

![README.md 와 requirements.txt 를 Workspace 맨 위로]({{ '/tutorial/images/f-g1.png' | relative_url }})

1. 왼쪽 창(`federated-task`)에서 `README.md` 와 `requirements.txt` 를 고릅니다(⌘ 누른 채 클릭).
2. 오른쪽 창(`handson-heart`)의 빈 곳에 끌어다 놓습니다.

**㉡ `config.yaml` → `federated_task/conf`**

![config.yaml 을 federated_task/conf 로]({{ '/tutorial/images/f-g2.png' | relative_url }})

1. 왼쪽은 `federated_task` → `conf` 로 들어가 `config.yaml` 을 고릅니다.
2. 오른쪽도 `federated_task` → `conf` 로 들어가 그 안에 놓습니다.

**㉢ `local_training` 의 `.py` 5개 → `federated_task/local_training`**

![local_training 의 파일 5개를 같은 폴더로]({{ '/tutorial/images/f-g3.png' | relative_url }})

1. 왼쪽 `federated_task` → `local_training` 에서 `.py` 파일 5개를 모두 고릅니다.
2. 오른쪽 `federated_task` → `local_training` 에 놓습니다.

**㉣ `manifest.json`, `tool.py` → `federated_task/tool_ai`**

![manifest.json 과 tool.py 를 tool_ai 로]({{ '/tutorial/images/f-g4.png' | relative_url }})

1. 왼쪽 `federated_task` → `tool_ai` 에서 `manifest.json` 과 `tool.py` 를 고릅니다.
2. 오른쪽 `federated_task` → `tool_ai` 에 놓습니다.

**㉤ `tools` 폴더 → Workspace 맨 위**

![tools 폴더를 Workspace 맨 위로]({{ '/tutorial/images/f-g5.png' | relative_url }})

1. 왼쪽 맨 위(`federated-task`)에서 `tools` 폴더를 고릅니다.
2. 오른쪽 맨 위(`handson-heart`)에 놓습니다. (이 폴더는 Workspace 에 원래 없으므로 통째로 넣어도 됩니다)

<details markdown="1">
<summary>터미널로 한 번에 넣기 (같은 결과)</summary>

`template/` 폴더에서 실행합니다.

```bash
ls -d federated-task  # 'No such file' 이면 template/ 폴더가 아니다
WS=$(echo ~/fedops-workspace/accounts/*/projects/handson-heart)
ls -d "$WS"          # 경로가 한 줄 나와야 한다
cd federated-task
cp README.md requirements.txt "$WS"/
cp federated_task/conf/config.yaml     "$WS"/federated_task/conf/
cp federated_task/local_training/*.py  "$WS"/federated_task/local_training/
cp federated_task/tool_ai/manifest.json federated_task/tool_ai/tool.py "$WS"/federated_task/tool_ai/
mkdir -p "$WS"/tools && cp tools/embed_preprocessing.py "$WS"/tools/
cd ..
```

</details>

> Windows 는 탐색기에서 같은 방법으로 넣거나, Studio 의 **Code** 탭에서 같은 파일을 열어 내용을 붙여넣어도 됩니다.

`federated_learning/`, `runtime/`, `task_readiness/`, `main.py`, `pyproject.toml`, `uv.lock` 은 FedOps 가 관리하는 파일이니 건드리지 않습니다.

## 3) Python 환경 설치 (Sync)

**① Python Environments 탭**

![Python Environments 탭의 Sync environment]({{ '/tutorial/images/ho3-07.png' | relative_url }})

1. **Python Environments** 탭을 누릅니다.
2. 아래로 내려 **Default** 환경의 **Sync environment** 를 누릅니다.

**② 진행 중**

![Sync 진행 중 — 76% Packages prepared]({{ '/tutorial/images/ho3-08.png' | relative_url }})

torch 등을 받느라 **10분 가까이** 걸립니다(2026-10-20 Mac 실측: 패키지 128개 설치 9분 20초). **76% 에서 오래 멈춘 것처럼 보이는데**, 패키지를 설치하는 중이니 기다립니다.

**③ 완료**

![환경이 ready 로 바뀐 화면]({{ '/tutorial/images/ho3-09.png' | relative_url }})

위쪽 환경 표시가 `Default · Python 3.12 · ready` 로 바뀌면 끝입니다.

> **왜 필요한가:** 학습 코드는 Studio 컨테이너 안의 별도 Python 환경에서 돕니다. `requirements.txt` 에 적힌 패키지(torch 등)를 이 환경에 설치하는 것이 Sync 입니다. Client 도 참여 전에 같은 Sync 를 합니다. 모든 참여자가 같은 패키지 목록으로 학습하게 하려는 것입니다.

## 4) Owner 의 데이터 두기

**① Task Test 탭**

![Task Test 탭의 Open Data Folder 와 Refresh]({{ '/tutorial/images/ho3-10.png' | relative_url }})

1. **Task Test** 탭을 누릅니다. Local data setup 에 `Folder ready` 가 보입니다.
2. **Open Data Folder** 를 누르면 데이터 폴더가 열립니다. 여기에 1장에서 만든 `data/out/hungarian/dataset.csv` 를 **이름 그대로** 넣습니다. 터미널로 하려면 `template/` 폴더에서:
   ```bash
   cp data/out/hungarian/dataset.csv ~/fedops-workspace/accounts/*/.local-data/federated-tasks/handson-heart/dataset/
   ```
3. 파일을 넣은 뒤 **Refresh** 를 누릅니다.

**② 인식 완료**

![Data detected 로 바뀐 화면]({{ '/tutorial/images/ho3-11.png' | relative_url }})

`Folder ready` 가 **`Data detected`** 로 바뀌면 됩니다. 파일 이름은 정확히 `dataset.csv`, 하위 폴더 없이 둡니다.

> 로컬 데이터는 어디에도 업로드되지 않습니다. Registry 에 올라가는 것은 코드와 모델뿐입니다.

> **Owner 가 왜 데이터를 두나요?** 4장에서 첫 모델(Initial Model)을 학습하고, 코드가 약속을 지키는지 실제 데이터로 점검하려면 데이터가 필요합니다. 이 튜토리얼에서 Owner 는 헝가리 병원이기도 합니다. Owner 에게 데이터가 전혀 없다면 공개 데이터나 합성 데이터로 첫 모델을 만들기도 합니다.

## 5) 전처리 통계 고정 — 이미 되어 있음

템플릿의 `data_preparation.py` 에는 **헝가리 데이터로 계산한 전처리 통계가 이미 들어 있습니다.** 이 튜토리얼을 그대로 따라 한다면 아무것도 하지 않아도 됩니다. 데이터를 바꿨다면 Owner 가 Workspace 에서 한 번 다시 고정합니다.

```bash
python tools/embed_preprocessing.py --data-root <Data Folder>
```

{: .warning }
> **Client 는 이 명령을 실행하지 않습니다.** 실행하면 코드가 바뀌어 게시된 Release 와 달라지고, 같은 환자도 병원마다 다른 숫자로 모델에 들어가게 됩니다.

<details markdown="1">
<summary>📚 연합학습 배경 — 데이터 형식도 약속이다</summary>

연합학습에서 서버도 Owner 도 Client 의 데이터를 볼 수 없습니다. 그래서 **모든 Client 가 같은 형식의 데이터를 둔다**는 약속이 코드에 들어 있어야 합니다. 이 템플릿에서는 세 곳이 그 약속입니다.

| 파일 | 약속 |
| --- | --- |
| `local_training/schema.py` | 열 이름 10개(수치 8개 + 범주 `cp`·`restecg`), 범주별 허용 값, 정답 열 `target`, 클래스 이름 `no_disease`·`disease` |
| `conf/config.yaml` | 입력 크기 10, 출력 크기 2, 모델 표시명 `Heart Disease MLP` |
| `tool_ai/manifest.json` | Agent 가 Tool 에 넣을 입력 이름과 범주 값 |

Client 의 CSV 가 이 약속과 다르면 참여 준비 점검(Readiness)에서 걸립니다. Client 는 이 약속을 Registry 의 **README** 에서 읽습니다.

</details>

## ✅ 체크리스트

- [ ] Studio Workspace 에 템플릿 파일이 들어갔다
- [ ] Python Environment 가 `ready` 다
- [ ] Task Test 에 `Data detected` 가 보인다

<details markdown="1">
<summary>자기 데이터·모델로 바꾸려면</summary>

1. `local_training/schema.py` 에서 피처 이름·범주 값·클래스 이름을 고친다
2. `conf/config.yaml` 의 `model.input_size` / `output_size` / `display_name` 을 맞춘다
3. `tool_ai/manifest.json` 의 `features` 와 `output.labels` 를 맞춘다
4. CSV 를 Data Folder 에 둔다
5. `python tools/embed_preprocessing.py --data-root <폴더>` 를 **반드시** 다시 실행 (전처리 통계 고정)

세 파일(`schema.py`, `config.yaml`, `manifest.json`)이 어긋나면 다음 단계의 Local Train 이나 Readiness 검사에서 걸립니다.

</details>

## 안 되면

| 증상 | 조치 |
| --- | --- |
| Open folder 를 누르면 `The host folder opener refused the connection` 경고 | Studio 가 Docker 재시작으로 다시 떴을 때 폴더를 여는 호스트 프로그램이 같이 뜨지 않은 것입니다. 터미널에서 `fedops run agent-studio --repair-host` (Studio 는 재시작되지 않음) |
| `cp: ... Not a directory` | `WS=$(echo ...)` 형태로 썼는지, `template/` 폴더에서 실행했는지 확인. Workspace 를 다른 이름으로 만들었다면 경로도 바꾼다 |
| My Web Draft 목록이 비어 있음 | Console 에서 Task 를 만들었는지, Studio 와 Console 이 같은 계정인지 확인 |
| Sync 실패 | `requirements.txt` 의 기본 줄을 지웠거나 버전을 바꿨는지 확인 |
| Sync 도중 Studio 가 응답하지 않고, 그 뒤 Local Train 이 `No module named 'torch._utils'` 로 실패 | Sync 중 Docker 가 멈춰 torch 가 반만 설치된 것입니다(2026-10-20 Mac 에서 겪음). Sync again 으로는 고쳐지지 않습니다. Docker Desktop 을 다시 켜고, Python Environments 의 Default 환경을 **Delete** 한 뒤 **Sync environment** 를 다시 누릅니다(코드와 `uv.lock` 은 남음) |
| Refresh 해도 `Folder ready` 그대로 | 파일 이름이 `dataset.csv` 인지, 하위 폴더 안에 넣지 않았는지 확인 |
| `고정 전처리가 아직 설정되지 않았다` | `tools/embed_preprocessing.py` 를 실행 |

## 다음 단계

[4. 첫 모델 학습과 Registry 게시]({{ '/v1.3/tutorial/owner/release/' | relative_url }})
