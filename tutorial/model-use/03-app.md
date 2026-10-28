---
layout: default
title: "3. 데모 앱 · 내 프로젝트에 붙이기"
parent: "모델 활용 트랙"
grand_parent: "FedOps 튜토리얼"
nav_order: 3
permalink: /v1.3/tutorial/model-use/app/
docs_version: "1.3"
lang: ko
---

# 3. 데모 앱 · 내 프로젝트에 붙이기
{: .no_toc }

{: .note }
> 📍 **지금 어디:** 모델 활용 3/3 — ① Agent → ② Serving API → **③ 앱**<br> 화면: 브라우저 + 내 코드 · 튜토리얼의 마지막 단계

{: .important }
> 🎯 **이 단계에서 하는 일:** 같은 최소 코드에 화면을 얹은 데모 앱으로 Agent 를 써 보고, 입력을 바꿔 가며 **모델의 숫자가 어떻게 움직이는지, LLM 은 그 숫자를 어떻게 설명하는지** 봅니다. 마지막으로 내 프로젝트에서 Agent 를 부르는 법을 익힙니다. 두 병원의 데이터에서 시작한 연합학습이 하나의 서비스 기능으로 끝나는 지점입니다.

{: .note }
> 데모 앱 화면의 글자는 한국어입니다.

1. TOC
{:toc}

```txt
agent_client.py ──┬──▶ test_agent.py   (CLI)
                   └──▶ demo_ui.py      (웹 앱)
                            └──▶ 내 프로젝트
```

## 1) 데모 앱 실행

2장에서 만든 `.env` 를 그대로 씁니다. **Python 3.10 이상**이 필요합니다(3.9 에서는 `Unable to evaluate type annotation 'int | None'` 으로 뜨지 않습니다).

```bash
cd app
uvicorn demo_ui:app --port 8090
```

