---
layout: default
title: "3. 준비하기"
parent: "공통 기초"
grand_parent: "FedOps 튜토리얼"
nav_order: 3
permalink: /v1.3/tutorial/basics/setup/
docs_version: "1.3"
lang: ko
---

# 3. 준비하기
{: .no_toc }

{: .note }
> 📍 **지금 어디:** 공통 기초 3/3 — ① 연합학습과 FedOps → ② 데이터와 모델 → **③ 준비하기** → 다음: 내 역할의 트랙

{: .important }
> 🎯 **이 단계에서 하는 일:** 내 PC 에 Agent Studio 를 띄우고, Studio 와 FedOps Console 에 로그인하고, 실습 템플릿을 받습니다. **Owner 와 Client 모두** 해야 합니다. 학습은 서버가 아니라 각자의 PC(Studio)에서 일어나기 때문입니다.

1. TOC
{:toc}

## 1) 사양 확인

```bash
python3 --version    # 3.10 ~ 3.12 이어야 함
```

- 메모리 16 GB 권장 (Studio 컨테이너 + CPU LLM 이 함께 동작. LLM 은 모델 활용 트랙에서만 씀)
- 디스크 20 GB 이상 여유
- 인터넷 연결 필요 (Docker 이미지·패키지·LLM 다운로드)

## 2) Docker Desktop 설치

[Docker Desktop](https://www.docker.com/products/docker-desktop/) 을 설치하고 실행해 둡니다. Linux 는 Docker Engine + compose 플러그인이면 됩니다.

{% raw %}
```bash
docker version --format '{{.Server.Version}}'
docker compose version
```
{% endraw %}

{: .highlight }
> **최신 Docker 를 쓰세요.** Docker 20.10 같은 오래된 버전에서는 이미 떠 있는 Studio 를 `fedops` 명령이 멈추지 못합니다(`unknown flag: --timeout`).

## 3) Agent Studio 실행

```bash
python3 -m venv ~/.venvs/fedops && source ~/.venvs/fedops/bin/activate
pip install -U fedops
fedops run agent-studio
```

브라우저에 Studio([http://localhost:24368](http://localhost:24368))가 열리면 성공입니다. 처음에는 Docker 이미지를 받느라 몇 분 걸립니다.

{: .note }
> **Intel Mac** 에서 `pip install -U fedops` 가 `llvmlite` 빌드 오류로 실패하면 `pip install --no-deps fedops` 로 설치하세요.

끝낼 때는 `fedops stop agent-studio` 입니다. Studio 는 `~/fedops-workspace/` 아래에 코드와 **로컬 데이터**를 둡니다. 이 폴더는 지우지 마세요.

> **왜 Studio 는 내 PC 에서 도나요?** 연합학습에서 데이터는 내 PC 를 떠나지 않아야 합니다. 그래서 학습·점검·참여는 전부 내 PC 의 Studio 에서 하고, 웹(Console)에서는 데이터가 필요 없는 일(공개·승인·서버 운영)만 합니다.

## 4) 계정과 로그인

**계정**은 FedOps Console 로그인 화면의 **Create account** 에서 만듭니다. 하나의 FedOps 계정으로 Console 과 Studio 에 모두 로그인합니다.

| 하려는 것 | 필요한 계정 |
| --- | --- |
| 한 역할만 | 1개 |
| 혼자서 두 역할 연습 (Owner 가 자기 Task 에 참여) | 1개 |
| Owner 와 Client 를 **나눠서** (참여 요청·승인까지 경험) — **이 튜토리얼의 기준** | **2개** — Owner 용, Client 용 |

로그인은 **두 곳에 따로** 합니다.

1. Agent Studio 첫 화면에서 FedOps 계정으로 로그인
2. 브라우저에서 FedOps Console 에도 로그인 — FedOps Web([https://ccl.gachon.ac.kr/fedops](https://ccl.gachon.ac.kr/fedops)) 오른쪽 위 **Open Console**, 또는 [https://ccl.gachon.ac.kr/fedops/console](https://ccl.gachon.ac.kr/fedops/console)

> Studio 와 Console 은 로그인이 공유되지 않습니다. 두 계정을 쓸 때는 **Studio 와 Console 이 같은 계정**인지 늘 확인하세요. 다르면 "내 Task 가 안 보인다"는 문제가 납니다.

## 5) 실습 템플릿 받기

```bash
git clone https://github.com/gachon-CCLab/FedOps-hands-on-guide.git
cd FedOps-hands-on-guide/template
```

이후 명령은 모두 이 `template/` 폴더를 기준으로 합니다. git 이 없으면 GitHub 페이지의 **Code → Download ZIP** 으로 받아 풀어도 됩니다.

| 역할 | 템플릿에서 쓰는 것 |
| --- | --- |
| Owner | 거의 전부 — 병원별 데이터 만들기, 일반 학습 코드, Federated Task 코드, Agent 규칙, 앱 코드 |
| Client | `data/` 만 — 클리블랜드 병원 데이터(`cleveland/dataset.csv`)를 만드는 데 씀. 코드는 Owner 가 게시한 것을 Studio 가 내려받습니다. 실제 상황이라면 Client 는 자기 기관 데이터를 갖고 있으므로 템플릿이 필요 없습니다 |

## ✅ 체크리스트

- [ ] `docker compose version` 이 버전을 출력한다
- [ ] [http://localhost:24368](http://localhost:24368) 에 Agent Studio 가 열린다
- [ ] Studio 와 Console 에 **같은 계정**으로 로그인됐다
- [ ] `template/` 폴더가 로컬에 있다

## 다음 단계

- Task Owner → [Task Owner 트랙]({{ '/v1.3/tutorial/owner/' | relative_url }})
- Client → [Client 트랙]({{ '/v1.3/tutorial/client/' | relative_url }})
