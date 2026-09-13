---
layout: "default"
title: "Campaign & Server Management"
nav_order: 6
permalink: "/v1.3/campaign/"
docs_version: "1.3"
lang: "ko"
guide_source: "매뉴얼 05_Operator_Campaing_and_ServerManage 3c95dfbe76bb8049b724f10b68d55622.md"
guide_status: "draft"
guide_note: "검토 중: Campaign 저장과 서버 생성 순서를 확인해야 합니다."
---

# Campaign & Server Management
{: .no_toc }

Scenario 05. Owner/Operator Campaign과 Server Management
{: .fs-5 .fw-400 }

## 대상

Published Federated Task의 연합학습 정책과 Kubernetes 집계 서버를 관리하는 Task Owner.

## 사전 조건

- Task에 Published Release가 있다.
- Initiative Model 또는 이전 Global Model이 사용 가능한 상태다.
- 필요한 Participant가 승인되어 있다.

## 절차

FedOps web에서 Server Management에 들어간다.

![image.png]({{ '/assets/images/v1.3/manual-05/image.png' | relative_url }})

Federated campaign 란 Save capaign을 먼저 클릭해야 Create scalable server를 클릭할 수 있다(확인필요)

![image.png]({{ '/assets/images/v1.3/manual-05/image-1.png' | relative_url }})

Compute resources에서 CPU와 Memory request를 확인한 후 

Server lifecycle에서 Create scalable server를 클릭한다.

> 
> 
> 
> Server lifecycle 기능 
> 
> - Pause: compute resource를 해제하되 필요한 persistent runtime data는 보존한다.
> - Resume: 저장 상태와 정책에 맞게 runtime을 복구한다.

![image.png]({{ '/assets/images/v1.3/manual-05/image-2.png' | relative_url }})

아래 Server logs에서 Refresh logs를 누르게 되면 생성되고 있는 내역을 확인 할 수 있으며, 아래 이미지와 같은 로그가 나오면 생성이 완료된 것 입니다.

![image.png]({{ '/assets/images/v1.3/manual-05/image-3.png' | relative_url }})

정상적으로 생성이 완료되면 Runtime overview에서 Refesh status시 아래 이미지와 같이 표시된다.

> 
> 
> 
> 확인 사항
> 
> - Deployment Ready
> - Pod Running / Ready
> - Service와 현재 endpoint
> - PVC Bound
> - CPU/Memory request
> - FL Server lifecycle
> 
> UI 새로고침을 반복해도 Not allocated라면 K8s resource 생성 결과와 Task runtime key를 확인한다.
> 

![image.png]({{ '/assets/images/v1.3/manual-05/image-4.png' | relative_url }})

Federated campaign(1)에서 연합학습을 수행할 round와 참여 client 수, Aggregation strategy를 선택 후 Save campagin(2)을 클릭한다.

> 
> 
> 
> Client 한 명의 Stop Client는 서버 정책을 자동 축소하지 않는다. 서버는 저장된
> clients-per-round를 유지하고 다른 eligible Client를 기다린다.
> 

saved(3)가 확인되면 Start FL server(4)를 클릭하여 서버를 시작하고 Show live log(5)를 통해 로그를 확인합니다. (Stop server를 통해 프로세스를 종료할 수 있다.)

> 
> 
> 
> **Start FL Server**를 누르면 다음이 원자적으로 연결되어야 한다.
> 
> ```
> Saved Campaign Policy
> → new campaignRunId
> → immutable Run snapshot
> → exact Published Release
> → Initial/previous Global Model
> → FL Server process
> ```
> 
> 새 Run은 Round 1부터 시작해야 하며, 이미 같은 Task의 process가 실행 중이면 중복 Start를 막는다.
> 

![image.png]({{ '/assets/images/v1.3/manual-05/image-5.png' | relative_url }})

live server log에 아래 이미지와 같이

[ROUND 1]

server start by round

가 뜨면 정상적으로 준비가 완료되었다는 뜻이다.

![image.png]({{ '/assets/images/v1.3/manual-05/image-6.png' | relative_url }})

학습이 다 종료되면 FL Server Management가 아래와 같이 변경되며 global model version이 추가된다.

> 
> 
> 
> **종료와 Global Model 정책**
> 
> - 모든 Round가 끝나면 FL Server Python process가 정상 종료되어야 한다.
> - 최종 artifact가 새 Global Model vN으로 등록되어야 한다.
> - 첫 Campaign은 Initiative Model에서 v1을 만든다.
> - 다음 Campaign은 이전 최종 vN에서 vN+1을 만든다.
> - Campaign metric과 Round는 다른 Run과 섞이지 않아야 한다.

![image.png]({{ '/assets/images/v1.3/manual-05/image-7.png' | relative_url }})

Global model  메뉴에서 확인 가능하다.

![image.png]({{ '/assets/images/v1.3/manual-05/image-8.png' | relative_url }})

Monitoring에서 아래 내용을 확인할 수 있다.

> 
> 
> - current Campaign Run과 communication round
> - clients completed/online
> - Global accuracy/loss
> - round duration
> - client를 선택했을 때 허용된 local metric
> - server/pod health와 최신 event 시각
> 
> Agent Studio에는 각 사용자의 자기 Client 상태만 표시되고, Web은 Owner 권한에 맞는 전체 상태를 표시한다.
> 

![image.png]({{ '/assets/images/v1.3/manual-05/image-9.png' | relative_url }})

## 완료 조건

- 저장한 Campaign 값이 Web, Server process와 Agent Studio에 동일하게 표시된다.
- Client는 Task ID로 현재 Run의 올바른 Server에 연결된다.
- Run마다 Round가 1부터 시작한다.
- 완료 후 process가 종료되고 Global Model version이 정확히 한 번 증가한다.
- 다음 Run이 이전 최종 Global Model을 Base Model로 사용한다.
