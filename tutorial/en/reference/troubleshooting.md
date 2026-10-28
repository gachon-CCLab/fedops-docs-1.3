---
layout: default
title: "Troubleshooting and Known Issues"
parent: "Reference"
grand_parent: "FedOps Tutorial (English)"
nav_order: 1
permalink: /v1.3/tutorial/en/reference/troubleshooting/
docs_version: "1.3"
lang: en
---

# Troubleshooting and Known Issues
{: .no_toc }

{: .note }
> Confirmed by following along on an Intel Mac + Docker Desktop on September 28, October 6, and October 11, 2026, and with two accounts — a Mac (Owner) + a Windows laptop (Client) — on October 19, using the previous data (Breast Cancer Wisconsin). These are FedOps and Studio issues, so they are expected to stay the same with the new data, but they have not been rechecked with Heart Disease yet. They may change when Agent Studio is updated.

## Known issues (waiting for a FedOps fix)

### 🔴 Tool prediction fails on the built Agent's API

- **Symptom:** `test_agent.py --sample 0` → `[실패: TOOL_UNAVAILABLE] Tool AI smoke test failed` (failed; log: `Readme file does not exist: README.md`)
- **Scope:** Generate Response in Agent Builder (Model Use ch. 1) works, and the API's `/health` and `/info` work too. Only the Tool step fails when calling the built Agent over the API
- **Cause:** Studio copies the Agent build snapshot without `README.md`, while the Task package settings require a README
- **Status:** waiting for a FedOps fix (reproduced again on 2026-10-06 and 2026-10-11). **Workaround:** after every Build, copy the Workspace's `README.md` into `~/fedops-workspace/accounts/*/.local-data/agents/builds/<agentId>/r1/components/tool-0/project/`. With this, Model Use ch. 2–3 were confirmed to work end to end

### 🟠 The first API call takes close to 10 minutes

- The first call after a build installs a fresh Tool runtime (about 2 GB). Measured 570 s on 2026-10-11 (Tool 509 s), 43 s from the second call
- If requests overlap or the PC sleeps meanwhile, the environment can break with `No module named 'torch._tensor'`, or the Agent API stops responding and the Studio container freezes
- Restarting Docker or Studio behaves similarly. Right after a restart on 2026-10-13, even the first LLM-only call without the Tool did not finish within 300 s; later calls took 40–50 s
- **Fix:** set a 900 s timeout for the first call, send one request at a time, and keep the PC awake meanwhile. If Studio freezes and even `docker stop` does not work, restart Docker Desktop

### 🟡 Studio fails to restart on an old Docker

- **Symptom:** `Could not replace existing container` or `unknown flag: --timeout`
- **Fix:** update Docker Desktop. For now, stop it with `docker stop fedops-agent-studio`, then run `fedops run agent-studio`

### 🟡 `pip install fedops` fails on an Intel Mac

- **Symptom:** `Failed building wheel for llvmlite`
- **Fix:** `pip install --no-deps fedops`

### 🟢 Clicking Finish Client Session leaves the screen unchanged

- The session already ended on the first click. Clicking again can give a 500; ignore it and move to the next step
- On the Mac (Owner) on 2026-10-20, **the first click gave a 500 right away** (shown only in the browser console). The campaign had already finished, and results and the Global Model were unaffected. Do not click repeatedly; move on
- If there is no button at all and `✓ Client session ended` is shown, the session ended automatically (Windows laptop, 2026-10-19). There is nothing to click

### 🟠 Docker freezes during Sync (out of memory)

- **Symptom:** during Python environment Sync or `fedops run agent-studio --repair-host`, Studio and `docker` commands stop responding. Then Local Train fails with `No module named 'torch._utils'`
- **Cause (presumed):** the Mac ran out of memory. It happened twice on a 16 GB Mac on 2026-10-20, both times with about 100 MB of memory left
- **Fix:** close heavy apps such as browser tabs and Notion, and restart Docker Desktop (Studio sign-in is lost, so sign in again). If torch is broken, **Delete** the Default environment in Python Environments and Sync again (Owner Track ch. 3)

### 🟢 The readiness check goes back to `Check required` when the server starts

- When a new campaign server starts, the check resets for both the Owner and the Client. Click **Check Participation Readiness** again before Start Client (Client Track ch. 3 and 4)
- If the first Start Client click fails with `[Errno 2] … task-binding.tmp`, click **Refresh** and try again

### 🟢 `handson-heart changed after selection` in Agent Builder

- Appears when you Prepare Global Model v1 for the first time (every time in earlier runs). The model has already been downloaded, so refresh and pick the Tool AI again; it shows `Global Model v1 · Ready`. An unsaved Base LLM choice is lost, so pick the Tool AI first and the Base LLM later

### 🟢 `Port 24400 is already assigned to another Agent.` in Serving API

