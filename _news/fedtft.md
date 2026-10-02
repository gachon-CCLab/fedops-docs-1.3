---
title: "FedTFT: Federated Temporal Fusion Transformer for Interpretable Multi-Horizon Psychiatric Risk Prediction Across Cross-Silo Hospitals"
summary: "Psychiatric inpatient monitoring generates multimodal data, but privacy constraints and cross-hospital heterogeneity limit centralized learning. We propose FedTFT, a federated Temporal Fusion Transformer…"
category: "paper"
author: "Akeel Ahamed et al."
date: 2026-05-05
original_date: "2026.05.05"
display_order: 1
source_url: "https://ieeexplore.ieee.org/document/11506081/"
hide_summary: true
lang: en
---

## Abstract

Psychiatric inpatient monitoring generates multimodal data, but privacy constraints and cross-hospital heterogeneity limit centralized learning. We propose FedTFT, a federated Temporal Fusion Transformer for multi-horizon psychiatric risk prediction with horizon-decoupled prediction heads for one-hour, one-day, and one-week forecasting and an area under the receiver operating characteristic curve (AUROC)-weighted server aggregation strategy for non-independent and identically distributed hospital data. Each horizon uses its own linear output head to reduce cross-horizon gradient interference, while local training uses proximal updates. We trained and evaluated the model on 246 patients from three South Korean hospitals without sharing raw records. On the global holdout set, FedTFT achieved 93.9% accuracy, AUROC 0.9054, event-F1 0.8242, and Brier score 0.0680. Under matched federated settings, FedTFT improved event-F1 by 19.58 percentage points(PP) over the best competing federated baseline in event-F1 and improved AUROC by 2.74 pp over the highest-AUROC competing federated baseline, while maintaining the lowest Brier score. Ablations confirmed contributions from both the horizondecoupled design and the AUROC-weighted aggregation strategy. Gradient SHapley Additive exPlanations (SHAP) analysis identified significant predictors such as treatment time, circadian heart-rate fluctuations, and mobility changes. These findings support accurate, calibrated, and interpretable privacy-preserving psychiatric risk forecasting for proactive intervention.

## Keywords

Federated Learning; Patient Monitoring; Privacy Preserving Machine Learning; Temporal Fusion Transformer; Wearable Sensors; Psychiatric Risk Prediction
