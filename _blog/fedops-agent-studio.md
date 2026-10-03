---
title: "FedOps Agent Studio"
summary: "코드와 로컬 데이터를 준비하고, 연합학습에 참여하고, 학습한 모델을 나만의 Agent와 서비스에 연결하기까지. FedOps Agent Studio를 만든 배경과 사용 흐름을 소개합니다."
category: Blog
author: "FedOps"
date: 2026-10-02
show_date: true
display_order: 0
cover_image: "/assets/blog/fedops-agent-studio-cover.png"
lang: ko
---

연합학습에 참여하려는 사용자에게는 자신의 데이터로 모델을 학습하는 일 외에도 준비할 것이 많습니다. Task 코드를 가져오고, Python 환경과 의존성을 맞추고, 데이터 경로를 연결한 뒤 Client를 실행해야 합니다. 학습 중에는 진행 상황과 실행 기록을 확인하고, 문제가 생기면 코드와 환경을 다시 점검해야 합니다.

학습을 마친 뒤에도 다음 작업이 남습니다. 얻은 모델을 실제로 사용하려면 추론 코드를 준비하고, 다른 모델이나 Tool과 연결하고, 애플리케이션이 호출할 수 있는 실행 환경을 만들어야 합니다. 새 모델이 나왔을 때 어떤 버전을 사용할지, 기존 Agent에 어떻게 반영할지도 결정해야 합니다.

**FedOps Agent Studio는 사용자의 로컬 장치에서 모델 개발, 연합학습 참여, Agent 구성·검증·Build와 실행·Serving을 연결하는 작업 환경입니다.** 코드와 데이터가 있는 곳에서 학습을 시작하고, 그 결과를 사용자의 목적에 맞는 Agent와 서비스로 이어갈 수 있도록 설계했습니다.

## 왜 Agent Studio가 필요한가

기존 FedOps 1.2에서는 Web에서 Task와 집계 서버를 관리하고, 사용자가 별도의 환경에서 Client를 직접 준비해 실행했습니다. 연합학습을 운영하는 기능은 제공되었지만, 로컬 개발 환경을 준비하고 학습 결과를 실제 사용으로 연결하는 과정에는 사용자의 추가 작업이 필요했습니다.

이 과정에서 함께 다뤄야 할 대상은 코드만이 아닙니다. 같은 Task라도 참여자마다 데이터 위치와 실행 환경이 다르고, 모델을 사용하는 Agent마다 선택한 모델 버전과 Tool, 실행 정책이 다릅니다. 학습 결과를 재사용하려면 이러한 연결 관계를 유지하면서 개발과 실행을 진행할 수 있어야 합니다.

Agent Studio는 이 작업들을 하나의 Workspace와 연결된 메뉴 흐름으로 제공합니다. 사용자는 로컬 모델을 개발하는 Task Owner로 시작할 수도 있고, Registry에 공개된 Task에 참여하는 Participant로 시작할 수도 있습니다. 학습한 모델을 Agent의 구성 요소로 선택하고, 검증한 결과를 자신의 애플리케이션에서 사용하는 흐름도 이어집니다.

## Workspace에서 코드·데이터·실행 환경을 준비하기

Workspace에서는 Task 코드, 로컬 데이터와 Python 실행 환경을 연결합니다. 사용자는 모델과 데이터 처리 코드를 수정하고, 필요한 의존성을 준비한 뒤 자신의 데이터로 Local Train을 수행할 수 있습니다.

Task Owner는 이 과정에서 최초 연합학습의 기준이 되는 **Initiative Model**을 준비합니다. 이후 Release Readiness 검사로 공개 준비 상태를 확인하고, 참여자가 사용할 코드·설정·모델을 Release Candidate로 제출합니다. Task의 최종 공개는 FedOps Web에서 진행합니다.

Release Candidate에는 참여자의 원본 학습 데이터를 포함하지 않습니다. 서버 평가에 필요한 검증 데이터는 Owner가 제공하기로 선택한 경우에 업로드할 수 있습니다. 로컬 학습에 사용하는 데이터와 공유할 검증 데이터를 구분하여 준비하는 구조입니다.

Agent Studio는 Docker 컨테이너로 실행되며, 로컬 Workspace와 데이터, Task별 Python 환경을 연결해 사용합니다. 사용자는 준비된 Studio 실행 환경 안에서 자신의 Task에 필요한 개발과 학습 작업을 진행할 수 있습니다.

## 공개된 Task를 자신의 데이터로 함께 학습하기

Participant는 Studio에서 Registry를 탐색하고, 참여 권한이 있는 Task의 공개 Release를 Workspace에 로드합니다. 자신의 로컬 데이터와 실행 환경을 준비한 뒤 참여 준비 상태를 확인합니다.

**Participation Ready와 Server Live가 모두 충족되면 FL Client를 시작할 수 있습니다.** Client는 학습 기준 모델을 받아 로컬 데이터로 학습하고, 생성된 Model Update를 집계 서버에 전달합니다. 참여자의 원본 학습 데이터는 로컬 환경에 유지됩니다.

사용자는 Studio에서 자신의 Client 진행 상황과 실행 기록, Local Metrics 이력을 확인할 수 있습니다. 데이터를 준비한 환경에서 학습을 실행하고 결과까지 살펴볼 수 있어, 다음 학습을 위해 무엇을 수정해야 하는지 판단하는 데 도움이 됩니다.