- Another Agent is already serving on that port. The screen shows a port in use as the default too. Change the port to the next number, such as `24401`, and Enable again

### 🟢 Delete on the Agents screen does nothing

- While that Agent's Serving API is on, the Delete button is locked (the screen does not say why). Click **Serving API** tab → **Disable API** first

### 🟢 Cannot create an Agent with the same name again (`An Agent draft with this name already exists.`)

- Deleting the Agent on the Agents screen leaves the **Agent Builder draft** separately. Open that draft in Agent Builder, delete it with **Delete** at the top, then create it again

### 🟢 Open folder / Open Data Folder does not open Finder

- `The host folder opener refused the connection` — when Studio came back up after, for example, a Docker restart, the host program that opens folders did not start with it. In the terminal: `fedops run agent-studio --repair-host` (Studio is not restarted)

### 🟢 The demo UI does not start (`Unable to evaluate type annotation 'int | None'`)

- It was run with Python 3.9. Use Python 3.10 or later, `pip install -r requirements.txt`, and run again

### 🟢 `prepare_data.py` stops with `클래스마다 3행 이상이어야 …` (each class needs at least 3 rows …)

- You put `switzerland` in `--hospitals`. The Swiss hospital data has only one patient without heart disease, so it cannot meet FedOps's participation conditions. Pick other hospitals

### ⚠️ The FL server live log prints an AWS access key ID

- DEBUG lines near the top of the live log in Server Management show the server's AWS access key ID and request signatures (not the secret key). Do not capture and share the live log screen. A defect to report to FedOps

## Frequently asked questions

<details markdown="1">
<summary>Which do I use for what, Studio or the Console?</summary>

**FedOps Console** (Open Console on the Web home page): create Tasks, publish to the Registry, federated learning servers and campaigns, approve participants, monitoring. **Studio**: code and data, local training and checks, joining federated learning, building Agents and APIs. You sign in to each separately with the same account.

</details>

<details markdown="1">
<summary>Is my data uploaded anywhere?</summary>

No. The data stays only in `~/fedops-workspace/.../.local-data/`; the Registry holds code, models, and the README, and only model parameters travel during federated learning.

</details>

<details markdown="1">
<summary>Why is accuracy below 0.8?</summary>

That is this data's natural level. Predicting heart disease from only 10 items of 1980s hospital records gives around 0.8 even when both hospitals are pooled. The purpose of this tutorial is not accuracy but running federated learning end to end with FedOps.

</details>

<details markdown="1">
<summary>Can I add more hospitals?</summary>

`python prepare_data.py --hospitals hungarian,cleveland,va` also builds the VA hospital data (130 rows). A third account joins with this file, and Clients per round in chapter 6 is set to 3. However, the VA hospital is skewed to 78% heart disease, and in simulation it more often lowered performance on the Owner's data. It makes a good experiment for seeing how non-IID data affects federated learning.

</details>

<details markdown="1">
<summary>Can I publish a Task privately?</summary>

Not currently. Publishing to the Registry includes switching to Public. If you do not want it after the practice, delete the Task in the Console.

</details>

<details markdown="1">
<summary>Can I run federated learning alone?</summary>

Yes. With Clients per round set to 1, rounds run with just your PC (confirmed in practice).

</details>

<details markdown="1">
<summary>What if the numbers in the Agent's answer differ from the model's result?</summary>

Check that the Harness Instructions include the rule "quote the Tool's numbers as is" and that Temperature is low (0.2), then build again. The correct answer is always the value in `toolResult.result`.

</details>

<details markdown="1">
<summary>How do I clean up after the practice?</summary>

1. Console Server Management → **Pause** (return server resources)
2. If you do not want it public, Task actions → **Delete task**
3. Studio → Agents → Serving API **Disable API** (to delete the Agent, Delete after that, and also Delete the Agent Builder draft)
4. Check that the demo UI is stopped (Ctrl+C in the terminal)
5. `fedops stop agent-studio`

</details>

<details markdown="1">
<summary>Can a Client edit the code it received?</summary>

No. A Client's code must match the Release the Owner published to pass the readiness check and to merge parameters with other participants. If the code has a problem, tell the Owner to publish a new Release.

</details>

<details markdown="1">
<summary>What does a Client clean up after taking part?</summary>

1. Click **Finish Client Session** once on the federated learning screen (if there is no button and `✓ Client session ended` is shown, it has already ended)
2. **Leave** if you will not take part in the Task again
3. `fedops stop agent-studio`

Your data stays in the Task's own data folder under `~/fedops-workspace/`. Delete it yourself if you no longer need it.

</details>

## Asking for help

If you get stuck, collect the following and contact the CCL lab: which step, the error message on screen, OS and Docker version (`docker version`), and Studio logs (`docker logs --tail 100 fedops-agent-studio`).
