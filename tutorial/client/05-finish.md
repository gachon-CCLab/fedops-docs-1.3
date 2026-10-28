---
layout: default
title: "5. 결과 확인과 마무리"
parent: "Client 트랙"
grand_parent: "FedOps 튜토리얼"
nav_order: 5
permalink: /v1.3/tutorial/client/finish/
docs_version: "1.3"
lang: ko
---

# 5. 결과 확인과 마무리
{: .no_toc }

{: .note }
> 📍 **지금 어디:** Client 5/5 — ① 찾기·요청 → ② Workspace·데이터 → ③ 준비 점검 → ④ 참여 → **⑤ 마무리**<br> 화면: **Agent Studio** · 상대편: Owner 는 [전체 결과]({{ '/v1.3/tutorial/owner/results/' | relative_url }})를 본다

{: .important }
> 🎯 **이 단계에서 하는 일:** 내 쪽에서 본 지표를 읽고, 참여 세션을 끝냅니다. Client 는 **자기 상태만** 보고, 모든 참여자를 합친 전체 지표는 Owner 가 봅니다. 그리고 세션 종료·참여 중단·탈퇴가 각각 무엇인지 구분합니다.

1. TOC
{:toc}

## 1) 내 지표 보기

![Client 의 Scores — Accuracy, F1 No Disease, F1 Disease]({{ '/tutorial/images/hc5-01.png' | relative_url }})

연합학습 화면을 아래로 내리면 **Scores** 에 이 Client 가 본 지표가 있습니다. Owner(헝가리)와 함께 2라운드를 돌린 Global Model 을 **내 클리블랜드 test 데이터**로 매긴 값입니다: Accuracy 75.41%, F1 Disease 71.70%, F1 No Disease 78.26% (예시, 2026-10-20, 클리블랜드 303행). 학습에는 무작위 요소가 있어 같은 데이터로도 숫자가 조금 다를 수 있습니다.

| 읽을 것 | 뜻 |
| --- | --- |
| Accuracy | 내 test 데이터에서 Global Model 이 맞힌 비율. 클리블랜드는 심장병 없음이 54% 라, 0.54 보다 확실히 커야 의미가 있다 |
| F1 Disease | 심장병 환자를 얼마나 잘 잡는지. 이 데이터에서 가장 중요한 지표 |
| F1 No Disease | 심장병 없는 환자를 얼마나 잘 가려내는지 |

> 이 점수는 **내 데이터로 매긴 점수**입니다. 헝가리 병원의 데이터로 매기면 다르게 나옵니다.

## 2) 세션 끝내기

![세션이 자동으로 끝난 화면 — Client session ended]({{ '/tutorial/images/hc5-02.png' | relative_url }})

캠페인이 끝난 직후에는 위쪽에 `completed` 와 **Finish Client Session** 버튼이 보이다가, 서버가 내려가면 세션이 **자동으로** 끝납니다(2026-10-20 Windows 노트북 실측: 완료 뒤 30초 안팎, Finish 는 누르지 않음). 자동으로 끝나면 위쪽에 `✓ Client session ended` 와 "The Client session has ended. The final Global Model and training history are preserved." 가 나오고, **Finish Client Session 버튼은 사라집니다.** 이 화면이면 따로 누를 것이 없습니다. 이전 실습의 Mac(Owner)에서는 캠페인이 끝난 뒤에도 `completed` 와 함께 **Finish Client Session** 버튼이 남아 있었습니다. 두 화면이 왜 다른지(Studio 버전 또는 역할 차이)는 확인하지 못했습니다.

1. **Finish Client Session** 버튼이 보이는 버전이라면 **한 번만** 누른다. 눌러도 화면이 그대로지만 세션은 끝난 것입니다. 다시 누르면 오류(500)가 납니다.

## ⚙️ 해설 — 끝내는 세 가지 방법

| 동작 | 언제 | 결과 |
| --- | --- | --- |
| **Finish Client Session** | 캠페인이 **완료된 뒤** | 이번 세션을 정리한다. 참여 기록은 남는다 (Studio 를 다시 켜도 보임). 버전에 따라 자동으로 끝나 버튼이 없을 수 있다 |
| **Stop Client** | 학습 **도중** 빠질 때 | 내 PC 의 참여만 멈춘다. 캠페인은 계속되고 서버는 다른 참여자를 기다린다 |
| **Leave** (탈퇴) | 이 Task 에 더 참여하지 않을 때 | 참여 자격을 내려놓는다. 다시 참여하려면 [1장]({{ '/v1.3/tutorial/client/join/' | relative_url }})부터 다시 요청한다. 최소 한 번의 완료된 참여를 요구하는 Task 는 그 조건을 채운 뒤 탈퇴할 수 있다 |

**이 튜토리얼에서는 세션 종료(자동 또는 Finish Client Session)까지만** 합니다. Owner 가 다음 캠페인을 열면 같은 Workspace 로 다시 참여할 수 있습니다(3장 점검부터).

<details markdown="1">
<summary>📚 연합학습 배경 — Client 가 얻는 것</summary>

Client 는 자기 데이터를 내주지 않고도 **다른 병원의 데이터로 학습된 효과**를 얻습니다. 다만 Global Model 은 모든 참여자에게 평균적으로 좋은 모델이지, 내 병원에 가장 좋은 모델이라는 보장은 없습니다. 내 데이터가 다른 병원과 크게 다르면 Global Model 이 내 test 에서는 혼자 학습한 모델보다 나쁠 수도 있습니다. 이 차이를 줄이는 연구 분야가 개인화 연합학습(personalized FL)입니다.

Task 가 Public 이면 등록된 Global Model 은 Registry 에서 내려받을 수 있습니다. Client 계정으로 Global Model 을 Agent 의 Tool AI 로 쓸 수 있는지는 아직 확인하지 못했습니다([모델 활용 트랙]({{ '/v1.3/tutorial/model-use/' | relative_url }})은 Owner 계정 기준입니다).

</details>

## ✅ 체크리스트

- [ ] Scores 에서 내 Accuracy 와 F1 Disease 를 봤다
- [ ] `✓ Client session ended` 를 확인했다 (버튼이 있으면 Finish Client Session 을 한 번 눌렀다)
- [ ] Finish / Stop / Leave 의 차이를 말할 수 있다

## 다 끝냈다면

- Owner 쪽에서 무슨 일이 있었는지 → [Task Owner 트랙]({{ '/v1.3/tutorial/owner/' | relative_url }})
- 이 모델을 서비스에 붙이는 법 → [모델 활용 트랙]({{ '/v1.3/tutorial/model-use/' | relative_url }})
