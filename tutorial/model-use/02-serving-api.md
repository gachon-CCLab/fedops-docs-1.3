---
layout: default
title: "2. API 로 호출하기"
parent: "모델 활용 트랙"
grand_parent: "FedOps 튜토리얼"
nav_order: 2
permalink: /v1.3/tutorial/model-use/serving-api/
docs_version: "1.3"
lang: ko
---

# 2. API 로 호출하기
{: .no_toc }

{: .note }
> 📍 **지금 어디:** 모델 활용 2/3 — ① Agent → **② Serving API** → ③ 앱<br> 화면: **Agent Studio** (Agents) + 터미널 · 다음: 데모 앱과 내 프로젝트에서 부른다

{: .important }
> 🎯 **이 단계에서 하는 일:** 빌드한 Agent 를 내 PC 의 **HTTP API** 로 열고(전용 포트 + 토큰), 템플릿의 최소 코드로 불러 봅니다. 이제 Studio 화면 밖의 어떤 프로그램이든 이 Agent 를, 그러니까 연합학습으로 만든 모델을 쓸 수 있게 됩니다.

{: .note }
> 캡처에서 흐리게 처리된 곳은 계정 이름·**토큰**입니다.

{: .warning }
> **알려진 문제(2026-10-11 에도 재현):** 빌드한 Agent 의 API 로 예측(`--sample`)을 요청하면 `Tool AI smoke test failed` (`Readme file does not exist: README.md`)로 실패합니다. Studio 가 빌드 스냅샷에 `README.md` 를 빼고 복사하기 때문입니다. **Build 할 때마다 아래 한 줄로 README 를 넣어 주면 끝까지 동작합니다.** (Owner 트랙 3장에서 연 Studio Workspace 의 README 를 복사합니다)

```bash
AGENT_ID=agent-xxxxxxxx   # Agents 화면에서 Agent 이름 아래 회색 글씨
cp ~/fedops-workspace/accounts/*/projects/handson-heart/README.md ~/fedops-workspace/accounts/*/.local-data/agents/builds/$AGENT_ID/r1/components/tool-0/project/
```

1. TOC
{:toc}

## 1) Serving API 켜기 (Agent Studio)

![Agents 메뉴, Agent 선택, Serving API 탭]({{ '/tutorial/images/hm2-01.png' | relative_url }})

1. 왼쪽 메뉴의 **Agents** 를 누른다. (1장 마지막의 Open in Agents 를 눌렀다면 이미 이 화면입니다)
2. **handson-heart-agent** 를 고른다. 이름 아래 회색 `agent-…` 가 Agent id 입니다(위 README 우회에 씁니다).
3. **Serving API** 탭을 누른다.

![Serving port 와 Enable Serving API]({{ '/tutorial/images/hm2-02.png' | relative_url }})

1. **Serving port** 를 고른다. 첫 Agent 면 `24400` 그대로 (범위 24400~24499).
2. **Enable Serving API** 를 누른다.

다른 Agent 가 이미 그 포트를 쓰고 있으면 **`Port 24400 is already assigned to another Agent.`** 가 나옵니다. 화면은 쓰고 있는 포트도 기본값으로 보여 줍니다. 그때는 포트를 `24401` 처럼 다음 번호로 바꾸고 **Enable Serving API** 를 다시 누릅니다. (2026-10-20 실습에서는 다른 Agent 두 개가 24400·24401 을 쓰고 있어 `24402` 를 썼습니다. 아래 예시의 포트는 자기 포트로 바꿉니다)

![ACTIVE 와 Copy token (토큰은 가림)]({{ '/tutorial/images/hm2-03.png' | relative_url }})

**`● ACTIVE`** 와 Endpoint `http://localhost:<포트>` 가 보이면 켜진 것입니다.

1. **Copy token** 을 눌러 토큰을 복사해 둔다. **토큰은 이때 한 번만 보입니다**(`Copy this token now`). 놓쳤으면 **Rotate token** 으로 새로 받습니다.

{: .warning }
> 토큰(`fas_…`)은 비밀번호처럼 다룹니다. 캡처해 공유하거나 git 에 올리지 마세요. 아래 `.env` 는 `.gitignore` 에 들어 있습니다.

### ⚙️ 옵션 해설 — Serving API

