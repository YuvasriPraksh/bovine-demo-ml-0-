from typing import Optional, List, Dict, Any, Union
from pydantic import BaseModel, Field

class LoginRequest(BaseModel):
    username: str = Field(..., description="Username")
    password: str = Field(..., description="Password")

class LoginResponse(BaseModel):
    success: bool
    token: str
    user: Dict[str, Any]

class AnimalRegistrationRequest(BaseModel):
    animal_id: int = Field(..., description="Unique numerical Animal ID (e.g. 12001)")
    breed: str = Field(default="Jersey_cross", description="Breed of the animal")
    age_years: float = Field(default=4.0, ge=0.5, le=20.0, description="Age in years")
    lactation_number: int = Field(default=2, ge=1, le=15, description="Lactation number")
    previous_mastitis_history: bool = Field(default=False, description="Has the animal had mastitis before? (True/False)")
    abnormal_behavior: bool = Field(default=False, description="Is the animal currently showing abnormal behavior? (True/False)")

class RiskFactor(BaseModel):
    factor: str
    feature_name: str
    observed_value: float
    impact_score: float
    details: str

class EnvironmentalRisk(BaseModel):
    ambient_temperature_c: float
    relative_humidity_pct: float
    calculated_thi: float
    conditions_favorable_for_pathogens: bool
    interpretation: str

class PredictionResponse(BaseModel):
    animal_id: str
    risk_score: float = Field(description="Risk percentage from 0 to 100%")
    risk_category: str = Field(description="No_Risk, Low, Moderate, or High")
    class_probabilities: Dict[str, float]
    top_risk_factors: List[RiskFactor]
    forecast_7d_risk_pct: float
    forecast_14d_risk_pct: float
    environmental_risk: EnvironmentalRisk
    recommendations: List[str]
    prediction: Optional[int] = Field(default=None, description="Binary classification (0=Healthy, 1=Mastitis)")
    mastitis_probability: Optional[float] = Field(default=None, description="Probability of mastitis (0-1)")
    healthy_probability: Optional[float] = Field(default=None, description="Probability of healthy status (0-1)")
    risk_level: Optional[str] = Field(default=None, description="Risk level (LOW, MEDIUM, HIGH)")
    risk_label: Optional[str] = Field(default=None, description="Human readable label")
    contributing_factors: Optional[List[Dict[str, Any]]] = Field(default=None, description="Model feature contributions")
    timestamp: Optional[str] = Field(default=None, description="ISO timestamp of prediction execution")

class PredictionInput(BaseModel):
    animal_id: Optional[Any] = Field(default="COW_SIM_001", description="Animal identifier")
    breed: Optional[str] = Field(default="Jersey_cross", description="Breed of the cow")
    age_years: Optional[float] = Field(default=4.5, description="Age of animal in years")
    lactation_number: Optional[int] = Field(default=3, description="Lactation parity")
    days_in_milk: Optional[int] = Field(default=75, description="Days in milk")
    previous_mastitis_history: Optional[int] = Field(default=0, description="1 if previous mastitis, 0 otherwise")
    vaccinated: Optional[int] = Field(default=1, description="1 if vaccinated, 0 otherwise")
    chronic_disease_flag: Optional[int] = Field(default=0, description="1 if chronic disease, 0 otherwise")
    ambient_temperature_c: Optional[float] = Field(default=28.5, description="Ambient barn temperature in C")
    relative_humidity_pct: Optional[float] = Field(default=72.0, description="Relative humidity in %")
    hygiene_score_0_100: Optional[float] = Field(default=60.0, description="Barn/teat hygiene score (0-100)")
    environment_total_mastitis_pathogen_load_log10: Optional[float] = Field(default=4.6, description="Log10 pathogen load proxy")
    S_aureus_load_log10_cfu_equiv: Optional[float] = Field(default=4.1, description="S. aureus proxy load")
    S_uberis_load_log10_cfu_equiv: Optional[float] = Field(default=4.2, description="S. uberis proxy load")
    E_coli_load_log10_cfu_equiv: Optional[float] = Field(default=3.9, description="E. coli proxy load")
    K_pneumoniae_load_log10_cfu_equiv: Optional[float] = Field(default=3.7, description="K. pneumoniae proxy load")
    S_agalactiae_load_log10_cfu_equiv: Optional[float] = Field(default=3.4, description="S. agalactiae proxy load")
    dominant_environment_pathogen: Optional[str] = Field(default="S_uberis", description="Dominant environmental pathogen")
    milk_yield_kg_day: Optional[float] = Field(default=14.5, description="Daily milk yield in kg")
    milk_conductivity_mS_cm: Optional[float] = Field(default=4.2, description="Milk electrical conductivity in mS/cm")
    body_temperature_c: Optional[float] = Field(default=38.6, description="Core body temperature in C")
    udder_surface_temperature_c: Optional[float] = Field(default=33.9, description="Udder surface temperature in C")
    activity_score: Optional[float] = Field(default=65.0, description="Activity index")
    rumination_min_day: Optional[float] = Field(default=480.0, description="Daily rumination time in min")
    feed_intake_kg_day: Optional[float] = Field(default=18.0, description="Daily feed intake in kg DM")
    water_intake_l_day: Optional[float] = Field(default=85.0, description="Daily water intake in L")

class AnimalSummary(BaseModel):
    animal_id: int
    farm_id: str
    record_date: str
    breed: str
    age_years: float
    lactation_number: int
    days_in_milk: int
    milk_yield_kg_day: float
    milk_conductivity_mS_cm: float
    body_temperature_c: float
    udder_surface_temperature_c: float
    mastitis_risk_category: str
    synthetic_risk_score_pct: float
    clinical_mastitis_now: int
    mastitis_in_next_7d: int
    mastitis_in_next_14d: int

class AnimalListResponse(BaseModel):
    total_count: int
    page: int
    page_size: int
    total_pages: int
    animals: List[AnimalSummary]

class AnimalDetailResponse(BaseModel):
    animal: Dict[str, Any]
    prediction: PredictionResponse
    historical_summary: Dict[str, Any]

class AnimalRegistrationResponse(BaseModel):
    success: bool
    message: str
    animal: AnimalSummary
    initial_prediction: PredictionResponse

class AlertItem(BaseModel):
    animal_id: int
    farm_id: str
    record_date: str
    breed: str
    risk_score: float
    risk_category: str
    body_temperature_c: float
    milk_conductivity_mS_cm: float
    udder_surface_temperature_c: float
    top_factors: List[str]
    alert_level: str
    recommendation: str

class DashboardSummaryResponse(BaseModel):
    total_animals: int
    no_risk_count: int
    low_risk_count: int
    moderate_risk_count: int
    high_risk_count: int
    risk_distribution_pct: Dict[str, float]
    herd_averages: Dict[str, float]
    environmental_status: Dict[str, Any]
    recent_high_risk_alerts: List[AlertItem]
    recent_predictions: List[AnimalSummary]
