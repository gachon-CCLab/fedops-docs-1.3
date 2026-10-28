---
layout: default
title: "1. Task 찾기와 참여 요청"
parent: "Client 트랙"
grand_parent: "FedOps 튜토리얼"
nav_order: 1
permalink: /v1.3/tutorial/client/join/
docs_version: "1.3"
lang: ko
---

# 1. Task 찾기와 참여 요청
{: .no_toc }

{: .note }
> 📍 **지금 어디:** Client 1/5 — **① 찾기·요청** → ② Workspace·데이터 → ③ 준비 점검 → ④ 참여 → ⑤ 마무리<br> 화면: **Registry** (Console 또는 Studio) · 상대편: Owner 가 [Owner 트랙 5장]({{ '/v1.3/tutorial/owner/participants/' | relative_url }})에서 이 요청을 승인한다

{: .important }
> 🎯 **이 단계에서 하는 일:** Registry 에서 참여할 Task 를 찾고, **README 로 이 Task 가 무엇을 하고 어떤 데이터를 요구하는지** 확인한 뒤 참여를 요청합니다. 데이터를 맞출 수 없는 Task 에 참여하면 3장의 점검에서 막힙니다. 그래서 요청 전에 README 를 읽는 것이 Client 의 첫 번째 일입니다.

1. TOC
{:toc}

## 1) Task 찾기

![Client 계정으로 본 Studio Registry 의 Heart Disease MLP 카드]({{ '/tutorial/images/hc1-01.png' | relative_url }})

1. Agent Studio 왼쪽 메뉴의 **Registry** 를 누른다.
2. **Public Registry** 를 고른다.
3. **Heart Disease MLP** 카드를 누른다. 카드 제목은 Task 이름(`handson-heart`)이 아니라 **모델 이름**입니다. 카드 아래에 `<Owner 핸들> / handson-heart` 처럼 Owner 와 Task 이름이 함께 보입니다.

카드를 누르면 오른쪽에 Task 정보가 열립니다. `Participation` 이 `approval_required` 이면 Owner 승인이 필요한 Task 입니다. FedOps Console(웹)의 위쪽 메뉴 **Registry** 에서도 같은 카드를 볼 수 있습니다.

## 2) README 읽기 — 참여 조건 확인

![Task Card 의 README — Local data setup]({{ '/tutorial/images/hc1-02.png' | relative_url }})

오른쪽 Task 정보를 아래로 내리면 **Task Card** 에 Owner 가 쓴 README 가 보입니다. 참여 전에 다음을 확인합니다.

| README 에서 볼 것 | 이 Task 의 경우 | 왜 |
| --- | --- | --- |
| **Intended use** (용도) | 심장병 없음/있음 분류, 교육용 | 내 데이터를 어디에 보태는지 알아야 한다 |
| **Local data setup** (데이터 형식) | CSV 1개 `dataset.csv`, 열 10개(`age` … `oldpeak`, `cp`·`restecg` 는 정해진 값만) + `target`(0/1) | 내 데이터가 이 형식이어야 참여할 수 있다 |
| **Federated participation** | 참여 절차, 클래스마다 최소 3행 | 내 데이터가 조건을 채우는지 본다 |
| **Limitations** | 진단에 쓰지 않음, 정확도 0.75~0.8 안팎 |  |
| **Privacy** | 데이터는 PC 밖으로 나가지 않음 | 무엇이 공유되는지 확인 |

> 이 튜토리얼의 클리블랜드 데이터는 같은 UCI 원본에서 나왔으므로 형식이 맞습니다. 실제 상황이라면 이 단계에서 **내 병원의 기록이 이 열 이름·값과 맞는지**를 따져 봅니다.

## 3) 참여 요청

둘 중 **한 곳에서만** 하면 됩니다. 결과는 같습니다.

| 어디서 | 방법 |
| --- | --- |
| FedOps Console (웹) | Registry → Task 카드 → **Federated Learning** 참여 버튼 |
| Agent Studio | 왼쪽 메뉴 **Registry** → Public Registry → Task 선택 → **Request to join** |

Agent Studio 에서 요청하는 화면입니다.

![Studio 의 Request to join 버튼]({{ '/tutorial/images/hc1-03.png' | relative_url }})

1. 오른쪽 위 **Request to join** 을 누른다.

![요청 후 Approval pending 상태]({{ '/tutorial/images/hc1-04.png' | relative_url }})

버튼 자리가 `Approval pending` 과 **Withdraw request**(요청 취소)로 바뀌고, `Participation status: pending-approval` 이 나옵니다. 왼쪽 카드에도 `requested` 가 붙습니다. Owner 가 승인할 때까지 이 **대기 상태**로 있고, 그동안에는 Workspace 로 가져오기를 쓸 수 없습니다.

![승인 뒤 바뀐 화면]({{ '/tutorial/images/hc1-05.png' | relative_url }})

Owner 가 승인하면 카드가 `approved` 로 바뀌고, 버튼이 **Leave Task** · **Federated Learning** · **Open in Workspace** 로 바뀝니다. 아래 Overview 에도 `Participation status: approved`, `Completed FL runs: 0` 이 보입니다. 화면 위 "Complete at least one Federated Learning run after approval before leaving this task." 는 이 Task 가 **한 번 이상 참여를 완료한 뒤에만 탈퇴(Leave)** 할 수 있다는 뜻입니다.

Owner 에게 요청을 보냈다고 알리고, 승인되면 2장으로 넘어갑니다.

## ⚙️ 해설 — 참여 방식은 Owner 가 정했다

| Task 의 Participation 설정 | 내가 겪는 일 |
| --- | --- |
| `Owner approval required` (이 튜토리얼) | 요청 → **Owner 승인을 기다림** → 참여 가능 |
| `Open (automatic approval)` | 요청하면 바로 참여 가능 |

<details markdown="1">
<summary>📚 연합학습 배경 — 참여하면 무엇이 공유되나</summary>

| 공유된다 | 공유되지 않는다 |
| --- | --- |
| 내 PC 에서 학습한 **모델 파라미터** (라운드마다) | 내 데이터 파일, 환자 기록 하나하나 |
| 내 데이터의 **행 수** (FedAvg 가중치로 쓰임) | 데이터가 있는 경로, PC 정보 |
| 내가 허용한 **평가 지표** (정확도 등) |  |
| 내 계정 핸들, 참여 기록 |  |

파라미터만 보내도 이론적으로는 학습 데이터의 일부 특성을 추정하는 공격이 가능하다고 알려져 있습니다. 민감한 실제 데이터로 참여할 때는 기관의 보안 정책을 먼저 확인하세요.

</details>

## ✅ 체크리스트

- [ ] Registry 에서 Task 를 찾았다
- [ ] README 의 데이터 형식이 내 데이터와 맞는지 확인했다
- [ ] 참여를 요청했고, Owner 의 승인을 받았다

## 다음 단계

[2. Workspace 와 내 데이터 준비]({{ '/v1.3/tutorial/client/workspace/' | relative_url }})
