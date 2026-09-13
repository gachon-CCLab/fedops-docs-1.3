---
layout: "default"
title: "Getting Started"
nav_order: 2
permalink: "/v1.3/getting-started/"
docs_version: "1.3"
lang: "ko"
guide_source: "매뉴얼 00_Getting_Started 3c95dfbe76bb80d483a4e339bad741ef.md"
guide_status: "draft"
---

# Getting Started
{: .no_toc }

시작하기: FedOps Agent Studio 설치와 Federated Task 생성
{: .fs-5 .fw-400 }

> FedOps 1.3을 처음 사용하는 사용자가 Agent Studio를 실행하고 첫 Federated Task를
생성하는 데 필요한 공통 준비 절차이다
> 

## 절차

### 1.준비사항

FedOps Agent Studio는 Docker 컨테이너로 실행된다. 먼저 다음 환경을 준비한다.

- macOS·Windows: [Docker Desktop](https://www.docker.com/products/docker-desktop/) 설치 및 실행
- Linux: Docker Engine 또는 Docker Desktop 설치 및 실행
- Python과 `pip`
- FedOps Web 계정

### 2. 예제와 테스트 데이터

처음 기능을 확인할 때는 다음 예제를 사용할 수 있다.

##### Federated Task 예제

- MNIST 숫자 분류
- 운동 후 소모 칼로리 예측
- WESAD 스트레스 예측

[예제와 테스트 데이터 받기](https://drive.google.com/drive/folders/1T2lposEnkvVzbv2DMVNs-eqyGJ9A7_EL?usp=sharing)

##### 5개 Client 연합학습 테스트 데이터

[Client별 분할 데이터 받기](https://drive.google.com/drive/folders/1wEYIQuIWUeCifh9rUZEJcndiAVQa0Jtn?usp=sharing)

예제 데이터는 기능 확인용이다. 원본 데이터는 FedOps Web에 업로드하지 않고 각 Client의
Agent Studio 로컬 데이터 폴더에 둔다.

### 3. FedOps Agent Studio 실행

터미널에서 FedOps Python 패키지를 최신 버전으로 설치하거나 업데이트한다.

```bash
pip install -U fedops
```

설치가 끝나면 Agent Studio를 실행한다.

```bash
fedops run agent-studio
```

실행 명령은 다음 작업을 자동으로 수행한다.

1. Docker 실행 상태를 확인한다.
2. 현재 장치에 맞는 최신 Agent Studio 이미지를 준비한다.
3. 사용자 Workspace를 연결하고 컨테이너를 실행한다.
4. Agent Studio 화면을 브라우저에서 연다.

![image.png]({{ '/assets/images/v1.3/manual-00/image.png' | relative_url }})

Agent Studio 로그인 화면이 열리면 FedOps Web에서 사용하는 계정으로 로그인한다.

사용을 마친 뒤에는 다음 명령으로 종료한다.

```bash
fedops stop agent-studio
```

이 명령은 Agent Studio 컨테이너를 중지한다. Host에 연결된 Workspace, Task Data, Python 환경과
작업 기록은 삭제하지 않는다.

## 다음 단계

- 직접 Web Draft를 생성하여 개발하려면 [Create a New Task]({{ '/v1.3/task-owner/create-task/' | relative_url }}) 문서를 따른다.
- 다른 사용자가 공개한 Task에 참여하려면 [Participant: Join & FL]({{ '/v1.3/participant/' | relative_url }}) 문서를 따른다.
