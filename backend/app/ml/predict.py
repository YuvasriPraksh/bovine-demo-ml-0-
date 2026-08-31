import os
import sys
import joblib
import numpy as np
import pandas as pd

# Add workspace root and ml/src to Python path so ML prediction engine can be imported
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
ML_SRC_DIR = os.path.join(ROOT_DIR, "ml", "src")
for p in [ROOT_DIR, ML_SRC_DIR]:
    if p not in sys.path:
        sys.path.insert(0, p)

try:
    from ml.src.predict import (
        predict_mastitis_risk,
        _pipeline as src_pipeline,
        MODEL_PATH as SRC_MODEL_PATH
    )
except ImportError:
    from predict import (
        predict_mastitis_risk,
        _pipeline as src_pipeline,
        MODEL_PATH as SRC_MODEL_PATH
    )

MODEL_PATH = os.path.join(ROOT_DIR, 'ml', 'models', 'strict_early_risk_model.pkl')
if not os.path.exists(MODEL_PATH):
    MODEL_PATH = os.path.join(ROOT_DIR, 'ml', 'models', 'best_model_XGBoost.pkl')

_model = None
_pipeline = None

def get_model_and_pipeline():
    global _model, _pipeline
    if _pipeline is None:
        if src_pipeline is not None:
            _pipeline = src_pipeline
        elif os.path.exists(MODEL_PATH):
            _pipeline = joblib.load(MODEL_PATH)
        else:
            print(f"[Warning] Model file not found at {MODEL_PATH}")
            _pipeline = None
    if _pipeline is not None and hasattr(_pipeline, 'named_steps'):
        _model = _pipeline.named_steps.get('classifier', None)
    return _model, _pipeline

REFERENCE_BASELINES = {
    'body_temperature_c': {'normal_max': 38.8, 'critical': 39.5, 'weight': 1.8, 'label': 'Elevated Body Temperature'},
    'udder_surface_temperature_c': {'normal_max': 34.2, 'critical': 35.5, 'weight': 2.0, 'label': 'Elevated Udder Surface Temperature'},
    'milk_conductivity_mS_cm': {'normal_max': 4.3, 'critical': 5.2, 'weight': 2.5, 'label': 'High Milk Electrical Conductivity (Ion leakage)'},
    'milk_yield_kg_day': {'normal_min': 15.0, 'critical': 10.0, 'weight': 1.4, 'label': 'Sudden Milk Yield Drop'},
    'hygiene_score_0_100': {'normal_min': 65.0, 'critical': 40.0, 'weight': 1.3, 'label': 'Poor Barn/Teat Hygiene Score'},
    'environment_total_mastitis_pathogen_load_log10': {'normal_max': 4.5, 'critical': 5.5, 'weight': 1.6, 'label': 'High Environmental Pathogen Exposure'},
    'S_aureus_load_log10_cfu_equiv': {'normal_max': 4.0, 'critical': 5.0, 'weight': 1.5, 'label': 'Elevated S. aureus Proxy Load'},
    'S_uberis_load_log10_cfu_equiv': {'normal_max': 4.0, 'critical': 5.0, 'weight': 1.5, 'label': 'Elevated S. uberis Proxy Load'},
    'E_coli_load_log10_cfu_equiv': {'normal_max': 4.0, 'critical': 5.0, 'weight': 1.5, 'label': 'Elevated E. coli Proxy Load'},
    'previous_mastitis_history': {'normal_max': 0, 'critical': 1, 'weight': 1.2, 'label': 'Prior History of Mastitis Episode'},
    'ambient_temperature_c': {'normal_max': 28.0, 'critical': 35.0, 'weight': 1.1, 'label': 'Heat Stress Environmental Condition'},
    'relative_humidity_pct': {'normal_max': 70.0, 'critical': 85.0, 'weight': 1.1, 'label': 'High Ambient Barn Humidity'}
}

def analyze_risk_factors(data_dict):
    factors = []
    for key, rule in REFERENCE_BASELINES.items():
        val = data_dict.get(key)
        if val is None:
            continue
        try:
            val = float(val)
        except (ValueError, TypeError):
            continue
        impact_score = 0.0
        details = ''
        if 'normal_max' in rule and val > rule['normal_max']:
            excess = (val - rule['normal_max']) / (rule['critical'] - rule['normal_max'] + 1e-5)
            impact_score = min(excess * rule['weight'], 3.0)
            norm_max = rule['normal_max']
            details = f'{val:.2f} (Threshold: <= {norm_max})'
        elif 'normal_min' in rule and val < rule['normal_min']:
            deficit = (rule['normal_min'] - val) / (rule['normal_min'] - rule['critical'] + 1e-5)
            impact_score = min(deficit * rule['weight'], 3.0)
            norm_min = rule['normal_min']
            details = f'{val:.2f} (Threshold: >= {norm_min})'

        if impact_score > 0.3:
            factors.append({
                'factor': rule['label'],
                'feature_name': key,
                'observed_value': val,
                'impact_score': round(impact_score, 2),
                'details': details
            })
    factors = sorted(factors, key=lambda x: x['impact_score'], reverse=True)
    return factors[:5]

