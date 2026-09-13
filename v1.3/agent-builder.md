---
layout: "default"
title: "Agent Builder & Serving"
nav_order: 5
permalink: "/v1.3/agent-builder/"
docs_version: "1.3"
lang: "ko"
guide_source: "매뉴얼 04_Agent_Builder_and_Serving 3c95dfbe76bb80868eaddbcf8e99151d.md"
guide_status: "draft"
---

# Agent Builder & Serving
{: .no_toc }

Scenario 04. Agent Builder, Test와 Serving
{: .fs-5 .fw-400 }

## 대상

Federated Task의 LLM 또는 AI model을 Federated AI Agent의 구성 요소로 사용하려는 사용자.

![3_AgentImprove.png]({{ '/assets/images/v1.3/manual-04/3_AgentImprove.png' | relative_url }})

그림처럼 Agent Build는 선택한 정확한 Model Version을 고정한다. 개선할 때는 Agent 전체가 아니라
Federated LLM 또는 Tool AI 하나를 선택해 그 Source Federated Task에서 연합학습한다.

## 사전 조건

- 사용할 Federated Task가 현재 계정의 Owned 또는 Approved Joined Task다.
- Task가 Agent Studio Workspace에 열려 있다.
- Tool AI는 Local Train 또는 FL로 준비된 compatible model version이 있다.
- Task Data adapter와 Tool manifest 검증을 통과했다.

## 절차

### 1. Federated AI Agent Build & Test

#### 1.1 Build

FedOps Agent Studio에서 Agent Builder 메뉴로 들어간다.

New Agent를 누르면서 Agent build 과정이 시작된다.

![image.png]({{ '/assets/images/v1.3/manual-04/image.png' | relative_url }})

우선 이름을 지정하고 만들어준다.

![image.png]({{ '/assets/images/v1.3/manual-04/image-1.png' | relative_url }})

LLM과 Tool AI 모델을 선택한다.

1,2는 LLM을 선택하는 과정이며, huggingface 모델을 선택하는 예시이다.

> 
> 
> 
> ### Base LLM 선택
> 
> 다음 중 정확히 하나를 선택한다.
> 
> - Hugging Face LLM: repository, revision, runtime format과 model file 지정
> - Federated LLM: Workspace/Registry에서 사용 가능한 model version 지정
> 
> Hugging Face LLM은 External · not federated로, Federated LLM은 Source Federated Task와 Global Model version과 함께 표시한다. 
> 

3번은 기선택된 LLM과 ToolAI 목록을 보여준다.
4번은 현재 선택할 수 있는 ToolAI 목록을 보여준다. 

> 
> 
> 
> ### Tool AI 추가
> 
> 1. 사용 가능한 Owned/Joined Federated Task를 선택한다
>     
>     이때 Tool은 0개 이상 추가할 수 있다. 
>     
> 2. Initiative Model 또는 Global Model vN 중 사용할 버전을 선택한다
>     
>     ![image.png]({{ '/assets/images/v1.3/manual-04/image-2.png' | relative_url }})
>     
> 3. model을 로컬에 준비한다(새로고침이 필요한다.)
> 4. Task Data가 연결되고 sample adapter가 통과하는지 확인한다.
> 
> 참여하지 않은 Registry Task는 선택 가능성을 보여줄 수 있지만, 실제 사용은 Join/승인,
> Workspace import와 local readiness 후에 허용한다.
> 

click후 LLM과 동일하게 우측에서 Add as Tool AI 버튼을 통해 선택한다.

![image.png]({{ '/assets/images/v1.3/manual-04/image-3.png' | relative_url }})

이때 다운로드가 필요한 모델은 아래와 같이 뜨며, 다운로드가 완료되면 새로고침하여 다시 선택하면 됩니다.

![image.png]({{ '/assets/images/v1.3/manual-04/image-4.png' | relative_url }})

Agent Harness 메뉴로 넘어가 Harness를 설정한다.

> 
> 
> 
> ### Harness 구성
> 
> Harness에는 다음 정책을 작성한다.
> 
> - 어떤 요청에서 어떤 Tool을 사용해야 하는가
> - Tool 실패 시 임의 결과를 만들지 않는 규칙
> - Tool 결과를 어떻게 설명할 것인가
> - privacy, context, memory와 safety 제약
> 
> Tool 이름과 JSON schema는 manifest에서 Runtime이 제공하며 사용자가 거대한 JSON을 Harness에 복사하지 않는다.
> 

![image.png]({{ '/assets/images/v1.3/manual-04/image-5.png' | relative_url }})

#### 1.2 Test

