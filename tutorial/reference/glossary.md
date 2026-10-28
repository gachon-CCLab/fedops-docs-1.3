---
layout: default
title: "용어집"
parent: "참고 자료"
grand_parent: "FedOps 튜토리얼"
nav_order: 2
permalink: /v1.3/tutorial/reference/glossary/
docs_version: "1.3"
lang: ko
---

# 용어집
{: .no_toc }

## 역할과 화면

| 용어 | 뜻 |
| --- | --- |
| **Task Owner** | 연합학습을 설계·공개·운영하는 사람. 이 튜토리얼에서는 헝가리 병원 |
| **Client (Participant)** | 공개된 Task 에 참여해 자기 데이터로 로컬 학습을 하는 사람 또는 기관. 이 튜토리얼에서는 클리블랜드 병원 |
| **FedOps Web** | FedOps 홈페이지. 소개와 문서 |
| **FedOps Console** | 웹 작업 화면. Task·Registry·참여자·서버·모니터링 |
| **Agent Studio** | 내 PC 에서 Docker 로 도는 개발 도구. 코드·데이터·학습·참여·Agent |

## FedOps 의 대상

| 용어 | 뜻 |
| --- | --- |
| **Federated Task** | 연합학습의 단위. 모델·전처리·학습 코드·Tool 정의를 담은 코드 묶음 |
| **Web Draft** | Console 에서 만든 직후, 코드가 아직 없는 Task 의 초안 |
| **Workspace** | Studio 안에서 Task 코드와 데이터를 다루는 작업 공간 |
| **Release Candidate** | 점검을 통과해 게시를 기다리는 코드·모델 묶음 |
| **Published Release** | 게시되어 고정된 묶음. 모든 Client 가 이것을 받아 실행한다 |
| **Registry** | 공개된 Task 목록 |
| **Campaign (캠페인)** | 연합학습 한 판. 라운드 수·인원·집계 방식을 정해 실행한다 |
| **Initial Model** | Owner 가 만든 첫 모델. 첫 캠페인의 출발점. 화면에는 **Initiative Model** 로 표시된다 |
| **Global Model vN** | N 번째 캠페인이 끝나 만들어진 모델 |
| **Readiness** | 게시 전(Release) 또는 참여 전(Participation)에 내 PC 에서 하는 자동 점검 |

## 연합학습 개념

| 용어 | 뜻 |
| --- | --- |
| **연합학습 (Federated Learning)** | 데이터를 모으지 않고, 모델을 데이터 쪽으로 보내 학습한 뒤 파라미터만 합치는 학습 방식 |
| **라운드 (Round)** | 서버가 모델을 보내고, Client 들이 학습하고, 서버가 합치는 한 바퀴 |
| **파라미터** | 모델 안의 숫자들. 학습은 이 숫자를 고치는 일이고, 연합학습에서 오가는 것도 이것이다 |
| **집계 (Aggregation)** | 여러 Client 의 파라미터를 하나로 합치는 일 |
| **FedAvg** | 데이터 수에 비례한 가중 평균으로 파라미터를 합치는 기본 집계 방식. FedOps 1.3 에서 고를 수 있는 유일한 방식 |
| **Clients per round** | 한 라운드에서 학습을 마쳐야 하는 Client 수. 이 수가 모일 때까지 서버가 기다린다 |
| **IID / non-IID** | Client 들의 데이터 분포가 같음 / 다름. 현실은 대부분 non-IID. 이 튜토리얼의 두 병원도 non-IID 다 |
| **Client drift** | non-IID 에서 각 Client 의 모델이 자기 데이터 쪽으로 멀어지는 현상 |
| **cross-silo** | 병원·기업처럼 소수의 기관이 참여하는 연합학습. 이 튜토리얼의 상황 |
| **FLamby** | 실제 의료 데이터로 만든 cross-silo 연합학습 벤치마크 모음(NeurIPS 2022). 이 튜토리얼의 병원별 분할은 그중 `Fed-Heart-Disease` 와 같다 |
| **파라미터 서명** | 모델 파라미터의 이름·모양·자료형으로 만든 지문. 모든 참여자의 모델 구조가 같은지 확인하는 데 쓴다 |

## 데이터와 모델

| 용어 | 뜻 |
| --- | --- |
| **UCI Heart Disease** | 병원 4곳(클리블랜드·헝가리·스위스·롱비치 VA)의 심장 검사 기록. 이 튜토리얼의 데이터 |
| **범주 피처** | 숫자로 적혀 있어도 크기 순서가 없는 값. 이 튜토리얼의 `cp`(가슴 통증 유형)와 `restecg`(심전도) |
| **전처리 통계** | 피처별 평균·표준편차와 범주 어휘표. Owner 가 코드에 고정해 모든 참여자가 같은 값을 쓴다 |
| **MLP** | 층을 쌓은 가장 기본적인 신경망. 이 튜토리얼의 모델(`TabularMLP`, 파라미터 1,010개) |
| **F1 DISEASE** | 심장병 환자를 얼마나 잘 잡는지. 이 튜토리얼에서 정확도와 함께 보는 핵심 지표 |

## Agent

| 용어 | 뜻 |
| --- | --- |
| **Tool AI** | Agent 가 숫자(예측)가 필요할 때 부르는 모델. 여기서는 연합학습으로 만든 Global Model |
| **Base LLM** | Agent 에서 문장을 쓰는 언어 모델 |
| **Harness** | Agent 의 LLM 이 지킬 규칙과 실행 설정 |
| **Serving API** | 빌드한 Agent 를 HTTP 로 부를 수 있게 연 것 (전용 포트 + 토큰) |