| 옵션·버튼 | 무엇을 정하나 | 이 튜토리얼 |
| --- | --- | --- |
| **Serving port** | Agent 가 열릴 내 PC 의 포트. 범위 24400–24499, Agent 마다 하나씩 | 24400, 이미 쓰고 있으면 다음 번호 |
| **Enable / Disable API** | API 를 열고 닫는다. 켜져 있는 동안 그 Agent 는 **삭제할 수 없다** | Enable |
| **Copy token** | API 를 부를 때 쓰는 비밀 열쇠(`fas_…`). **한 번만 보여 준다** | 복사해 `.env` 에 |
| **Rotate token** | 새 토큰을 만들고 이전 토큰을 무효로 한다 | 토큰을 놓쳤거나 새어 나갔을 때 |
| **Advanced · Direct Tool API** | LLM 을 거치지 않고 Tool(모델)만 직접 부르는 길. Tool 마다 따로 켠다. **기본은 꺼짐** | 끔 — 5) 에서 막히는 것만 확인 |

> **왜 토큰이 필요한가:** API 는 내 PC 의 포트로 열립니다. 같은 네트워크의 다른 프로그램도 그 포트에 닿을 수 있으므로, 토큰을 가진 쪽만 Agent 를 부를 수 있게 합니다.

## 2) 최소 코드 설정

템플릿의 `app` 폴더에서 합니다.

```bash
cd app
pip install -r requirements.txt
cp .env.example .env
```

`.env` 를 채웁니다.

```txt
AGENT_SERVING_URL=http://localhost:24400   # 1) 에서 고른 포트
AGENT_SERVING_TOKEN=fas_...                # 1) 에서 복사한 토큰
AGENT_TOOL_ID=local:handson-heart
AGENT_TIMEOUT_S=900                        # 빌드 후 첫 호출만. 이후 240
```

{: .highlight }
> 빌드 후 **첫 호출은 10분 가까이** 걸립니다. Tool 실행 환경을 새로 설치하기 때문입니다. 2026-10-20 실측 **449초**(그중 Tool 412초), 두 번째부터 **43초**(Tool 13초). 첫 호출만 `AGENT_TIMEOUT_S=900` 으로 늘리고, **끝날 때까지 다른 요청을 겹쳐 보내지 마세요.** PC 가 잠들지 않게 두는 것도 중요합니다.

## 3) 호출해 보기

**① 살아 있나**

```bash
python test_agent.py --health
```

```json
{
  "status": "ready",
  "agentId": "agent-…",
  "buildRevision": 1,
  "llmRuntimeStatus": "installed",
  "toolCount": 1,
  "provider": "local-huggingface",
  "model": "bartowski/Qwen_Qwen3.5-4B-GGUF"
}
```

`status: ready` 면 됩니다. Hugging Face LLM 은 준비가 끝나도 `llmRuntimeStatus` 가 `installed` 로 나옵니다.

**② 어떤 Tool 이 붙어 있나**

```bash
python test_agent.py --info
```

JSON 전체 뒤 마지막 줄에 `Tool id: local:handson-heart  (handson-heart)` 가 나옵니다. `/info` 는 Tool 의 입력 명세(manifest)를 함께 주므로, 앱이 입력 폼을 자동으로 만들 수 있습니다. 이 Task 의 명세에는 10개 입력과, `cp`·`restecg` 가 정해진 값 중 하나여야 한다는 정보(`enum`)가 들어 있습니다.

**③ 예측 받기**

```bash
python test_agent.py --sample 0
```

`data/out/test.csv`(두 병원의 평가용 행) 0번째 행을 Tool 입력으로 보냅니다. 이 행의 실제 라벨은 심장병 없음(`target=0`)입니다.

2026-10-20 실측(Global Model v1):

```txt
(참고) 이 행의 실제 라벨 target=0

=== 답변 (449.0초, status=succeeded) ===        ← 빌드 후 첫 호출. 두 번째는 42.7초
판정 결과: no_disease (심장병 없음) 0.982
no_disease 0.982 / disease 0.018
이 결과는 심장병이 없는 것으로 매우 확실히 판정되었습니다.
이 결과는 공개 데이터로 학습된 실습용 모델의 출력이며 진단 근거가 아닙니다.

=== Tool 예측 ===
  no_disease (label=0, confidence=0.982)
    no_disease: 0.982
       disease: 0.018
  modelVersionId: 6ad72541…
  Tool 소요: 411804 ms                           ← 두 번째는 12838 ms

=== trace ===
  tool-routing   passed
  tool-ai        passed 411804
  base-llm       passed
```

