from fastapi import APIRouter
from app.services.data_service import get_dashboard_summary

router = APIRouter()

@router.get("/dashboard")
def get_dashboard():
    return get_dashboard_summary()
