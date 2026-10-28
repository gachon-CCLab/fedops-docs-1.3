---
layout: default
title: "3. 참여 준비 점검"
parent: "Client 트랙"
grand_parent: "FedOps 튜토리얼"
nav_order: 3
permalink: /v1.3/tutorial/client/readiness/
docs_version: "1.3"
lang: ko
---

# 3. 참여 준비 점검
{: .no_toc }

{: .note }
> 📍 **지금 어디:** Client 3/5 — ① 찾기·요청 → ② Workspace·데이터 → **③ 준비 점검** → ④ 참여 → ⑤ 마무리<br> 화면: **Agent Studio** · 상대편: Owner 는 이 동안 [캠페인을 준비]({{ '/v1.3/tutorial/owner/campaign/' | relative_url }})한다

{: .important }
> 🎯 **이 단계에서 하는 일:** 서버에 붙기 전에 **내 PC 에서 미리 다 돌려 봅니다.** 받은 코드가 게시된 Release 그대로인지, 내 데이터가 형식에 맞는지, 내 모델이 다른 참여자의 모델과 같은 모양인지를 검사합니다. 서버가 아직 꺼져 있어도 할 수 있습니다. 라운드가 시작된 뒤 내 PC 에서 문제가 나면 다른 참여자 모두가 기다리게 되므로, 점검은 미리 끝내 둡니다.

1. TOC
{:toc}

## 🖱️ 따라 하기

![Client 의 Federated Learning 메뉴와 Heart Disease MLP 카드]({{ '/tutorial/images/hc3-01.png' | relative_url }})

1. 왼쪽 메뉴의 **Federated Learning** 을 누른다.
2. **Heart Disease MLP** 카드를 누른다. 점검 전에는 카드에 `not_configured`, `Needs Attention` 이 보입니다.

![Client 의 Check Participation Readiness 버튼]({{ '/tutorial/images/hc3-02.png' | relative_url }})

1. Task Data 줄의 **Check Participation Readiness** 를 누른다. 내 로컬 데이터로 모델을 학습·평가해 보며 검사합니다. 생각보다 오래 걸립니다(약 5분 40초, 2026-10-20 Windows 노트북 실측). `Evaluating local model 92%` 에서 오래 머물러도 기다립니다.

![Local Ready 와 Readiness details 9 / 9]({{ '/tutorial/images/hc3-03.png' | relative_url }})

`○ Check required` 가 **`✓ Local Ready`** 로, 아래에 **`Readiness details · 9 / 9`** 가 나오면 통과입니다. **Start Client 는 아직 누르지 않습니다.** Owner 가 서버를 켜야 합니다(4장).

## ⚙️ 해설 — 화면의 배지와 점검 항목

| 배지 | 뜻 |
| --- | --- |
| `○ Check required` → `✓ Local Ready` | 내 PC 쪽 준비(코드·환경·데이터)가 끝났는지 |
| `● Server Live` / `Server Offline` | Owner 의 집계 서버가 켜져 있는지. **Local Ready 와 별개**다 |

**Readiness details** 를 펼치면 항목별 결과가 나옵니다. 9개 항목은 다음과 같습니다.

| 항목 | 확인하는 것 | 실패하면 |
| --- | --- | --- |
| Federated Task linked | 이 Workspace 가 Registry 의 Federated Task 와 연결되어 있는지 | 2장 1) 에서 Joined Registry Task 로 다시 연다 |
| Participant Runtime compatible | 내 Studio 의 참여자 실행 환경이 이 Task 와 맞는지 | Agent Studio 를 최신 버전으로 올린다 |
| Published Release installed | 내 코드가 Owner 가 게시한 Release 그대로인지 | 코드를 고쳤다면 되돌린다 |
| Federated parameter contract | 내 모델의 파라미터 이름·모양이 Release 의 서명과 같은지 | Owner 에게 알린다 (Release 문제) |
| Local dataset accessible | Data Folder 에 `dataset.csv` 가 있고 읽히는지 | 2장 4) 의 파일 이름·위치를 확인한다 |
| Participation Readiness | 지금의 코드와 **지금의 데이터**로 점검이 끝났는지 | 데이터를 바꿨으면 다시 점검한다 |
| Python environment ready | 2장의 Sync 가 끝났는지 | 2장 2) 다시 |
| Global Model available | 서버에서 받을 Global Model 이 있는지 | Owner 에게 알린다 (캠페인 준비 확인) |
| Participation authorized | 이 계정의 참여가 승인되어 있는지 | 1장의 참여 요청과 Owner 승인을 확인한다 |

**데이터를 바꾸면 점검을 다시 해야 합니다.** 점검 결과는 그때의 코드와 데이터에 묶여 있어서, 파일을 바꾸면 `Task Data or Workspace source changed` 로 돌아갑니다.

{: .warning }
> **Owner 가 캠페인을 바꾸거나 서버를 켜도 점검이 풀립니다.** 새 캠페인 서버가 켜지면 Owner·Client 모두 `○ Check required` 로 돌아가고, 그 상태에서는 **Start Client 가 눌리지 않습니다.** 가능하면 Owner 가 캠페인 설정을 마친 뒤에 점검하고, 4장에서 Start Client 전에 `✓ Local Ready` 를 다시 확인합니다.

<details markdown="1">
<summary>📚 연합학습 배경 — 왜 서버와 따로 점검하나</summary>

연합학습 라운드는 **가장 늦은 참여자**를 기다립니다. 한 Client 가 라운드 중간에 "열 이름이 틀렸다"로 실패하면, 서버는 정해진 인원이 모일 때까지 계속 기다리거나 그 라운드를 버려야 합니다. 그래서 FedOps 는 "내 쪽 준비(Local)"와 "서버 상태(Server)"를 나눠, 각자 자기 PC 에서 미리 끝낼 수 있는 것은 모두 끝내 두게 합니다.

파라미터 서명 비교는 [공통 기초 2장]({{ '/v1.3/tutorial/basics/data-and-model/' | relative_url }})의 "모델 구조가 왜 고정되어야 하나"와 같은 이야기입니다. 모양이 하나라도 다르면 FedAvg 로 합칠 수 없습니다.

</details>

## ✅ 체크리스트

- [ ] `✓ Local Ready` 와 `Readiness details · 9 / 9` 를 봤다
- [ ] Owner 에게 "준비됐다"고 알렸다

## 안 되면

| 증상 | 조치 |
| --- | --- |
| Participation Readiness 실패 | 대개 Data Folder 에 `dataset.csv` 가 없거나 열 이름이 다르다. Readiness details 에서 실패한 항목을 본다 |
| 어휘표에 없는 값 (`cp`·`restecg`) | `dataset.csv` 를 손으로 고쳤거나 다른 데이터를 넣었다. `prepare_data.py` 로 다시 만든다 |
| 카드가 안 보임 | 참여 승인을 받았는지, 2장에서 Workspace 를 열었는지 확인 |

## 다음 단계

[4. 연합학습 참여]({{ '/v1.3/tutorial/client/federated-learning/' | relative_url }}) — Owner 가 서버를 켜면 시작합니다.
