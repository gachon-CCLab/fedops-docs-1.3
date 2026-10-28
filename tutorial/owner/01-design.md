---
layout: default
title: "1. 설계하기"
parent: "Task Owner 트랙"
grand_parent: "FedOps 튜토리얼"
nav_order: 1
permalink: /v1.3/tutorial/owner/design/
docs_version: "1.3"
lang: ko
---

# 1. 설계하기
{: .no_toc }

{: .note }
> 📍 **지금 어디:** Task Owner 1/7 — **① 설계** → ② Task 만들기 → ③ Workspace → ④ 학습·게시 → ⑤ 승인 → ⑥ 캠페인 → ⑦ 결과<br> 다음: Console 에서 Task 를 만든다

{: .important }
> 🎯 **이 단계에서 하는 일:** FedOps 를 켜기 전에, 한 PC 에서 평범하게 학습을 돌려 **이 데이터와 모델 조합이 실제로 배우는지** 확인합니다. 그리고 병원 한 곳 데이터만으로는 왜 부족한지를 숫자로 봅니다. 연합학습은 디버깅이 어렵습니다. 모델이 애초에 배우지 못하는 문제를 연합학습 단계에서 발견하면 원인 찾기가 훨씬 힘듭니다.

1. TOC
{:toc}

## 1) 병원별 데이터 만들기

템플릿의 `data/uci/` 에 UCI 원본 파일 4개(병원마다 1개)가 들어 있습니다. `prepare_data.py` 는 이 파일을 **새로 나누지 않고** 병원별로 정리만 합니다.

```bash
cd data
pip install numpy pandas
python prepare_data.py
```

```txt
hungarian: 원본 294행 → 결측 행을 빼고 261행
cleveland: 원본 303행 → 결측 행을 빼고 303행

출력: out
  hungarian/dataset.csv          261행   no_disease=163(62%) disease=98(38%)
  cleveland/dataset.csv          303행   no_disease=164(54%) disease=139(46%)
  train.csv (hungarian+cleveland)   373행   no_disease=216(58%) disease=157(42%)
  test.csv  (hungarian+cleveland)   191행   no_disease=111(58%) disease=80(42%)
```

| 파일 | 쓰임 |
| --- | --- |
| `out/hungarian/dataset.csv` | **Owner(헝가리 병원)의 로컬 데이터.** 3장에서 Studio 의 Data Folder 에 넣는다 |
| `out/cleveland/dataset.csv` | Client(클리블랜드 병원)의 로컬 데이터. Client 가 자기 PC 에서 같은 명령으로 만든다. Owner 는 쓰지 않는다 |
| `out/<병원>/train.csv`, `test.csv` | 그 병원 데이터를 학습용 66% / 평가용 34% 로 나눈 것. 아래 3) 에서 "병원 한 곳만으로 학습"할 때 쓴다 |
| `out/train.csv`, `test.csv` | 두 병원의 train / test 를 합친 것. 아래 2) 의 "데이터를 모을 수 있다면" 기준선 |

### ⚙️ 옵션 해설 — `prepare_data.py`

| 값 | 기본 | 무엇이 달라지나 |
| --- | --- | --- |
| `--hospitals` | `hungarian,cleveland` | 만들 병원. `va` 를 더하면 세 번째 참여자용 데이터가 생긴다. `switzerland` 는 심장병 없는 환자가 1명뿐이라 오류로 막힌다(클래스마다 3행 이상 필요) |
| `--test-size` | 0.34 | 병원마다 떼어 둘 평가 비율. FLamby 와 같은 값. `dataset.csv` 에는 영향이 없다(항상 그 병원 전부) |
| `--seed` | 43 | train / test 를 나누는 난수 시드. 역시 `dataset.csv` 에는 영향이 없다 |

> Owner 와 Client 가 다른 옵션으로 만들어도 **각자의 `dataset.csv` 는 같습니다.** 병원 파일을 정리만 하기 때문입니다.

