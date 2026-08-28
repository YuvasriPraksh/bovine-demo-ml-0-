"""
predict.py
----------
Reusable mastitis risk prediction component.

Public API:
    predict_mastitis_risk(input_data)  -> dict with prediction + explainability

The pipeline (preprocessing + model) is loaded once at import time.
All preprocessing (imputation, scaling, one-hot encoding) is applied
automatically through the saved sklearn Pipeline — never duplicated here.

Hardware integration note:
    Sensor readings -> convert to dict matching REQUIRED_FEATURES -> call
    predict_mastitis_risk(dict) -> use returned JSON for display or alerting.
"""

import os
import sys
import numpy as np
import pandas as pd
import joblib

# ---------------------------------------------------------------------------
# Feature schema — must match the strict model training exactly
# ---------------------------------------------------------------------------
REQUIRED_FEATURES = {
    'Breed':                      str,
    'Age_Years':                  (int, float),
    'Lactation_Number':           (int, float),
    'Parity':                     (int, float),
    'Days_In_Milk':               (int, float),
    'Previous_Mastitis_History':  (int, float),
    'Vaccination_Status':         (int, float),
    'Body_Temperature_C':         (int, float),
    'Udder_Temperature_C':        (int, float),
    'Activity_Index':             (int, float),
    'Rumination_Time_min':        (int, float),
    'Feed_Intake_kgDM':           (int, float),
    'Water_Intake_L':             (int, float),
    'Ambient_Temperature_C':      (int, float),
    'Humidity_pct':               (int, float),
    'THI':                        (int, float),
    'Hygiene_Score':              (int, float),
    'Bedding_Cleanliness_Score':  (int, float),
    'Milking_Frequency':          (int, float),
}

# Risk thresholds
THRESHOLD_LOW    = 0.30
THRESHOLD_HIGH   = 0.70

MODEL_PATH = 'models/strict_early_risk_model.pkl'

# Human-readable labels for feature contributions in the UI
FEATURE_LABELS = {
    'Body_Temperature_C':        'Body Temperature',
    'Udder_Temperature_C':       'Udder Temperature',
    'Activity_Index':            'Activity Index',
    'Rumination_Time_min':       'Rumination Time',
    'Feed_Intake_kgDM':          'Feed Intake',
    'Water_Intake_L':            'Water Intake',
    'Ambient_Temperature_C':     'Ambient Temperature',
    'Humidity_pct':              'Humidity',
    'THI':                       'Temperature-Humidity Index',
    'Hygiene_Score':             'Hygiene Score',
    'Bedding_Cleanliness_Score': 'Bedding Cleanliness',
    'Milking_Frequency':         'Milking Frequency',
    'Age_Years':                 'Age',
    'Lactation_Number':          'Lactation Number',
    'Parity':                    'Parity',
    'Days_In_Milk':              'Days in Milk',
    'Previous_Mastitis_History': 'Previous Mastitis History',
    'Vaccination_Status':        'Vaccination Status',
    'Breed_Holstein_Friesian':   'Breed: Holstein Friesian',
    'Breed_Gir':                 'Breed: Gir',
    'Breed_Sahiwal':             'Breed: Sahiwal',
}

# Load model once at module level
try:
    if os.path.exists(MODEL_PATH):
        _pipeline = joblib.load(MODEL_PATH)
    else:
        _pipeline = None
        print(f"Warning: Model not found at {MODEL_PATH}")
except Exception as e:
    _pipeline = None
    print(f"Warning: Could not load model — {e}")


# ---------------------------------------------------------------------------
# Input validation
# ---------------------------------------------------------------------------
def validate_input(input_df: pd.DataFrame) -> None:
    missing = [f for f in REQUIRED_FEATURES if f not in input_df.columns]
    if missing:
        raise ValueError(f"Missing required features: {missing}")

    for feat, expected in REQUIRED_FEATURES.items():
        val = input_df[feat].iloc[0]
        if pd.isnull(val):
            raise ValueError(f"Feature '{feat}' is null. All features must have a value.")
        if not isinstance(val, expected):
            if expected == (int, float):
                try:
                    float(val)
                except (ValueError, TypeError):
                    raise ValueError(
                        f"Feature '{feat}' must be numeric, got {type(val).__name__} ({val!r})"
                    )
            elif expected is str and not isinstance(val, str):
                raise ValueError(
                    f"Feature '{feat}' must be a string, got {type(val).__name__} ({val!r})"
                )