이때 FedOps Web은 참여 요청의 승인, Campaign 설정과 FL Server 운영을 담당합니다. Agent Studio는 참여자의 장치에서 코드·데이터·학습 실행을 담당합니다. 두 환경은 같은 Task를 중심으로 연결됩니다.

## 공동으로 학습한 모델을 나만의 Agent로 구성하기

학습한 모델은 Agent에서 전문 기능을 수행하는 **Tool AI Model**로 사용할 수 있습니다. Agent Builder에서는 Base LLM, Tool AI Model과 Agent Harness를 선택·구성합니다. Base LLM에는 일반 LLM이나 Federated LLM을 사용할 수 있고, Tool AI Model에는 원하는 Task의 모델 버전을 선택할 수 있습니다.

![FedOps Agent Studio에서 Base LLM과 Tool AI Model을 선택하는 화면]({{ '/assets/images/v1.3/manual-04/image-3.png' | relative_url }})

예를 들어 운동 정보로 소비 칼로리를 예측하는 모델을 Tool AI로 연결할 수 있습니다. 언어 모델은 사용자의 질문을 해석하고 필요한 상황에서 예측 Tool을 호출한 뒤, 그 결과를 활용해 응답합니다. 언어 모델과 예측 모델이 서로 다른 역할을 맡으면서 하나의 Agent 안에서 함께 동작하는 방식입니다.

이 연결에는 **Agent Harness**가 필요합니다. 어떤 요청에서 어떤 Tool을 사용할지, Tool이 실패했을 때 어떻게 처리할지, 결과를 어떤 방식으로 설명할지 등의 실행 규칙을 구성합니다. 모델 선택과 함께 모델을 사용하는 방식도 정의하는 것입니다.

Agent Builder에서 Agent 구성을 준비한 뒤, 실제 요청에 대한 응답과 Tool 호출 흐름을 확인하고 검증을 진행합니다. 검증한 구성을 Build하면 선택한 모델 버전과 Harness·실행 설정이 해당 Build에 고정됩니다.

## Local Chat에서 확인하고 Serving API로 연결하기

완성한 Agent는 Studio의 Local Chat에서 직접 사용할 수 있습니다. 사용자는 질문에 대한 응답과 실제 Tool 실행을 확인하며, 구성한 Agent가 의도한 작업을 수행하는지 살펴볼 수 있습니다.

Serving API를 활성화하면 자신의 애플리케이션이나 서비스에서 구축한 Agent를 호출할 수 있습니다. 외부 시스템은 API로 요청을 보내고 결과를 받으며, Agent의 추론과 Tool 실행은 Studio를 실행하는 사용자의 환경에서 수행됩니다.

모델 개발과 연합학습으로 얻은 결과를 서비스에 연결할 때, Studio에서 검증하고 Build한 Agent 구성을 이어서 활용할 수 있습니다.

## 사용한 결과를 다음 모델과 Agent 버전으로 이어가기

Agent를 사용하다 보면 개선이 필요한 구성 모델이 있을 수 있습니다. 이때 Task Owner의 주도하에 참여자들은 해당 모델의 **Source Federated Task**로 돌아가 후속 연합학습에 참여합니다. 참여자들의 로컬 학습 결과가 집계되면 새로운 Global Model Version이 Registry에 등록됩니다.

사용자는 새 모델의 결과를 확인하고, Agent 구성에서 사용할 버전을 선택합니다. 변경한 구성을 다시 테스트·검증한 뒤 새로운 Agent Build를 만듭니다.

**새 Global Model이 생성되어도 기존 Agent Build의 모델 버전은 자동으로 바뀌지 않습니다.** 어떤 모델과 설정을 검증해 사용했는지 유지하고, 다음 버전의 적용은 사용자가 결정합니다.

이 개선 과정에서 연합학습의 대상은 Agent를 구성하는 학습 가능한 모델입니다. 여러 Tool AI Model이 연결되어 있다면 각각 자신의 Source Federated Task를 통해 개선할 수 있습니다. Harness의 호출 규칙이나 응답 방식에 문제가 있다면 해당 구성을 수정하고 다시 검증합니다. 운영 중 얻은 데이터도 사용 권한과 활용 범위를 확인한 뒤 후속 로컬 학습에 사용할 수 있습니다.

Studio가 연결하는 흐름은 다음과 같습니다.

**로컬 개발·학습 → 연합학습 참여 → 모델 버전 선택 → Agent 구성·검증·Build → 로컬 실행·Serving → 개선할 구성 모델 선택 → 후속 학습과 새 Agent Build**

## FedOps Agent Studio 시작하기

FedOps Agent Studio는 코드와 로컬 데이터를 준비하는 작업부터, 함께 학습한 모델을 자신의 Agent에 활용하고 다음 버전으로 개선하는 과정까지 연결합니다. 사용자는 모델을 만드는 사람, 학습에 참여하는 사람, 모델을 활용하는 사람으로 같은 환경에서 작업을 이어갈 수 있습니다.

설치와 실행 방법은 [Getting Started]({{ '/v1.3/getting-started/' | relative_url }})에서 확인할 수 있습니다. 자신의 목적에 따라 [Create a New Task]({{ '/v1.3/task-owner/create-task/' | relative_url }}), [Participant: Join & FL]({{ '/v1.3/participant/' | relative_url }}), [Agent Builder & Serving]({{ '/v1.3/agent-builder/' | relative_url }}) 문서로 이어집니다.
