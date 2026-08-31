from fastapi import APIRouter, HTTPException
from app.services.data_service import get_sensor_data_by_id

router = APIRouter()

@router.get("/sensor-data/{animal_id}")
def get_sensor_data(animal_id: int):
    telemetry = get_sensor_data_by_id(animal_id)
    if not telemetry:
        raise HTTPException(status_code=404, detail=f"Sensor telemetry for animal {animal_id} not found.")
    return telemetry
