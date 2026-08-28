import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler

# Define features
CATEGORICAL_FEATURES = ['Breed']
NUMERIC_FEATURES = [
    'Age_Years', 'Lactation_Number', 'Parity', 'Days_In_Milk',
    'Previous_Mastitis_History', 'Vaccination_Status',
    'Body_Temperature_C', 'Udder_Temperature_C', 'Activity_Index',
    'Rumination_Time_min', 'Feed_Intake_kgDM', 'Water_Intake_L',
    'Milk_Yield', 'Milk_Temperature', 'Milk_Fat_pct', 'Milk_Protein_pct',
    'Milk_Lactose_pct', 'Milk_Solids_pct',
    'Ambient_Temperature_C', 'Humidity_pct', 'THI', 'Hygiene_Score',
    'Bedding_Cleanliness_Score', 'Milking_Frequency'
]

def load_and_filter_data(filepath):
    df = pd.read_csv(filepath)
    # Filter only 800 index observations
    df_filtered = df[(df['Data_Source'] == 'Original') | (df['Record_Type'] == 'Index_Observation')].copy()
    
    # Assert we have exactly 800 rows
    assert len(df_filtered) == 800, f"Expected 800 rows, got {len(df_filtered)}"
    
    # Drop rows where target is missing, though we know it's not for these 800
    df_filtered = df_filtered.dropna(subset=['class1'])
    
    X = df_filtered[CATEGORICAL_FEATURES + NUMERIC_FEATURES]
    y = df_filtered['class1'].astype(int)
    
    return X, y

def get_preprocessor():
    # Numeric pipeline: Impute with median, then scale
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])
    
    # Categorical pipeline: Impute with most frequent, then one-hot encode
    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])
    
    # Combine using ColumnTransformer
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, NUMERIC_FEATURES),
            ('cat', categorical_transformer, CATEGORICAL_FEATURES)
        ])
    
    return preprocessor
