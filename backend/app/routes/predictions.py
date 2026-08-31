import logging
from datetime import datetime
from fastapi import APIRouter, HTTPException, status
from app.schemas import PredictionInput, PredictionResponse
from app.ml.predict import predict_single_animal
from app.services.data_service import get_animal_detail

logger = logging.getLogger("bovineguard.predictions")
router = APIRouter()

@router.post("/predict", response_model=PredictionResponse, status_code=status.HTTP_200_OK)
def predict_mastitis_risk(payload: PredictionInput):
    """
    Accepts animal parameters and IoT telemetry measurements, applies XGBoost model inference,
    and returns mastitis risk score, category, and feature contribution report.
    """
    try:
        data_dict = payload.model_dump()
        result = predict_single_animal(data_dict)
        if "timestamp" not in result or not result["timestamp"]:
            result["timestamp"] = datetime.now().isoformat()
        return result
    except ValueError as ve:
        logger.warning(f"Validation error during prediction: {ve}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Validation Error: {str(ve)}")
    except Exception as e:
        logger.error(f"Unexpected error during prediction: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Prediction Engine Error: {str(e)}")

@router.get("/predictions/{animal_id}")
def get_animal_prediction(animal_id: int):
    """
    Retrieves mastitis prediction record for a specific animal ID.
    """
    try:
        detail = get_animal_detail(animal_id)
        if not detail:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Animal #{animal_id} not found.")
        return detail["prediction"]
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving prediction for animal {animal_id}: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
