from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

@router.get("/health")
def health_check():
    return {
        "status": "online",
        "service": "Bovine Mastitis AI Early Forecasting Service",
        "timestamp": datetime.now().isoformat(),
        "model_status": "loaded",
        "data_source": "data/mastitis_dataset.xlsx (In-Memory Pandas Engine)"
    }
