from fastapi import APIRouter, HTTPException
from app.schemas import LoginRequest, LoginResponse

router = APIRouter()

DEMO_USERS = {
    "admin": {
        "name": "Dr. Ramesh Sharma",
        "role": "Chief Herd Veterinarian",
        "farm": "Amul Dairy Research Station",
        "password": "password"
    },
    "manager": {
        "name": "Suresh Patel",
        "role": "Farm Operations Manager",
        "farm": "Kaira District Dairy Coop",
        "password": "password"
    }
}

@router.post("/login", response_model=LoginResponse)
@router.post("/auth/login", response_model=LoginResponse)
def login(payload: LoginRequest):
    user_key = payload.username.strip().lower()
    
    if user_key in DEMO_USERS and (payload.password == DEMO_USERS[user_key]["password"] or payload.password == "password"):
        user_info = DEMO_USERS[user_key]
        return {
            "success": True,
            "token": f"token_{user_key}_sih2026",
            "user": {
                "username": user_key,
                "name": user_info["name"],
                "role": user_info["role"],
                "farm": user_info["farm"]
            }
        }
    
    if len(payload.username.strip()) > 0:
        return {
            "success": True,
            "token": f"token_{user_key}_custom",
            "user": {
                "username": payload.username,
                "name": payload.username.title(),
                "role": "Dairy Herd Inspector",
                "farm": "Indian Dairy Research Station"
            }
        }

    raise HTTPException(status_code=401, detail="Invalid username or password.")
