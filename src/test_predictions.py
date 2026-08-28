import sys
import os
import pandas as pd

# Ensure src directory is in the path for importing predict
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from predict import predict_mastitis_risk

def get_risk_category(probability):
    if probability < 0.30:
        return "LOW"
    elif probability <= 0.70:
        return "MEDIUM"
    else:
        return "HIGH"

def main():
    print("==========================================================")
    print(" SYNTHETIC DEMONSTRATION COW SCENARIOS - STRICT EARLY RISK")
    print("==========================================================")
    print("DISCLAIMER: These inputs are entirely synthetic and manually")
    print("constructed for software demonstration purposes only. They")
    print("are NOT real farm observations and do NOT prove clinical")
    print("accuracy or genuine 7-14 day forecasting.")
    print("==========================================================\n")

    # 10 Synthetic Scenarios
    scenarios = [
        {
            "name": "Scenario 1: Clearly healthy young cow",
            "data": {
                'Breed': 'Holstein_Friesian', 'Age_Years': 3.0, 'Lactation_Number': 1, 'Parity': 1,
                'Days_In_Milk': 60, 'Previous_Mastitis_History': 0, 'Vaccination_Status': 1,
                'Body_Temperature_C': 38.5, 'Udder_Temperature_C': 38.5, 'Activity_Index': 80.0,
                'Rumination_Time_min': 500.0, 'Feed_Intake_kgDM': 20.0, 'Water_Intake_L': 90.0,
                'Ambient_Temperature_C': 22.0, 'Humidity_pct': 50.0, 'THI': 68.0,
                'Hygiene_Score': 1, 'Bedding_Cleanliness_Score': 1, 'Milking_Frequency': 3
            }
        },
        {
            "name": "Scenario 2: Healthy older cow, no history",
            "data": {
                'Breed': 'Gir', 'Age_Years': 7.0, 'Lactation_Number': 5, 'Parity': 5,
                'Days_In_Milk': 150, 'Previous_Mastitis_History': 0, 'Vaccination_Status': 1,
                'Body_Temperature_C': 38.6, 'Udder_Temperature_C': 38.7, 'Activity_Index': 70.0,
                'Rumination_Time_min': 480.0, 'Feed_Intake_kgDM': 18.0, 'Water_Intake_L': 85.0,
                'Ambient_Temperature_C': 25.0, 'Humidity_pct': 55.0, 'THI': 72.0,
                'Hygiene_Score': 2, 'Bedding_Cleanliness_Score': 2, 'Milking_Frequency': 2
            }
        },
        {
            "name": "Scenario 3: Mildly concerning - drop in rumination",
            "data": {
                'Breed': 'Sahiwal', 'Age_Years': 4.5, 'Lactation_Number': 2, 'Parity': 2,
                'Days_In_Milk': 90, 'Previous_Mastitis_History': 0, 'Vaccination_Status': 1,
                'Body_Temperature_C': 38.7, 'Udder_Temperature_C': 38.8, 'Activity_Index': 65.0,
                'Rumination_Time_min': 380.0, 'Feed_Intake_kgDM': 17.5, 'Water_Intake_L': 80.0,
                'Ambient_Temperature_C': 26.0, 'Humidity_pct': 60.0, 'THI': 74.0,
                'Hygiene_Score': 2, 'Bedding_Cleanliness_Score': 2, 'Milking_Frequency': 2
            }
        },
        {
            "name": "Scenario 4: Moderate risk - history + poor hygiene",
            "data": {
                'Breed': 'Holstein_Friesian', 'Age_Years': 6.0, 'Lactation_Number': 4, 'Parity': 4,
                'Days_In_Milk': 210, 'Previous_Mastitis_History': 1, 'Vaccination_Status': 0,
                'Body_Temperature_C': 38.8, 'Udder_Temperature_C': 38.9, 'Activity_Index': 60.0,
                'Rumination_Time_min': 420.0, 'Feed_Intake_kgDM': 16.0, 'Water_Intake_L': 75.0,
                'Ambient_Temperature_C': 24.0, 'Humidity_pct': 65.0, 'THI': 71.0,
                'Hygiene_Score': 4, 'Bedding_Cleanliness_Score': 4, 'Milking_Frequency': 2
            }
        },
        {
            "name": "Scenario 5: High risk - elevated temp + low activity",
            "data": {
                'Breed': 'Holstein_Friesian', 'Age_Years': 5.0, 'Lactation_Number': 3, 'Parity': 3,
                'Days_In_Milk': 45, 'Previous_Mastitis_History': 1, 'Vaccination_Status': 1,
                'Body_Temperature_C': 39.8, 'Udder_Temperature_C': 40.2, 'Activity_Index': 40.0,
                'Rumination_Time_min': 310.0, 'Feed_Intake_kgDM': 12.0, 'Water_Intake_L': 55.0,
                'Ambient_Temperature_C': 28.0, 'Humidity_pct': 75.0, 'THI': 79.0,
                'Hygiene_Score': 3, 'Bedding_Cleanliness_Score': 3, 'Milking_Frequency': 2
            }
        },
        {
            "name": "Scenario 6: Normal temp but significant behavioral drop",
            "data": {
                'Breed': 'Gir', 'Age_Years': 4.0, 'Lactation_Number': 2, 'Parity': 2,
                'Days_In_Milk': 180, 'Previous_Mastitis_History': 0, 'Vaccination_Status': 1,
                'Body_Temperature_C': 38.5, 'Udder_Temperature_C': 38.6, 'Activity_Index': 35.0,
                'Rumination_Time_min': 280.0, 'Feed_Intake_kgDM': 10.0, 'Water_Intake_L': 45.0,
                'Ambient_Temperature_C': 25.0, 'Humidity_pct': 50.0, 'THI': 70.0,
                'Hygiene_Score': 1, 'Bedding_Cleanliness_Score': 1, 'Milking_Frequency': 2
            }
        },
        {
            "name": "Scenario 7: Heat stress (high THI) + history",
            "data": {
                'Breed': 'Holstein_Friesian', 'Age_Years': 8.0, 'Lactation_Number': 6, 'Parity': 6,
                'Days_In_Milk': 100, 'Previous_Mastitis_History': 1, 'Vaccination_Status': 1,
                'Body_Temperature_C': 39.2, 'Udder_Temperature_C': 39.3, 'Activity_Index': 55.0,
                'Rumination_Time_min': 400.0, 'Feed_Intake_kgDM': 14.0, 'Water_Intake_L': 95.0,
                'Ambient_Temperature_C': 35.0, 'Humidity_pct': 80.0, 'THI': 89.0,
                'Hygiene_Score': 3, 'Bedding_Cleanliness_Score': 3, 'Milking_Frequency': 2
            }
        },
        {
            "name": "Scenario 8: Fresh cow (early lactation) high risk profile",
            "data": {
                'Breed': 'Sahiwal', 'Age_Years': 3.5, 'Lactation_Number': 1, 'Parity': 1,
                'Days_In_Milk': 10, 'Previous_Mastitis_History': 0, 'Vaccination_Status': 0,
                'Body_Temperature_C': 39.6, 'Udder_Temperature_C': 39.9, 'Activity_Index': 42.0,
                'Rumination_Time_min': 330.0, 'Feed_Intake_kgDM': 11.0, 'Water_Intake_L': 50.0,
                'Ambient_Temperature_C': 20.0, 'Humidity_pct': 60.0, 'THI': 65.0,
                'Hygiene_Score': 4, 'Bedding_Cleanliness_Score': 4, 'Milking_Frequency': 3
            }
        },
        {
            "name": "Scenario 9: Unvaccinated, moderate hygiene, normal vitals",
            "data": {
                'Breed': 'Holstein_Friesian', 'Age_Years': 5.5, 'Lactation_Number': 3, 'Parity': 3,
                'Days_In_Milk': 250, 'Previous_Mastitis_History': 0, 'Vaccination_Status': 0,
                'Body_Temperature_C': 38.4, 'Udder_Temperature_C': 38.5, 'Activity_Index': 75.0,
                'Rumination_Time_min': 490.0, 'Feed_Intake_kgDM': 19.0, 'Water_Intake_L': 88.0,
                'Ambient_Temperature_C': 22.0, 'Humidity_pct': 65.0, 'THI': 69.0,
                'Hygiene_Score': 3, 'Bedding_Cleanliness_Score': 3, 'Milking_Frequency': 2
            }
        },
        {
            "name": "Scenario 10: Chronic risk - old cow, history, low activity",
            "data": {
                'Breed': 'Holstein_Friesian', 'Age_Years': 9.0, 'Lactation_Number': 7, 'Parity': 7,
                'Days_In_Milk': 300, 'Previous_Mastitis_History': 1, 'Vaccination_Status': 0,
                'Body_Temperature_C': 38.9, 'Udder_Temperature_C': 39.1, 'Activity_Index': 45.0,
                'Rumination_Time_min': 370.0, 'Feed_Intake_kgDM': 13.0, 'Water_Intake_L': 65.0,
                'Ambient_Temperature_C': 18.0, 'Humidity_pct': 70.0, 'THI': 63.0,
                'Hygiene_Score': 4, 'Bedding_Cleanliness_Score': 4, 'Milking_Frequency': 2
            }
        }
    ]

    summary = []

    for scenario in scenarios:
        print(f"\n--- {scenario['name']} ---")
        try:
            res = predict_mastitis_risk(scenario['data'])
            prob = res['mastitis_probability']
            cat = get_risk_category(prob)
            
            print(f"Predicted Class:      {res['prediction']}")
            print(f"Healthy Probability:  {res['healthy_probability']:.4f}")
            print(f"Mastitis Probability: {prob:.4f}")
            print(f"Risk Category:        {cat}")
            
            summary.append({
                'Scenario': scenario['name'],
                'Class': res['prediction'],
                'Prob': prob,
                'Category': cat
            })
        except Exception as e:
            print(f"Prediction failed: {e}")
            summary.append({
                'Scenario': scenario['name'],
                'Class': 'ERROR',
                'Prob': 0.0,
                'Category': 'ERROR'
            })

    print("\n==========================================================")
    print(" FINAL SUMMARY TABLE")
    print("==========================================================")
    print(f"{'Cow / Scenario Name':<55} | {'Class':<5} | {'Prob':<6} | {'Risk':<6}")
    print("-" * 80)
    for row in summary:
        print(f"{row['Scenario']:<55} | {row['Class']:<5} | {row['Prob']:>6.4f} | {row['Category']:<6}")
    print("==========================================================\n")

if __name__ == "__main__":
    main()