Test & Build 메뉴로 넘어가 설정된 Agent를 테스트 해볼 수 있다.

먼저 Prepare Base LLM 버튼을 click하여 base llm 준비가 완료되는 것을 기다린다.

![image.png]({{ '/assets/images/v1.3/manual-04/image-6.png' | relative_url }})

이후 Sample Index를 선택한 후 Load Sample for Agent를 눌러, Agent에게 질문할 내용 (모델이 실제 예측에 사용할 데이터 한개)를 지정한다.

![image.png]({{ '/assets/images/v1.3/manual-04/image-7.png' | relative_url }})

질문을 입력하고 Generate Response를 눌러 응답을 확인한다. 
이때 Tool routing과 streaming response를 확인한다.

※ 응답이 길면 **Stop generation**으로 중단할 수 있는지 확인한다.

![image.png]({{ '/assets/images/v1.3/manual-04/image-8.png' | relative_url }})

Agent Run Validation을 진행한 후 Build Agent를 눌러 에이전트를 완성한다.

이때 build revision 고정되는 내용은 아래와 같다

> 
> 
> - Base LLM repo/revision/file 또는 Federated LLM model version
> - Tool별 taskId, localProjectId, source fingerprint와 model checksum/version
> - Harness와 runtime policy
> 
> Workspace source나 model이 바뀌면 기존 build를 조용히 변경하지 말고 새 build를 만든다.
> 

![image.png]({{ '/assets/images/v1.3/manual-04/image-9.png' | relative_url }})

### 2. Agent 사용

#### 2.1 FedOps Agent Studio에서 직접 테스트

> 
> 
> 
> ### Built Agent 검증
> 
> Agents에서 build를 선택하고 다음을 확인한다.
> 
> - build smoke test
> - Agent chat과 실제 Tool routing trace
> - Tool direct predict
> - 각 Federated component의 model version과 새 version 존재 여부
> - component에서 해당 Federated Learning Task로 이동

Agents 메뉴를 선택하여 직접 테스트 한다.

![image.png]({{ '/assets/images/v1.3/manual-04/image-10.png' | relative_url }})

#### 2.2 Local Serving API

1. FedOps Agent Studio에서 Serving API 메뉴에 들어간다. (1~3)
2. **Serving API**에서 Agent별 사용 port를 정한다. (4)
3. Tool별 Serving Data Source를 등록하고 허용 여부를 설정한다. (5)
4. **Enable Serving API**를 누른다. (6)

![image.png]({{ '/assets/images/v1.3/manual-04/image-11.png' | relative_url }})

1. 표시된 token은 안전하게 보관하고 외부 문서에 기록하지 않는다.

![image.png]({{ '/assets/images/v1.3/manual-04/image-12.png' | relative_url }})

1. 자동 생성된 cURL/Postman 예제로 health, info, chat와 predict를 확인한다.

![image.png]({{ '/assets/images/v1.3/manual-04/image-13.png' | relative_url }})

ENDPOINTS를 통해 API 형식을 확인할 수 있다.

![image.png]({{ '/assets/images/v1.3/manual-04/image-14.png' | relative_url }})

> **주의점**
> 
> 
> 입력은 manifest schema에 맞는 inline payload 또는 등록된 local Data Source reference를 사용한다.
> 임의 host path를 API input으로 받지 않는다.
> 
> Serving request, Agent response와 Tool prediction을 자동으로 학습 데이터에 추가하지 않는다.
> Improve에 사용할 데이터는 각 Federated Task의 Data Contract와 사용자 정책에 따라 Task Data에
> 명시적으로 연결하고 다시 검증한다. 
> 

##### 새 Global model이 생겼을때 기존 Built Agent가 자동 변경되지 않는다.

이는 재현성과 rollback 가능성을 유지하기 위함이며, Agent에 **Model update available**이 표시되는지 확인한 뒤 다시 build 과정을 거치면 된다.

### 3. API 내역 확인

위 단계와 동일한 화면에서 Requests 메뉴를 누르면 API 요청 내역을 확인할 수 있다. 

![image.png]({{ '/assets/images/v1.3/manual-04/image-15.png' | relative_url }})

## 완료 조건

- Base LLM 하나와 선택한 모든 Tool AI가 로컬에 준비된다.
- 여러 Tool 중 Harness와 schema에 맞는 Tool이 선택된다.
- raw Task Data path가 Web이나 Base LLM에 직접 노출되지 않는다.
- build가 source/model/Harness fingerprint를 고정한다.
- chat와 direct predict API가 같은 Tool contract로 동작한다.
