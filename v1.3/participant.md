---
layout: "default"
title: "Participant: Join & FL"
nav_order: 4
permalink: "/v1.3/participant/"
docs_version: "1.3"
lang: "ko"
guide_source: "매뉴얼 03_Participant_Join_and_FederatedLearning 3c95dfbe76bb803299c8c8da55fab8f6.md"
guide_status: "draft"
---

# Participant: Join & FL
{: .no_toc }

Scenario 03. Participant Join과 Federated Learning
{: .fs-5 .fw-400 }

## 대상

Registry의 Federated Task에 참여해 자신의 로컬 데이터로 연합학습하려는 사용자

## 사전 조건

- Task가 Public Registry에 Published 상태로 존재한다.
- Agent Studio가 참여에 사용할 FedOps 계정으로 로그인되어 있다.
- 참여할 데이터는 현재 장치에 있다.

## 절차

### 1. Federated Task 참여

task 참여는 Web에서와 studio에서 동일한 작업을 수행할 수 있다. 둘 중 하나만 진행하면 된다.

#### 1.1 FedOps Web에서 Federated Task 참여

https://ccl.gachon.ac.kr/fedops

FedOps Web에 로그인 후 Registry에 들어간다.

![image.png]({{ '/assets/images/v1.3/manual-03/image.png' | relative_url }})

참여하고자 하는 task를 선택하여 들어가면 Federated Learning에 참여할 수 있다.

![image.png]({{ '/assets/images/v1.3/manual-03/image-1.png' | relative_url }})

누르게 되면 task owner가 참여를 수락하기 전까지 아래와 같이 표시된다.

(승인 전에는 참여 전용 Files & Versions와 Workspace import를 사용할 수 없어야 한다)

![image.png]({{ '/assets/images/v1.3/manual-03/image-2.png' | relative_url }})

#### 1.2 FedOps Agent Studio에서 Federated Task 참여

registry의 Public Registry에서 원하는 task 선택 후 Request to join을 선택한다.

![image.png]({{ '/assets/images/v1.3/manual-03/image-3.png' | relative_url }})

task owner가 참여를 수락하기 전까지 아래와 같이 표시된다.

![image.png]({{ '/assets/images/v1.3/manual-03/image-4.png' | relative_url }})

### 2. FedOps Agent Studio에서 Task Workspace 준비

Task Owner가 참여를 수락하면 아래 과정을 진행할 수 있다.

#### 2.1 Web Draft 열기

Web Draft를 여는 데에는 두가지 방법이 있다.

##### 2.1.1 Registry에서 열기

Fedops Agent Studio에서 registry의 Public Registry 중 원하는 task를 선택해 open in workspace를 선택한다.

![image.png]({{ '/assets/images/v1.3/manual-03/image-5.png' | relative_url }})

##### 2.1.2 Workspace에서 열기

Agent Studio 좌측 메뉴의 Workspace에 들어간다.

![image.png]({{ '/assets/images/v1.3/manual-03/image-6.png' | relative_url }})

우측 상단 New Federated Task를 클릭한다.

![image.png]({{ '/assets/images/v1.3/manual-03/image-7.png' | relative_url }})

Joined Registry Task에서, 참여 수락된 Task를 선택한다.

![image.png]({{ '/assets/images/v1.3/manual-03/image-8.png' | relative_url }})

#### 2.2 Python Environment

생성된 project를 클릭하여 들어간 후 Python Environment에 들어간다.

선택한 Python 환경의 Sync를 실행한다.

![image.png]({{ '/assets/images/v1.3/manual-03/image-9.png' | relative_url }})

### 3. Task 코드와 로컬 데이터 준비

#### 3.1 Task 코드 확인

Participant는 FedOps 관리 파일을 수정하지 않는다. Owner source 변경이 필요하면 새 Release가 필요하다.

#### 3.2 로컬 데이터 연결

workspace의 Task Test 메뉴로 이동한다.

Open Data Folder를 클릭한다.

![image.png]({{ '/assets/images/v1.3/manual-03/image-10.png' | relative_url }})

해당 task 전용 Data Folder 위치의 파일 탐색기가 열리는데 task에서 요구하는 데이터를 넣는다.
(이때 path를 코드와 맞춰준다) 

![image.png]({{ '/assets/images/v1.3/manual-03/image-11.png' | relative_url }})

데이터를 넣은 후엔 refresh를 눌러 Agent Studio가 데이터 상태를 다시 확인하도록 한다. 

### 4. Federated Learning

> 
> 
> 
> Client는 화면을 이동해도 background에서 계속 실행된다. 따라서 서로 다른 Task의 Client는 동시에 실행할 수 있지만 같은 Task의 Client를 중복 시작하면 안된다.
> 

Federated Learning에서 해당 task를 선택한다. 이때 **Server live**를 확인한다.

![image.png]({{ '/assets/images/v1.3/manual-03/image-12.png' | relative_url }})

dataset을 넣어두지 않은 경우 Open Data Folder를 눌러 task에 맞는 dataset을 폴더에 넣고 
Check Participation Readiness(workspace에서도 가능하다)를 눌러 검증한 후 Start Client를 통해 연합학습에 참여한다.

![image.png]({{ '/assets/images/v1.3/manual-03/image-13.png' | relative_url }})

※ 검증 단계에서 문제가 생기면 어느 부분이 갖추어지지 않았는지 확인할 수 있다.

![image.png]({{ '/assets/images/v1.3/manual-03/image-14.png' | relative_url }})

> Participation Readiness시 Server availability는 local code/data readiness와 별도 상태로 확인합니다. 서버가 꺼져 있어도 로컬 준비 자체는 완료할 수 있다.
> 

학습이 끝나면 Finish Client Session을 눌러준다.

![image.png]({{ '/assets/images/v1.3/manual-03/image-15.png' | relative_url }})

#### 종료와 재참여 정책

- 진행 중 **stop client**는 이 장치의 참여만 즉시 중단한다
- Server는 저장된 clients-per-round 정책을 유지하고 다른 eligible Client를 기다린다.
- Campaign 완료 후 최종 Global Model을 받은 것을 확인하고 Client session을 종료한다.
- 참여 탈퇴 정책이 적용된 Task는 최소 한 번의 완료된 FL 참여 후 Leave할 수 있다.
- 이후 다시 Join 요청을 보낼 수 있다.

### 완료 조건

- Client가 Task ID로 올바른 집계 서버에 연결된다.
- raw dataset이 Web으로 업로드되지 않는다.
- Round별 local metric과 model flow가 실시간으로 갱신된다.
- 완료된 참여 history가 Agent Studio 재시작 후에도 남아 있다.
- Web Monitoring에는 전체/허용된 client metric이, Studio에는 내 Client metric만 표시된다.

### 실패 시 확인 순서

1. 참여 상태가 **approved**인지 확인한다.
2. Workspace의 taskId와 Registry Task가 같은지 확인한다.
3. data fingerprint 변경 후 Readiness를 다시 실행했는지 확인한다.
4. Server가 Live이고 Campaign Run이 생성됐는지 확인한다.
5. taskId가 현재 runtime endpoint와 일치하는지 확인한다.
6. parameter signature/model format compatibility 오류를 확인한다.
