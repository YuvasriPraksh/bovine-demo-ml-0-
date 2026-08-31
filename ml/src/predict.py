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
# ---------------------------------------------------------------------------
# Feature schema — matches the unified 23-factor feature schema
# ---------------------------------------------------------------------------
REQUIRED_FEATURES = {
    'breed':                                          str,
    'dominant_environment_pathogen':                  str,
    'age_years':                                      (int, float),
    'previous_mastitis_history':                      (int, float),
    'vaccinated':                                     (int, float),
    'chronic_disease_flag':                           (int, float),
    'ambient_temperature_c':                          (int, float),
    'relative_humidity_pct':                          (int, float),
    'environment_total_mastitis_pathogen_load_log10': (int, float),
    'S_aureus_load_log10_cfu_equiv':                  (int, float),
    'S_uberis_load_log10_cfu_equiv':                  (int, float),
    'E_coli_load_log10_cfu_equiv':                    (int, float),
    'K_pneumoniae_load_log10_cfu_equiv':              (int, float),
    'S_agalactiae_load_log10_cfu_equiv':              (int, float),
    'milk_yield_kg_day':                              (int, float),
    'milk_conductivity_mS_cm':                        (int, float),
    'body_temperature_c':                             (int, float),
    'udder_surface_temperature_c':                    (int, float),
    'activity_score':                                 (int, float),
    'rumination_min_day':                             (int, float),
    'feed_intake_kg_day':                             (int, float),
    'water_intake_l_day':                             (int, float),
    'hygiene_score_0_100':                            (int, float)
}

# Risk thresholds
THRESHOLD_LOW    = 0.30
THRESHOLD_HIGH   = 0.70

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CANDIDATE_MODEL_PATHS = [
    os.path.join(BASE_DIR, 'ml', 'models', 'strict_early_risk_model.pkl'),
    os.path.join(BASE_DIR, 'ml', 'models', 'best_model_XGBoost.pkl'),
    os.path.join(BASE_DIR, 'models', 'strict_early_risk_model.pkl'),
    os.path.join(BASE_DIR, 'models', 'best_model_XGBoost.pkl'),
    'ml/models/strict_early_risk_model.pkl',
    'ml/models/best_model_XGBoost.pkl',
    'models/strict_early_risk_model.pkl',
    'models/best_model_XGBoost.pkl'
]

MODEL_PATH = None
for candidate in CANDIDATE_MODEL_PATHS:
    if os.path.exists(candidate):
        MODEL_PATH = candidate
        break

if MODEL_PATH is None:
    MODEL_PATH = os.path.join(BASE_DIR, 'ml', 'models', 'strict_early_risk_model.pkl')

