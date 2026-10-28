---
layout: default
title: "1. Design"
parent: "Task Owner Track"
grand_parent: "FedOps Tutorial (English)"
nav_order: 1
permalink: /v1.3/tutorial/en/owner/design/
docs_version: "1.3"
lang: en
---

# 1. Design
{: .no_toc }

{: .note }
> 📍 **Where you are:** Task Owner 1/7 — **① Design** → ② Create Task → ③ Workspace → ④ Train · publish → ⑤ Approve → ⑥ Campaign → ⑦ Results<br> Next: create the Task in the Console

{: .important }
> 🎯 **What you do in this step:** Before turning FedOps on, run ordinary training on one PC to check that **this data and model combination actually learns**. Then see in numbers why one hospital's data alone is not enough. Federated learning is hard to debug. If you only find out at the federated stage that the model cannot learn at all, finding the cause is much harder.

1. TOC
{:toc}

## 1) Build the per-hospital data

The template's `data/uci/` contains the four original UCI files (one per hospital). `prepare_data.py` **does not re-split** these files; it only cleans them per hospital.

```bash
cd data
pip install numpy pandas
python prepare_data.py
```

The script prints in Korean (`원본` = original, `행` = rows, `결측 행을 빼고` = after dropping rows with missing values, `출력` = output):

```txt
hungarian: 원본 294행 → 결측 행을 빼고 261행
cleveland: 원본 303행 → 결측 행을 빼고 303행

출력: out
  hungarian/dataset.csv          261행   no_disease=163(62%) disease=98(38%)
  cleveland/dataset.csv          303행   no_disease=164(54%) disease=139(46%)
  train.csv (hungarian+cleveland)   373행   no_disease=216(58%) disease=157(42%)
  test.csv  (hungarian+cleveland)   191행   no_disease=111(58%) disease=80(42%)
```

| File | Use |
| --- | --- |
| `out/hungarian/dataset.csv` | **Local data of the Owner (Hungarian hospital).** Placed in Studio's Data Folder in chapter 3 |
| `out/cleveland/dataset.csv` | Local data of the Client (Cleveland hospital). The Client builds it on its own PC with the same command. The Owner does not use it |
| `out/<hospital>/train.csv`, `test.csv` | That hospital's data split 66% for training / 34% for evaluation. Used in 3) below for "training on one hospital only" |
| `out/train.csv`, `test.csv` | Both hospitals' train / test combined. The "if we could pool the data" baseline in 2) below |

### ⚙️ Options explained — `prepare_data.py`

| Option | Default | What changes |
| --- | --- | --- |
| `--hospitals` | `hungarian,cleveland` | Hospitals to build. Adding `va` gives data for a third participant. `switzerland` is rejected with an error because it has only one patient without heart disease (each class needs at least 3 rows) |
| `--test-size` | 0.34 | Evaluation share held out per hospital. Same value as FLamby. Does not affect `dataset.csv` (always the whole hospital) |
| `--seed` | 43 | Random seed for the train / test split. Also does not affect `dataset.csv` |

> Even if the Owner and Client use different options, **each `dataset.csv` is the same**, because the hospital files are only cleaned.

<details markdown="1">
<summary>📚 Federated learning background — IID and non-IID</summary>

**IID** (independent and identically distributed) means every institution's data was drawn from the same distribution. Then each client learns in a similar direction, and averaging gives almost the same result as training on all the data.

In **non-IID** settings each client pulls the model toward its own data. The Hungarian hospital (38% heart disease) and the Cleveland hospital (46%) differ not only in rate but also in patient age and test value distributions. Adding the VA hospital (78%) makes the difference much larger. Averaging these directions may fit nobody well, needing more rounds or improving accuracy less. FedProx, SCAFFOLD, FedBN and others try to reduce this. FedAvg is the only aggregation method you can choose in FedOps 1.3 ([chapter 6]({{ '/v1.3/tutorial/en/owner/campaign/' | relative_url }})).

</details>

## 2) Regular training (without FedOps)

Plain PyTorch training on one PC. By default it trains on `out/train.csv`, which **pools both hospitals' data** — the "if we could pool the data" baseline that is impossible in reality. From the next step on, this code moves into the FedOps shape.

```bash
cd ../centralized
pip install -r requirements.txt
python train_centralized.py
```

