---
layout: default
title: "Glossary"
parent: "Reference"
grand_parent: "FedOps Tutorial (English)"
nav_order: 2
permalink: /v1.3/tutorial/en/reference/glossary/
docs_version: "1.3"
lang: en
---

# Glossary
{: .no_toc }

## Roles and screens

| Term | Meaning |
| --- | --- |
| **Task Owner** | The person who designs, publishes, and runs federated learning. The Hungarian hospital in this tutorial |
| **Client (Participant)** | A person or institution that joins a published Task and trains locally on its own data. The Cleveland hospital in this tutorial |
| **FedOps Web** | The FedOps home page. Introduction and docs |
| **FedOps Console** | The web workspace. Tasks, Registry, participants, servers, monitoring |
| **Agent Studio** | A development tool running in Docker on your PC. Code, data, training, participation, Agents |

## FedOps objects

| Term | Meaning |
| --- | --- |
| **Federated Task** | The unit of federated learning. A code bundle containing the model, preprocessing, training code, and Tool definition |
| **Web Draft** | A Task right after being created in the Console, with no code yet |
| **Workspace** | The working area in Studio for a Task's code and data |
| **Release Candidate** | A code and model bundle that passed the checks and waits to be published |
| **Published Release** | A published, fixed bundle. Every Client receives and runs it |
| **Registry** | The list of published Tasks |
| **Campaign** | One run of federated learning. Executed with a set number of rounds, participants, and aggregation method |
| **Initial Model** | The first model built by the Owner. The starting point of the first campaign. Shown on screen as **Initiative Model** |
| **Global Model vN** | The model produced when the Nth campaign finishes |
| **Readiness** | Automatic checks run on your PC before publishing (Release) or before joining (Participation) |

## Federated learning concepts

| Term | Meaning |
| --- | --- |
| **Federated Learning** | A way of training that does not gather data: the model is sent to the data, trained there, and only the parameters are merged |
| **Round** | One loop in which the server sends the model, Clients train, and the server merges |
| **Parameters** | The numbers inside a model. Training is adjusting these numbers, and they are what travels in federated learning |
| **Aggregation** | Merging several Clients' parameters into one |
| **FedAvg** | The basic aggregation method that merges parameters by a weighted average proportional to data size. The only method available in FedOps 1.3 |
| **Clients per round** | The number of Clients that must finish training in a round. The server waits until this many gather |
| **IID / non-IID** | Clients' data distributions are the same / different. Reality is mostly non-IID. The two hospitals in this tutorial are non-IID too |
| **Client drift** | Under non-IID, each Client's model moving away toward its own data |
| **cross-silo** | Federated learning among a small number of institutions such as hospitals or companies. The situation in this tutorial |
| **FLamby** | A collection of cross-silo federated learning benchmarks built from real medical data (NeurIPS 2022). This tutorial's per-hospital split is the same as its `Fed-Heart-Disease` |
| **Parameter signature** | A fingerprint made from the names, shapes, and dtypes of model parameters. Used to check that every participant's model structure is the same |

## Data and model

| Term | Meaning |
| --- | --- |
| **UCI Heart Disease** | Heart test records from four hospitals (Cleveland, Hungary, Switzerland, Long Beach VA). The data of this tutorial |
| **Categorical feature** | A value written as a number but with no order. `cp` (chest pain type) and `restecg` (ECG) in this tutorial |
| **Preprocessing statistics** | Per-feature means and standard deviations and the category vocabulary. The Owner fixes them in the code so every participant uses the same values |
| **MLP** | The most basic neural network, built by stacking layers. The model of this tutorial (`TabularMLP`, 1,010 parameters) |
| **F1 DISEASE** | How well heart disease patients are caught. The key metric this tutorial watches along with accuracy |

## Agent

| Term | Meaning |
| --- | --- |
| **Tool AI** | The model an Agent calls when it needs a number (prediction). Here, the Global Model built by federated learning |
| **Base LLM** | The language model that writes sentences in an Agent |
| **Harness** | The rules and runtime settings the Agent's LLM follows |
| **Serving API** | A built Agent opened so it can be called over HTTP (its own port + token) |