# Human-readable labels for feature contributions in the UI
FEATURE_LABELS = {
    'body_temperature_c':                             'Body Temperature',
    'udder_surface_temperature_c':                    'Udder Surface Temperature',
    'milk_conductivity_mS_cm':                        'Milk Electrical Conductivity',
    'environment_total_mastitis_pathogen_load_log10': 'Total Environmental Pathogen Load',
    'S_aureus_load_log10_cfu_equiv':                  'S. aureus Load',
    'S_uberis_load_log10_cfu_equiv':                  'S. uberis Load',
    'E_coli_load_log10_cfu_equiv':                    'E. coli Load',
    'K_pneumoniae_load_log10_cfu_equiv':              'K. pneumoniae Load',
    'S_agalactiae_load_log10_cfu_equiv':              'S. agalactiae Load',
    'activity_score':                                 'Activity Index',
    'rumination_min_day':                             'Daily Rumination Time',
    'feed_intake_kg_day':                             'Daily Feed Intake',
    'water_intake_l_day':                             'Daily Water Intake',
    'milk_yield_kg_day':                              'Daily Milk Yield',
    'ambient_temperature_c':                          'Ambient Temperature (Heat Stress)',
    'relative_humidity_pct':                          'Relative Humidity',
    'hygiene_score_0_100':                            'Farm Hygiene Score',
    'age_years':                                      'Age (Years)',
    'previous_mastitis_history':                      'Previous Mastitis History',
    'vaccinated':                                     'Vaccination Protection',
    'chronic_disease_flag':                           'Chronic Health Condition'
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
# Input validation & alias mapping
# ---------------------------------------------------------------------------
DEFAULT_FEATURE_VALUES = {
    'breed': 'Holstein_Friesian',
    'dominant_environment_pathogen': 'S. uberis',
    'age_years': 4.5,
    'previous_mastitis_history': 0,
    'vaccinated': 1,
    'chronic_disease_flag': 0,
    'ambient_temperature_c': 28.0,
    'relative_humidity_pct': 65.0,
    'environment_total_mastitis_pathogen_load_log10': 3.5,
    'S_aureus_load_log10_cfu_equiv': 2.5,
    'S_uberis_load_log10_cfu_equiv': 2.8,
    'E_coli_load_log10_cfu_equiv': 2.2,
    'K_pneumoniae_load_log10_cfu_equiv': 2.1,
    'S_agalactiae_load_log10_cfu_equiv': 2.0,
    'milk_yield_kg_day': 22.0,
    'milk_conductivity_mS_cm': 4.8,
    'body_temperature_c': 38.6,
    'udder_surface_temperature_c': 38.3,
    'activity_score': 65.0,
    'rumination_min_day': 480.0,
    'feed_intake_kg_day': 18.0,
    'water_intake_l_day': 85.0,
    'hygiene_score_0_100': 60.0
}

ALIAS_MAP = {
    'Breed': 'breed',
    'Age_Years': 'age_years',
    'Previous_Mastitis_History': 'previous_mastitis_history',
    'Vaccination_Status': 'vaccinated',
    'Body_Temperature_C': 'body_temperature_c',
    'Udder_Temperature_C': 'udder_surface_temperature_c',
    'Milk_Yield': 'milk_yield_kg_day',
    'Milk_Conductivity': 'milk_conductivity_mS_cm',
    'Ambient_Temperature_C': 'ambient_temperature_c',
    'Humidity_pct': 'relative_humidity_pct',
    'Activity_Index': 'activity_score',
    'Rumination_Time_min': 'rumination_min_day',
    'Feed_Intake_kgDM': 'feed_intake_kg_day',
    'Water_Intake_L': 'water_intake_l_day',
    'Hygiene_Score': 'hygiene_score_0_100'
}

def validate_input(input_df: pd.DataFrame) -> pd.DataFrame:
    # Map legacy column names to unified factor names
    for legacy_col, v2_col in ALIAS_MAP.items():
        if legacy_col in input_df.columns and v2_col not in input_df.columns:
            input_df[v2_col] = input_df[legacy_col]

    # Fill defaults for any missing required features
    for feat, default_val in DEFAULT_FEATURE_VALUES.items():
        if feat not in input_df.columns:
            input_df[feat] = default_val

    missing = [f for f in REQUIRED_FEATURES if f not in input_df.columns]
    if missing:
        raise ValueError(f"Missing required features: {missing}")

    for feat, expected in REQUIRED_FEATURES.items():
        val = input_df[feat].iloc[0]
        if pd.isnull(val):
            input_df[feat] = DEFAULT_FEATURE_VALUES.get(feat, 0.0)
    return input_df


# ---------------------------------------------------------------------------
# Contributing-factor calculation (Logistic Regression)
# ---------------------------------------------------------------------------
def _get_contributing_factors(input_df: pd.DataFrame, pipeline, top_n: int = 5):
    """
    Returns the top-n model-associated contributing factors.
    Supports both linear models (coef_) and tree-based models like XGBoost (feature_importances_).
    """
    try:
        preprocessor = pipeline.named_steps['preprocessor']
        classifier   = pipeline.named_steps['classifier']

        # Transform input — safely convert to dense 1-D array
        transformed = preprocessor.transform(input_df)
        if hasattr(transformed, 'toarray'):
            transformed = transformed.toarray()
        vec = transformed.flatten()

        if hasattr(classifier, 'coef_'):
            coef = classifier.coef_[0]
            contributions = vec * coef
        elif hasattr(classifier, 'feature_importances_'):
            importances = classifier.feature_importances_
            contributions = vec * importances
        else:
            return []

        # Build feature name list in the same column order as the transformer
        num_names = list(preprocessor.transformers_[0][2])  # NUMERIC_FEATURES
        cat_features = list(preprocessor.transformers_[1][2])
        cat_names = list(
            preprocessor.named_transformers_['cat']
            .named_steps['onehot']
            .get_feature_names_out(cat_features)
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


def predict_mastitis_risk_batch(df: pd.DataFrame) -> pd.DataFrame:
    """
    Predict mastitis risk for a DataFrame of cows in batch.

    Args:
        df : DataFrame containing cow feature columns.

    Returns:
        DataFrame with added columns: mastitis_probability, mastitis_risk_category.
    """
    if _pipeline is None:
        raise RuntimeError(f"Model pipeline not loaded. Expected at: {MODEL_PATH}")

    df_norm = df.copy()

    # Map legacy aliases and fill default values for missing columns
    for legacy_col, v2_col in ALIAS_MAP.items():
        if legacy_col in df_norm.columns and v2_col not in df_norm.columns:
            df_norm[v2_col] = df_norm[legacy_col]

    for feat, default_val in DEFAULT_FEATURE_VALUES.items():
        if feat not in df_norm.columns:
            df_norm[feat] = default_val

    probs = _pipeline.predict_proba(df_norm)[:, 1]
    df_norm['mastitis_probability'] = probs
    
    categories = []
    for p in probs:
        if p < THRESHOLD_LOW:
            categories.append("LOW")
        elif p <= THRESHOLD_HIGH:
            categories.append("MEDIUM")
        else:
            categories.append("HIGH")
    df_norm['mastitis_risk_category'] = categories
    return df_norm


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
