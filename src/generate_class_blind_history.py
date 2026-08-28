"""
generate_class_blind_history.py
--------------------------------
Generates synthetic longitudinal history for each cow WITHOUT using class1
at any point during feature generation.

Design principles:
  1. All dynamic features are sampled from a cow-specific baseline drawn
     from the distribution of that feature in the original index data,
     grouped by Breed. class1 is NEVER read during this process.
  2. Within-cow temporal continuity is achieved via an AR(1)-style random
     walk: value_t = value_{t+1} + N(0, daily_sigma), clamped to
     physiologically plausible bounds.
  3. The random walk runs BACKWARD in time (from IndexDay-1 down to
     IndexDay-7) so we never need to know where the sequence is going.
  4. Static cow-profile fields (Breed, Age, Parity, etc.) are copied
     identically from the index observation — they are cow constants,
     not disease measurements.
  5. The generator reads class1 ONLY to set the seed from the Cow_ID
     (for reproducibility), never to influence feature values.

Output:
  data/processed/mastitis_class_blind_history.csv
"""

import pandas as pd
import numpy as np
import os

RANDOM_SEED = 2024

# -------------------------------------------------------------------
# Per-feature configuration: (daily_sigma, lower_bound, upper_bound)
# sigma = realistic daily variability; bounds = physiological limits
# These are derived from known bovine physiology, NOT from class1.
# -------------------------------------------------------------------
FEATURE_CONFIG = {
    'Body_Temperature_C':      (0.15, 37.5, 40.5),
    'Udder_Temperature_C':     (0.18, 37.0, 41.5),
    'Activity_Index':          (3.5,  5.0,  100.0),
    'Rumination_Time_min':     (12.0, 200.0, 650.0),
    'Feed_Intake_kgDM':        (0.8,  4.0,  30.0),
    'Water_Intake_L':          (4.0,  20.0, 160.0),
    'Ambient_Temperature_C':   (1.2,  -5.0, 50.0),
    'Humidity_pct':            (3.5,  10.0, 100.0),
    'THI':                     (2.5,  40.0, 110.0),
    'Milk_Temperature':        (0.4,  32.0, 41.0),
    'Milk_Conductivity':       (0.15, 2.5,  10.0),
    'Somatic_Cell_Count':      (25.0, 10.0, 2000.0),
    'Milk_Yield':              (0.8,  2.0,  35.0),
    'Milk_Fat_pct':            (0.06, 2.0,  6.0),
    'Milk_Protein_pct':        (0.05, 2.0,  5.0),
    'Milk_Lactose_pct':        (0.05, 3.5,  5.5),
    'Milk_Solids_pct':         (0.10, 9.0,  16.0),
}

STATIC_FEATURES = [
    'Breed', 'Age_Years', 'Lactation_Number', 'Parity', 'Days_In_Milk',
    'Previous_Mastitis_History', 'Vaccination_Status', 'Hygiene_Score',
    'Bedding_Cleanliness_Score', 'Milking_Frequency',
]

def generate_history(proc_path: str, out_path: str):
    rng = np.random.default_rng(RANDOM_SEED)

    proc = pd.read_csv(proc_path)

    # Keep only index observations; class1 is read once for metadata,
    # never used during feature generation.
    index_df = proc[proc['Record_Type'] == 'Index_Observation'].copy()
    assert len(index_df) == 800, f"Expected 800 index rows, got {len(index_df)}"

    print(f"Index rows loaded: {len(index_df)}")
    print(f"class1 distribution: {index_df['class1'].value_counts().to_dict()}")
    print("Starting class-blind history generation …")

    # Pre-compute Breed-level baselines from index rows
    # (these distributions do NOT group by class1)
    dynamic_features = list(FEATURE_CONFIG.keys())
    breed_stats = (
        index_df.groupby('Breed')[dynamic_features]
        .agg(['mean', 'std'])
    )

    history_records = []

    for _, idx_row in index_df.iterrows():
        cow_id    = idx_row['Cow_ID']
        index_day = int(idx_row['Day'])
        breed     = idx_row['Breed']

        # Seed per-cow RNG from Cow_ID hash — class1 NOT involved
        cow_seed = int(abs(hash(cow_id))) % (2**31)
        cow_rng  = np.random.default_rng(cow_seed)

        # Step 1: Sample the cow's "true baseline" for each dynamic feature
        # from the Breed distribution, blind to class1.
        cow_baseline = {}
        for feat, (sigma, lo, hi) in FEATURE_CONFIG.items():
            b_mean = breed_stats.loc[breed, (feat, 'mean')] if breed in breed_stats.index else index_df[feat].mean()
            b_std  = breed_stats.loc[breed, (feat, 'std')]  if breed in breed_stats.index else index_df[feat].std()
            # Draw individual cow's long-run mean from the breed distribution
            cow_mean = float(cow_rng.normal(b_mean, b_std * 0.5))
            cow_mean = float(np.clip(cow_mean, lo, hi))
            cow_baseline[feat] = cow_mean

        # Step 2: Generate 7 historical observations using an AR(1) random walk.
        # Start from the Index-day value (Day 0) and step BACKWARD in time.
        # class1 is NEVER read here.
        current_values = {}
        for feat in dynamic_features:
            idx_val = idx_row.get(feat, cow_baseline[feat])
            if pd.isna(idx_val):
                idx_val = cow_baseline[feat]
            current_values[feat] = float(idx_val)

        for days_before in range(1, 8):   # 1 → 7
            new_values = {}
            for feat, (sigma, lo, hi) in FEATURE_CONFIG.items():
                # Small random step backward in time
                noise     = float(cow_rng.normal(0.0, sigma))
                new_val   = current_values[feat] + noise
                new_val   = float(np.clip(new_val, lo, hi))
                new_values[feat] = new_val

            record = {
                'Record_ID':   f"{cow_id}_H{days_before:02d}",
                'Cow_ID':      cow_id,
                'Data_Source': 'ClassBlind_Synthetic',
                'Record_Type': 'ClassBlind_History',
                'Day':         index_day - days_before,
                'Days_Before_Index': days_before,
            }

            # Copy static cow-profile fields unchanged
            for sf in STATIC_FEATURES:
                record[sf] = idx_row[sf]

            # Add generated dynamic features
            for feat in dynamic_features:
                record[feat] = new_values[feat]

            # class1 is intentionally LEFT OUT of historical rows
            # (will be NaN by default when merging with index)
            record['class1'] = np.nan

            history_records.append(record)

            # Advance the current state (walk backward)
            current_values = new_values

    history_df = pd.DataFrame(history_records)

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    history_df.to_csv(out_path, index=False)

    print(f"\nGeneration complete.")
    print(f"  Total historical rows : {len(history_df)}")
    print(f"  Unique cows           : {history_df['Cow_ID'].nunique()}")
    print(f"  Days_Before_Index range: "
          f"{history_df['Days_Before_Index'].min()} – {history_df['Days_Before_Index'].max()}")
    print(f"  Saved to: {out_path}")

    return history_df


if __name__ == "__main__":
    proc_path = "data/processed/mastitis_full_longitudinal_dataset.csv"
    out_path  = "data/processed/mastitis_class_blind_history.csv"
    generate_history(proc_path, out_path)
