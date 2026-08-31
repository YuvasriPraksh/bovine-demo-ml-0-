"""
test_v2_schema.py
-----------------
Verification script for 27-feature v2 dataset generation & preprocessing compatibility.
"""

import os
import pandas as pd
import numpy as np
from preprocessing import load_and_filter_data

EXPECTED_27_COLUMNS = [
    'record_date',
    'farm_id',
    'animal_id',
    'breed',
    'age_years',
    'previous_mastitis_history',
    'vaccinated',
    'chronic_disease_flag',
    'ambient_temperature_c',
    'relative_humidity_pct',
    'environment_total_mastitis_pathogen_load_log10',
    'S_aureus_load_log10_cfu_equiv',
    'S_uberis_load_log10_cfu_equiv',
    'E_coli_load_log10_cfu_equiv',
    'K_pneumoniae_load_log10_cfu_equiv',
    'S_agalactiae_load_log10_cfu_equiv',
    'dominant_environment_pathogen',
    'milk_yield_kg_day',
    'milk_conductivity_mS_cm',
    'body_temperature_c',
    'udder_surface_temperature_c',
    'clinical_mastitis_now',
    'synthetic_risk_score_pct',
    'mastitis_risk_category',
    'mastitis_in_next_7d',
    'mastitis_in_next_14d',
    'days_to_synthetic_event'
]

def test_v2_schema():
    v2_path = "data/processed/mastitis_dataset_v2.csv"
    assert os.path.exists(v2_path), f"Dataset file missing: {v2_path}"
    
    df = pd.read_csv(v2_path)
    print(f"Loaded {len(df)} rows and {len(df.columns)} columns from {v2_path}")
    
    # 1. Check all 27 features exist
    missing_cols = [col for col in EXPECTED_27_COLUMNS if col not in df.columns]
    assert len(missing_cols) == 0, f"Missing expected columns in v2 dataset: {missing_cols}"
    print("[OK] All 27 specified feature columns are present.")
    
    # 2. Check no null values
    null_counts = df[EXPECTED_27_COLUMNS].isnull().sum()
    assert null_counts.sum() == 0, f"Unexpected null values found: {null_counts[null_counts > 0]}"
    print("[OK] Zero missing values across all 27 features.")
    
    # 3. Check risk categories
    valid_categories = {'No Risk', 'Low Risk', 'Moderate Risk', 'High Risk'}
    found_categories = set(df['mastitis_risk_category'].unique())
    assert found_categories.issubset(valid_categories), f"Invalid risk categories: {found_categories}"
    print(f"[OK] Risk categories validated: {found_categories}")
    
    # 4. Test backward compatibility loading pipeline
    X, y = load_and_filter_data(v2_path)
    assert len(X) == len(df), f"Expected {len(df)} rows in X, got {len(X)}"
    assert len(y) == len(df), f"Expected {len(df)} rows in y, got {len(y)}"
    print(f"[OK] Backward compatibility loader test passed! Features shape: {X.shape}, Target shape: {y.shape}")
    
    print("\n[SUCCESS] ALL V2 SCHEMA CHECKS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    test_v2_schema()