> 1장 Test 탭과 숫자가 다른 이유: 1장은 Owner 의 헝가리 데이터의 0번째 행, 여기는 템플릿 `test.csv` 의 0번째 행이라 서로 다른 환자입니다.

## 4) 응답 읽는 법

**예측값은 `toolResult.result` 안에 한 겹 더 들어 있습니다.** `response` 는 LLM 이 쓴 문장이고, `toolResult.tool.modelVersionId` 는 어느 모델 버전이 답했는지입니다. 최소 코드의 `to_prediction()` 이 이 처리를 해 줍니다.

## 5) 경계 확인 (선택)

```bash
python test_agent.py --chat "무엇을 할 수 있어?"      # Tool 없이 → LLM 만 답한다
```

2026-10-20 실측(63초): trace 에 `base-llm` 만 남고 `(Tool 결과 없음 — input 을 함께 보내지 않으면 Tool 은 실행되지 않는다)` 가 나옵니다.

```bash
echo '{"bogus_key": 1.0}' > bad.json
python test_agent.py --payload bad.json --chat "x" # 키가 틀림 → 409 BAD_INPUT (missing required field(s) ...)
python test_agent.py --invoke --sample 0           # Tool 직접 호출 → 기본은 막힘
```

2026-10-20 실측:

```txt
[실패: BAD_INPUT] 보낸 Tool 입력이 manifest 와 맞지 않는다: input is missing required field(s): age, sex, trestbps, chol, fbs, thalach, exang, oldpeak, cp, restecg.
[실패: TOOL_UNAVAILABLE] Tool 을 실행할 수 없다: Direct Tool API is disabled for this Tool AI. Enable it in Serving API > Advanced.
```

직접 호출은 Serving API 탭의 **Advanced · Direct Tool API** 에서 Tool 별로 켜야 쓸 수 있습니다.

### ⚙️ 해설 — 최소 코드의 설정값 (`.env`)

| 값 | 뜻 | 바꾸면 |
| --- | --- | --- |
| `AGENT_SERVING_URL` | Agent 주소 | 포트를 바꿨으면 같이 바꾼다 |
| `AGENT_SERVING_TOKEN` | 위에서 복사한 토큰 | Rotate 하면 새 값으로 |
| `AGENT_TOOL_ID` | 부를 Tool 의 id. Workspace 이름에서 온다(`local:handson-heart`). 비워 두면 `/info` 의 첫 Tool 을 쓴다 | 다른 Task 의 모델을 쓰면 바뀐다 |
| `AGENT_TIMEOUT_S` | 응답을 기다리는 최대 시간(초) | 빌드 후 첫 호출만 900, 이후 240 |

## ✅ 체크리스트

- [ ] Serving API 가 `● ACTIVE` 이고 토큰이 `.env` 에 들어 있다
- [ ] 빌드 스냅샷에 README 를 복사했다
- [ ] `--health` 가 `status: ready`
- [ ] `--info` 에 `local:handson-heart` 가 보인다
- [ ] `--sample 0` 이 예측과 함께 답을 준다

## 오류 상태 읽기

| 최소 코드가 알려 주는 상태 | 뜻 | 고칠 곳 |
| --- | --- | --- |
| `BAD_INPUT` | 보낸 입력이 명세와 다름 (예: `cp` 에 5) | 내가 보낸 payload |
| `NEEDS_MODEL` | LLM 미준비 | Studio 에서 Prepare Base LLM |
| `TOOL_UNAVAILABLE` | 연결 불가·토큰 거부·Tool 실패·타임아웃 | Studio · 포트 · 토큰 확인. `Readme file does not exist` 면 위 README 우회 |
| `NEEDS_REBUILD` | Tool/Harness 가 빌드 후 바뀜 | Agent 다시 Build (그 뒤 README 우회도 다시) |

## 다음 단계

[3. 데모 앱 · 내 프로젝트에 붙이기]({{ '/v1.3/tutorial/model-use/app/' | relative_url }})
