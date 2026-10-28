---
layout: default
title: "5. 참여자 승인"
parent: "Task Owner 트랙"
grand_parent: "FedOps 튜토리얼"
nav_order: 5
permalink: /v1.3/tutorial/owner/participants/
docs_version: "1.3"
lang: ko
---

# 5. 참여자 승인
{: .no_toc }

{: .note }
> 📍 **지금 어디:** Task Owner 5/7 — ① 설계 → ② Task 만들기 → ③ Workspace → ④ 학습·게시 → **⑤ 승인** → ⑥ 캠페인 → ⑦ 결과<br> 화면: **FedOps Console** · 상대편: Client 가 [Client 트랙 1장]({{ '/v1.3/tutorial/client/join/' | relative_url }})에서 참여를 요청했다 · 다음: 캠페인을 설정하고 서버를 켠다

{: .important }
> 🎯 **이 단계에서 하는 일:** Client(클리블랜드 병원)가 보낸 참여 요청을 보고 **누구를 이 연합학습에 받을지** 정합니다. 승인받은 Client 만 Task 의 코드와 모델을 받아 Workspace 를 열고 학습에 참여할 수 있습니다. 2장에서 Participation 을 `Owner approval required` 로 정했기 때문에 있는 단계입니다(`Open` 이면 요청이 자동 승인되어 이 단계가 없습니다).

1. TOC
{:toc}

## 🖱️ 따라 하기

![Participants 탭 — 승인 전 requested 상태와 Approve 버튼]({{ '/tutorial/images/ho5-01.png' | relative_url }})

1. Console → My Federated Tasks → `handson-heart` 에 들어간다.
2. **Participants** 탭을 누른다. "Review join requests and manage approved access to this task." 라는 안내가 보인다.
3. 요청한 사람의 줄에서 `@핸들`, 상태 `requested`, 요청 시각을 확인한다.
4. **Approve** 를 누른다.

![Participants 탭 — 승인 후 approved 로 바뀐 참여자]({{ '/tutorial/images/ho5-02.png' | relative_url }})

1. 상태가 **`approved`** 로 바뀌었는지 확인한다. 오른쪽의 **Revoke** 는 승인을 거둘 때만 누릅니다. `0 completed FL runs` 는 아직 이 Task 의 연합학습을 한 번도 끝내지 않았다는 뜻입니다.

이제 Client 쪽에서 Workspace 를 열 수 있습니다([Client 트랙 2장]({{ '/v1.3/tutorial/client/workspace/' | relative_url }})). Client 가 데이터를 두고 참여 준비 점검을 하는 동안 Owner 는 6장의 서버 준비로 넘어가면 됩니다.

## ⚙️ 옵션 해설 — 참여자 상태와 버튼

| 상태 | 뜻 | 쓸 수 있는 버튼 |
| --- | --- | --- |
| `requested` | 요청이 들어와 Owner 의 결정을 기다림 | **Approve** / **Reject** |
| `approved` | 참여 가능. 코드·모델을 받아 Workspace 를 열 수 있다 | **Revoke** (승인 취소) |
| `rejected` | 거절됨 | — |

| 버튼 | 누르면 |
| --- | --- |
| **Approve** | Client 가 참여 전용 파일·버전을 받고 Workspace 로 가져올 수 있게 된다 |
| **Reject** | 요청을 거절한다 |
| **Revoke** | 이미 승인한 참여 권한을 거둔다 |

각 줄에는 그 참여자가 **완료한 연합학습 횟수**(`N completed FL runs`)와 마지막 참여 시각도 나옵니다. 누가 실제로 학습에 기여했는지 볼 수 있습니다.

**이 튜토리얼의 판단 기준:** 요청한 계정이 함께 실습하기로 한 사람(클리블랜드 병원 역할)인지 핸들로 확인하고 승인합니다. 실제 의료 연합학습이라면 계약·IRB 등으로 미리 정해진 기관인지 확인하는 단계에 해당합니다.

<details markdown="1">
<summary>📚 연합학습 배경 — 몇 명을 받아야 하나</summary>

- **승인 인원 ≥ 라운드당 인원.** 6장에서 정할 Clients per round 는 "한 라운드에 몇 명이 학습을 마쳐야 합치는가"입니다. 승인한 사람보다 크게 잡으면 서버는 영원히 기다립니다.
- **많을수록 좋지만 느려진다.** 참여자가 늘면 Global Model 이 보는 데이터가 다양해지지만, 가장 느린 참여자를 기다려야 해서 라운드가 길어집니다.
- **데이터가 비슷한 곳만 받으면** non-IID 의 어려움은 줄지만, 연합학습으로 얻을 다양성도 줄어듭니다. 반대로 너무 다른 곳을 받으면 오히려 나빠질 수 있습니다. 예를 들어 이 데이터의 VA 병원(심장병 78%)을 세 번째로 넣으면, 시뮬레이션에서 Owner 기준 성능이 떨어지는 경우가 더 많았습니다. 이 튜토리얼은 Owner(헝가리, 심장병 38%)와 Client(클리블랜드, 46%) 두 곳이 참여합니다. 승인할 사람은 **Client 1명**입니다.

</details>

## ✅ 체크리스트

- [ ] Participants 에서 Client 의 요청을 봤다
- [ ] Approve 후 상태가 `approved` 다
- [ ] 승인한 인원 수를 안다 (6장 Clients per round 에 씀)

## 혼자 연습한다면

승인할 사람이 없습니다. Owner 는 자기 Task 에 이미 참여할 수 있습니다(화면에 `Owner · Participant` 배지). 그대로 6장으로 넘어가세요.

## 다음 단계

[6. 캠페인 설정과 서버 시작]({{ '/v1.3/tutorial/owner/campaign/' | relative_url }})
