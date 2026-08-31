import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler

# Comprehensive feature definitions incorporating all factors
CATEGORICAL_FEATURES = ['breed', 'dominant_environment_pathogen']
NUMERIC_FEATURES = [
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
    'milk_yield_kg_day',
    'milk_conductivity_mS_cm',
    'body_temperature_c',
    'udder_surface_temperature_c',
    'activity_score',
    'rumination_min_day',
    'feed_intake_kg_day',
    'water_intake_l_day',
    'hygiene_score_0_100'
]

# Legacy and V2 alias mapping
COLUMN_ALIAS_MAP = {
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
    'Hygiene_Score': 'hygiene_score_0_100',
    'class1': 'clinical_mastitis_now'
}

DEFAULT_FACTOR_VALUES = {
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

def load_and_filter_data(filepath):
    df = pd.read_csv(filepath)
    df_filtered = df.copy()
    
    # Map legacy column names to unified factor names
    for col, unified_col in COLUMN_ALIAS_MAP.items():
        if col in df_filtered.columns and unified_col not in df_filtered.columns:
            df_filtered[unified_col] = df_filtered[col]
            
    # Ensure target column exists
    if 'clinical_mastitis_now' not in df_filtered.columns:
        if 'class1' in df_filtered.columns:
            df_filtered['clinical_mastitis_now'] = df_filtered['class1']
        elif 'mastitis_in_next_7d' in df_filtered.columns:
            df_filtered['clinical_mastitis_now'] = df_filtered['mastitis_in_next_7d']
            
    # Fill defaults for any missing factors
    for feat, default_val in DEFAULT_FACTOR_VALUES.items():
        if feat not in df_filtered.columns:
            df_filtered[feat] = default_val
            
    df_filtered = df_filtered.dropna(subset=['clinical_mastitis_now'])
    
    X = df_filtered[CATEGORICAL_FEATURES + NUMERIC_FEATURES]
    y = df_filtered['clinical_mastitis_now'].astype(int)
    
    return X, y

def get_preprocessor():
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])
    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])
    return ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, NUMERIC_FEATURES),
            ('cat', categorical_transformer, CATEGORICAL_FEATURES)
        ]
    )


