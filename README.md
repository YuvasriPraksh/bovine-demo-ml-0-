# 🐄 MastitisAI
### Bovine Mastitis Early-Risk Prediction & Monitoring System

> An AI-assisted software prototype for estimating bovine mastitis risk from physiological, behavioural, environmental and farm-management parameters.

[![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)](https://www.python.org/)
[![Scikit-learn](https://img.shields.io/badge/ML-Scikit--learn-orange?logo=scikit-learn)](https://scikit-learn.org/)
[![Streamlit](https://img.shields.io/badge/UI-Streamlit-red?logo=streamlit)](https://streamlit.io/)
[![Status](https://img.shields.io/badge/Status-SIH%20Prototype-success)]()
[![Data](https://img.shields.io/badge/Data-Synthetic-yellow)]()

---

## 🌱 What is this project?

Mastitis is an inflammation of the mammary gland in dairy cattle. It can affect animal health, milk production, milk quality and farm profitability.

One of the challenges with mastitis management is that visible clinical signs may appear only after the condition has already developed.

Our idea is to use information that can be collected continuously from a cow and its surroundings to identify animals that show a **higher estimated risk of mastitis**.

The current prototype takes multiple cow-level and farm-level parameters and passes them through a machine-learning pipeline.

The output is not simply:

> "Mastitis / No Mastitis"

Instead, the system provides:

- Estimated mastitis-risk probability
- Risk category
- Model-associated contributing factors
- Suggested monitoring action
- A dashboard for viewing the result

The long-term goal is to connect the software with real livestock sensors and farm-management systems.

---

# 🎯 Problem We Are Trying to Solve

Traditional monitoring can depend heavily on manual observation.

A farmer may need to notice changes such as:

- unusual body temperature
- changes in activity
- reduced rumination
- changes in feed or water intake
- poor hygiene conditions
- previous mastitis history
- environmental stress

Individually, these signals may not be enough.

Our approach is to combine them and let a machine-learning model estimate the overall risk.

```text
              COW + FARM DATA
                     │
                     ▼
        ┌─────────────────────────┐
        │  Physiological Signals  │
        │  Behavioural Signals    │
        │  Cow History             │
        │  Environment              │
        │  Farm Management          │
        └────────────┬────────────┘
                     │
                     ▼
              DATA PROCESSING
                     │
                     ▼
             MACHINE LEARNING
                     │
                     ▼
          MASTITIS-RISK SCORE
                     │
              ┌──────┴──────┐
              ▼             ▼
          RISK LEVEL     FACTORS
          LOW/MED/HIGH   CONTRIBUTING
              │             │
              └──────┬──────┘
                     ▼
             FARMER DASHBOARD
