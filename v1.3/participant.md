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

Participant Join과 Federated Learning
{: .fs-5 .fw-400 }

## 대상

Registry에 공개된 Federated Task에 참여해 자신의 로컬 데이터로 연합학습하려는 사용자를 위한 가이드이다. 참여 요청과 승인, Workspace 준비, Client 실행과 종료까지 다룬다.

## 사전 조건

- [Getting Started]({{ '/v1.3/getting-started/' | relative_url }})에 따라 Agent Studio를 실행하고 참여에 사용할 계정으로 로그인한다.
- 참여할 Task가 Registry에 게시되어 있는지 확인한다.
- Task의 README에서 데이터 형식을 확인하고, 사용할 데이터를 현재 장치에 준비한다.

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

## 종료와 재참여

- 학습 도중 **Stop Client**를 선택하면 현재 장치의 참여를 중단한다. 다른 참여자의 Client나 전체 Campaign을 종료하는 동작은 아니다.
- Client가 중단되어도 서버의 Clients per round 값은 자동으로 줄어들지 않는다. 서버는 저장된 정책에 따라 참여 가능한 다른 Client를 기다린다.
- Campaign이 완료되면 최종 Global Model 수신과 참여 기록을 확인한 뒤 **Finish Client Session**으로 세션을 종료한다. 완료된 참여 기록은 Agent Studio를 다시 실행한 뒤에도 확인한다.
- Client 세션 종료와 Task 탈퇴는 구분한다. 최소 한 번의 완료된 참여를 요구하는 Task는 해당 조건을 충족한 뒤 Leave를 진행한다.
- 탈퇴 후 다시 참여하려면 Join을 요청하고, 참여 상태와 로컬 준비 상태를 다시 확인한다.

## 문제가 발생했을 때

다음 순서로 확인한다. 문제가 해결된 단계에서 Readiness 또는 Client 실행을 다시 시도한다.

1. **참여 권한:** 참여 상태가 Approved인지, 승인받은 계정으로 Studio에 로그인했는지 확인한다.
2. **Task 연결:** Workspace의 `taskId`가 참여하려는 Registry Task와 같은지 확인한다.
3. **로컬 준비:** Python 환경과 데이터 배치가 Task의 요구사항에 맞는지 확인한다. 데이터를 변경했다면 Participation Readiness를 다시 실행한다.
4. **서버 상태:** Server가 Live인지, 현재 Campaign Run이 시작되었는지 확인한다. 서버가 대기 중이면 Owner에게 실행 상태를 확인한다.
5. **연결 오류:** Client 로그에서 해당 Task의 현재 서버 endpoint에 연결하고 있는지 확인한다.
6. **모델 호환성:** 파라미터 구조나 모델 형식 오류가 있으면 사용 중인 Release와 모델 버전을 확인한다. 오류가 계속되면 Task ID, 버전과 오류 로그를 Owner에게 전달한다.
