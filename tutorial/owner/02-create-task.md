---
layout: default
title: "2. Task 만들기"
parent: "Task Owner 트랙"
grand_parent: "FedOps 튜토리얼"
nav_order: 2
permalink: /v1.3/tutorial/owner/create-task/
docs_version: "1.3"
lang: ko
---

# 2. Task 만들기
{: .no_toc }

{: .note }
> 📍 **지금 어디:** Task Owner 2/7 — ① 설계 → **② Task 만들기** → ③ Workspace → ④ 학습·게시 → ⑤ 승인 → ⑥ 캠페인 → ⑦ 결과<br> 화면: **FedOps Console** · 다음: Studio 에서 이 Task 의 Workspace 를 연다

{: .important }
> 🎯 **이 단계에서 하는 일:** FedOps 에 "이런 연합학습을 하겠다"는 **빈 껍데기(Web Draft)** 를 만듭니다. 이름, 어떤 종류의 모델인지, 누가 볼 수 있고 누가 참여할 수 있는지를 정합니다. 코드·데이터·모델은 아직 없습니다. 그건 다음 장에서 Studio 로 채웁니다. 이 단계에서는 아직 **아무것도 공개되지 않습니다.**

1. TOC
{:toc}

## 🖱️ 따라 하기

![My Federated Tasks 화면의 Create Federated Task 버튼]({{ '/tutorial/images/ho2-01.png' | relative_url }})

1. FedOps Console 위쪽 메뉴의 **My Federated Tasks** 에서 **Create Federated Task** 를 누른다.

![Task 이름 handson-heart 와 Data modality 입력]({{ '/tutorial/images/ho2-02.png' | relative_url }})

1. **Federated Task name** 에 `handson-heart` 를 입력한다. 아래 **Registry ID** 는 자동으로 채워진다.
2. **Data modality** 를 **Tabular** 로 바꾼다.
3. 나머지는 그대로 두고 **Create** 를 누른다. (각 칸의 의미는 아래 옵션 해설)

![만들어진 handson-heart Task 관리 화면]({{ '/tutorial/images/ho2-03.png' | relative_url }})

제목이 `handson-heart` 인 Task 관리 화면이 나오면 성공입니다. 위쪽 탭들(Registry Release, Participants, Server Management, Monitoring, Global Model)은 이후 장에서 차례로 씁니다.

## ⚙️ 옵션 해설

### 이름과 식별

| 칸 | 무엇을 정하나 | 이 튜토리얼 |
| --- | --- | --- |
| **Creation Mode** | `Federated Task (FedOps 1.3)` 또는 Legacy(FedOps 1.2 방식) | 1.3 — Legacy 는 기존 1.2 Task 를 이어 쓸 때만 |
| **Federated Task name** | 사람이 알아보는 이름. Studio Workspace 이름이 되고, 나중에 Agent 의 Tool id(`local:handson-heart`)가 된다 | `handson-heart` |
| **Registry ID** | Registry 에서 Task 를 구별하는 ID. 공개되면 `@내핸들/registry-id` 형태가 된다 | 이름에서 자동 |
| **Primary Model working name** | 모델의 임시 이름. **Registry 에 보이는 최종 이름은 코드의 `config.yaml` → `model.display_name`** 에서 정해진다 | 비워 둠 — 최종 이름은 템플릿의 `Heart Disease MLP` |

### 모델의 종류

| 칸 | 선택지 | 바꾸면 | 이 튜토리얼 |
| --- | --- | --- | --- |
| **Model role** | `AI · Tool AI` / `LLM · Base LLM` | 완성된 모델을 Agent Builder 가 어느 자리에 제안할지가 달라진다. Tool AI 는 숫자(예측)를 내는 도구, Base LLM 은 문장을 쓰는 언어 모델 자리 | **AI · Tool AI** — 우리 모델은 확률을 내는 분류기 |
| **Task category** | Classification / Regression / Generation / Representation learning / Other | Registry 에 표시되는 분류 정보. 학습 방식 자체는 코드가 정한다 | **Classification** — 심장병 없음/있음 두 클래스 |
| **Data modality** | Undecided / Image / Tabular / Time series / Text / Multimodal | Registry 표시와 검색용 정보 | **Tabular** — 환자 1명당 검사 값 10개짜리 표 |

