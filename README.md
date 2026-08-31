# 🐄 MastitisAI — Bovine Mastitis Early-Risk Prediction System

> **A High-Performance Machine Learning & IoT Analytics Platform for Early Detection of Bovine Mastitis Risk in Dairy Livestock.**

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![XGBoost](https://img.shields.io/badge/ML-XGBoost_CV-orange.svg?style=flat-square&logo=xgboost&logoColor=white)](https://xgboost.readthedocs.io/)
[![Scikit-Learn](https://img.shields.io/badge/Pipeline-Scikit--Learn-blue.svg?style=flat-square&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![Streamlit](https://img.shields.io/badge/UI-Streamlit-red.svg?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Status](https://img.shields.io/badge/Status-Production_Ready-brightgreen.svg?style=flat-square)]()

---

## 📌 Executive Summary

**Mastitis** is the single most costly disease affecting dairy cattle worldwide. Clinical symptoms often manifest only after significant udder tissue damage and drop in milk quality have occurred.

**MastitisAI** solves this challenge by fusing 23 multi-dimensional data sources—including thermography, milk electrical conductivity, pathogen loads, behavioral pedometers, environmental heat stress, and health history—into a hyper-tuned **XGBoost Classifier**. The system delivers real-time risk scores, probability distributions, contributing factor explainability, and actionable veterinary recommendations before visible clinical symptoms appear.

---

## 🏆 Model Performance Benchmarks

Trained on 12,000 observations with 5-Fold Stratified Cross-Validation hyperparameter tuning:

| Evaluation Metric | Model Score | Benchmark Highlights |
|---|---|---|
| **Test Recall (Sensitivity)** | **`99.24%`** | **Primary Safety Metric:** Caught 130 of 131 true mastitis test cases |
| **Test Accuracy** | **`99.29%`** | Exceptional overall classification precision across herd |
| **Test Precision** | **`89.04%`** | Controlled false alarm rate for practical farm operations |
| **Test F1-Score** | **`0.9386`** | Optimal balance between sensitivity and precision |
| **Test ROC-AUC** | **`0.9997`** | Near-perfect mathematical class separability |
| **Test PR-AUC** | **`0.9953`** | Robust prediction performance under class imbalance |

---

## 🧬 23 Integrated Factors & Features

```text
                               ┌─────────────────────────────────────────┐
                               │           MASTITIS-AI PIPELINE           │
                               └────────────────────┬────────────────────┘
                                                    │
     ┌───────────────────────┬──────────────────────┼──────────────────────┬──────────────────────┐
     ▼                       ▼                      ▼                      ▼                      ▼
┌──────────────┐     ┌──────────────┐       ┌──────────────┐       ┌──────────────┐       ┌──────────────┐
│ MICROBIOLOGY │     │ PHYSIOLOGY   │       │  BEHAVIOR &  │       │ ENVIRONMENT  │       │  HEALTH &    │
│ & PATHOGENS  │     │ & MILK VITALS│       │  NUTRITION   │       │  & HYGIENE   │       │   HISTORY    │
├──────────────┤     ├──────────────┤       ├──────────────┤       ├──────────────┤       ├──────────────┤
│ Total Load   │     │ Body Temp    │       │ Activity     │       │ Ambient Temp │       │ Breed        │
│ S. aureus    │     │ Udder Temp   │       │ Rumination   │       │ Humidity     │       │ Age (Years)  │
│ S. uberis    │     │ Conductivity │       │ Feed Intake  │       │ Farm Hygiene │       │ Prev History │
│ E. coli      │     │ Milk Yield   │       │ Water Intake │       │ Bedding      │       │ Vaccination  │
│ K. pneumoniae│     └──────────────┘       └──────────────┘       └──────────────┘       │ Chronic Flag │
│ S. agalactiae│                                                                          └──────────────┘
│ Dominant Type│
└──────────────┘
```

---

## 🚀 Quick Start Guide

### 1. Prerequisites & Installation
```bash
git clone https://github.com/YuvasriPraksh/bovine-demo-ml-0-.git
cd bovine-mastitis-prediction
pip install -r requirements.txt
```

### 2. Run Streamlit Interactive Web Application
```bash
streamlit run streamlit_app.py
```

### 3. Execute Model Retraining & Optimization Pipeline
```bash
python src/train_xgboost_best.py
```

### 4. Run Test Verification Suite
```bash
python src/test_predictions.py
```

---

## 📁 Repository Directory Structure

```text
bovine-mastitis-prediction/
├── data/
│   └── synthetic_bovine_mastitis_integrated_dataset.csv  # Integrated 12k dataset
├── models/
│   ├── best_model_XGBoost.pkl                            # Optimized XGBoost model pipeline
│   └── strict_early_risk_model.pkl                      # Active inference model pipeline
├── outputs/
│   ├── figures/                                           # Evaluation charts & ROC/PR curves
│   └── reports/                                           # Evaluation reports & logs
├── src/
│   ├── hardware_interface.py                              # Hardware/IoT JSON interface
│   ├── predict.py                                         # ML inference engine & explainability
│   ├── preprocessing.py                                   # Data preprocessor & alias mapping
│   ├── test_predictions.py                                # Scenario test verification suite
│   └── train_xgboost_best.py                              # XGBoost hyperparameter optimizer
├── README.md                                              # System documentation
├── requirements.txt                                       # Python dependencies
└── streamlit_app.py                                       # Streamlit web application
```

---

## 🔌 IoT & Hardware Sensor Integration API

To send raw IoT sensor readings from farm hardware to the prediction model:

```python
from hardware_interface import process_sensor_reading

sensor_payload = {
    "cow_id": "COW_105",
    "body_temperature_c": 39.8,
    "udder_surface_temperature_c": 40.2,
    "milk_conductivity_mS_cm": 7.1,
    "milk_yield_kg_day": 10.5,
    "S_aureus_load_log10_cfu_equiv": 4.5,
    "hygiene_score_0_100": 30.0
}

result = process_sensor_reading(sensor_payload)
print(f"Risk Level: {result['risk_level']} | Probability: {result['mastitis_probability']*100:.1f}%")
```

---

## 📜 License & Disclaimers

This repository is constructed for software demonstration and agricultural AI research purposes. All datasets are synthetic representations designed to model physiological correlations.
