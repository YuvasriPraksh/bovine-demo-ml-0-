"""
hardware_interface.py
---------------------
Hardware-ready integration interface for Bovine Mastitis Early-Risk Prediction.

Provides a clean entry point `process_sensor_reading(sensor_data)` that:
  1. Accepts JSON string or dictionary representing sensor data + metadata.
  2. Extracts optional metadata (cow_id, timestamp).
  3. Validates and passes physiological/environmental/management features to `predict_mastitis_risk`.
  4. Formats a standardized, JSON-serializable output structure suitable for API/IoT/Dashboard consumption.
"""

import json
import sys
import os

# Ensure src directory is in Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from predict import predict_mastitis_risk, REQUIRED_FEATURES

def process_sensor_reading(sensor_data):
    """
    Processes sensor data payload (dict or JSON string) and computes mastitis risk.

    Args:
        sensor_data (dict or str): Payload containing cow measurements and optional metadata ('cow_id', 'timestamp').

    Returns:
        dict: Standardized, JSON-compatible risk assessment report.
    """
    # 1. Parse JSON if input is string
    if isinstance(sensor_data, str):
        try:
            payload = json.loads(sensor_data)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON string provided: {e}")
    elif isinstance(sensor_data, dict):
        payload = sensor_data.copy()
    else:
        raise TypeError("sensor_data must be a dictionary or a valid JSON string.")

    # 2. Extract metadata
    cow_id = payload.get("cow_id", "COW_UNKNOWN")
    timestamp = payload.get("timestamp", "N/A")

    # 3. Extract model feature subset
    feature_payload = {}
    for feat in REQUIRED_FEATURES.keys():
        if feat in payload:
            feature_payload[feat] = payload[feat]
        else:
            raise ValueError(f"Missing required feature for model prediction: '{feat}'")

    # 4. Invoke ML pipeline via predict_mastitis_risk
    ml_result = predict_mastitis_risk(feature_payload)

    # 5. Format contributing factors with hardware-friendly key names
    formatted_factors = []
    for factor in ml_result.get("contributing_factors", []):
        direction_label = "increases_risk" if factor["direction"] == "risk" else "decreases_risk"
        formatted_factors.append({
            "feature": factor["name"],
            "label": factor["label"],
            "direction": direction_label,
            "contribution": factor["contribution"]
        })

    # 6. Set hardware-safe risk status text
    if ml_result["risk_level"] == "HIGH":
        risk_label = "Elevated Mastitis Risk Detected"
        recommended_action = "Flag for immediate observation. Inspect udder and schedule veterinary check."
    elif ml_result["risk_level"] == "MEDIUM":
        risk_label = "Moderate Risk — Increased Monitoring Recommended"
        recommended_action = "Increase observation frequency. Re-check hygiene and milking conditions."
    else:
        risk_label = "Low Mastitis Risk"
        recommended_action = "Continue routine monitoring and standard farm management."

    # 7. Construct final serializable response
    response = {
        "cow_id": cow_id,
        "timestamp": timestamp,
        "mastitis_probability": ml_result["mastitis_probability"],
        "healthy_probability": ml_result["healthy_probability"],
        "risk_level": ml_result["risk_level"],
        "risk_label": risk_label,
        "recommended_action": recommended_action,
        "contributing_factors": formatted_factors,
        "disclaimer": (
            "This software prototype evaluates risk based on model-associated factors. "
            "It is not a clinical veterinary diagnosis."
        )
    }

    return response

if __name__ == "__main__":
    # Quick sanity test
    test_payload = {
        "cow_id": "COW_TEST_001",
        "timestamp": "2026-08-28T14:30:00Z",
        "Breed": "Holstein_Friesian",
        "Age_Years": 5.0,
        "Lactation_Number": 3,
        "Parity": 3,
        "Days_In_Milk": 110,
        "Previous_Mastitis_History": 1,
        "Vaccination_Status": 1,
        "Body_Temperature_C": 39.4,
        "Udder_Temperature_C": 39.7,
        "Activity_Index": 46.0,
        "Rumination_Time_min": 360.0,
        "Feed_Intake_kgDM": 14.0,
        "Water_Intake_L": 62.0,
        "Ambient_Temperature_C": 27.5,
        "Humidity_pct": 68.0,
        "THI": 77.0,
        "Hygiene_Score": 3,
        "Bedding_Cleanliness_Score": 3,
        "Milking_Frequency": 2
    }
    output = process_sensor_reading(test_payload)
    print("Hardware Interface Output Sanity Check:")
    print(json.dumps(output, indent=2))