> Task category 와 Data modality 를 바꿔도 학습 코드는 그대로입니다. Client 가 Registry 에서 "이 Task 가 무엇을 하는지" 판단하는 정보입니다.

### 공개와 참여 — 가장 중요한 두 칸

| 칸 | 선택지 | 무엇이 달라지나 |
| --- | --- | --- |
| **Visibility** | `Private` | 권한 있는 사람만 Task 를 본다. Registry 목록에 나오지 않는다 |
|  | `Public` | Registry 에 나온다. **Task 정보와 등록된 Global Model 다운로드**가 공개된다. 서버 조작·YAML·로그·Owner 기능은 공개되지 않는다 |
| **Participation** | `Owner approval required` | Client 가 참여를 **요청**하고 Owner 가 **승인**해야 참여할 수 있다 |
|  | `Open (automatic approval)` | 요청하면 바로 승인된다 |

**이 튜토리얼의 선택:**

- **Visibility = Private 으로 시작합니다.** 코드와 모델이 준비되기 전에 빈 Task 를 남에게 보일 이유가 없습니다. 4장에서 Registry 에 게시할 때 Public 으로 바뀝니다.
- **Participation = Owner approval required** 입니다. 의료 데이터 연합학습에서는 "누가 우리 모델 학습에 데이터를 보태는지"를 Owner 가 알아야 합니다. 아무나 들어와 이상한 데이터로 학습하면 Global Model 이 망가질 수 있기 때문입니다. 그리고 이 튜토리얼에서 **요청 → 승인** 과정을 직접 경험해 보려는 이유도 있습니다.

<details markdown="1">
<summary>📚 연합학습 배경 — 왜 참여자를 가려 받나</summary>

연합학습 서버는 client 가 보낸 파라미터를 **그대로 믿고** 평균 냅니다. 데이터를 볼 수 없으니 검증이 어렵습니다. 그래서:

- **데이터 품질 문제:** 라벨이 엉망인 데이터로 학습한 client 하나가 Global Model 을 나쁘게 만들 수 있습니다.
- **악의적 참여 (poisoning):** 일부러 모델을 망가뜨리거나 특정 입력에서 오작동하게 만드는 파라미터를 보내는 공격이 연구되어 있습니다.

현실의 의료 연합학습은 대개 참여 병원을 계약으로 미리 정해 둡니다(cross-silo). 이 튜토리얼의 헝가리·클리블랜드 병원도 그런 관계라고 생각하면 됩니다. `Owner approval required` 는 그 관행을 화면으로 옮긴 것입니다. `Open` 은 공개 연구 협업처럼 참여 장벽을 낮추고 싶을 때 씁니다.

</details>

### 설명

| 칸 | 무엇을 정하나 |
| --- | --- |
| **Public summary** | Registry 카드의 한 줄 설명 (280자). Private 이면 권한 있는 사람에게만 보인다 |
| **Federated Task tags** | 검색용 태그 (쉼표로 구분) |

> Client 가 실제로 읽는 자세한 설명은 이 칸이 아니라 코드의 **`README.md`** 입니다. Registry 의 Task 카드에 README 가 그대로 보이고, Client 는 거기서 데이터 형식(열 10개와 `target`)을 확인합니다. 4장에서 확인합니다.

### 여기서 정하지 않는 것

라운드 수, 참여 인원, 집계 방식은 **Task 를 만들 때 정하지 않습니다.** 6장의 캠페인에서 학습을 돌릴 때마다 정합니다. 모델 구조·전처리·학습 설정은 다음 장의 코드(`config.yaml`)에서 정합니다.

## ✅ 체크리스트

- [ ] Console 의 My Federated Tasks 에 `handson-heart` 가 있다
- [ ] Visibility 와 Participation 을 무엇으로 했는지, 왜 그런지 설명할 수 있다

## 다음 단계

[3. Workspace 에 코드와 데이터 넣기]({{ '/v1.3/tutorial/owner/workspace/' | relative_url }}) — 방금 만든 빈 Task 를 Studio 에서 열고, 모든 참여자가 실행할 코드를 채웁니다.