<details markdown="1">
<summary>📚 연합학습 배경 — IID 와 non-IID</summary>

**IID**(independent and identically distributed)는 모든 기관의 데이터가 같은 분포에서 뽑혔다는 뜻입니다. 이 경우 각 client 의 학습 방향이 비슷해서, 평균을 내도 전체 데이터로 학습한 것과 거의 같아집니다.

**non-IID** 에서는 각 client 가 자기 데이터 쪽으로 모델을 당깁니다. 헝가리 병원(심장병 38%)과 클리블랜드 병원(46%)은 비율뿐 아니라 환자 나이·검사 값 분포도 다릅니다. VA 병원(78%)을 더하면 차이가 훨씬 커집니다. 이 방향들을 평균하면 어느 쪽에도 딱 맞지 않을 수 있고, 라운드가 더 많이 필요하거나 정확도가 덜 오를 수 있습니다. 이를 줄이려는 연구가 FedProx, SCAFFOLD, FedBN 등입니다. FedOps 1.3 에서 고를 수 있는 집계 방식은 FedAvg 하나입니다([6장]({{ '/v1.3/tutorial/owner/campaign/' | relative_url }})).

</details>

## 2) 일반 학습 (FedOps 없이)

한 PC 에서 도는 평범한 PyTorch 학습입니다. 기본값은 **두 병원 데이터를 모두 모은** `out/train.csv` 로 학습합니다. 현실에서는 할 수 없는 "모을 수 있다면"의 기준선입니다. 다음 단계부터 이 코드를 FedOps 모양으로 옮깁니다.

```bash
cd ../centralized
pip install -r requirements.txt
python train_centralized.py
```

```txt
데이터: train 373행 / test 191행, 입력 10차원, 2클래스
학습 시작 (epochs=30, batch_size=32, lr=0.001)
  epoch   1/30  train_loss=0.7064
  ...
  epoch  30/30  train_loss=0.4109

test accuracy = 0.796   f1_macro = 0.789   loss = 0.4561
  (무작위로 찍으면 accuracy 약 0.50, 가장 많은 클래스만 찍으면 약 0.58)
  confusion matrix (행=실제, 열=예측):
                  no_disease     disease
      no_disease          93          18
         disease          21          59
```

(2026-10-20 실측, torch 2.2.2. 학습에는 무작위 요소가 있어 환경에 따라 숫자가 조금 다를 수 있습니다)

**accuracy 0.796** — "전부 심장병 없음으로 찍기"(0.58)보다 확실히 높으니 모델이 배웠습니다. 틀린 39건 가운데 21건은 심장병 환자를 "없음"으로 놓친 경우입니다. 의료에서는 심장병 환자를 놓치는 실수가 더 위험해서, 이 튜토리얼은 정확도와 함께 **F1 DISEASE**(심장병을 얼마나 잘 잡는지)를 계속 봅니다.

### ⚙️ 옵션 해설 — 학습 설정

`train_centralized.py` 의 인자이자, 나중에 Federated Task 의 `config.yaml` → `local_training` 에 들어가는 값입니다.

| 값 | 기본 | 바꾸면 | 이 튜토리얼의 선택 |
| --- | --- | --- | --- |
| `--epochs` | 30 | 늘리면 데이터를 더 여러 번 봐서 손실이 더 내려가지만, 너무 많으면 학습 데이터에만 맞는 과적합이 생긴다 | 30 — 이 데이터 크기에서 충분히 수렴함 |
| `--learning-rate` | 0.001 | 크면 빠르지만 불안정, 작으면 안정적이지만 느리다 | 0.001 — Adam 의 통상값 |
| `--batch-size` | 32 | 크면 한 번에 많이 보고 덜 흔들림, 작으면 자주 고침 | 32 — 병원 한 곳(170행 안팎)에서도 배치가 여러 개 나옴 |
| `--data-root` | `../data/out` | `train.csv` / `test.csv` 를 읽을 폴더 | 아래 3) 에서 병원 폴더로 바꿔 본다 |

