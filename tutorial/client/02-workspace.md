---
layout: default
title: "2. Workspace 와 내 데이터 준비"
parent: "Client 트랙"
grand_parent: "FedOps 튜토리얼"
nav_order: 2
permalink: /v1.3/tutorial/client/workspace/
docs_version: "1.3"
lang: ko
---

# 2. Workspace 와 내 데이터 준비
{: .no_toc }

{: .note }
> 📍 **지금 어디:** Client 2/5 — ① 찾기·요청 → **② Workspace·데이터** → ③ 준비 점검 → ④ 참여 → ⑤ 마무리<br> 화면: **Agent Studio** · 전제: Owner 가 참여를 승인했다

{: .important }
> 🎯 **이 단계에서 하는 일:** Owner 가 게시한 코드를 내 Studio 로 가져와(**Workspace**) 실행 환경을 설치하고, **내 데이터(클리블랜드 병원)를 내 PC 의 정해진 폴더에** 둡니다. 데이터는 이 폴더에만 있고 어디에도 올라가지 않습니다. 학습은 4장에서 Owner 의 코드가 이 폴더의 데이터를 읽어 내 PC 안에서 합니다.

1. TOC
{:toc}

## 1) Workspace 열기

![Workspace 의 Joined Registry Task 탭]({{ '/tutorial/images/hc2-01.png' | relative_url }})

1. Studio 왼쪽 메뉴 **Workspace** 에서 오른쪽 위 **＋ New Federated Task** 를 누른다.
2. **Joined Registry Task** 탭을 고른다.
3. **Approved Registry Task** 에서 `handson-heart · <Owner 핸들>/handson-heart` 를 고른다. 아래에 `Participation status: approved`, `Local Workspace: Not downloaded yet` 이 보인다.
4. **Open Registry Task in Workspace** 를 누른다. Studio 가 게시된 Release 와 모델을 한 번 검증하고 Workspace 를 엽니다(같은 Task 를 다시 열면 기존 Workspace 를 씁니다).

아래 두 방법 가운데 어느 쪽으로 열어도 같습니다. 위는 Workspace 에서 여는 방법입니다.

| 방법 | 순서 |
| --- | --- |
| Registry 에서 | Studio 왼쪽 메뉴 **Registry** → Public Registry → Task 선택 → **Open in Workspace** |
| Workspace 에서 | Studio 왼쪽 메뉴 **Workspace** → 오른쪽 위 **＋ New Federated Task** → **Joined Registry Task** 탭 → 승인된 Task 선택 |

> Owner 는 같은 창의 **My Web Draft** 탭에서 엽니다([Owner 트랙 3장]({{ '/v1.3/tutorial/owner/workspace/' | relative_url }})). Client 는 **Joined Registry Task** 입니다. 탭 이름이 곧 역할의 차이입니다.

{: .highlight }
> **Client 는 코드를 고치지 않습니다.** 받은 코드는 Owner 가 게시한 Release 그대로여야 합니다. 고치면 3장의 점검에서 "게시된 Release 와 다르다"로 막히고, 고쳐서 참여할 수 있더라도 다른 참여자와 파라미터를 합칠 수 없게 됩니다. 코드에 문제가 있으면 Owner 에게 알려 새 Release 를 내게 합니다.

## 2) Python 환경 설치 (Sync)

**① Python Environments 탭**

![Client 의 Python Environments 탭과 Sync environment]({{ '/tutorial/images/hc2-02.png' | relative_url }})

1. **Python Environments** 탭을 누릅니다.
2. 아래로 내려 **Default** 환경의 **Sync environment** 를 누릅니다.

**② 진행 중**

![Sync 진행 중 — 76% Packages prepared]({{ '/tutorial/images/hc2-03.png' | relative_url }})

torch 등 패키지 141개를 받느라 **10분 안팎** 걸립니다(약 12분 20초, 2026-10-20 Windows 노트북 실측). **76% `Packages prepared` 에서 오래 멈춘 것처럼 보이는데**(이번에는 약 11분), 패키지를 설치하는 중이니 기다립니다.

**③ 완료**

![환경이 ready 로 바뀐 Client 화면]({{ '/tutorial/images/hc2-04.png' | relative_url }})

위쪽 환경 표시가 `Default · Python 3.12 · ready` 로 바뀌면 끝입니다. 아래 Default 환경 카드도 `ready` 로, 버튼은 **Sync again** 으로 바뀝니다.

> Owner 가 정한 `requirements.txt` 그대로 설치됩니다. 모든 참여자가 같은 패키지로 학습해야 결과가 같은 의미를 갖습니다.

## 3) 내 데이터 만들기

