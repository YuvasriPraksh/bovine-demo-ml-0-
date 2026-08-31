# 🇮🇳 Pashu Sanjeevani AI — Bovine Mastitis Early-Warning & Risk Surveillance Portal

> **An Enterprise-Grade, 23-Factor Machine Learning & IoT Platform for Early Forecasting of Bovine Mastitis in Dairy Livestock.**
> *Department of Animal Husbandry & Dairying · Ministry of Fisheries, Animal Husbandry & Dairying (Govt. of India Inspired Prototype)*

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18.3+-61DAFB.svg?style=for-the-badge&logo=react&logoColor=black)](https://react.dev/)
[![XGBoost](https://img.shields.io/badge/XGBoost-Optimized-FF6F00.svg?style=for-the-badge&logo=xgboost&logoColor=white)](https://xgboost.readthedocs.io/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-Pipeline-F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)

---

## 📌 Problem Statement & Impact

**Bovine Mastitis** is an inflammation of the mammary gland caused by pathogenic infection, leading to severe economic losses in the global dairy sector through reduced milk yield, compromised milk quality, veterinary treatment costs, and premature culling.

Traditional detection relies on visual symptoms or somatic cell counts (SCC) after tissue inflammation has already established. **Pashu Sanjeevani AI** continuously analyzes **23 multi-dimensional indicators**—including udder surface thermography, inline milk electrical conductivity, pathogen CFU concentrations, pedometer activity, rumination time, and ambient heat stress—to forecast mastitis risk **days before clinical symptoms manifest**.

> [!NOTE]
> **Clinical Disclaimer:** This system functions strictly as a decision-support, early-warning risk prediction tool for dairy farm management and veterinary screening. It does not replace professional clinical veterinary diagnosis.

---

## 🏗️ End-to-End System Architecture

```text
[ React + Vite PWA Frontend ]
            │  (HTTP POST /api/predict)
            ▼
 [ FastAPI Backend Server ]  ──► (Preloads Model at Lifespan Startup)
            │
            ▼
 [ ML Preprocessing Pipeline ] (ColumnTransformer, Imputers, StandardScalers)
            │
            ▼
[ Trained XGBoost Model (.pkl) ] (ml/models/strict_early_risk_model.pkl)
            │
            ▼
[ Risk Prediction & Explainability ] (Probabilities, Risk Levels & Contributing Factors)
            │
            ▼
 [ FastAPI Response Payload ]
            │
            ▼
[ Frontend Dashboard & Early Alert ]
```

---

## 🏛️ Directory Structure

```text
bovine-mastitis-prediction/
├── backend/                      # SIH FastAPI Backend Service
│   ├── app/
│   │   ├── config.py             # Settings, CORS, & environment variables
│   │   ├── main.py               # FastAPI entry point & lifespan model preloader
│   │   ├── schemas.py            # Pydantic data schemas
│   │   ├── ml/                   # Backend Production ML Adapter (predict.py)
│   │   ├── routes/               # API Endpoints (/api/predict, /api/animals, etc.)
│   │   └── services/             # Data services & dataset loader (data_service.py)
│   ├── Procfile                  # Production process file
│   └── requirements.txt          # Backend dependencies
│
├── frontend/                     # SIH React + Vite Dashboard Application
│   ├── dist/                     # Production web build bundle
│   ├── public/                   # Manifest & PWA icons
│   ├── package.json              # Node dependencies
│   └── vite.config.js            # Vite configuration
│
├── ml/                           # Unified Machine Learning Directory
│   ├── models/                   # Production Pre-Trained Model Artifacts (.pkl)
│   │   ├── strict_early_risk_model.pkl
│   │   └── best_model_XGBoost.pkl
│   ├── src/                      # Production Core Runtime Inference Engine
│   │   ├── predict.py            # Feature validation & tree contribution analyzer
│   │   ├── preprocessing.py      # Scikit-learn preprocessing pipelines
│   │   └── hardware_interface.py # IoT sensor payload ingestion handler
│   ├── training/                 # Model Training & Hyperparameter Tuning
│   │   ├── train.py
│   │   ├── train_strict.py
│   │   └── train_xgboost_best.py
│   └── scripts/                  # Data Generation & Audit Utilities
│       ├── generate_v2_dataset.py
│       ├── generate_class_blind_history.py
│       └── audit_class_blind_history.py
│
├── tests/                        # Automated Test Suites & Simulation Scripts
│   ├── test_end_to_end_integration.py
│   ├── test_predictions.py
│   ├── test_v2_schema.py
│   ├── simulate_sensor_input.py
│   └── demo_scenarios.py
│
├── data/                         # Project Datasets
│   ├── processed/                # Primary datasets (mastitis_dataset.csv / xlsx)
│   └── raw/                      # Integrated raw training dataset
│
├── outputs/                      # Generated Evaluation Figures & Reports
│   ├── figures/                  # Confusion matrices, ROC curves, feature importances
│   └── reports/                  # Model evaluation reports & CSV audits
│
├── streamlit_app.py              # Standalone Streamlit Interactive Portal
├── requirements.txt              # Unified Root Dependencies File
├── render.yaml                   # Cloud Deployment Specification
└── README.md                     # System Documentation
```

---

## 🧬 23 Integrated Factors & Features

| Category | Feature Name | Description & Unit |
|---|---|---|
| **Microbiology & Pathogens** | `environment_total_mastitis_pathogen_load_log10` | Total environmental pathogen pressure ($\log_{10}$ CFU equiv) |
| | `S_aureus_load_log10_cfu_equiv` | *Staphylococcus aureus* load ($\log_{10}$ CFU) |
| | `S_uberis_load_log10_cfu_equiv` | *Streptococcus uberis* load ($\log_{10}$ CFU) |
| | `E_coli_load_log10_cfu_equiv` | *Escherichia coli* load ($\log_{10}$ CFU) |
| | `K_pneumoniae_load_log10_cfu_equiv` | *Klebsiella pneumoniae* load ($\log_{10}$ CFU) |
| | `S_agalactiae_load_log10_cfu_equiv` | *Streptococcus agalactiae* load ($\log_{10}$ CFU) |
| | `dominant_environment_pathogen` | Dominant environmental pathogen strain |
| **Physiology & Milk Vitals** | `body_temperature_c` | Core body temperature (°C) |
| | `udder_surface_temperature_c` | Udder surface thermography (°C) |
| | `milk_conductivity_mS_cm` | Milk electrical conductivity (mS/cm — key mastitis marker) |
| | `milk_yield_kg_day` | Daily milk volume (kg/day) |
| **Behavior & Nutrition** | `activity_score` | Pedometer activity index |
| | `rumination_min_day` | Daily rumination time (minutes/day) |
| | `feed_intake_kg_day` | Dry matter feed intake (kgDM/day) |
| | `water_intake_l_day` | Daily water consumption (L/day) |
| **Environment & Hygiene** | `ambient_temperature_c` | Barn ambient temperature (°C) |
| | `relative_humidity_pct` | Relative atmospheric humidity (%) |
| | `hygiene_score_0_100` | Barn and udder cleanliness score (0–100) |
| **Profile & Health History** | `breed` | Livestock breed (*Holstein Friesian*, *Jersey*, *Gir*, *Sahiwal*) |
| | `age_years` | Animal age (Years) |
| | `previous_mastitis_history` | Prior mastitis history (0 = No, 1 = Yes) |
| | `vaccinated` | Vaccination protection status (0 = No, 1 = Yes) |
| | `chronic_disease_flag` | Chronic health condition (0 = No, 1 = Yes) |

---

## 📡 REST API Specification

### `POST /api/predict`

#### Request Payload Example:
```json
{
  "animal_id": "COW_12001",
  "breed": "Holstein_Friesian",
  "age_years": 4.5,
  "body_temperature_c": 39.6,
  "udder_surface_temperature_c": 39.2,
  "milk_conductivity_mS_cm": 5.4,
  "milk_yield_kg_day": 12.0,
  "hygiene_score_0_100": 45.0,
  "ambient_temperature_c": 32.0,
  "relative_humidity_pct": 80.0,
  "previous_mastitis_history": 1,
  "vaccinated": 1
}
```

#### Response Payload Example:
```json
{
  "animal_id": "COW_12001",
  "risk_category": "High",
  "risk_score": 87.4,
  "class_probabilities": {
    "No_Risk": 8.8,
    "Low": 3.8,
    "Moderate": 26.2,
    "High": 61.2
  },
  "top_risk_factors": [
    {
      "factor": "Elevated Body Temperature",
      "feature_name": "body_temperature_c",
      "observed_value": 39.6,
      "impact_score": 0.82,
      "details": "Model contribution: +0.8240 (risk)"
    }
  ],
  "forecast_7d_risk_pct": 96.1,
  "forecast_14d_risk_pct": 99.0,
  "environmental_risk": {
    "ambient_temperature_c": 32.0,
    "relative_humidity_pct": 80.0,
    "calculated_thi": 86.1,
    "conditions_favorable_for_pathogens": true,
    "interpretation": "Elevated heat/humidity index associates with increased bacterial proliferation risk in bedding"
  },
  "recommendations": [
    "Conduct on-farm California Mastitis Test (CMT) or individual quarter conductivity check during next milking.",
    "Isolate milk from this cow until subclinical status is cleared.",
    "Inspect teat skin integrity, pre-dip contact time, and post-milking barrier teat dip application."
  ],
  "prediction": 1,
  "mastitis_probability": 0.874,
  "healthy_probability": 0.126,
  "risk_level": "HIGH",
  "risk_label": "At Risk",
  "timestamp": "2026-08-31T22:56:30.123456"
}
```

---

## 🚀 Setup & Local Execution Instructions

### 1. Environment Setup
```bash
# Clone repository
git clone https://github.com/YuvasriPraksh/bovine-demo-ml-0-.git
cd bovine-mastitis-prediction

# Create and activate Python virtual environment
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Run FastAPI Backend Server
```bash
# Start FastAPI backend (Port 8000)
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
Interactive Swagger API documentation will be available at: `http://localhost:8000/docs`

### 3. Run Frontend App or Streamlit App
```bash
# Option A: Run Streamlit Portal (Port 8501)
streamlit run streamlit_app.py

# Option B: Run React Frontend (Port 5173)
cd frontend
npm install
npm run dev
```

### 4. Run Automated Integration Tests
```bash
# Run full end-to-end integration test suite
python -m unittest tests/test_end_to_end_integration.py
```

---

## ☁️ Production Deployment (Render)

The project includes a production `render.yaml` configuration file for Render deployment:
- **Service Name:** `bovine-mastitis-backend`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Model binaries (`ml/models/strict_early_risk_model.pkl`) and dataset assets are included in deployment.
