---
layout: default
title: "1. AI Agent 만들기"
parent: "모델 활용 트랙"
grand_parent: "FedOps 튜토리얼"
nav_order: 1
permalink: /v1.3/tutorial/model-use/agent/
docs_version: "1.3"
lang: ko
---

# 1. AI Agent 만들기
{: .no_toc }

{: .note }
> 📍 **지금 어디:** 모델 활용 1/3 — **① Agent** → ② Serving API → ③ 앱<br> 화면: **Agent Studio** (Agent Builder) · 다음: 빌드한 Agent 를 API 로 연다

{: .important }
> 🎯 **이 단계에서 하는 일:** 연합학습으로 만든 모델을 **Tool AI** 로, 문장을 쓸 **Base LLM** 과 묶고, LLM 이 지켜야 할 규칙(**Harness**)을 붙여 Agent 를 빌드합니다. 사용자는 "이 환자 기록의 판정 결과를 설명해줘"라고 묻고, Agent 는 모델이 낸 숫자를 근거로 답합니다.

{: .note }
> 그림의 **빨간 네모 + 번호**가 누를 곳이고, 아래 설명의 번호와 같습니다. Agent Builder 는 화면이 넓어 1440px 폭으로 찍습니다.

1. TOC
{:toc}

## 1) Agent 초안 만들기

![Agent Builder 메뉴와 New Agent 버튼]({{ '/tutorial/images/hm1-01.png' | relative_url }})

1. 왼쪽 메뉴의 **Agent Builder** 를 누른다.
2. **+ New Agent** 를 누른다.

![Agent Name 입력과 Create Agent]({{ '/tutorial/images/hm1-02.png' | relative_url }})

1. Agent Name 에 `handson-heart-agent` 를 입력한다.
2. **Create Agent** 를 누른다.

같은 이름의 초안이 이미 있으면 `An Agent draft with this name already exists.` 가 나옵니다. 아래 "안 되면" 표를 보세요.

## 2) Tool AI 고르기 (Models 탭)

**Tool AI 를 먼저, Base LLM 을 나중에** 고르는 순서가 편합니다. Tool AI 를 고를 때 화면을 새로고침해야 하는 경우가 있는데, 그러면 저장 안 한 Base LLM 선택이 사라지기 때문입니다.

![WORKSPACE · TOOL AI 의 Heart Disease MLP]({{ '/tutorial/images/hm1-03.png' | relative_url }})

1. 가운데 WORKSPACE · TOOL AI 목록에서 **Heart Disease MLP** 를 누른다.

![Model version 선택과 Prepare model version]({{ '/tutorial/images/hm1-04.png' | relative_url }})

연합학습을 했다면 Global Model v1 을 씁니다. 처음에는 `Download required` 로 보입니다.

1. 오른쪽 아래 **Model version** 에서 `Global Model v1 · Download required` 를 고른다.
2. **Prepare model version** 을 누른다.

![changed after selection 메시지]({{ '/tutorial/images/hm1-05.png' | relative_url }})

**`handson-heart changed after selection. Select it again and rebuild the Agent.`** 가 나옵니다(2026-10-20 에도 그대로). 고장이 아닙니다. 모델은 이미 받아졌습니다. 브라우저를 **새로고침**한 뒤 Agent Builder → `handson-heart-agent` 초안 → Heart Disease MLP 를 다시 누르면 됩니다.

![Global Model v1 Ready 와 Add as Tool AI]({{ '/tutorial/images/hm1-06.png' | relative_url }})

1. 새로고침 뒤에는 **`Global Model v1 · Ready`** 로 바뀌어 있다. 이걸 고른다.
2. **Add as Tool AI** 를 누른다.

> 연합학습을 건너뛰었다면 `Initiative Model · Ready` 를 그대로 두고 Add as Tool AI 를 누릅니다.

### ⚙️ 해설 — 어떤 모델 버전을 Tool 로 쓰나

| 버전 | 무엇 | 언제 |
| --- | --- | --- |
| `Initiative Model` | Owner 가 헝가리 데이터로 혼자 만든 첫 모델 (Owner 트랙 4장) | 연합학습을 건너뛰었을 때 |
| `Global Model v1, v2, …` | 연합학습 결과 | **이 튜토리얼의 선택** — 두 병원의 데이터가 반영된 모델 |

