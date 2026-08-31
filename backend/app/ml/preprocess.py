import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

NUMERICAL_FEATURES = [
    'age_years',
    'lactation_number',
    'days_in_milk',
    'previous_mastitis_history',
    'vaccinated',
    'chronic_disease_flag',
    'ambient_temperature_c',
    'relative_humidity_pct',
    'hygiene_score_0_100',
    'environment_total_mastitis_pathogen_load_log10',
    'S_aureus_load_log10_cfu_equiv',
    'S_uberis_load_log10_cfu_equiv',
    'E_coli_load_log10_cfu_equiv',
    'K_pneumoniae_load_log10_cfu_equiv',
    'S_agalactiae_load_log10_cfu_equiv',
    'milk_yield_kg_day',
    'milk_conductivity_mS_cm',
    'body_temperature_c',
    'udder_surface_temperature_c'
]

CATEGORICAL_FEATURES = [
    'breed',
    'dominant_environment_pathogen'
]

ALL_MODEL_FEATURES = NUMERICAL_FEATURES + CATEGORICAL_FEATURES

TARGET_COLUMN = 'mastitis_risk_category'

LABEL_MAP = {
    'No_Risk': 0,
    'Low': 1,
    'Moderate': 2,
    'High': 3
}

INV_LABEL_MAP = {v: k for k, v in LABEL_MAP.items()}

def create_preprocessor():
    numeric_transformer = StandardScaler()
    categorical_transformer = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, NUMERICAL_FEATURES),
            ('cat', categorical_transformer, CATEGORICAL_FEATURES)
        ],
        remainder='drop'
    )
    return preprocessor