브라우저에서 [http://localhost:8090](http://localhost:8090) 을 엽니다.

![Demo UI 첫 화면, READY 배지와 TOOL 입력]({{ '/tutorial/images/hm3-01.png' | relative_url }})

왼쪽 위 AGENT 칸에 **`READY · bartowski/Qwen_Qwen3.5-4B-GGUF · Tool 1개`** 가 보이면 Agent 에 연결된 것입니다. 아래 **TOOL 입력** 칸은 하드코딩이 아니라 Agent 의 `/info` 가 알려 주는 Tool 명세로 자동으로 만들어집니다(`출처 agent`). 수치 8개는 숫자 칸, **`cp`(가슴 통증 유형)와 `restecg`(심전도)는 정해진 값 중 고르는 선택 상자**로 나옵니다. 명세에 허용 값(`enum`)이 적혀 있기 때문입니다. Agent 가 꺼져 있으면 로컬 명세 파일로 폼만 그리고 `출처 local-file` 로 표시됩니다.

## 2) 해 볼 것 ① — 샘플 보내기

![샘플 채우기 버튼과 행 정보]({{ '/tutorial/images/hm3-02.png' | relative_url }})

1. TOOL 입력 맨 아래 **샘플 채우기** 를 누른다.

`data/out/test.csv` 의 실제 행 하나가 무작위로 들어가고, 아래에 몇 번째 행인지와 실제 라벨이 나옵니다. 이번에는 `test.csv 127번째 행 · 실제 라벨 0 (no_disease)` 이었습니다.

![질문 칸과 Agent 에게 보내기]({{ '/tutorial/images/hm3-03.png' | relative_url }})

1. 위로 올라가 **질문** 칸의 문장을 확인한다(기본값 그대로 써도 된다).
2. **Agent 에게 보내기** 를 누른다. 1분 안팎 걸립니다. 스트리밍이 없어 그동안 화면이 조용합니다.

![답변, TOOL 예측, TRACE]({{ '/tutorial/images/hm3-04.png' | relative_url }})

**답변**, **TOOL 예측** 카드, **TRACE** 표가 차례로 나옵니다.

2026-10-20 실측(40초):

- TOOL 예측: **no_disease 0.957 / disease 0.043**
- 답변: `판정 결과: no_disease (심장병 없음) 0.957 … 진단 근거가 아닙니다.`
- TRACE: `tool-routing`, `tool-ai`(9656 ms), `base-llm` 모두 passed

답변의 숫자와 TOOL 예측 카드의 숫자가 같으면 됩니다. 4B 모델이라 가끔 퍼센트로 쓰기도 합니다. 값이 같으면 괜찮습니다.

## 3) 해 볼 것 ② — 입력값 바꾸기

심장병 없음으로 나온 행에서 해 보면 변화가 잘 보입니다. 심장병 있음 행이었다면 샘플 채우기를 다시 누릅니다.

![cp · exang · oldpeak 바꾸기]({{ '/tutorial/images/hm3-05.png' | relative_url }})

1. **cp**(가슴 통증 유형)를 `4`(증상 없음)로 바꾼다.
2. **exang**(운동 유발 협심증)을 `1` 로 바꾼다.
3. **oldpeak**(ST 분절 하강)을 `2.5` 로 바꾼다.

그리고 위로 올라가 다시 **Agent 에게 보내기** 를 누릅니다.

![값을 바꾼 뒤 판정이 disease 로 뒤집힌 결과]({{ '/tutorial/images/hm3-06.png' | relative_url }})

같은 환자에서 세 값만 바꿨는데 판정이 **no_disease 0.957 → disease 0.884** 로 뒤집혔습니다(2026-10-20 실측, 36초). 최상위 확률이 0.7 미만이 되면 LLM 이 Harness 규칙대로 **"판정이 확실하지 않다"** 고 밝힙니다. 이번에는 0.884 라 "비교적 확실하다"고 답했습니다.

> 이 데이터에서는 "가슴 통증이 없는데(`cp` = 4) 심장병이 있는" 환자가 많아, `cp` = 4 가 심장병 쪽으로 기우는 신호입니다. 직관과 다를 수 있지만 모델은 데이터에 있는 패턴을 배울 뿐입니다.

## 4) 해 볼 것 ③ — Tool 없이 보내기

![Tool 없이 보내기 체크와 보내기]({{ '/tutorial/images/hm3-07.png' | relative_url }})

1. **Tool 없이 보내기** 를 켠다.
2. **Agent 에게 보내기** 를 누른다.

![모델 결과가 없다는 답변]({{ '/tutorial/images/hm3-08.png' | relative_url }})

TOOL 예측이 비고, TRACE 에는 `base-llm` 만 남습니다. LLM 은 판정하지 않고 **"… 모델 결과가 없습니다"** 라고 답합니다(2026-10-20 실측, 25초). Tool 은 요청에 `input` 이 있을 때만 실행되고, Harness 가 짐작으로 판정하지 못하게 막기 때문입니다.

## 5) 내 프로젝트에 붙이기

파일 하나 복사가 전부입니다. (빈 폴더 + `httpx` 만으로 아래 코드가 동작하는 것을 2026-10-20 에 확인했습니다. 52초, no_disease 0.982)

```bash
cp template/app/agent_client.py <내 프로젝트>/
pip install httpx
export AGENT_SERVING_URL=http://localhost:24400
export AGENT_SERVING_TOKEN=fas_...
export AGENT_TOOL_ID=local:handson-heart
```

```py
from agent_client import AgentClient, AgentUnavailableError, AgentStatus, to_prediction

client = AgentClient.from_env()
try:
    envelope = client.chat(
        "이 환자 기록의 판정 결과를 설명해줘",
        tool_input={
            "age": 29, "sex": 1, "trestbps": 120, "chol": 243, "fbs": 0,
            "thalach": 160, "exang": 0, "oldpeak": 0.0, "cp": 2, "restecg": 0,
        },
    )
except AgentUnavailableError as error:
    if error.agent_status is AgentStatus.BAD_INPUT:
        ...  # 내 payload 버그
    elif error.agent_status is AgentStatus.NEEDS_REBUILD:
        ...  # 운영자에게: Agent 다시 Build
    raise

print(envelope["response"])            # LLM 문장
prediction = to_prediction(envelope)   # label, class_name, confidence, probabilities, model_version_id ...
```

- `tool_input` 의 키는 Tool 명세의 features 와 **정확히 같아야** 합니다. 라벨 열(`target`)은 뺍니다.
- `cp`·`restecg` 는 **숫자**로 보냅니다(`"cp": 2`). 허용 값 밖이면 `BAD_INPUT` 입니다.
- Tool id 를 모르면 `client.resolve_tool_id()`, 피처 목록은 `client.info()["tools"][0]["toolManifest"]`.
- 대화를 이어 가려면 이전 대화를 `client.chat(..., history=[{"role": "user", "content": ...}, {"role": "assistant", "content": ...}])` 로 함께 보냅니다(최근 40개까지). Harness 의 Memory 설정과 관계없이, Agent 는 보낸 기록만큼 기억합니다([1장 Harness 해설]({{ '/v1.3/tutorial/model-use/agent/' | relative_url }})).

## 설계할 때 지킬 것

{: .warning }
> **토큰은 서버 쪽에만** 둡니다. 브라우저나 모바일 앱에 넣지 마세요. 데모 앱처럼 내 백엔드가 Agent 를 부르고, 프런트는 내 백엔드만 부르게 만듭니다.

| 상황 | 권장 (한 번에 40~120초, 스트리밍 없음) |
| --- | --- |
| 웹 요청 처리 중 호출 | 작업 큐에 넣고 결과를 나중에 보여 준다 |
| 화면에 바로 보여야 함 | 진행 표시를 띄우고 기다린다. 타임아웃 240초 이상 |
| 여러 건 처리 | 순차로. 동시에 던지면 더 느려진다 |

예측을 저장한다면 `modelVersionId`(어느 모델이 답했는지), `requestId`, 보낸 payload 를 함께 남기세요. 모델을 재학습해도 앱 코드는 그대로이고, 바뀌는 것은 `AGENT_TOOL_ID` 와 입력 키뿐입니다.

<details markdown="1">
<summary>📚 배경 — 입력을 바꾸면 왜 확률이 움직이나</summary>

3\) 에서 `cp`·`exang`·`oldpeak` 만 바꿨더니 확률이 움직였습니다. 모델이 학습 중에 "운동하면 협심증이 오고 ST 분절이 내려가면 심장병 쪽"이라는 패턴을 배웠기 때문입니다. 이 패턴은 Owner(헝가리) 혼자의 데이터가 아니라 연합학습에 참여한 두 병원의 데이터에서 함께 배운 것입니다.