`Download required` 는 그 버전이 아직 내 PC 에 없다는 뜻이고, **Prepare model version** 이 서버에서 받아옵니다. Agent 를 빌드하면 그 순간의 버전이 고정되므로, 나중에 v2 가 생겨도 다시 고르고 다시 빌드하기 전까지 Agent 는 v1 을 씁니다.

## 3) Base LLM 고르기

![Hugging Face LLM 과 Use as Base LLM]({{ '/tutorial/images/hm1-07.png' | relative_url }})

왼쪽 TOOL AI 칸에 **Heart Disease MLP** 가 들어갔습니다.

1. 오른쪽 BASE LLM SOURCE 에서 **Hugging Face LLM** 을 누른다.
2. 아래 값(`bartowski/Qwen_Qwen3.5-4B-GGUF`, `main`, `GGUF · llama.cpp`, `Qwen_Qwen3.5-4B-Q4_K_M.gguf`)은 기본값 그대로 두고 **Use as Base LLM** 을 누른다.

![Base LLM 과 Tool AI 가 들어간 화면과 Save]({{ '/tutorial/images/hm1-08.png' | relative_url }})

왼쪽에 Base LLM 과 Tool AI 가 하나씩 들어갔습니다.

1. 위쪽 **Save** 를 누른다. `Agent draft saved.` 가 나옵니다.

{: .highlight }
> **Save 를 꼭 누르세요.** 저장하지 않고 새로고침하면 Base LLM 선택이 사라집니다.

### ⚙️ 해설 — Base LLM 칸

| 칸 | 기본값 | 뜻 |
| --- | --- | --- |
| Repository | `bartowski/Qwen_Qwen3.5-4B-GGUF` | Hugging Face 의 모델 저장소. 40억(4B) 파라미터의 작은 LLM |
| Revision | `main` | 저장소의 버전 |
| Format | `GGUF · llama.cpp` | CPU 에서 돌리기 좋은 압축 형식과 실행기 |
| File | `Qwen_Qwen3.5-4B-Q4_K_M.gguf` | 4비트로 줄인 파일 (약 2.8 GB) |

**왜 작은 LLM 인가:** Studio 는 노트북 CPU 에서 돕니다. 큰 LLM 은 답 하나에 몇십 분이 걸리거나 메모리가 모자랍니다. 이 Agent 에서 LLM 은 판단하지 않고 Tool 이 준 숫자를 설명만 하므로 작은 모델로도 충분합니다. 대신 규칙을 가끔 어깁니다(아래 5절).

## 4) Agent Harness (규칙)

![Agent Harness 탭 설정]({{ '/tutorial/images/hm1-09.png' | relative_url }})

1. **Agent Harness** 탭을 누른다.
2. Instructions 칸의 기본 문장을 지우고 템플릿의 `template/agent/harness-instructions.txt` 내용을 붙여 넣는다.
3. **Tool routing** 을 `explicit` 으로 바꾼다.
4. **Memory** 를 `none` 으로 바꾼다.
5. **Save** 를 누른다.

Temperature `0.2`, Max output tokens `512` 는 기본값 그대로 둡니다.

Harness 의 핵심 규칙: **Tool 이 준 숫자를 그대로 인용하고 새로 만들지 않는다. 퍼센트(%)로 바꾸지 않는다.** 두 클래스의 확률을 `no_disease 0.316 / disease 0.684` 형식으로 한 줄에 쓴다. 어떤 항목이 영향을 줬는지는 말하지 않는다(Tool 이 그 정보를 주지 않으므로 추측이 됨). 의료 데이터라 **"진단 근거가 아니다"를 마지막 줄에 밝히고, 치료·검사 조언은 하지 않는다.**

### ⚙️ 옵션 해설 — Harness

| 옵션 | 선택지 | 무엇을 정하나 | 이 튜토리얼 |
| --- | --- | --- | --- |
| **Instructions** | 자유 문장 | LLM 이 따를 규칙. 답의 형식, 하지 말 것 | 템플릿의 `harness-instructions.txt` |
| **Temperature** | 0 이상 숫자 | 답의 무작위성. 높으면 표현이 다양해지고 낮으면 일정해진다 | **0.2** — 숫자를 정확히 옮겨야 해서 낮게 |
| **Max output tokens** | 숫자 | 답의 최대 길이 | 512 — 몇 문장이면 충분 |
| **Context window** | 숫자 | LLM 이 한 번에 읽을 수 있는 길이 (규칙 + 질문 + Tool 결과) | 32768 (기본) |
| **Tool routing** | `automatic` / `explicit` | Tool 을 언제 부를지에 대한 설정. **현재 Studio 에서는 동작에 쓰이지 않는다.** 실제로는 요청에 입력값이 있을 때만 Tool 이 실행되고, Tool 이 하나면 그 Tool 을 쓴다 | `explicit` (의도 기록용) |
| **Memory** | `session` / `none` | 이전 대화를 기억할지에 대한 설정. **현재 동작에 쓰이지 않는다.** 대화를 기억하는지는 부르는 쪽이 보내는 대화 기록(`history`, 최근 40개)이 정한다 | `none` (의도 기록용) |
| **Safety** | `standard` / `strict` | 안전 정책 수준. **현재 동작에 쓰이지 않는다** | `standard` (기본) |