템플릿에 들어 있는 클리블랜드 병원 원본으로 데이터를 만듭니다. 템플릿을 아직 받지 않았다면 [공통 기초 3장]({{ '/v1.3/tutorial/basics/setup/' | relative_url }})의 5)절대로 먼저 받습니다.

```bash
cd FedOps-hands-on-guide/template/data
pip install numpy pandas
python prepare_data.py
```

출력에 `cleveland/dataset.csv  303행  no_disease=164(54%) disease=139(46%)` 가 보이면 됩니다.

## 4) 내 데이터 두기

![Client 의 Task Test — Open Data Folder 와 Refresh]({{ '/tutorial/images/hc2-05.png' | relative_url }})

1. **Task Test** 탭을 누릅니다. Local data setup 에 `Folder ready` 가 보입니다.
2. **Open Data Folder** 를 누르면 이 Task 전용 데이터 폴더가 열립니다. 여기에 3)에서 만든 `out/cleveland/dataset.csv` 를 **이름 그대로** 넣습니다.
3. 파일을 넣은 뒤 **Refresh** 를 누릅니다.

![Data detected 로 바뀐 Client 화면]({{ '/tutorial/images/hc2-06.png' | relative_url }})

`Folder ready` 가 **`Data detected`** 로 바뀌면 됩니다. 파일 이름은 정확히 `dataset.csv`, 하위 폴더 없이 둡니다. `hungarian` 폴더의 파일을 넣지 않도록 주의하세요. 그건 Owner 의 병원 데이터입니다.

### ⚙️ 해설 — 내 데이터가 갖춰야 할 것

README 의 **Local data setup** 이 기준입니다.

| 조건 | 이 Task | 어기면 |
| --- | --- | --- |
| 파일 이름 | `dataset.csv` 하나 | `Data detected` 가 안 뜬다 |
| 열 이름 | 10개 피처 + `target` — **헤더 이름이 정확히 같아야** 한다 | 3장 점검에서 열이 없다고 실패 |
| 값 | `cp` 는 1~4, `restecg` 는 0~2 만. `target` 은 0 또는 1 | 점검 또는 학습 실패 (어휘표에 없는 값) |
| 클래스 | 클래스마다 최소 3행 | 클래스 부족 오류 |

{: .warning }
> **전처리 통계 스크립트(`tools/embed_preprocessing.py`)를 실행하지 마세요.** README 에 "데이터를 바꿨거나 처음 준비했다면 Task Owner 만 고정 전처리 상태를 갱신한다"는 문장이 있습니다. 이것은 **Owner 가 코드를 만들 때** 하는 일입니다. Client 가 실행하면 코드가 바뀌어 게시된 Release 와 달라집니다. Client 는 Owner 가 헝가리 데이터로 고정한 통계를 그대로 써야 두 병원의 숫자가 같은 기준으로 바뀝니다([Owner 트랙 1장 4절]({{ '/v1.3/tutorial/owner/design/' | relative_url }})).

<details markdown="1">
<summary>📚 연합학습 배경 — 같은 형식, 다른 분포</summary>

연합학습은 모든 참여자의 데이터 **형식**이 같다고 가정합니다(같은 열, 같은 의미, 같은 단위). 하지만 **분포**는 다를 수 있고, 대개 다릅니다. 내 데이터(클리블랜드)는 심장병 46%, Owner 의 헝가리 데이터는 38% 이고, 환자 나이·검사 값의 분포도 다릅니다. 이렇게 형식은 같고 분포가 다른 상황(non-IID)에서 각자의 데이터를 합친 효과를 내는 것이 연합학습의 일입니다.

형식이 다르면(예: 한 병원은 콜레스테롤을 mg/dl, 다른 병원은 mmol/L 로 기록) 점검은 통과하더라도 모델이 엉뚱한 것을 배웁니다. 이런 의미의 차이는 코드가 잡지 못하므로, 실제 협업에서는 데이터 정의서를 맞추는 일이 먼저입니다. UCI Heart Disease 는 1980년대에 네 병원이 같은 항목 정의로 기록을 모았기 때문에 이 문제가 비교적 적습니다.

</details>

## ✅ 체크리스트

- [ ] Studio Workspace 에 참여한 Task 가 열렸다
- [ ] Python Environment 가 `ready` 다
- [ ] `prepare_data.py` 로 `cleveland/dataset.csv` 를 만들었다
- [ ] Task Test 에 `Data detected` 가 보인다
- [ ] 코드는 아무것도 고치지 않았다

## 다음 단계

[3. 참여 준비 점검]({{ '/v1.3/tutorial/client/readiness/' | relative_url }})
