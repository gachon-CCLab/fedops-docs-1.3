---
layout: "default"
title: "Create a New Task"
nav_order: 1
permalink: "/v1.3/task-owner/create-task/"
docs_version: "1.3"
lang: "ko"
guide_source: "매뉴얼 01_Owner_Web_First_Task 3c95dfbe76bb802180e5f00dd9ab12f0.md"
guide_status: "draft"
parent: "Task Owner"
guide_note: "검토 중: Web Draft 정의 등 원문의 작성 메모가 남아 있습니다."
---

# Create a New Task
{: .no_toc }

Scenario 01. Web Draft에서 Registry Publish까지
{: .fs-5 .fw-400 }

## 대상

FedOps Web에서 새 Federated Task를 만든 뒤 Agent Studio에서 구현하려는 Task Owner.

## 사전 조건

- [Getting Started]({{ '/v1.3/getting-started/' | relative_url }})의 설치·실행 과정을 완료
- FedOps Web 계정으로 로그인
- Agent Studio가 같은 FedOps 계정으로 로그인
- Agent Studio Workspace가 host에 연결
- 사용할 raw dataset은 로컬 장치에 준비

## 절차

### 1. FedOps Web에서 Federated Task 생성

> 이 단계에서 Task는 아직 Registry에 공개되지 않는다. 
Dataset 경로, model architecture, preprocessing과 local-training 값은 Agent Studio에서 실제 코드와 데이터를 연결하며 완성한다.
연합학습 Round, Clients per round와 aggregation strategy는 이후 Server Management의 Campaign에서 설정한다.
> 

https://ccl.gachon.ac.kr/fedops

FedOps Web에 로그인 후 My Federated Tasks에 들어간다.

![image.png]({{ '/assets/images/v1.3/manual-01/image.png' | relative_url }})

Create Federated Task를 클릭한다.

![image.png]({{ '/assets/images/v1.3/manual-01/image-1.png' | relative_url }})

이미지의 예시를 참고하여 생성한다. (FedOps 1.3을 선택한다)

![image.png]({{ '/assets/images/v1.3/manual-01/image-2.png' | relative_url }})

- 각 항목에 대한 상세 설명
    
    
    | 항목 | 설명 |
    | --- | --- |
    | **Creation Mode** | Federated Task를 생성할 방식을 선택 <br>FedOps 1.3에서는 Federated Task(FedOps 1.3)가 기본, 기존 FedOps 1.2 workflow를 사용하는 경우에만 Legacy 방식을 선택 |
    | **Federated Task Name** | 사용자가 알아보기 쉬운 Federated Task의 이름 입력<br>(모델과 학습 관련 세부 내용은 이후 Agent Studio에서 구성) |
    | **Registry ID** | Registry에서 Task 식별 ID 입력 |
    | **Primary Model working name** | Task에서 사용할 Primary Model의 작업용 이름을 입력<br>최종 Registry model name은 Release 전에 Agent Studio에서 확정 |
    | **Model role** | Release된 모델을 Agent Builder에서 어떤 역할로 사용할지 지정 |
    | **Task category** | Task가 수행하는 작업 유형을 선택 예: Classfication |
    | **Data modality** | 모델이 처리하는 데이터 유형을 선택 예: Image |
    | **Public summary** | Registry 등에서 Task를 이해할 수 있도록 목적과 기능 설명 |
    | **Federated Task tags** | Registry에서 Task를 검색하거나 구분할 때 사용할 태그 입력 |
    | **Visibility** | Registry에서의 공개 범위 설정 |
    | **Participation** | 다른 사용자가 이 Federated Task에 참여하는 방식 설정 |

생성을 완료하고 Web Draft가 만들어졌는지 확인한다.

<aside>
💡

Web Draft가 뭔데요? 설명 및 정의 필요

</aside>

### 2. FedOps Agent Studio에서 Task Workspace 준비

#### 2.1 Web Draft 열기

Agent Studio 좌측 메뉴의 Workspace에 들어간다.

![image.png]({{ '/assets/images/v1.3/manual-01/image-3.png' | relative_url }})

우측 상단 New Federated Task를 클릭한다.