{: .highlight }
> **확인 결과 (2026-10-13).** 실행 중인 Studio(2026-09-09 이미지)의 코드를 따라가 보니, LLM 호출에 쓰이는 것은 Instructions, Temperature, Max output tokens, Context window 뿐입니다. **Tool routing, Memory, Safety 는 저장되고 화면에 표시되지만 동작을 바꾸지 않습니다.** (Base LLM 으로 Federated Task 의 LLM 을 고른 경우에만 이 값들이 그 Task 코드에 그대로 전달됩니다.)
>
> 실측: Memory 를 `none` 으로 둔 Agent 에 이전 대화(`history`)를 함께 보내자 앞 대화에서 알려 준 단어를 그대로 답했고, 대화 기록 없이 보내면 기억하지 못했습니다. 즉 **대화를 기억하는지는 앱이 history 를 보내는지로 정해집니다.** Tool 은 요청에 입력값(`input`)이 있을 때만 실행됩니다(3장 "Tool 없이 보내기"). 그래서 이 튜토리얼은 세 값을 "의도를 기록해 두는 설정"으로 다룹니다.

<details markdown="1">
<summary>📚 배경 — 왜 LLM 이 숫자를 만들면 안 되나</summary>

LLM 은 그럴듯한 문장을 만드는 모델이라, 근거 없이도 "심장병 확률 87%" 같은 숫자를 지어낼 수 있습니다(환각, hallucination). 의료처럼 숫자가 중요한 곳에서는 위험합니다. 그래서 이 Agent 는 역할을 나눕니다.

- **판단(숫자)** 은 데이터로 학습되고 검증된 Tool AI 가 한다 — 연합학습으로 두 병원 데이터를 본 모델
- **설명(문장)** 만 LLM 이 한다 — Harness 로 "숫자를 그대로 인용하고 만들지 말 것"을 강제

연합학습으로 만든 모델의 가치가 Agent 안에서 그대로 살아 있게 하는 구조입니다.

</details>

## 5) 테스트 (Test & Build 탭)

![Test & Build 탭과 Prepare Base LLM]({{ '/tutorial/images/hm1-10.png' | relative_url }})

1. **Test & Build** 탭을 누른다.
2. **Prepare Base LLM** 을 누른다. LLM(약 2.8 GB)을 받습니다. 처음이면 수십 분 걸릴 수 있습니다. 이미 받아 둔 파일이 있으면 몇 초면 끝납니다.

![LLM ready 와 Load sample for Agent]({{ '/tutorial/images/hm1-11.png' | relative_url }})

진행 막대가 `ready · 100.0%`, `2.81 GiB / 2.81 GiB` 가 되면 됩니다.

1. **Sample index** 는 `0` 그대로 둔다. (Owner 의 헝가리 데이터의 0번째 행)
2. **Load sample for Agent** 를 누른다.

![Message 와 Generate Response]({{ '/tutorial/images/hm1-12.png' | relative_url }})

**`● Tool input ready`** 와 `{"index":0,"rows":261,"label":0,"class_name":"no_disease"}` 가 보이면 샘플이 들어간 것입니다(실제 라벨은 심장병 없음). 입력은 나이·혈압·가슴 통증 유형 등 10개 값입니다. 가운데 `Sample {index} is loaded` 처럼 중괄호가 그대로 보이는 것은 Studio 화면 문구 문제라 무시합니다.

1. **Message** 칸의 기본 문구(영어, 이미지용)를 지우고 `이 환자 기록의 판정 결과를 설명해줘` 를 입력한다.
2. **Generate Response** 를 누른다. 2026-10-20 실측 **약 2분 20초**(Tool 9초).

