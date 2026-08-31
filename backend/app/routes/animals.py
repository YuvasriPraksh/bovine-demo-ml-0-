from typing import Optional
from fastapi import APIRouter, HTTPException, Query
from app.schemas import AnimalRegistrationRequest, AnimalRegistrationResponse
from app.services.data_service import get_animals_list, get_animal_detail, register_animal_record

router = APIRouter()

@router.get("/animals")
def list_animals(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    risk: Optional[str] = None,
    breed: Optional[str] = None,
    sort_by: str = Query("animal_id"),
    sort_order: str = Query("asc")
):
    return get_animals_list(
        page=page,
        page_size=page_size,
        search=search,
        risk_filter=risk,
        breed_filter=breed,
        sort_by=sort_by,
        sort_order=sort_order
    )

@router.post("/animals/register", response_model=AnimalRegistrationResponse)
def register_animal(payload: AnimalRegistrationRequest):
    try:
        result = register_animal_record(payload.model_dump())
        return result
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")

@router.get("/animals/{animal_id}")
def get_animal(animal_id: int):
    data = get_animal_detail(animal_id)
    if not data:
        raise HTTPException(status_code=404, detail=f"Animal with ID {animal_id} not found.")
    return data
