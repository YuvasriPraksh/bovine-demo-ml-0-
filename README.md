# 🇮🇳 Pashu Sanjeevani AI — Bovine Mastitis Early-Warning & Risk Surveillance Portal

> **An Enterprise-Grade, 23-Factor Machine Learning & IoT Platform for Early Prediction of Bovine Mastitis in Dairy Livestock.**
> *Department of Animal Husbandry & Dairying · Ministry of Fisheries, Animal Husbandry & Dairying (Govt. of India Inspired Prototype)*

[![Live Web App](https://img.shields.io/badge/🌐_Live_App-Pashu_Sanjeevani_AI-059669.svg?style=for-the-badge&logo=streamlit&logoColor=white)](https://5aitk8wxhcznsfd2zup5a5.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![XGBoost](https://img.shields.io/badge/XGBoost-Optimized-FF6F00.svg?style=for-the-badge&logo=xgboost&logoColor=white)](https://xgboost.readthedocs.io/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-Pipeline-F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![Status](https://img.shields.io/badge/Status-Hardware_Ready-brightgreen.svg?style=for-the-badge)]()

---

## 🌟 Live Demo & Web Portal

🔗 **Official Deployment Link:** [https://5aitk8wxhcznsfd2zup5a5.streamlit.app/](https://5aitk8wxhcznsfd2zup5a5.streamlit.app/)

---

## 📌 Problem Statement & Impact

**Bovine Mastitis** is an inflammation of the mammary gland caused by pathogenic infection, leading to severe economic losses in the global dairy sector through reduced milk yield, compromised milk quality, veterinary treatment costs, and premature culling.

Traditional detection relies on visual symptoms or somatic cell counts (SCC) after tissue inflammation has already established. **Pashu Sanjeevani AI** continuously analyzes **23 multi-dimensional indicators**—including udder surface thermography, inline milk electrical conductivity, pathogen CFU concentrations, pedometer activity, rumination time, and ambient heat stress—to forecast mastitis risk **days before clinical symptoms manifest**.

---

## 🏆 Model Performance & Evaluation Benchmarks

Evaluated on an independent test set of **2,400 observations** (from a 12,000-cow dataset) using 5-Fold Stratified Cross-Validation hyperparameter tuning:

| Metric | Score | Key Result / Clinical Significance |
|---|---|---|
| **Test Recall (Sensitivity)** | **`99.24%`** | **Primary Safety Metric:** Caught 130 of 131 true mastitis cases (Only 1 false negative) |
| **Test Accuracy** | **`99.29%`** | High overall herd classification accuracy |
| **Test Precision** | **`89.04%`** | Low false alarm rate for practical dairy farm operations |
| **Test F1-Score** | **`0.9386`** | Optimal balance between precision and sensitivity |
| **Test ROC-AUC** | **`0.9997`** | Near-perfect mathematical class separability |
| **Test PR-AUC** | **`0.9953`** | Robust prediction performance under class imbalance |

---

## 🧬 23 Integrated Factors & Features

The model evaluates a comprehensive taxonomy of 23 biological, microbial, sensor, and environmental factors:

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
| **Profile & Health History** | `breed` | Livestock breed (*Holstein Friesian*, *Gir*, *Sahiwal*) |
| | `age_years` | Animal age (Years) |
| | `previous_mastitis_history` | Prior mastitis history (0 = No, 1 = Yes) |
| | `vaccinated` | Vaccination protection status (0 = No, 1 = Yes) |
| | `chronic_disease_flag` | Chronic health condition (0 = No, 1 = Yes) |

---

## 🏛️ Web Portal Architecture (5 Interactive Tabs)

```text
       🇮🇳 PASHU SANJEEVANI AI NATIONAL PORTAL (STREMLIT UI)
                         │
    ┌────────────────────┼────────────────────┬────────────────────┬────────────────────┐
    ▼                    ▼                    ▼                    ▼                    ▼
📊 TAB 1             🐄 TAB 2             🦠 TAB 3             📡 TAB 4             📋 TAB 5
Pashu Diagnostic     Herd Surveillance    Pathogen & Milk      IoT Edge Gateway     Farmer SOP &
Center (Single Cow)  & Bulk CSV Engine    Biomarker Radar      Developer Console    Helpline Contact
```

1. **📊 Pashu Diagnostic Center**: Single cow diagnostic evaluation, live animated risk probability gauge bar, top 5 AI explainability drivers (*Increases Risk* vs *Protective Factor*), vitals grid, and veterinary protocol.
2. **🐄 Herd Surveillance & Bulk CSV Engine**: Whole-herd batch processing engine. Allows 1-click execution on 12,000-cow datasets or custom CSV uploads, displaying priority risk tables and CSV export.
3. **🦠 Pathogen & Biomarker Radar**: Multi-strain pathogen CFU bar charts, dominant pathogen strain indicators, and milk electrical conductivity warnings.
4. **📡 IoT Edge Gateway Console**: Real-time JSON payload inspector, formatted MQTT/REST API integration code for microcontrollers (ESP32 / Arduino / Raspberry Pi).
5. **📋 Farmer SOP Guidelines & Helplines**: Sanitary milking SOPs, biosecurity protocols, and 24x7 Pashu Sanjeevani helpline details.

---

## 📡 IoT & Hardware Edge Node API

To stream sensor payloads from hardware microcontrollers to the AI engine:

```python
from hardware_interface import process_sensor_reading

# Accept JSON string or dict directly from MQTT / HTTP POST
json_payload = """
{
    "cow_id": "COW_999",
    "body_temperature_c": 39.7,
    "udder_surface_temperature_c": 40.1,
    "milk_conductivity_mS_cm": 6.8,
    "milk_yield_kg_day": 12.0,
    "S_aureus_load_log10_cfu_equiv": 4.2
}
"""

response = process_sensor_reading(json_payload)

print("Risk Category:", response["risk_level"])            # "HIGH"
print("Probability:", response["mastitis_probability"])   # 0.9996
print("Top Factor:", response["contributing_factors"][0]) # Udder Surface Temperature
```

---

## 🛠️ Local Installation & Setup

```bash
# 1. Clone Repository
git clone https://github.com/YuvasriPraksh/bovine-demo-ml-0-.git
cd bovine-mastitis-prediction

# 2. Install Dependencies
pip install -r requirements.txt

# 3. Launch Local Streamlit Web Application
streamlit run streamlit_app.py

# 4. Retrain & Tune XGBoost Model
python src/train_xgboost_best.py

# 5. Run Hardware Integration Audit Suite
python scratch/hardware_readiness_audit.py
```

---

## 📁 Repository Directory Structure

```text
bovine-mastitis-prediction/
├── data/
│   └── synthetic_bovine_mastitis_integrated_dataset.csv   # Unified 12k dataset
├── models/
│   ├── best_model_XGBoost.pkl                             # Optimized XGBoost pipeline
│   └── strict_early_risk_model.pkl                       # Active inference model pipeline
├── outputs/
│   ├── figures/                                           # Evaluation charts & ROC/PR curves
│   └── reports/                                           # Evaluation reports & logs
├── src/
│   ├── hardware_interface.py                              # Hardware/IoT JSON interface
│   ├── predict.py                                         # ML inference engine & explainability
│   ├── preprocessing.py                                    # Data preprocessor & alias mapping
│   ├── test_predictions.py                                 # Scenario test verification suite
│   └── train_xgboost_best.py                              # XGBoost hyperparameter optimizer
├── README.md                                               # Official repository documentation
├── requirements.txt                                        # Python dependencies
└── streamlit_app.py                                        # Streamlit web dashboard
```

---

## 📜 Disclaimer & License

*Pashu Sanjeevani AI is a software prototype developed for livestock AI research, IoT integration demonstration, and agricultural decision support. All datasets are synthetic representations designed to model physiological correlations.*
