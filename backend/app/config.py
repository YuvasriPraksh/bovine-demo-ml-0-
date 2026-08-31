import os

class Settings:
    PROJECT_NAME: str = "BovineGuard AI - Bovine Mastitis Predictive Modelling"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "AI-Based Early Forecasting of Bovine Mastitis in Indian Dairy Farms"
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    DATA_FILE_PATH: str = os.getenv(
        "DATA_FILE_PATH",
        os.path.join(os.path.dirname(__file__), "../../data/mastitis_dataset.xlsx")
    )
    
    CORS_ORIGINS: list = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "*"
    ]

settings = Settings()
