import unittest
import sys
import os

# Add workspace root and backend to sys.path
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
BACKEND_DIR = os.path.join(ROOT_DIR, "backend")
for path in [ROOT_DIR, BACKEND_DIR]:
    if path not in sys.path:
        sys.path.insert(0, path)

from backend.app.ml.predict import predict_single_animal, get_model_and_pipeline
from backend.app.schemas import PredictionInput, PredictionResponse

class TestBovineMastitisIntegration(unittest.TestCase):
    def test_model_preloading(self):
        """Test that the trained XGBoost model and pipeline load successfully."""
        model, pipeline = get_model_and_pipeline()
        self.assertIsNotNone(pipeline, "ML pipeline should be loaded.")
        self.assertTrue(os.path.exists(os.path.join(ROOT_DIR, "ml", "models", "strict_early_risk_model.pkl")),
                        "Model file strict_early_risk_model.pkl should exist in ml/models/")

    def test_prediction_healthy_case(self):
        """Test prediction for a healthy cow sample input."""
        healthy_input = {
            "animal_id": "COW_HEALTHY_001",
            "breed": "Holstein_Friesian",
            "age_years": 4.0,
            "body_temperature_c": 38.4,
            "udder_surface_temperature_c": 33.5,
            "milk_conductivity_mS_cm": 4.1,
            "milk_yield_kg_day": 24.0,
            "hygiene_score_0_100": 75.0,
            "previous_mastitis_history": 0,
            "vaccinated": 1
        }
        res = predict_single_animal(healthy_input)
        
        self.assertEqual(res["animal_id"], "COW_HEALTHY_001")
        self.assertIn("risk_score", res)
        self.assertIn("risk_category", res)
        self.assertIn("prediction", res)
        self.assertIn("mastitis_probability", res)
        self.assertIn("timestamp", res)
        self.assertLess(res["mastitis_probability"], 0.70, "Healthy cow should have low/moderate risk.")

    def test_prediction_at_risk_case(self):
        """Test prediction for a high-risk mastitis cow sample input."""
        risk_input = {
            "animal_id": "COW_ALERT_999",
            "breed": "Jersey_cross",
            "body_temperature_c": 39.8,
            "udder_surface_temperature_c": 39.4,
            "milk_conductivity_mS_cm": 5.8,
            "milk_yield_kg_day": 8.0,
            "hygiene_score_0_100": 35.0,
            "previous_mastitis_history": 1,
            "ambient_temperature_c": 34.0,
            "relative_humidity_pct": 85.0
        }
        res = predict_single_animal(risk_input)
        
        self.assertEqual(res["animal_id"], "COW_ALERT_999")
        self.assertGreater(res["risk_score"], 30.0, "High-temp, high-conductivity cow should have elevated risk score.")
        self.assertIn(res["risk_category"], ["Moderate", "High"])
        self.assertEqual(res["prediction"], 1, "Binary prediction should flag mastitis risk.")

    def test_pydantic_schema_validation(self):
        """Test Pydantic schema validation for incoming API payload."""
        payload = PredictionInput(
            animal_id="COW_TEST_SCHEMA",
            body_temperature_c=38.6,
            milk_conductivity_mS_cm=4.2
        )
        data_dict = payload.model_dump()
        res = predict_single_animal(data_dict)
        response_schema = PredictionResponse(**res)
        self.assertEqual(response_schema.animal_id, "COW_TEST_SCHEMA")

if __name__ == "__main__":
    unittest.main()