다만 이 모델은 **왜** 그렇게 판단했는지(어느 항목이 얼마나 기여했는지)를 알려 주지 않습니다. 그래서 Harness 가 LLM 에게 "기여도를 설명하지 말 것"을 시킵니다. 설명 가능성(XAI)이 필요하면 SHAP 같은 기여도 계산을 Tool 의 출력에 넣어야 하고, 그것은 Owner 가 Task 코드에서 정할 일입니다.

</details>

## ✅ 체크리스트

- [ ] [http://localhost:8090](http://localhost:8090) 에서 `READY` 배지가 보인다
- [ ] 폼이 10칸(숫자 8개 + 선택 상자 2개)으로 자동 생성됐다
- [ ] 샘플을 보내면 답변·TOOL 예측·TRACE 가 나오고 숫자가 같다
- [ ] 값을 바꾸면 확률이 달라진다
- [ ] Tool 없이 보내면 "모델 결과가 없습니다" 가 나온다
- [ ] 내 프로젝트에서 `agent_client.py` 로 호출했다

## 튜토리얼을 마치며

| 지나온 길 | 누가 | 어디서 |
| --- | --- | --- |
| 데이터·모델 설계 | Owner (헝가리) | 내 PC |
| Task 만들기·게시 | Owner | Console + Studio |
| 참여 요청·승인 | Client (클리블랜드) ↔ Owner | Registry ↔ Console |
| 로컬 학습·집계 | 두 병원 + 서버 | 각자의 Studio + 집계 서버 |
| Global Model | Owner | Console |
| Agent · API · 앱 | 모델을 쓰는 사람 | Studio + 내 코드 |

다음은 같은 흐름을 **내 데이터와 내 모델**로 해 보는 것입니다. [Owner 트랙 3장의 "자기 데이터·모델로 바꾸려면"]({{ '/v1.3/tutorial/owner/workspace/' | relative_url }})과 [Federated Task Developer Guide](https://gachon-cclab.github.io/fedops-docs-1.3/v1.3/developer-guide/)에서 시작하세요.