def generate_recommendations(risk_category, top_factors, env_risk_favorable):
    recs = []
    if risk_category in ['High', 'Moderate']:
        recs.append('Conduct on-farm California Mastitis Test (CMT) or individual quarter conductivity check during next milking.')
        recs.append('Isolate milk from this cow until subclinical status is cleared.')
        recs.append('Inspect teat skin integrity, pre-dip contact time, and post-milking barrier teat dip application.')
    else:
        recs.append('Maintain standard milking hygiene and scheduled herd health monitoring.')

    if env_risk_favorable:
        recs.append('Environmental conditions (heat/humidity index) favor pathogen proliferation: increase stall bedding replacement and ventilation.')

    has_temp_issue = any('Temperature' in str(f.get('factor', '')) for f in top_factors)
    if has_temp_issue and risk_category == 'High':
        recs.append('Elevated biometric temperature detected: check for systemic clinical signs (swollen quarters, appetite loss, rectal temp).')

    recs.append('Note: These recommendations serve as decision-support alerts and do not replace professional veterinary clinical diagnosis.')
    return recs

def predict_single_animal(data: dict):
    # Run prediction using the XGBoost model pipeline from src/predict.py
    ml_result = predict_mastitis_risk(data)

    prob_mastitis = float(ml_result.get("mastitis_probability", 0.0))
    prob_healthy = float(ml_result.get("healthy_probability", 1.0 - prob_mastitis))
    risk_level = ml_result.get("risk_level", "LOW")

    # Map mastitis probability to risk score (0 - 100%) and risk category
    risk_score = round(prob_mastitis * 100.0, 1)

    if prob_mastitis < 0.20:
        risk_category = "No_Risk"
    elif prob_mastitis < 0.40:
        risk_category = "Low"
    elif prob_mastitis < 0.70:
        risk_category = "Moderate"
    else:
        risk_category = "High"

    # Multi-class probability breakdown for dashboard charts
    class_probs = {
        "No_Risk": round(max(0.0, prob_healthy * 70.0), 1),
        "Low": round(max(0.0, prob_healthy * 30.0), 1),
        "Moderate": round(max(0.0, prob_mastitis * 30.0), 1),
        "High": round(max(0.0, prob_mastitis * 70.0), 1)
    }

    # Extract top risk factors from model-based contributing factors & reference rules
    model_factors = ml_result.get("contributing_factors", [])
    top_factors = []
    for factor in model_factors:
        feat_name = factor.get("name", "")
        obs_val = 0.0
        if feat_name in data and data[feat_name] is not None:
            try:
                obs_val = float(data[feat_name])
            except (ValueError, TypeError):
                obs_val = 0.0
        contrib = factor.get("contribution", 0.0)
        direction = factor.get("direction", "risk")
        top_factors.append({
            "factor": factor.get("label", feat_name),
            "feature_name": feat_name,
            "observed_value": obs_val,
            "impact_score": round(abs(contrib), 2),
            "details": f"Model contribution: {contrib:+.4f} ({direction})"
        })

    # Fallback to reference baseline rule factors if model factors empty
    if not top_factors:
        top_factors = analyze_risk_factors(data)

    amb_temp = float(data.get('ambient_temperature_c', 28.0) or 28.0)
    rel_hum = float(data.get('relative_humidity_pct', 65.0) or 65.0)
    thi = 0.8 * amb_temp + (rel_hum / 100.0) * (amb_temp - 14.4) + 46.4
    env_risk_favorable = bool(thi >= 72.0 or (amb_temp >= 28.0 and rel_hum >= 75.0))

    env_indicator = {
        'ambient_temperature_c': amb_temp,
        'relative_humidity_pct': rel_hum,
        'calculated_thi': round(thi, 1),
        'conditions_favorable_for_pathogens': env_risk_favorable,
        'interpretation': 'Elevated heat/humidity index associates with increased bacterial proliferation risk in bedding' if env_risk_favorable else 'Barn environmental temperature and humidity are within optimal range'
    }

    forecast_7d_prob = round(min(99.0, prob_mastitis * 100.0 * 1.1), 1)
    forecast_14d_prob = round(min(99.0, prob_mastitis * 100.0 * 1.25), 1)

    recommendations = generate_recommendations(risk_category, top_factors, env_risk_favorable)

    from datetime import datetime
    timestamp_str = datetime.now().isoformat()

    return {
        # Frontend UI expected response contract
        'animal_id': str(data.get('animal_id', 'SIMULATED_COW')),
        'risk_category': risk_category,
        'risk_score': risk_score,
        'class_probabilities': class_probs,
        'top_risk_factors': top_factors,
        'forecast_7d_risk_pct': forecast_7d_prob,
        'forecast_14d_risk_pct': forecast_14d_prob,
        'environmental_risk': env_indicator,
        'recommendations': recommendations,
        'timestamp': timestamp_str,

        # Core ML model prediction contract
        'prediction': ml_result.get('prediction', 1 if prob_mastitis >= 0.5 else 0),
        'mastitis_probability': ml_result.get('mastitis_probability', prob_mastitis),
        'healthy_probability': ml_result.get('healthy_probability', prob_healthy),
        'risk_level': ml_result.get('risk_level', risk_level),
        'risk_label': ml_result.get('risk_label', 'At Risk' if prob_mastitis >= 0.3 else 'Healthy / Low Risk'),
        'contributing_factors': ml_result.get('contributing_factors', [])
    }