![Agent 답변과 Latest execution trace]({{ '/tutorial/images/hm1-13.png' | relative_url }})

Agent 의 답이 나옵니다.

1. **Latest execution trace** 를 펼쳐 `toolResult.result` 의 숫자와 답의 숫자를 비교한다.

2026-10-20 실측 (Global Model v1):

```txt
Tool 결과 : no_disease, confidence 0.9844 (no_disease 0.9844 / disease 0.0156)
LLM 답변 : 한 줄 결론: 판정은 no_disease (심장병 없음)이며, 신뢰도(confidence)는 0.984입니다.
            확률: no_disease 0.984 / disease 0.016
            판정 설명: 최상위 확률이 0.984로 매우 높으므로 이 판정은 매우 확실합니다.
            주의: 이 결과는 공개 데이터로 학습된 실습용 모델의 출력이며 진단 근거가 아닙니다.
```

이번에는 Harness 의 네 줄 형식과 "퍼센트로 바꾸지 않기"를 그대로 지켰습니다. 화면에 `**` 가 글자 그대로 보이는 것은 Studio 가 마크다운을 그리지 않아서입니다.

> **숫자가 Tool 결과와 같으면 성공입니다.** 작은 LLM(4B)은 Harness 의 형식 규칙(예: 퍼센트로 바꾸지 않기)을 가끔 어기거나 형식을 일부 생략합니다. 값이 다르면 Harness 를 손보고, 형식만 다르면 넘어갑니다.

같은 행이라도 Initiative Model 과 Global Model 은 확률이 다르게 나옵니다.

## 6) 검증하고 빌드

![Run Validation Passed 와 Build Agent]({{ '/tutorial/images/hm1-14.png' | relative_url }})

1. 아래로 내려 **Run Validation** 을 누른다. 몇 초 뒤 오른쪽에 **`Passed`**, 다섯 항목 모두 ✓ 가 됩니다.
2. **Build Agent** 를 누른다.

![Immutable Agent build completed 와 Open in Agents]({{ '/tutorial/images/hm1-15.png' | relative_url }})

**`Immutable Agent build completed.`**, 이름 옆 배지 `built`, Latest build `r1` 이 보이면 끝입니다. 몇 초면 됩니다.

1. **Open in Agents** 를 누르면 다음 장(Serving API)으로 이어집니다.

{: .note }
> Tool 코드나 Harness 를 고쳤으면 **반드시 다시 Build** 하세요. 빌드는 그 시점의 코드·모델을 고정합니다.

## ✅ 체크리스트

- [ ] Tool AI 로 Heart Disease MLP(Global Model v1)를 추가했다
- [ ] Base LLM 을 고르고 Save 했다
- [ ] Harness 를 붙여 넣고 `explicit` · `none` 으로 Save 했다
- [ ] Base LLM 이 `ready · 100%` 다
- [ ] Generate Response 의 숫자가 Tool 결과와 같다
- [ ] Validation `Passed`, Build `r1` 완료

## 안 되면

| 증상 | 조치 |
| --- | --- |
| `An Agent draft with this name already exists.` | 예전에 같은 이름으로 만든 **초안**이 남아 있다. Agents 화면에서 Agent 를 지워도 Agent Builder 의 초안은 따로 남는다. Agent Builder 에서 그 초안을 열고 위쪽 **Delete** 로 지우거나, 다른 이름을 쓴다 |
| Agents 화면에서 **Delete** 를 눌러도 반응이 없다 | 그 Agent 의 Serving API 가 켜져 있으면 Delete 가 잠긴다. **Serving API** 탭에서 **Disable API** 를 먼저 누른다 |
| Tool AI 목록이 비어 있음 | Owner 트랙 4장의 Local Train 을 먼저 한다 |
| `... changed after selection. Select it again and rebuild the Agent.` | 페이지를 새로고침하고 Tool AI 를 다시 골라 Add 한다 (연합학습 뒤 Global Model 을 처음 고를 때 나옴) |
| Test & Build 에 `Base LLM: Not selected` | Models 탭에서 고른 뒤 Save 를 안 했다 |
| Validation 실패 | 실패한 항목이 가리키는 곳을 고친다. Base LLM 이면 Prepare 부터 |
| 너무 느림 | 다른 프로그램을 닫는다. 16 GB 미만이면 버겁다 |

## 다음 단계

[2. API 로 호출하기]({{ '/v1.3/tutorial/model-use/serving-api/' | relative_url }})