Output (Korean labels: `데이터` = data, `학습 시작` = training starts, `무작위로 찍으면` = random guessing, `가장 많은 클래스만 찍으면` = always guessing the majority class):

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

(Measured 2026-10-20, torch 2.2.2. Training is random, so numbers may differ slightly by environment.)

**accuracy 0.796** — clearly above "always guess no disease" (0.58), so the model learned. Of the 39 mistakes, 21 missed heart disease patients as "no disease". In medicine, missing a heart disease patient is the more dangerous mistake, so this tutorial keeps watching **F1 DISEASE** (how well heart disease is caught) along with accuracy.

### ⚙️ Options explained — training settings

These are arguments of `train_centralized.py` and later the values under `config.yaml` → `local_training` in the Federated Task.

| Option | Default | If you change it | This tutorial's choice |
| --- | --- | --- | --- |
| `--epochs` | 30 | More passes over the data lower the loss further, but too many cause overfitting to the training data | 30 — converges well enough at this data size |
| `--learning-rate` | 0.001 | Larger is faster but unstable, smaller is stable but slow | 0.001 — usual value for Adam |
| `--batch-size` | 32 | Larger sees more at once and wobbles less, smaller updates more often | 32 — still several batches for one hospital (around 170 rows) |
| `--data-root` | `../data/out` | Folder to read `train.csv` / `test.csv` from | Changed to a hospital folder in 3) below |

## 3) What if we train on one hospital only?

Check why federated learning is needed. Train on the Owner's Hungarian data only.

```bash
python train_centralized.py --data-root ../data/out/hungarian --out out/hungarian
```

```txt
데이터: train 173행 / test 88행, 입력 10차원, 2클래스
...
test accuracy = 0.761   f1_macro = 0.752   loss = 0.4622
  (무작위로 찍으면 accuracy 약 0.50, 가장 많은 클래스만 찍으면 약 0.62)
```

This run scored 0.761 on the Hungarian test set (88 rows). The 0.796 in 2) was measured on both hospitals' test sets combined, so the two cannot be compared directly. On the same Hungarian test set, the comparison looks like this.

| Training data | Hungarian test accuracy |
| --- | --- |
| Hungary only (173 rows) — **Owner alone** | about 0.76 |
| Hungary + Cleveland (373 rows) — **if we could pool** | about 0.79 |

(Simulation 2026-10-20, average of 20 seeds)

Less data means lower performance. But hospitals cannot pool their data. **Narrowing the gap between one hospital and "if we could pool", without moving data,** is the goal of federated learning. In this tutorial two hospitals, the Owner (Hungary) and the Client (Cleveland), train together.

> **It is fine if the gap looks small.** On this data, pooling both hospitals differs by only a few percentage points. What to watch in this tutorial is not the size of the numbers but **how federated learning works** in FedOps.

## 4) Preprocessing statistics are part of the agreement

Per-feature means and standard deviations and the category vocabulary (preprocessing statistics) computed during training are saved separately in `out/preprocessing.json`. If these values differ, the model sees the same input differently, so **the Owner's training, every Client's training, and Agent inference must all use the same values**.

> If each hospital computed its own means, the same patient would become different numbers at each hospital before entering the model. So the FedOps template **fixes the Owner's statistics in the code** and distributes them to all participants (`embed_preprocessing.py` in chapter 3).

## ✅ Checklist

- [ ] `data/out/` contains `hungarian/dataset.csv`
- [ ] The regular training's test accuracy is clearly above 0.58
- [ ] You saw that using one hospital only lowers performance

## If something goes wrong

| Symptom | Fix |
| --- | --- |
| `train.csv 가 없다` (train.csv not found) | Run `prepare_data.py` first |
| `원본 파일이 없다` (original files not found) | Check that `template/data/uci/` has the four `processed.*.data` files. If you downloaded a ZIP, check that it is fully extracted |
| `클래스마다 3행 이상이어야 …` (each class needs at least 3 rows …) | You put `switzerland` in `--hospitals`. Pick other hospitals |
| torch install fails | If Python is 3.13, use 3.12. Intel Macs only have up to torch 2.2.2 (within the allowed range) |
| Accuracy near 0.58 | `python train_centralized.py --epochs 60` |

## Next

[2. Create a Task]({{ '/v1.3/tutorial/en/owner/create-task/' | relative_url }}) — register your design with FedOps as "this is the federated learning I want to run".
