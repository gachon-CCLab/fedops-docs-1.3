---
layout: "default"
title: "Overview"
nav_order: 1
permalink: "/"
docs_version: "1.3"
lang: "ko"
guide_source: "FedOps 1 3 Document 3c75dfbe76bb80db9259dbf26b3b6a31.md"
guide_status: "draft"
---

# Overview
{: .no_toc }

FedOps 1.3 - Federated AI AgentOps Main Doc
{: .fs-5 .fw-400 }

## FedOps 1.2 → 1.3

FedOps 1.2는 FedOps Web에서 계정별 Task와 집계 서버를 관리하고, 사용자가 별도 환경에서 직접 Client를 실행해 연합학습에 참여하는 구조가 중심이었다.

FedOps 1.3은 FedOps Agent Studio를 통해, 사용자의 로컬 장치에서 모델 개발, 데이터 연결, 로컬 학습, 연합학습 참여, Federated AI Agent Build와 Serving을 하나로 연결한다.

---

## 1. FedOps 1.3

FedOps 1.3은 여러 사용자가 원본 데이터를 공유하지 않고 모델을 함께 학습하고,

그 모델을 AI Agent의 구성 요소로 사용하며, 필요한 구성 모델만 다시 연합학습으로 개선하는 **Federated AI AgentOps** 플랫폼이다.

![0_Federated AI AgentOps.png]({{ '/assets/images/v1.3/overview/0_Federated_AI_AgentOps.png' | relative_url }})

```markdown
Federated Task 생성·공개
→ Registry에서 발견·참여
→ 각 사용자 장치에서 연합학습
→ 버전이 관리되는 Global Model 생성
→ Federated AI Agent Build·Use
→ 선택한 구성 모델 지속 개선
```

FedOps 1.3은 위 생명주기를 하나로 지원한다.

## 2. Federated AI AgentOps Lifecycle

![1_Federated AI AgentOps.png]({{ '/assets/images/v1.3/overview/1_Federated_AI_AgentOps.png' | relative_url }})

전체 흐름은 여섯 단계로 구성된다.

| 단계 | 사용자가 하는 일 | 만들어지는 결과 |
| --- | --- | --- |
| **1. Create & Regist** | Task Draft로 시작하거나 기존 Local Model을 가져와 로컬학습한다. | Initiative Model과 게시 가능한 Federated Task |
| **2. Load & Join** | Owner가 Task를 공개하고 Participant가 Registry에서 참여한다. | Published Task와 승인된 Participant |
| **3. Federated Learning** | 각 Client가 자신의 데이터로 학습하고 Model Update만 보낸다. | Round별 집계 결과 |
| **4. Global Model** | Initiative Model부터 학습 결과를 버전으로 관리한다. | Global Model v1, v2, …, vN |
| **5. Build Agent** | Base LLM, Tool AI와 Agent Harness를 구성하고 검증한다. | 정확한 Model Version이 고정된 Agent Build |
| **6. Reasoning & Improve** | Agent를 로컬 또는 API로 사용하고 필요한 구성 모델을 다시 학습한다. | 새 Global Model Version과 새 Agent Revision |

원본 데이터는 모든 단계에서 사용자 장치에 남는다. FedOps FL Server에는 원본 데이터가 아니라
각 Client가 로컬학습으로 만든 Model Update만 전달된다.

## 3. FedOps의 Web, Registry와 Agent Studio의 역할

| 구성요소 | 역할 |
| --- | --- |
| **FedOps Web** | Task 생성, 참여 정책, Owner Publish, Campaign, FL Server와 전체 Monitoring 관리 |
| **FedOps Registry** | Published Task, Release Snapshot, Initiative/Global Model Version과 참여 상태 제공 |
| **FedOps Agent Studio** | Workspace, 로컬 데이터, Python 환경, 로컬학습, FL Client, Agent Build·Test·Serving 실행 |
| **FedOps FL Server** | Task ID로 Client를 연결하고 Round별 Model Update를 집계해 새 Global Model 생성 |

Web은 Task와 연합학습을 관리하는 Control Plane,

Agent Studio는 사용자 장치에서 코드·데이터·학습과 Agent를 실행하는 Local Plane이다.

## 4. FedOps 1.3 FL End-to-End Flow

![2_EndtoEndFlow.png]({{ '/assets/images/v1.3/overview/2_EndtoEndFlow.png' | relative_url }})

### 4.1 Task Owner

