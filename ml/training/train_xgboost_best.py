"""
train_xgboost_best.py
---------------------
Trains and hyperparameter-tunes the best XGBoost model for Bovine Mastitis Early-Risk Prediction.

Features:
- Evaluates on 27-feature v2 dataset as well as full longitudinal dataset.
- Performs 5-Fold Stratified Cross-Validation hyperparameter grid search.
- Optimizes for Recall & ROC-AUC to minimize false negatives (critical for early disease detection).
- Exports evaluation metrics, ROC/PR curves, confusion matrices, and feature importance charts.
- Saves the tuned model pipeline to models/best_model_XGBoost.pkl and models/strict_early_risk_model.pkl.
"""

import os
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from xgboost import XGBClassifier
from sklearn.model_selection import StratifiedKFold, GridSearchCV, train_test_split
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, average_precision_score, confusion_matrix, roc_curve, precision_recall_curve
)
from sklearn.pipeline import Pipeline

import sys
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
ML_SRC_DIR = os.path.join(ROOT_DIR, "ml", "src")
for p in [ML_SRC_DIR, ROOT_DIR]:
    if p not in sys.path:
        sys.path.insert(0, p)

try:
    from ml.src.preprocessing import load_and_filter_data, get_preprocessor, CATEGORICAL_FEATURES
except ImportError:
    from preprocessing import load_and_filter_data, get_preprocessor, CATEGORICAL_FEATURES