![image.png]({{ '/assets/images/v1.3/manual-01/image-4.png' | relative_url }})

My Web Draft에서, 방금 FedOps Web에서 생성한 Task를 선택한다.

![image.png]({{ '/assets/images/v1.3/manual-01/image-5.png' | relative_url }})

#### 2.2 Python Environment

생성된 project를 클릭하여 들어간 후 Python Environment에 들어간다.

선택한 Python 환경의 Sync를 먼저 실행한다.

(이때 필요에 따라 라이브러리를 추가, 수정, 제거한다.)

![image.png]({{ '/assets/images/v1.3/manual-01/image-6.png' | relative_url }})

### 3. Task 코드와 로컬 데이터 준비

#### 3.1 Task 코드 확인 및 수정

workspace의 code 메뉴에서는 Federated Task의 코드를 확인하고 수정할 수 있다.

Task 작성자는 이 영역에서 자신의 모델, 데이터 전처리 및 학습 코드를 작성하여 자신만의 모델을 로컬 학습 테스트하고, Federated Task를 구성한다.

![image.png]({{ '/assets/images/v1.3/manual-01/image-7.png' | relative_url }})

주요 코드 작성 방법과 수정 가능한 파일, 고정 함수 계약은 Federated Task Developer Guide에서 설명한다. 

[Federated Task Developer Guide]({{ '/v1.3/developer-guide/' | relative_url }}) 

#### 3.2 로컬 데이터 연결

workspace의 Task Test 메뉴로 이동한다.

Open Data Folder를 클릭한다.

![image.png]({{ '/assets/images/v1.3/manual-01/image-8.png' | relative_url }})

해당 task 전용 Data Folder 위치의 파일 탐색기가 열리는데 task에서 요구하는 데이터를 넣는다.
(이때 path를 코드와 맞춰야한다) 

![image.png]({{ '/assets/images/v1.3/manual-01/image-9.png' | relative_url }})

데이터를 넣은 후엔 refresh를 눌러 Agent Studio가 데이터 상태를 다시 확인하도록 한다. 

### 4. Local Train 및 Release 준비

1. Task Test에서 **Local Train & Export Model**을 실행한다.
이 단계에서 로컬 데이터를 통해 모델을 학습하고 Model Release에 사용할 초기 모델을 생성한다.
2. 로컬 학습이 완료되면 **Check Release Readiness**를 실행한다.
Release에 필요한 Task 계약과 구성이 준비되었는지 검사하는 단계로 정상 완료 되어야 진행 가능한다.
3. 검사가 완료되면 **Submit Release Candidate**를 실행한다.
Registry에 게시할 Release Candidate를 준비한다.

![image.png]({{ '/assets/images/v1.3/manual-01/image-10.png' | relative_url }})

### 5. Registry에 Federated Task 게시

FedOps Web에서 작업한다.

해당하는 Task Management의 Registry Release로 이동하여 방금 준비한 Task를 Registry에 게시한다.

![image.png]({{ '/assets/images/v1.3/manual-01/image-11.png' | relative_url }})

게시된 Federated Task는 Registry에서 확인할 수 있다.

### 6. Federated Task 참여자 관리

FedOps web에서 진행된다.

Registry에 Federated Task가 게시되면 다른 사용자는 해당 Task에 대한 참여를 요청할 수 있다.

![image.png]({{ '/assets/images/v1.3/manual-01/image-12.png' | relative_url }})

Task Owner는 Task Management의 Participants 메뉴에서 참여 요청과 승인된 사용자를 관리한다.

task owner는 participants에 들어가 Approve 여부를 선택한다.

![image.png]({{ '/assets/images/v1.3/manual-01/image-13.png' | relative_url }})

참여를 수락하면 아래와 같이 변한다.

![image.png]({{ '/assets/images/v1.3/manual-01/image-14.png' | relative_url }})

## 다음 단계

- 집계 서버 시작: [Campaign & Server Management]({{ '/v1.3/campaign/' | relative_url }})
- 다른 사용자 참여: [Participant: Join & FL]({{ '/v1.3/participant/' | relative_url }})
- Agent 제작: [Agent Builder & Serving]({{ '/v1.3/agent-builder/' | relative_url }})
