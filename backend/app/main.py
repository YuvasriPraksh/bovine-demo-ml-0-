from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.services.data_service import load_dataset
from app.ml.predict import get_model_and_pipeline

from app.routes.health import router as health_router
from app.routes.auth import router as auth_router
from app.routes.dashboard import router as dashboard_router
from app.routes.animals import router as animals_router
from app.routes.predictions import router as predictions_router
from app.routes.sensor_data import router as sensor_router
from app.routes.model_info import router as model_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Initializing Bovine Mastitis AI Backend...")
    try:
        load_dataset()
        get_model_and_pipeline()
        print("Dataset and ML model preloaded successfully.")
    except Exception as e:
        print(f"Startup warning: {e}")
    yield
    print("Shutting down backend...")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router, prefix="/api", tags=["Health"])
app.include_router(auth_router, prefix="/api", tags=["Authentication"])
app.include_router(dashboard_router, prefix="/api", tags=["Dashboard"])
app.include_router(animals_router, prefix="/api", tags=["Animals"])
app.include_router(predictions_router, prefix="/api", tags=["Predictions & ML"])
app.include_router(sensor_router, prefix="/api", tags=["Sensor Data"])
app.include_router(model_router, prefix="/api", tags=["Model Performance"])

@app.get("/")
def root():
    return {
        "message": "AI-Based Predictive Modelling for Early Forecasting of Bovine Mastitis API is active.",
        "documentation": "/docs",
        "health_check": "/api/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=True)
