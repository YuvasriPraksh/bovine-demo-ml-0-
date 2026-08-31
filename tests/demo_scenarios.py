"""
demo_scenarios.py — 10 synthetic demonstration cows
Reads results entirely from the saved model. Nothing is forced.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
from predict import predict_mastitis_risk

SCENARIOS = [
    {
        "name": "Cow A — Clearly healthy, young, low-risk",
        "data": dict(Breed='Holstein_Friesian', Age_Years=3.0, Lactation_Number=1, Parity=1,
                     Days_In_Milk=60, Previous_Mastitis_History=0, Vaccination_Status=1,
                     Body_Temperature_C=38.4, Udder_Temperature_C=38.5, Activity_Index=82.0,
                     Rumination_Time_min=510.0, Feed_Intake_kgDM=20.5, Water_Intake_L=92.0,
                     Ambient_Temperature_C=22.0, Humidity_pct=50.0, THI=67.0,
                     Hygiene_Score=1, Bedding_Cleanliness_Score=1, Milking_Frequency=3),
    },
    {
        "name": "Cow B — Older cow, no history, good management",
        "data": dict(Breed='Gir', Age_Years=7.0, Lactation_Number=5, Parity=5,
                     Days_In_Milk=180, Previous_Mastitis_History=0, Vaccination_Status=1,
                     Body_Temperature_C=38.6, Udder_Temperature_C=38.7, Activity_Index=70.0,
                     Rumination_Time_min=470.0, Feed_Intake_kgDM=18.0, Water_Intake_L=84.0,
                     Ambient_Temperature_C=25.0, Humidity_pct=55.0, THI=72.0,
                     Hygiene_Score=2, Bedding_Cleanliness_Score=2, Milking_Frequency=2),
    },
    {
        "name": "Cow C — Previous mastitis, moderate hygiene",
        "data": dict(Breed='Sahiwal', Age_Years=5.0, Lactation_Number=3, Parity=3,
                     Days_In_Milk=90, Previous_Mastitis_History=1, Vaccination_Status=1,
                     Body_Temperature_C=38.7, Udder_Temperature_C=38.8, Activity_Index=65.0,
                     Rumination_Time_min=430.0, Feed_Intake_kgDM=17.0, Water_Intake_L=78.0,
                     Ambient_Temperature_C=26.0, Humidity_pct=62.0, THI=74.0,
                     Hygiene_Score=3, Bedding_Cleanliness_Score=3, Milking_Frequency=2),
    },
    {
        "name": "Cow D — Elevated body temperature, reduced activity",
        "data": dict(Breed='Holstein_Friesian', Age_Years=4.5, Lactation_Number=2, Parity=2,
                     Days_In_Milk=45, Previous_Mastitis_History=0, Vaccination_Status=1,
                     Body_Temperature_C=39.6, Udder_Temperature_C=39.4, Activity_Index=48.0,
                     Rumination_Time_min=380.0, Feed_Intake_kgDM=15.0, Water_Intake_L=65.0,
                     Ambient_Temperature_C=24.0, Humidity_pct=60.0, THI=72.0,
                     Hygiene_Score=2, Bedding_Cleanliness_Score=2, Milking_Frequency=2),
    },
    {
        "name": "Cow E — Elevated udder temperature, low rumination",
        "data": dict(Breed='Holstein_Friesian', Age_Years=6.0, Lactation_Number=4, Parity=4,
                     Days_In_Milk=200, Previous_Mastitis_History=1, Vaccination_Status=0,
                     Body_Temperature_C=38.9, Udder_Temperature_C=40.1, Activity_Index=55.0,
                     Rumination_Time_min=310.0, Feed_Intake_kgDM=14.0, Water_Intake_L=62.0,
                     Ambient_Temperature_C=27.0, Humidity_pct=68.0, THI=76.0,
                     Hygiene_Score=3, Bedding_Cleanliness_Score=4, Milking_Frequency=2),
    },
    {
        "name": "Cow F — High THI / heat stress, history positive",
        "data": dict(Breed='Holstein_Friesian', Age_Years=7.5, Lactation_Number=5, Parity=5,
                     Days_In_Milk=120, Previous_Mastitis_History=1, Vaccination_Status=1,
                     Body_Temperature_C=39.2, Udder_Temperature_C=39.3, Activity_Index=52.0,
                     Rumination_Time_min=400.0, Feed_Intake_kgDM=14.5, Water_Intake_L=96.0,
                     Ambient_Temperature_C=36.0, Humidity_pct=82.0, THI=91.0,
                     Hygiene_Score=3, Bedding_Cleanliness_Score=3, Milking_Frequency=2),
    },
    {
        "name": "Cow G — Poor hygiene and bedding, multiple risk factors",
        "data": dict(Breed='Sahiwal', Age_Years=6.0, Lactation_Number=4, Parity=4,
                     Days_In_Milk=250, Previous_Mastitis_History=1, Vaccination_Status=0,
                     Body_Temperature_C=38.8, Udder_Temperature_C=38.9, Activity_Index=58.0,
                     Rumination_Time_min=420.0, Feed_Intake_kgDM=15.5, Water_Intake_L=70.0,
                     Ambient_Temperature_C=25.0, Humidity_pct=66.0, THI=73.0,
                     Hygiene_Score=5, Bedding_Cleanliness_Score=5, Milking_Frequency=2),
    },
    {
        "name": "Cow H — Fresh cow (early lactation), no history, high temp",
        "data": dict(Breed='Gir', Age_Years=3.5, Lactation_Number=1, Parity=1,
                     Days_In_Milk=8, Previous_Mastitis_History=0, Vaccination_Status=0,
                     Body_Temperature_C=39.7, Udder_Temperature_C=39.9, Activity_Index=44.0,
                     Rumination_Time_min=330.0, Feed_Intake_kgDM=11.0, Water_Intake_L=50.0,
                     Ambient_Temperature_C=20.0, Humidity_pct=58.0, THI=65.0,
                     Hygiene_Score=4, Bedding_Cleanliness_Score=4, Milking_Frequency=3),
    },
    {
        "name": "Cow I — Normal vitals but severely reduced feed and water",
        "data": dict(Breed='Sahiwal', Age_Years=4.0, Lactation_Number=2, Parity=2,
                     Days_In_Milk=150, Previous_Mastitis_History=0, Vaccination_Status=1,
                     Body_Temperature_C=38.5, Udder_Temperature_C=38.6, Activity_Index=36.0,
                     Rumination_Time_min=290.0, Feed_Intake_kgDM=9.5, Water_Intake_L=42.0,
                     Ambient_Temperature_C=23.0, Humidity_pct=52.0, THI=68.0,
                     Hygiene_Score=2, Bedding_Cleanliness_Score=2, Milking_Frequency=2),
    },
    {
        "name": "Cow J — Chronic risk: old, multiple lactations, history, poor hygiene",
        "data": dict(Breed='Holstein_Friesian', Age_Years=9.0, Lactation_Number=7, Parity=7,
                     Days_In_Milk=290, Previous_Mastitis_History=1, Vaccination_Status=0,
                     Body_Temperature_C=38.9, Udder_Temperature_C=39.1, Activity_Index=46.0,
                     Rumination_Time_min=360.0, Feed_Intake_kgDM=13.0, Water_Intake_L=63.0,
                     Ambient_Temperature_C=18.0, Humidity_pct=70.0, THI=63.0,
                     Hygiene_Score=4, Bedding_Cleanliness_Score=5, Milking_Frequency=2),
    },
]

def main():
    print("=" * 70)
    print("  BOVINE MASTITIS — 10 SYNTHETIC DEMONSTRATION SCENARIOS")
    print("  All predictions by actual trained model. Nothing forced.")
    print("=" * 70)

    summary_rows = []

    for sc in SCENARIOS:
        print(f"\n{sc['name']}")
        print("-" * 60)
        res = predict_mastitis_risk(sc["data"], top_n=5)

        prob  = res["mastitis_probability"]
        level = res["risk_level"]
        pred  = res["prediction"]

        print(f"  Predicted Class:      {pred}  ({res['risk_label']})")
        print(f"  Mastitis Probability: {prob*100:.1f}%")
        print(f"  Risk Level:           {level}")
        print("  Model-associated contributing factors:")
        for i, f in enumerate(res["contributing_factors"], 1):
            arrow = "^" if f["direction"] == "risk" else "v"
            print(f"    {i}. [{arrow}] {f['label']:30s}  {f['contribution']:+.4f}")

        summary_rows.append({
            "Scenario":    sc["name"].split("—")[0].strip(),
            "Class":       pred,
            "Prob %":      f"{prob*100:.1f}",
            "Risk":        level,
            "Top Factor":  res["contributing_factors"][0]["label"] if res["contributing_factors"] else "N/A",
        })

    print("\n\n" + "=" * 70)
    print("  FINAL SUMMARY TABLE")
    print("=" * 70)
    print(f"{'Scenario':<10} {'Class':^6} {'Prob %':^8} {'Risk':^8}  Top Factor")
    print("-" * 70)
    for r in summary_rows:
        print(f"{r['Scenario']:<10} {r['Class']:^6} {r['Prob %']:^8} {r['Risk']:^8}  {r['Top Factor']}")

    print("\nDISCLAIMER: All 10 inputs are synthetic demonstration data.")
    print("This is not a clinical diagnosis or 7-14 day forecasting proof.")

if __name__ == "__main__":
    main()
