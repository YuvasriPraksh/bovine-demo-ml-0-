import os
import json
import joblib
import numpy as np
import pandas as pd
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

from app.ml.preprocess import (
    create_preprocessor,
    ALL_MODEL_FEATURES,
    NUMERICAL_FEATURES,
    CATEGORICAL_FEATURES,
    TARGET_COLUMN,
    LABEL_MAP,
    INV_LABEL_MAP
)

def train_model(data_path=None, model_dir=None):
    if data_path is None:
        # Try both possible locations
        possible_paths = [
            os.path.join(os.path.dirname(__file__), '../../../data/mastitis_dataset.xlsx'),
            os.path.join(os.path.dirname(__file__), '../../../data/mastitis_dataset.csv'),
            'data/mastitis_dataset.xlsx',
            'data/mastitis_dataset.csv'
        ]
        for p in possible_paths:
            if os.path.exists(p):
                data_path = p
                break

    if not data_path or not os.path.exists(data_path):
        raise FileNotFoundError(f'Dataset not found at {data_path}')

    if model_dir is None:
        model_dir = os.path.join(os.path.dirname(__file__), 'model')
    os.makedirs(model_dir, exist_ok=True)

    print(f'Loading dataset from {data_path}...')
    if data_path.endswith('.xlsx'):
        df = pd.read_excel(data_path)
    else:
        df = pd.read_csv(data_path)

    print(f'Dataset shape: {df.shape}')
    
    # Check features and target
    missing_cols = [col for col in ALL_MODEL_FEATURES if col not in df.columns]
    if missing_cols:
        raise ValueError(f'Missing required feature columns: {missing_cols}')
    if TARGET_COLUMN not in df.columns:
        raise ValueError(f'Missing target column: {TARGET_COLUMN}')

    X = df[ALL_MODEL_FEATURES].copy()
    y = df[TARGET_COLUMN].map(LABEL_MAP).copy()

    # Train / Test split (80/20 stratified)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )

    print(f'Training samples: {len(X_train)}, Testing samples: {len(X_test)}')

    # Build and fit preprocessing pipeline
    preprocessor = create_preprocessor()
    X_train_transformed = preprocessor.fit_transform(X_train)
    X_test_transformed = preprocessor.transform(X_test)

    # Get feature names after one-hot encoding
    cat_encoder = preprocessor.named_transformers_['cat']
    cat_feature_names = cat_encoder.get_feature_names_out(CATEGORICAL_FEATURES).tolist()
    transformed_feature_names = NUMERICAL_FEATURES + cat_feature_names

    # Train XGBoost Classifier
    print('Training XGBoost Multi-class Classifier...')
    model = XGBClassifier(
        n_estimators=150,
        max_depth=6,
        learning_rate=0.08,
        subsample=0.85,
        colsample_bytree=0.85,
        objective='multi:softprob',
        num_class=4,
        random_state=42,
        eval_metric='mlogloss'
    )
    model.fit(X_train_transformed, y_train)

    # Evaluate model
    y_pred = model.predict(X_test_transformed)
    y_pred_proba = model.predict_proba(X_test_transformed)

    acc = float(accuracy_score(y_test, y_pred))
    prec = float(precision_score(y_test, y_pred, average='weighted'))
    rec = float(recall_score(y_test, y_pred, average='weighted'))
    f1 = float(f1_score(y_test, y_pred, average='weighted'))
    cm = confusion_matrix(y_test, y_pred).tolist()

    class_names = [INV_LABEL_MAP[i] for i in range(4)]
    report = classification_report(y_test, y_pred, target_names=class_names, output_dict=True)

    print(f'Model Accuracy: {acc * 100:.2f}%')
    print(f'Model Precision: {prec * 100:.2f}%')
    print(f'Model Recall: {rec * 100:.2f}%')
    print(f'Model F1-Score: {f1 * 100:.2f}%')

    # Feature Importance
    importances = model.feature_importances_
    feat_importance = []
    for name, imp in zip(transformed_feature_names, importances):
        feat_importance.append({'feature': name, 'importance': round(float(imp) * 100, 2)})
    feat_importance = sorted(feat_importance, key=lambda x: x['importance'], reverse=True)

    # Save artifacts
    model_path = os.path.join(model_dir, 'mastitis_xgb_model.joblib')
    pipeline_path = os.path.join(model_dir, 'pipeline.joblib')
    metrics_path = os.path.join(model_dir, 'model_metrics.json')
    feat_imp_path = os.path.join(model_dir, 'feature_importance.json')

    joblib.dump(model, model_path)
    joblib.dump(preprocessor, pipeline_path)

    metrics_payload = {
        'model_name': 'XGBoost Multi-Class Bovine Mastitis Risk Classifier',
        'algorithm': 'Extreme Gradient Boosting (XGBoost)',
        'framework': 'xgboost / scikit-learn',
        'training_records': int(len(X_train)),
        'test_records': int(len(X_test)),
        'accuracy': round(acc, 4),
        'precision': round(prec, 4),
        'recall': round(rec, 4),
        'f1_score': round(f1, 4),
        'classes': class_names,
        'confusion_matrix': cm,
        'classification_report': report,
        'transformed_feature_names': transformed_feature_names
    }

    with open(metrics_path, 'w', encoding='utf-8') as f:
        json.dump(metrics_payload, f, indent=2)

    with open(feat_imp_path, 'w', encoding='utf-8') as f:
        json.dump(feat_importance, f, indent=2)

    print(f'Artifacts successfully saved in {model_dir}:')
    print(f' - Model: {model_path}')
    print(f' - Pipeline: {pipeline_path}')
    print(f' - Metrics: {metrics_path}')
    print(f' - Feature Importance: {feat_imp_path}')

    return metrics_payload

if __name__ == '__main__':
    train_model()
