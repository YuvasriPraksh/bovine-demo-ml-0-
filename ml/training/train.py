import os
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split, StratifiedKFold, cross_validate
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, roc_curve
)

from preprocessing import load_and_filter_data, get_preprocessor

def train_and_evaluate(data_path=None):
    if data_path is None:
        if os.path.exists('data/processed/mastitis_dataset_v2.csv'):
            data_path = 'data/processed/mastitis_dataset_v2.csv'
        else:
            data_path = 'data/processed/mastitis_full_longitudinal_dataset.csv'
    X, y = load_and_filter_data(data_path)
    
    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Define models
    scale_pos_weight = (len(y_train) - sum(y_train)) / sum(y_train)
    
    models = {
        'LogisticRegression': LogisticRegression(
            max_iter=2000, class_weight='balanced', random_state=42
        ),
        'RandomForest': RandomForestClassifier(
            n_estimators=300, class_weight='balanced', random_state=42
        ),
        'XGBoost': XGBClassifier(
            n_estimators=100, scale_pos_weight=scale_pos_weight, random_state=42,
            eval_metric='logloss', use_label_encoder=False
        )
    }
    
    preprocessor = get_preprocessor()
    
    results = []
    best_model_name = None
    best_recall = -1
    best_pipeline = None
    
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    
    # Dictionary to store ROC curve data
    roc_data = {}
    
    with open('outputs/reports/model_evaluation.txt', 'w') as f:
        f.write("=== Model Evaluation Report ===\n\n")
        f.write("Dataset Information:\n")
        f.write(f"Total labeled observations: {len(X)}\n")
        f.write(f"Class distribution: 0={len(y)-sum(y)}, 1={sum(y)}\n\n")
        
        for name, model in models.items():
            print(f"Training {name}...")
            pipeline = Pipeline(steps=[
                ('preprocessor', preprocessor),
                ('classifier', model)
            ])
            
            # Cross-validation
            cv_results = cross_validate(
                pipeline, X_train, y_train, cv=cv,
                scoring=['accuracy', 'precision', 'recall', 'f1', 'roc_auc']
            )
            
            # Train on full train set
            pipeline.fit(X_train, y_train)
            
            # Predict on test set
            y_pred = pipeline.predict(X_test)
            y_prob = pipeline.predict_proba(X_test)[:, 1]
            
            # Metrics
            acc = accuracy_score(y_test, y_pred)
            prec = precision_score(y_test, y_pred, zero_division=0)
            rec = recall_score(y_test, y_pred, zero_division=0)
            f1 = f1_score(y_test, y_pred, zero_division=0)
            roc_auc = roc_auc_score(y_test, y_prob)
            
            # Store results
            results.append({
                'Model': name,
                'Test_Accuracy': acc,
                'Test_Precision': prec,
                'Test_Recall': rec,
                'Test_F1': f1,
                'Test_ROC_AUC': roc_auc,
                'CV_Recall_Mean': cv_results['test_recall'].mean()
            })
            
            # Tracking ROC
            fpr, tpr, _ = roc_curve(y_test, y_prob)
            roc_data[name] = (fpr, tpr, roc_auc)
            
            # Confusion matrix
            cm = confusion_matrix(y_test, y_pred)
            
            # Plot Confusion Matrix
            plt.figure(figsize=(5,4))
            sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
            plt.title(f'Confusion Matrix: {name}')
            plt.ylabel('True Label')
            plt.xlabel('Predicted Label')
            plt.tight_layout()
            plt.savefig(f'outputs/figures/confusion_matrix_{name}.png')
            plt.close()
            
            f.write(f"--- {name} ---\n")
            f.write(f"Test Accuracy:  {acc:.4f}\n")
            f.write(f"Test Precision: {prec:.4f}\n")
            f.write(f"Test Recall:    {rec:.4f}  <-- FOCUS METRIC\n")
            f.write(f"Test F1-score:  {f1:.4f}\n")
            f.write(f"Test ROC-AUC:   {roc_auc:.4f}\n")
            f.write(f"Confusion Matrix:\n{cm}\n\n")
            
            # Selection criteria: Primary is Recall for class 1
            if rec > best_recall:
                best_recall = rec
                best_model_name = name
                best_pipeline = pipeline
                
    # Model Comparison Table
    results_df = pd.DataFrame(results)
    results_df.to_csv('outputs/reports/model_comparison.csv', index=False)
    
    # ROC Curve Plot
    plt.figure(figsize=(8,6))
    for name, (fpr, tpr, auc_val) in roc_data.items():
        plt.plot(fpr, tpr, label=f"{name} (AUC = {auc_val:.3f})")
    plt.plot([0, 1], [0, 1], 'k--')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC Curves - Mastitis Risk Prototype')
    plt.legend()
    plt.tight_layout()
    plt.savefig('outputs/figures/roc_curves.png')
    plt.close()
    
    # Feature Importance for Best Model (if tree-based or Logistic Regression)
    model_step = best_pipeline.named_steps['classifier']
    preprocessor_step = best_pipeline.named_steps['preprocessor']
    
    cat_features = preprocessor_step.named_transformers_['cat'].named_steps['onehot'].get_feature_names_out(['Breed'])
    num_features = preprocessor_step.transformers_[0][2] # NUMERIC_FEATURES
    feature_names = np.concatenate([num_features, cat_features])
    
    importances = None
    if hasattr(model_step, 'feature_importances_'):
        importances = model_step.feature_importances_
    elif hasattr(model_step, 'coef_'):
        importances = np.abs(model_step.coef_[0])
        
    if importances is not None:
        indices = np.argsort(importances)[::-1]
        
        plt.figure(figsize=(10, 8))
        plt.title(f"Feature Importances ({best_model_name})")
        plt.bar(range(min(20, len(importances))), importances[indices][:20], align="center")
        plt.xticks(range(min(20, len(importances))), [feature_names[i] for i in indices][:20], rotation=90)
        plt.xlim([-1, min(20, len(importances))])
        plt.tight_layout()
        plt.savefig(f'outputs/figures/feature_importance_{best_model_name}.png')
        plt.close()
        
        with open('outputs/reports/model_evaluation.txt', 'a') as f:
            f.write(f"\nTop 10 Important Features for best model ({best_model_name}):\n")
            for i in range(min(10, len(importances))):
                f.write(f"{i+1}. {feature_names[indices[i]]} ({importances[indices[i]]:.4f})\n")
    
    # Save the best model
    joblib.dump(best_pipeline, f'models/best_model_{best_model_name}.pkl')
    print(f"Best model saved: {best_model_name} with recall {best_recall:.4f}")

if __name__ == "__main__":
    train_and_evaluate()
