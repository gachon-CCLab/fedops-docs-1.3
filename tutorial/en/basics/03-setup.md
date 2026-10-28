---
layout: default
title: "3. Setup"
parent: "Basics"
grand_parent: "FedOps Tutorial (English)"
nav_order: 3
permalink: /v1.3/tutorial/en/basics/setup/
docs_version: "1.3"
lang: en
---

# 3. Setup
{: .no_toc }

{: .note }
> 📍 **Where you are:** Basics 3/3 — ① Federated learning and FedOps → ② Data and model → **③ Setup** → next: your role's track

{: .important }
> 🎯 **What you do in this step:** Run Agent Studio on your PC, sign in to Studio and the FedOps Console, and get the practice template. **Both the Owner and the Client** must do this, because training happens not on the server but on each person's PC (Studio).

1. TOC
{:toc}

## 1) Check your system

```bash
python3 --version    # must be 3.10 ~ 3.12
```

- 16 GB memory recommended (the Studio container and a CPU LLM run together; the LLM is used only in the Model Use Track)
- 20 GB+ free disk
- Internet connection required (Docker images, packages, LLM download)

## 2) Install Docker Desktop

Install and start [Docker Desktop](https://www.docker.com/products/docker-desktop/). On Linux, Docker Engine + the compose plugin is enough.

{% raw %}
```bash
docker version --format '{{.Server.Version}}'
docker compose version
```
{% endraw %}

{: .highlight }
> **Use a recent Docker.** With an old version such as Docker 20.10, the `fedops` command cannot stop an already running Studio (`unknown flag: --timeout`).

## 3) Run Agent Studio

```bash
python3 -m venv ~/.venvs/fedops && source ~/.venvs/fedops/bin/activate
pip install -U fedops
fedops run agent-studio
```

Success when Studio ([http://localhost:24368](http://localhost:24368)) opens in your browser. The first time it takes a few minutes to pull the Docker image.

{: .note }
> On an **Intel Mac**, if `pip install -U fedops` fails with an `llvmlite` build error, install with `pip install --no-deps fedops`.

To stop, run `fedops stop agent-studio`. Studio keeps code and **local data** under `~/fedops-workspace/`. Do not delete this folder.

> **Why does Studio run on my PC?** In federated learning, data must not leave your PC. So training, checks, and joining all happen in Studio on your PC, and the web (Console) only does things that need no data (publishing, approval, server operation).

## 4) Accounts and sign-in

Create an **account** with **Create account** on the FedOps Console sign-in screen. One FedOps account signs in to both the Console and Studio.

| Goal | Accounts needed |
| --- | --- |
| One role only | 1 |
| Practice both roles alone (Owner joins its own Task) | 1 |
| Split Owner and Client (experience request and approval) — **this tutorial's setup** | **2** — one for the Owner, one for the Client |

Sign in **in two places separately**.

1. Sign in with your FedOps account on the Agent Studio start screen
2. Also sign in to the FedOps Console in your browser — **Open Console** at the top right of FedOps Web ([https://ccl.gachon.ac.kr/fedops](https://ccl.gachon.ac.kr/fedops)), or [https://ccl.gachon.ac.kr/fedops/console](https://ccl.gachon.ac.kr/fedops/console)

> Studio and the Console do not share sign-in. With two accounts, always check that **Studio and the Console use the same account**. Otherwise you get "my Task is not visible".

## 5) Get the practice template

```bash
git clone https://github.com/gachon-CCLab/FedOps-hands-on-guide.git
cd FedOps-hands-on-guide/template
```

All later commands run from this `template/` folder. Without git, use **Code → Download ZIP** on the GitHub page and unzip it.

| Role | What you use from the template |
| --- | --- |
| Owner | Almost everything — building per-hospital data, regular training code, Federated Task code, Agent rules, app code |
| Client | Only `data/` — used to build the Cleveland hospital data (`cleveland/dataset.csv`). Studio downloads the code the Owner published. In real life a Client already has its own institution's data and does not need the template |

## ✅ Checklist

- [ ] `docker compose version` prints a version
- [ ] Agent Studio opens at [http://localhost:24368](http://localhost:24368)
- [ ] You are signed in to Studio and the Console with **the same account**
- [ ] The `template/` folder is on your PC

## Next

- Task Owner → [Task Owner Track]({{ '/v1.3/tutorial/en/owner/' | relative_url }})
- Client → [Client Track]({{ '/v1.3/tutorial/en/client/' | relative_url }})
