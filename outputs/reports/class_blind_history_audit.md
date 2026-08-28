# Class-Blind History Generation – Audit Report

## 1. Basic Structure Checks

- **Unique cows in new history:** 800  (expected: 800)
- **Every cow has exactly 7 historical rows:** True  (min=7, max=7)
- **Total historical rows:** 5600  (expected: 5600)
- **Days_Before_Index values present:** [1, 2, 3, 4, 5, 6, 7]  (expected: 1–7)
- **Day = IndexDay − Days_Before_Index violations:** 0  (expected: 0)
- **class1 in historical rows:** column present but all NaN = True  (non-NaN count: 0)

## 2. Code-Level Audit — Was class1 read during generation?

- Lines in generator that READ class1 (excluding comments): [4, 10, 19, 74, 145]
  - Line 4: `Generates synthetic longitudinal history for each cow WITHOUT using class1`
  - Line 10: `grouped by Breed. class1 is NEVER read during this process.`
  - Line 19: `5. The generator reads class1 ONLY to set the seed from the Cow_ID`
  - Line 74: `print(f"class1 distribution: {index_df['class1'].value_counts().to_dict()}")`
  - Line 145: `record['class1'] = np.nan`

## 3. Direct Correlation: Historical Feature Values vs class1

A high direct correlation at T-7 would mean the generated values are already separated by class, indicating label leakage.

| Feature | T-7 r(feat, class1) | T-3 r(feat, class1) | T-1 r(feat, class1) |
|---|---|---|---|
| Body_Temperature_C | 0.2386 | 0.2671 | 0.3048 |
| Udder_Temperature_C | 0.2725 | 0.2992 | 0.3092 |
| Activity_Index | -0.1821 | -0.1899 | -0.2011 |
| Rumination_Time_min | -0.1367 | -0.1379 | -0.1412 |
| Feed_Intake_kgDM | -0.0832 | -0.1003 | -0.0962 |
| Water_Intake_L | -0.3321 | -0.3546 | -0.3657 |
| Ambient_Temperature_C | 0.0254 | 0.0413 | 0.0307 |
| Humidity_pct | 0.0358 | 0.0181 | 0.0009 |
| THI | 0.044 | 0.045 | 0.0391 |

## 4. Delta Correlation: (Index_value − T-7_value) vs class1

The OLD history had r ≈ −0.55 for Body_Temperature_C and −0.55 for Udder_Temperature_C, indicating class-aware backfilling.

| Feature | OLD r(delta@7, class1) | NEW r(delta@7, class1) | OLD r(delta@3, class1) | NEW r(delta@3, class1) |
|---|---|---|---|---|
| Body_Temperature_C | -0.5055 | -0.0301 | -0.3196 | -0.02 |
| Udder_Temperature_C | -0.5483 | -0.039 | -0.3045 | -0.0279 |
| Activity_Index | -0.1045 | 0.0265 | -0.7741 | 0.02 |
| Rumination_Time_min | -0.0691 | 0.0214 | -0.7265 | -0.006 |
| Feed_Intake_kgDM | 0.2948 | 0.0008 | 0.0 | 0.0348 |
| Water_Intake_L | 0.4334 | 0.0101 | 0.0 | -0.0058 |
| Ambient_Temperature_C | 0.0521 | 0.0074 | 0.0 | -0.0261 |
| Humidity_pct | -0.0232 | -0.0567 | 0.0 | -0.0332 |
| THI | 0.0458 | -0.0244 | 0.0 | -0.0239 |

## 5. Mean Values by class1 at T-7, T-5, T-3, T-1 (NEW history)

For the OLD contaminated history, mastitis cows had consistently higher temperature at EVERY historical time step (flat separation). In the class-blind data the difference should be near zero and irregular.

### Body_Temperature_C

| Days_Before_Index | Healthy(0) Mean | Mastitis(1) Mean | Diff |
|---|---|---|---|
| 7 | 38.5153 | 38.8093 | 0.294 |
| 5 | 38.5307 | 38.7944 | 0.2637 |
| 3 | 38.5232 | 38.8015 | 0.2783 |
| 1 | 38.5248 | 38.798 | 0.2732 |
| 0 (Index) | 38.5237 | 38.7892 | 0.2655 |

### Activity_Index

| Days_Before_Index | Healthy(0) Mean | Mastitis(1) Mean | Diff |
|---|---|---|---|
| 7 | 71.4114 | 64.759 | -6.6524 |
| 5 | 71.3382 | 64.7821 | -6.5561 |
| 3 | 71.7656 | 65.3878 | -6.3778 |
| 1 | 71.8161 | 65.5453 | -6.2708 |
| 0 (Index) | 71.729 | 65.6467 | -6.0823 |

### Rumination_Time_min

| Days_Before_Index | Healthy(0) Mean | Mastitis(1) Mean | Diff |
|---|---|---|---|
| 7 | 455.3136 | 438.2077 | -17.1059 |
| 5 | 455.0508 | 438.8751 | -16.1757 |
| 3 | 454.8035 | 439.6711 | -15.1324 |
| 1 | 454.5043 | 440.3502 | -14.1541 |
| 0 (Index) | 454.7941 | 439.3604 | -15.4337 |

## 6. Verdict

**Max |r(delta@T-7, class1)| in NEW history:** 0.0567

**[SAFE] No evidence of systematic label encoding in the new history.**

### Comparison Summary

| Metric | OLD (contaminated) | NEW (class-blind) |
|---|---|---|
| r(delta Body_Temp@T-7, class1) | -0.5055 | -0.0301 |
| r(delta Udder_Temp@T-7, class1) | -0.5483 | -0.039 |
| r(delta Water_Intake@T-7, class1) | 0.4334 | 0.0101 |
| Flat class separation across all 7 days | YES | NO |
| class1 used in generation | YES | NO (confirmed) |