- FedOps Web에서 Task Draft를 만들거나 Agent Studio에서 기존 Local Model을 연다.
- Workspace에 로컬 데이터를 연결하고 Python 환경을 준비한다.
- Local Train으로 첫 시작 모델인 Initiative Model을 만든다.
- Release Readiness를 통과하고 Release Candidate를 제출한다.
- Web에서 Owner Publish하여 Task를 Registry에 공개한다.
- Participant 요청을 승인하고 Campaign을 저장한 뒤 FL Server를 시작한다.
- Client 참여, Round, Client Metric과 Global Model 계보를 확인한다.

→ 처음부터 새 Task를 만드는 경우에는 [Create a New Task]({{ '/v1.3/task-owner/create-task/' | relative_url }}) 문서를 따른다.

→ 이미 모델을 보유중이라면 [Import a Local Model]({{ '/v1.3/task-owner/import-model/' | relative_url }}) 문서를 따른다.

### 4.2 Task Participant

- Registry에서 사용할 Federated Task를 찾고 Join을 요청한다.
- 승인된 Published Release를 Agent Studio Workspace에서 연다.
- 자신의 로컬 데이터와 Python 환경을 연결한다.
- Participation Readiness를 확인한다.
- `Participation Ready`와 `Server Live`가 모두 충족되면 FL Client를 시작한다.
- Client는 Global Model을 받고, 로컬학습·평가 후 Model Update만 서버에 보낸다.
- Round별 Local Metric, Model Flow와 Participation History를 확인한다.

→ 상세 절차는 [Participant: Join & FL]({{ '/v1.3/participant/' | relative_url }}) 문서를 따른다.

### 4.3 Campaign과 FL Server 운영

Task Owner는 Clients per round, Round 수와 Aggregation 전략을 Campaign으로 저장한다.
저장한 Campaign으로 FL Server를 시작하며, 완료된 Campaign의 결과는 새 Global Model Version으로 등록된다.

→ 운영 절차는 [Campaign & Server Management]({{ '/v1.3/campaign/' | relative_url }}) 문서를 따른다.

## 5. Global Model을 Federated AI Agent로 사용하기

![3_AgentImprove.png]({{ '/assets/images/v1.3/overview/3_AgentImprove.png' | relative_url }})

### 5.1 Federated AI Agent 구성

하나의 Agent Draft는 다음 구성요소를 갖는다.

- **Base LLM 1개**: Hugging Face LLM 또는 Federated LLM
- **Tool AI 1개 이상**: 각 Tool의 Source Federated Task와 Model Version
- **Agent Harness**: Tool 선택, 호출 방식, 응답 원칙과 Runtime 정책

`Validate & Test`를 통과해 Build하면 선택한 모든 Model Version이 Agent Build에 고정된다.

### 5.2 Federated AI Agent 사용

Built Agent는 다음 두 방식으로 사용한다.

- Agent Studio에서 Local Chat과 Tool AI 실행
- Serving API를 활성화하여 사용자 서비스나 Application에서 호출

→ 상세 절차는 [Agent Builder & Serving]({{ '/v1.3/agent-builder/' | relative_url }}) 문서를 따른다.

### 5.3 Agent의 구성 모델 개선

Agent 전체를 하나의 모델처럼 연합학습하지 않는다.

1. 개선할 Federated LLM 또는 Tool AI를 선택한다.
2. 해당 모델의 Source Federated Task로 이동한다.
3. 그 Task의 Federated Learning에 다시 참여한다.
4. 새 Global Model Version이 만들어지면 Agent Draft에서 새 버전을 선택한다.
5. 다시 Validate & Test하고 새 Agent Revision을 Build한다.

새 Global Model이 등록되어도 실행 중인 Agent는 자동으로 바뀌거나 덮어써지지 않는다.

## 6. 상세 시나리오 정보

| 목적 | 상세 시나리오 |
| --- | --- |
| Agent Studio를 처음 준비한다 | [Getting Started]({{ '/v1.3/getting-started/' | relative_url }}) |
| Web Draft에서 새 Federated Task를 만든다 | [Create a New Task]({{ '/v1.3/task-owner/create-task/' | relative_url }}) |
| 기존 Local Model을 Federated Task로 전환한다 | [Import a Local Model]({{ '/v1.3/task-owner/import-model/' | relative_url }}) |
| Registry Task에 참여하고 FL Client를 실행한다 | [Participant: Join & FL]({{ '/v1.3/participant/' | relative_url }}) |
| 모델을 Agent 구성요소로 사용하고 API로 제공한다 | [Agent Builder & Serving]({{ '/v1.3/agent-builder/' | relative_url }}) |
| Campaign과 FL Server를 운영한다 | [Campaign & Server Management]({{ '/v1.3/campaign/' | relative_url }}) |
