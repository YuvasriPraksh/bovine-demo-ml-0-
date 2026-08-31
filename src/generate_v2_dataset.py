"""
generate_v2_dataset.py
---------------------
Generates an updated synthetic dataset (v2) implementing the exact 27-feature schema
specified by the user.

Schema includes:
1. record_date
2. farm_id
3. animal_id
4. breed
5. age_years
6. previous_mastitis_history
7. vaccinated
8. chronic_disease_flag
9. ambient_temperature_c
10. relative_humidity_pct
11. environment_total_mastitis_pathogen_load_log10
12. S_aureus_load_log10_cfu_equiv
13. S_uberis_load_log10_cfu_equiv
14. E_coli_load_log10_cfu_equiv
15. K_pneumoniae_load_log10_cfu_equiv
16. S_agalactiae_load_log10_cfu_equiv
17. dominant_environment_pathogen
18. milk_yield_kg_day
19. milk_conductivity_mS_cm
20. body_temperature_c
21. udder_surface_temperature_c
22. clinical_mastitis_now
23. synthetic_risk_score_pct
24. mastitis_risk_category
25. mastitis_in_next_7d
26. mastitis_in_next_14d
27. days_to_synthetic_event
"""

import os
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

RANDOM_SEED = 42

def generate_dataset_v2(n_samples: int = 800, out_path: str = "data/processed/mastitis_dataset_v2.csv") -> pd.DataFrame:
    rng = np.random.default_rng(RANDOM_SEED)
    
    start_date = datetime(2026, 8, 1)
    dates = [ (start_date + timedelta(days=int(d))).strftime("%Y-%m-%d") for d in rng.integers(0, 30, size=n_samples) ]
    
    farms = [f"FARM_{i:03d}" for i in range(1, 6)]
    farm_ids = rng.choice(farms, size=n_samples)
    
    animal_ids = [f"COW_{i:04d}" for i in range(1, n_samples + 1)]
    
    breeds = ["Holstein Friesian", "Jersey", "Gir", "Sahiwal"]
    breed_choices = rng.choice(breeds, size=n_samples, p=[0.4, 0.3, 0.15, 0.15])
    
    age_years = np.round(rng.normal(4.8, 1.5, size=n_samples).clip(2.0, 10.0), 1)
    
    prev_mastitis = rng.choice([0, 1], size=n_samples, p=[0.75, 0.25])
    vaccinated = rng.choice([0, 1], size=n_samples, p=[0.20, 0.80])
    chronic_flag = rng.choice([0, 1], size=n_samples, p=[0.88, 0.12])
    
    amb_temp = np.round(rng.normal(28.5, 4.0, size=n_samples).clip(15.0, 42.0), 1)
    rel_humidity = np.round(rng.normal(68.0, 12.0, size=n_samples).clip(30.0, 95.0), 1)
    
    # Pathogen loads (log10 CFU equivalent)
    # Environmental factors increase base loads
    env_stress = (amb_temp - 25.0).clip(0, None) * 0.05 + (rel_humidity - 60.0).clip(0, None) * 0.02
    
    s_aureus = np.round((rng.normal(2.5, 0.8, size=n_samples) + env_stress).clip(1.0, 6.0), 2)
    s_uberis = np.round((rng.normal(2.8, 0.9, size=n_samples) + env_stress).clip(1.0, 6.0), 2)
    e_coli = np.round((rng.normal(2.3, 0.7, size=n_samples) + env_stress).clip(1.0, 6.0), 2)
    k_pneumoniae = np.round((rng.normal(2.2, 0.7, size=n_samples) + env_stress).clip(1.0, 6.0), 2)
    s_agalactiae = np.round((rng.normal(2.0, 0.6, size=n_samples) + env_stress).clip(1.0, 5.5), 2)
    
    pathogen_matrix = np.column_stack([s_aureus, s_uberis, e_coli, k_pneumoniae, s_agalactiae])
    pathogen_names = ["S. aureus", "S. uberis", "E. coli", "K. pneumoniae", "S. agalactiae"]
    
    total_load = np.round(np.log10(np.sum(10**pathogen_matrix, axis=1)), 2)
    dominant_pathogen = [pathogen_names[idx] for idx in np.argmax(pathogen_matrix, axis=1)]
    
    # Disease risk synthesis:
    # Pathogen load, high ambient temp, history, and lack of vaccination increase risk
    base_risk = (
        (total_load - 2.5).clip(0, None) * 15.0 +
        prev_mastitis * 12.0 +
        chronic_flag * 10.0 -
        vaccinated * 8.0 +
        (amb_temp - 30.0).clip(0, None) * 2.0
    )
    # Add random noise
    risk_score_raw = base_risk + rng.normal(15.0, 10.0, size=n_samples)
    risk_score_pct = np.round(risk_score_raw.clip(0.0, 100.0), 1)
    
    # Days to event calculation based on risk score
    # High risk score => event in near future
    days_to_event = []
    for score in risk_score_pct:
        if score >= 75.0:
            days_to_event.append(rng.integers(0, 4))
        elif score >= 50.0:
            days_to_event.append(rng.integers(3, 8))
        elif score >= 30.0:
            days_to_event.append(rng.integers(7, 15))
        else:
            days_to_event.append(rng.integers(15, 45))
            
    days_to_event = np.array(days_to_event)
    
    clinical_now = ((days_to_event == 0) | ((risk_score_pct > 80.0) & (rng.random(n_samples) < 0.5))).astype(int)
    mastitis_7d = ((days_to_event <= 7) | (clinical_now == 1)).astype(int)
    mastitis_14d = ((days_to_event <= 14) | (clinical_now == 1)).astype(int)
    
    # Physiological indicators correlated with disease risk / inflammation
    inflammation_factor = (risk_score_pct / 100.0) ** 1.5
    
    body_temp = np.round((rng.normal(38.6, 0.2, size=n_samples) + inflammation_factor * 1.5).clip(38.0, 40.5), 2)
    udder_temp = np.round((body_temp - 0.3 + rng.normal(0.0, 0.2, size=n_samples) + inflammation_factor * 1.8).clip(37.5, 41.5), 2)
    milk_cond = np.round((rng.normal(4.8, 0.4, size=n_samples) + inflammation_factor * 2.8).clip(3.5, 8.5), 2)
    milk_yield = np.round((rng.normal(24.0, 4.0, size=n_samples) - inflammation_factor * 12.0).clip(5.0, 35.0), 1)
    
    risk_categories = []
    for score in risk_score_pct:
        if score < 25.0:
            risk_categories.append("No Risk")
        elif score < 50.0:
            risk_categories.append("Low Risk")
        elif score < 75.0:
            risk_categories.append("Moderate Risk")
        else:
            risk_categories.append("High Risk")
            
    df = pd.DataFrame({
        "record_date": dates,
        "farm_id": farm_ids,
        "animal_id": animal_ids,
        "breed": breed_choices,
        "age_years": age_years,
        "previous_mastitis_history": prev_mastitis,
        "vaccinated": vaccinated,
        "chronic_disease_flag": chronic_flag,
        "ambient_temperature_c": amb_temp,
        "relative_humidity_pct": rel_humidity,
        "environment_total_mastitis_pathogen_load_log10": total_load,
        "S_aureus_load_log10_cfu_equiv": s_aureus,
        "S_uberis_load_log10_cfu_equiv": s_uberis,
        "E_coli_load_log10_cfu_equiv": e_coli,
        "K_pneumoniae_load_log10_cfu_equiv": k_pneumoniae,
        "S_agalactiae_load_log10_cfu_equiv": s_agalactiae,
        "dominant_environment_pathogen": dominant_pathogen,
        "milk_yield_kg_day": milk_yield,
        "milk_conductivity_mS_cm": milk_cond,
        "body_temperature_c": body_temp,
        "udder_surface_temperature_c": udder_temp,
        "clinical_mastitis_now": clinical_now,
        "synthetic_risk_score_pct": risk_score_pct,
        "mastitis_risk_category": risk_categories,
        "mastitis_in_next_7d": mastitis_7d,
        "mastitis_in_next_14d": mastitis_14d,
        "days_to_synthetic_event": days_to_event
    })
    
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    df.to_csv(out_path, index=False)
    print(f"Successfully generated 27-feature dataset v2 with {len(df)} rows at: {out_path}")
    return df

if __name__ == "__main__":
    generate_dataset_v2()
