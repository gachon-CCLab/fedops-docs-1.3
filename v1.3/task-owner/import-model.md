---
layout: "default"
title: "Import a Local Model"
nav_order: 2
permalink: "/v1.3/task-owner/import-model/"
docs_version: "1.3"
lang: "ko"
guide_source: "매뉴얼 02_Owner_Local_First_Task (작성 필) 3c95dfbe76bb807793bad650b9e25fec.md"
guide_status: "draft"
parent: "Task Owner"
guide_note: "작성 중: 기존 Local Model 전환 절차는 보완이 필요한 초안입니다."
---

# Import a Local Model
{: .no_toc }

Scenario 02. Local Project를 Federated Task로 전환
{: .fs-5 .fw-400 }

## 대상

이미 PyTorch/Python 모델 프로젝트와 데이터를 보유하고 있고, 기존 개발 흐름을 유지하면서
FedOps Federated Task로 전환하려는 Owner

## 핵심 원칙

Local Project를 Studio에 등록하는 것과 Web의 Federated Task를 만드는 것은 다른 작업이다.

```
Local ML Project
→ Agent Studio에서 원래 개발 계속
→ FedOps contract 연결/검증
→ Web Draft 생성 또는 연결
→ Release Candidate
→ Owner Publish
```

## 절차

#### 1. Local Project 열기

Agent Studio 좌측 메뉴의 Workspace에 들어간다.

![image.png]({{ '/assets/images/v1.3/manual-02/image.png' | relative_url }})

우측 상단 New Federated Task를 클릭한다

![image.png]({{ '/assets/images/v1.3/manual-02/image-1.png' | relative_url }})

Start local Project 시작 동작을 선택한다.

![image.png]({{ '/assets/images/v1.3/manual-02/image-2.png' | relative_url }})

1. 기존 프로젝트를 원래 위치에서 열거나, 명시적으로 Studio Workspace에 import한다.
2. import를 선택한 경우 원본과 Studio copy 중 어느 쪽이 source of truth인지 결정한다.

같은 프로젝트를 여러 번 복사해 서로 다른 source가 생기지 않게 한다.

#### 2. FedOps 계약 적용

기존 코드를 모두 Baseline에 맞춰 다시 작성하지 않는다. 다음 adapter 경계를 연결한다.

- model 생성과 model state load/save
- local dataset loader와 preprocessing
- train/evaluate callback
- Tool AI input/output manifest와 predict hook
- requirements와 Python version

FedOps 관리 entrypoint의 이름과 signature는 바꾸지 않는다.

#### 3. Local Data와 실행 확인

1. 기존 데이터 위치를 Task Data에 연결하거나 필요한 데이터만 배치한다.
2. Python Environment를 sync한다.
3. Local Train으로 Initiative Model을 export한다.
4. Release Readiness와 Participation Readiness를 각각 확인한다.

Release Readiness는 공개 가능한 Task인지, Participation Readiness는 실제 참여 장치에서
local update를 만들 수 있는지를 검사한다.

#### 4. Web identity 연결

다음 중 하나를 선택한다.

- 새 Federated Task Draft를 만들고 현재 `localProjectId`와 연결
- 이미 만든 Web Draft의 `taskId`와 연결

연결 결과는 `localProjectId ↔ taskId` 하나여야 하며 local path를 Web에 저장하지 않는다.

#### 5. Release와 Publish

1. Task Card용 `README.md`를 참여자 관점으로 작성한다.
2. Release Candidate를 제출한다.
3. Web에서 Owner Publish한다.
4. Registry snapshot과 model checksum을 확인한다.

## 완료 조건

- 기존 프로젝트의 로컬 개발이 유지된다.
- 한 local project가 정확히 한 Web Task identity와 연결된다.
- raw dataset은 Release에 포함되지 않는다.
- 다른 사용자가 Published Release로 동일한 실행 코드를 받을 수 있다.

### 주의 사항

- path나 폴더 이름을 `taskId` 대신 사용하지 않는다.
- 기존 프로젝트를 열 때 자동으로 Web Draft를 생성하지 않는다.
- 기존 model artifact를 Initiative Model로 사용하려면 parameter signature와 model manifest
검증을 먼저 통과해야 한다.