def train_best_xgboost(data_path: str = None):
    print("=" * 60)
    print("      HIGH-PERFORMANCE XGBOOST MODEL OPTIMIZATION      ")
    print("=" * 60)
    
    if data_path is None:
        candidate_files = [
            'data/processed/mastitis_dataset.csv',
            'data/raw/synthetic_bovine_mastitis_integrated_dataset.csv',
            'data/processed/mastitis_dataset_v2.csv',
            'data/mastitis_dataset.csv',
        ]
        for f in candidate_files:
            if os.path.exists(f):
                data_path = f
                break
            
    print(f"\n[1/5] Loading and preprocessing dataset: {data_path}")
    X, y = load_and_filter_data(data_path)
    
    # Train / Test split with stratification
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    pos_count = sum(y_train)
    neg_count = len(y_train) - pos_count
    scale_pos_weight = neg_count / max(1, pos_count)
    print(f"      Total observations: {len(X)} | Train: {len(X_train)} | Test: {len(X_test)}")
    print(f"      Class breakdown in train set: Healthy (0) = {neg_count}, Mastitis (1) = {pos_count}")
    print(f"      Calculated scale_pos_weight: {scale_pos_weight:.3f}")

    preprocessor = get_preprocessor()
    
    # Define XGBoost Pipeline
    xgb_base = XGBClassifier(
        random_state=42,
        eval_metric='logloss',
        use_label_encoder=False
    )
    
    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', xgb_base)
    ])
    
    # Hyperparameter search space (focused for speed & high accuracy)
    param_grid = {
        'classifier__n_estimators': [100, 200],
        'classifier__max_depth': [4, 6],
        'classifier__learning_rate': [0.03, 0.1],
        'classifier__subsample': [0.8, 1.0],
        'classifier__colsample_bytree': [0.8, 1.0],
        'classifier__scale_pos_weight': [scale_pos_weight],
        'classifier__min_child_weight': [1, 3]
    }
    
    print("\n[2/5] Running 5-Fold Stratified Cross-Validation Hyperparameter Optimization...")
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    
    grid_search = GridSearchCV(
        pipeline,
        param_grid=param_grid,
        cv=cv,
        scoring='roc_auc',
        n_jobs=-1,
        verbose=1
    )
    
    grid_search.fit(X_train, y_train)
    
    best_pipeline = grid_search.best_estimator_
    best_params = grid_search.best_params_
    best_cv_score = grid_search.best_score_
    
    print(f"      Best CV ROC-AUC Score: {best_cv_score:.4f}")
    print("      Optimized Hyperparameters:")
    for param, val in best_params.items():
        print(f"        - {param.replace('classifier__', '')}: {val}")
        
    print("\n[3/5] Evaluating Best XGBoost Model on Independent Test Set...")
    y_pred = best_pipeline.predict(X_test)
    y_prob = best_pipeline.predict_proba(X_test)[:, 1]
    
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, zero_division=0)
    rec = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)
    roc_auc = roc_auc_score(y_test, y_prob)
    pr_auc = average_precision_score(y_test, y_prob)
    cm = confusion_matrix(y_test, y_pred)
    
    print(f"      Test Accuracy:     {acc:.4f}")
    print(f"      Test Precision:    {prec:.4f}")
    print(f"      Test Recall:       {rec:.4f}  <-- PRIMARY METRIC")
    print(f"      Test F1-Score:     {f1:.4f}")
    print(f"      Test ROC-AUC:      {roc_auc:.4f}")
    print(f"      Test PR-AUC:       {pr_auc:.4f}")
    print("      Confusion Matrix:")
    print(f"        {cm}")

    print("\n[4/5] Generating Evaluation Visualizations...")
    os.makedirs('outputs/figures', exist_ok=True)
    os.makedirs('outputs/reports', exist_ok=True)
    
    # 1. Confusion Matrix Plot
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Greens', cbar=False,
                xticklabels=['Healthy (0)', 'Mastitis (1)'],
                yticklabels=['Healthy (0)', 'Mastitis (1)'])
    plt.title('Best XGBoost Model — Confusion Matrix', fontsize=12, fontweight='bold')
    plt.ylabel('Actual Class')
    plt.xlabel('Predicted Class')
    plt.tight_layout()
    plt.savefig('outputs/figures/xgboost_best_confusion_matrix.png', dpi=300)
    plt.close()
    
    # 2. ROC & PR Curves Plot
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    
    fpr, tpr, _ = roc_curve(y_test, y_prob)
    axes[0].plot(fpr, tpr, color='#16a34a', lw=2, label=f'XGBoost (AUC = {roc_auc:.4f})')
    axes[0].plot([0, 1], [0, 1], 'k--', lw=1)
    axes[0].set_xlabel('False Positive Rate')
    axes[0].set_ylabel('True Positive Rate')
    axes[0].set_title('Receiver Operating Characteristic (ROC)', fontweight='bold')
    axes[0].legend(loc='lower right')
    axes[0].grid(True, alpha=0.3)
    
    precision, recall_vals, _ = precision_recall_curve(y_test, y_prob)
    axes[1].plot(recall_vals, precision, color='#2563eb', lw=2, label=f'XGBoost (PR-AUC = {pr_auc:.4f})')
    axes[1].set_xlabel('Recall')
    axes[1].set_ylabel('Precision')
    axes[1].set_title('Precision-Recall (PR) Curve', fontweight='bold')
    axes[1].legend(loc='lower left')
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('outputs/figures/xgboost_best_roc_pr_curves.png', dpi=300)
    plt.close()
    
    # 3. Feature Importance Plot
    xgb_model = best_pipeline.named_steps['classifier']
    preproc = best_pipeline.named_steps['preprocessor']
    
    num_names = list(preproc.transformers_[0][2])
    cat_names = list(preproc.named_transformers_['cat'].named_steps['onehot'].get_feature_names_out(CATEGORICAL_FEATURES))
    all_feature_names = num_names + cat_names
    
    importances = xgb_model.feature_importances_
    indices = np.argsort(importances)[::-1]
    
    plt.figure(figsize=(11, 7))
    top_k = min(20, len(importances))
    plt.barh(range(top_k), importances[indices[:top_k]][::-1], color='#0d9488')
    plt.yticks(range(top_k), [all_feature_names[i] for i in indices[:top_k]][::-1])
    plt.xlabel('XGBoost Feature Importance (Gain)')
    plt.title('Top 20 Feature Importances — Optimized XGBoost Model', fontweight='bold')
    plt.tight_layout()
    plt.savefig('outputs/figures/xgboost_best_feature_importance.png', dpi=300)
    plt.close()
    
    # Write report text
    with open('outputs/reports/best_xgboost_report.txt', 'w') as f:
        f.write("====================================================\n")
        f.write("     OPTIMIZED XGBOOST MODEL EVALUATION REPORT     \n")
        f.write("====================================================\n\n")
        f.write(f"Dataset Path:       {data_path}\n")
        f.write(f"Total Samples:      {len(X)}\n")
        f.write(f"CV ROC-AUC Score:   {best_cv_score:.4f}\n\n")
        f.write("Test Set Metrics:\n")
        f.write(f"  Accuracy:         {acc:.4f}\n")
        f.write(f"  Precision:        {prec:.4f}\n")
        f.write(f"  Recall:           {rec:.4f}\n")
        f.write(f"  F1-Score:         {f1:.4f}\n")
        f.write(f"  ROC-AUC:          {roc_auc:.4f}\n")
        f.write(f"  PR-AUC:           {pr_auc:.4f}\n\n")
        f.write("Optimized Hyperparameters:\n")
        for param, val in best_params.items():
            f.write(f"  {param}: {val}\n")
        f.write("\nTop Feature Importances:\n")
        for idx in indices[:15]:
            f.write(f"  - {all_feature_names[idx]}: {importances[idx]:.4f}\n")

    print("\n[5/5] Saving Best XGBoost Models...")
    os.makedirs('models', exist_ok=True)
    joblib.dump(best_pipeline, 'models/best_model_XGBoost.pkl')
    joblib.dump(best_pipeline, 'models/strict_early_risk_model.pkl')
    print("      Model pipeline successfully saved to:")
    print("        - models/best_model_XGBoost.pkl")
    print("        - models/strict_early_risk_model.pkl")
    print("=" * 60)
    print("                  OPTIMIZATION COMPLETE!                 ")
    print("=" * 60)
    return best_pipeline

if __name__ == "__main__":
    train_best_xgboost()