# ---------------------------------------------------------------------------
# Contributing-factor calculation (Logistic Regression)
# ---------------------------------------------------------------------------
def _get_contributing_factors(input_df: pd.DataFrame, pipeline, top_n: int = 5):
    """
    Returns the top-n model-associated contributing factors.

    Method: element-wise product of scaled feature values and LR coefficients.
    A positive product pushes toward mastitis; negative toward healthy.

    Returns a list of dicts:
        [{'name': str, 'label': str, 'contribution': float, 'direction': 'risk'|'protective'}, ...]
    """
    try:
        preprocessor = pipeline.named_steps['preprocessor']
        classifier   = pipeline.named_steps['classifier']

        if not hasattr(classifier, 'coef_'):
            return []   # Feature not supported for non-LR models

        # Transform input — safely convert to dense 1-D array
        transformed = preprocessor.transform(input_df)
        if hasattr(transformed, 'toarray'):
            transformed = transformed.toarray()
        vec = transformed.flatten()

        coef = classifier.coef_[0]
        contributions = vec * coef

        # Build feature name list in the same column order as the transformer
        num_names = list(preprocessor.transformers_[0][2])  # NUMERIC_FEATURES
        cat_names = list(
            preprocessor.named_transformers_['cat']
            .named_steps['onehot']
            .get_feature_names_out(['Breed'])
        )
        all_names = num_names + cat_names

        paired = sorted(zip(all_names, contributions), key=lambda x: abs(x[1]), reverse=True)

        factors = []
        for name, contrib in paired[:top_n]:
            label = FEATURE_LABELS.get(name, name.replace('_', ' '))
            direction = 'risk' if contrib > 0 else 'protective'
            factors.append({
                'name':         name,
                'label':        label,
                'contribution': float(round(contrib, 4)),
                'direction':    direction,
            })
        return factors

    except Exception as e:
        return [{'name': 'error', 'label': f'Factor calculation error: {e}',
                 'contribution': 0.0, 'direction': 'risk'}]


# ---------------------------------------------------------------------------
# Main public function
# ---------------------------------------------------------------------------
def predict_mastitis_risk(input_data, top_n: int = 5) -> dict:
    """
    Predict mastitis risk for one animal.

    Args:
        input_data : dict or single-row pd.DataFrame with all 19 required features.
        top_n      : number of contributing factors to return.

    Returns:
        {
            "prediction":           0 or 1,
            "mastitis_probability": float  (0–1),
            "healthy_probability":  float  (0–1),
            "risk_level":           "LOW" | "MEDIUM" | "HIGH",
            "risk_label":           "Healthy / Low Risk" | "At Risk",
            "contributing_factors": [
                {"name": str, "label": str, "contribution": float, "direction": str},
                ...
            ]
        }
    """
    if _pipeline is None:
        raise RuntimeError(f"Model pipeline not loaded. Expected at: {MODEL_PATH}")

    # Normalise input
    if isinstance(input_data, dict):
        input_df = pd.DataFrame([input_data])
    elif isinstance(input_data, pd.DataFrame):
        input_df = input_data.reset_index(drop=True).copy()
    else:
        raise TypeError("input_data must be a dict or pd.DataFrame")

    if len(input_df) != 1:
        raise ValueError("predict_mastitis_risk accepts exactly one animal per call.")

    validate_input(input_df)

    # Run pipeline
    prediction     = int(_pipeline.predict(input_df)[0])
    probabilities  = _pipeline.predict_proba(input_df)[0]
    prob_mastitis  = float(probabilities[1])
    prob_healthy   = float(probabilities[0])

    # Risk classification
    if prob_mastitis < THRESHOLD_LOW:
        risk_level = "LOW"
        risk_label = "Healthy / Low Risk"
    elif prob_mastitis <= THRESHOLD_HIGH:
        risk_level = "MEDIUM"
        risk_label = "At Risk"
    else:
        risk_level = "HIGH"
        risk_label = "At Risk"

    # Contributing factors
    factors = _get_contributing_factors(input_df, _pipeline, top_n=top_n)

    return {
        "prediction":           prediction,
        "mastitis_probability": round(prob_mastitis, 4),
        "healthy_probability":  round(prob_healthy,  4),
        "risk_level":           risk_level,
        "risk_label":           risk_label,
        "contributing_factors": factors,
    }


# ---------------------------------------------------------------------------
# CLI demo
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("Bovine Mastitis Early-Risk Prediction — CLI Demo")
    print("DISCLAIMER: Synthetic prototype. Not a clinical diagnosis.\n")

    demo = {
        'Breed': 'Holstein_Friesian',
        'Age_Years': 5.5, 'Lactation_Number': 4, 'Parity': 4,
        'Days_In_Milk': 120, 'Previous_Mastitis_History': 1,
        'Vaccination_Status': 1, 'Body_Temperature_C': 39.5,
        'Udder_Temperature_C': 39.8, 'Activity_Index': 45.0,
        'Rumination_Time_min': 350.0, 'Feed_Intake_kgDM': 14.5,
        'Water_Intake_L': 60.0, 'Ambient_Temperature_C': 28.0,
        'Humidity_pct': 70.0, 'THI': 78.5, 'Hygiene_Score': 3,
        'Bedding_Cleanliness_Score': 3, 'Milking_Frequency': 2,
    }

    result = predict_mastitis_risk(demo)
    print(f"Prediction:           {result['prediction']} ({result['risk_label']})")
    print(f"Mastitis Probability: {result['mastitis_probability']*100:.1f}%")
    print(f"Risk Level:           {result['risk_level']}")
    print("\nModel-Associated Contributing Factors:")
    for i, f in enumerate(result['contributing_factors'], 1):
        arrow = "^" if f['direction'] == 'risk' else "v"
        print(f"  {i}. [{arrow}] {f['label']}  (score: {f['contribution']:+.4f})")
