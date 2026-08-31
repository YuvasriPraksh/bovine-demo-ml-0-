import os
import json
from fastapi import APIRouter

router = APIRouter()

@router.get("/model-performance")
def get_model_performance():
    metrics_path = os.path.join(os.path.dirname(__file__), "../ml/model/model_metrics.json")
    feat_path = os.path.join(os.path.dirname(__file__), "../ml/model/feature_importance.json")

    metrics = {}
    feature_importance = []

    if os.path.exists(metrics_path):
        with open(metrics_path, "r", encoding="utf-8") as f:
            metrics = json.load(f)

    if os.path.exists(feat_path):
        with open(feat_path, "r", encoding="utf-8") as f:
            feature_importance = json.load(f)

    return {
        "metrics": metrics,
        "feature_importance": feature_importance
    }