## 3) 병원 한 곳만으로 학습하면?

연합학습이 왜 필요한지 확인합니다. Owner 의 헝가리 데이터만으로 학습합니다.

```bash
python train_centralized.py --data-root ../data/out/hungarian --out out/hungarian
```

```txt
데이터: train 173행 / test 88행, 입력 10차원, 2클래스
...
test accuracy = 0.761   f1_macro = 0.752   loss = 0.4622
  (무작위로 찍으면 accuracy 약 0.50, 가장 많은 클래스만 찍으면 약 0.62)
```

이번 실행은 헝가리 test(88행)에서 0.761 이었습니다. 위 2) 의 0.796 은 두 병원 test 를 합친 것에서 잰 값이라 그대로 비교할 수는 없습니다. 같은 헝가리 test 로 맞춰 비교하면 아래와 같습니다.

| 학습 데이터 | 헝가리 test accuracy |
| --- | --- |
| 헝가리만 (173행) — **Owner 혼자** | 약 0.76 |
| 헝가리 + 클리블랜드 (373행) — **모을 수 있다면** | 약 0.79 |

(2026-10-20 시뮬레이션, 시드 20개 평균)

데이터가 적을수록 성능이 떨어집니다. 하지만 병원들은 데이터를 모을 수 없습니다. **병원 한 곳의 성능과 "모을 수 있다면" 사이의 간격을, 데이터를 옮기지 않고 좁히는 것**이 연합학습의 목표입니다. 이 튜토리얼에서는 Owner(헝가리)와 Client(클리블랜드) 두 병원이 함께 학습합니다.

> **간격이 작아 보여도 괜찮습니다.** 이 데이터에서는 두 병원을 모아도 몇 %p 차이입니다. 이 튜토리얼에서 볼 것은 숫자의 크기가 아니라 FedOps 로 연합학습이 **어떻게 돌아가는지**입니다.

## 4) 전처리 통계도 약속의 일부

학습 때 계산한 피처별 평균·표준편차와 범주 어휘표(전처리 통계)는 `out/preprocessing.json` 에 따로 저장됩니다. 같은 입력이라도 이 값이 다르면 모델이 다르게 받아들이므로, **Owner 의 학습 · 모든 Client 의 학습 · Agent 추론이 모두 같은 값**을 써야 합니다.

> 각 병원이 자기 데이터로 평균을 따로 내면, 같은 환자도 병원마다 다른 숫자로 바뀌어 모델에 들어갑니다. 그래서 FedOps 템플릿은 Owner 가 정한 통계를 **코드 안에 고정**해 모든 참여자에게 같이 배포합니다(3장의 `embed_preprocessing.py`).

## ✅ 체크리스트

- [ ] `data/out/` 에 `hungarian/dataset.csv` 가 있다
- [ ] 일반 학습의 test accuracy 가 0.58 보다 확실히 크다
- [ ] 병원 한 곳만 쓰면 성능이 떨어지는 것을 봤다

## 안 되면

| 증상 | 조치 |
| --- | --- |
| `train.csv 가 없다` | `prepare_data.py` 를 먼저 실행 |
| `원본 파일이 없다` | `template/data/uci/` 에 `processed.*.data` 4개가 있는지 확인. ZIP 으로 받았다면 압축을 다 풀었는지 확인 |
| `클래스마다 3행 이상이어야 …` | `--hospitals` 에 `switzerland` 를 넣었다. 다른 병원을 고른다 |
| torch 설치 실패 | Python 3.13 이면 3.12 로. Intel Mac 은 torch 2.2.2 까지만 있다(허용 범위 안) |
| accuracy 가 0.58 근처 | `python train_centralized.py --epochs 60` |

## 다음 단계

[2. Task 만들기]({{ '/v1.3/tutorial/owner/create-task/' | relative_url }}) — 설계한 내용을 FedOps 에 "이런 연합학습을 하겠다"고 등록합니다.
