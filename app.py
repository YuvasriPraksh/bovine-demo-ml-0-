"""
app.py — Bovine Mastitis AI Early-Risk Monitoring System
SIH Prototype · Streamlit UI
"""

import sys
import os
import json
import numpy as np
import pandas as pd
import streamlit as st

# Ensure src directory is in Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from hardware_interface import process_sensor_reading
from predict import predict_mastitis_risk

# ── 1. PAGE CONFIG ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MastitisAI — Early-Risk Monitoring System",
    page_icon="🐄",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── 2. CUSTOM CSS & STYLING ───────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* Global Padding & Max Width */
.main .block-container {
    padding-top: 1.2rem;
    padding-bottom: 2rem;
    max-width: 1240px;
}

/* Application Header Banner */
.header-container {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    color: #ffffff;
    padding: 1.4rem 1.8rem;
    border-radius: 14px;
    box-shadow: 0 4px 14px rgba(15, 23, 42, 0.12);
    margin-bottom: 1.5rem;
}
.header-title {
    font-size: 1.8rem;
    font-weight: 800;
    margin: 0;
    color: #ffffff;
    display: flex;
    align-items: center;
    gap: 0.6rem;
}
.header-subtitle {
    font-size: 0.95rem;
    color: #94a3b8;
    margin-top: 0.2rem;
}
.status-pill {
    background: rgba(34, 197, 94, 0.15);
    color: #4ade80;
    border: 1px solid rgba(74, 222, 128, 0.3);
    padding: 3px 12px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
    display: inline-flex;
    align-items: center;
    gap: 6px;
}
.tag-pill {
    background: rgba(148, 163, 184, 0.15);
    color: #cbd5e1;
    border: 1px solid rgba(203, 213, 225, 0.25);
    padding: 3px 12px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 500;
}

/* Demo Metric Cards */
.overview-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 1rem 1.2rem;
    text-align: center;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}
.overview-val {
    font-size: 1.8rem;
    font-weight: 700;
    color: #0f172a;
    line-height: 1.2;
}
.overview-lbl {
    font-size: 0.78rem;
    font-weight: 600;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}

/* Result Cards */
.result-card {
    background: #ffffff;
    border-radius: 16px;
    padding: 1.6rem 1.8rem;
    border: 1px solid #e2e8f0;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
    margin-bottom: 1.2rem;
}
.prob-large {
    font-size: 4.2rem;
    font-weight: 800;
    line-height: 1;
    letter-spacing: -0.02em;
}
.prob-low { color: #16a34a; }
.prob-medium { color: #d97706; }
.prob-high { color: #dc2626; }

/* Risk Badges */
.badge-low {
    background: #dcfce7;
    color: #15803d;
    font-weight: 700;
    padding: 6px 18px;
    border-radius: 20px;
    font-size: 1rem;
    letter-spacing: 0.02em;
    display: inline-block;
}
.badge-medium {
    background: #fef9c3;
    color: #854d0e;
    font-weight: 700;
    padding: 6px 18px;
    border-radius: 20px;
    font-size: 1rem;
    letter-spacing: 0.02em;
    display: inline-block;
}
.badge-high {
    background: #fee2e2;
    color: #b91c1c;
    font-weight: 700;
    padding: 6px 18px;
    border-radius: 20px;
    font-size: 1rem;
    letter-spacing: 0.02em;
    display: inline-block;
}

/* Explainability Factor Items */
.factor-card-risk {
    background: #fef2f2;
    border-left: 4px solid #ef4444;
    border-radius: 8px;
    padding: 0.75rem 1rem;
    margin-bottom: 0.5rem;
}
.factor-card-protective {
    background: #f0fdf4;
    border-left: 4px solid #22c55e;
    border-radius: 8px;
    padding: 0.75rem 1rem;
    margin-bottom: 0.5rem;
}

/* Action Banner */
.action-banner-low {
    background: #f0fdf4;
    border: 1px solid #bbf7d0;
    color: #166534;
    border-radius: 12px;
    padding: 1.1rem 1.3rem;
}
.action-banner-medium {
    background: #fefce8;
    border: 1px solid #fef08a;
    color: #854d0e;
    border-radius: 12px;
    padding: 1.1rem 1.3rem;
}
.action-banner-high {
    background: #fff1f2;
    border: 1px solid #fecdd3;
    color: #9f1239;
    border-radius: 12px;
    padding: 1.1rem 1.3rem;
}

/* Section Headings */
.section-head {
    font-size: 1.1rem;
    font-weight: 700;
    color: #0f172a;
    margin-bottom: 0.8rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

/* System Flow Architecture Box */
.flow-box {
    background: #1e293b;
    color: #e2e8f0;
    font-family: monospace;
    font-size: 0.82rem;
    padding: 1rem;
    border-radius: 10px;
    line-height: 1.4;
}

/* Footer Disclaimer */
.disclaimer-card {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    font-size: 0.8rem;
    color: #64748b;
    line-height: 1.5;
    margin-top: 2rem;
}
</style>
""", unsafe_allow_html=True)

# ── PRESET HARDWARE DEMONSTRATION SCENARIOS ──────────────────────────────────
PRESET_SCENARIOS = {
    "Custom Input (Manual Form Input)": None,
    "Scenario A: COW_101 — Healthy (Low Risk Demo)": {
        "cow_id": "COW_101_HEALTHY", "Breed": "Holstein_Friesian", "Age_Years": 3.0, "Lactation_Number": 1, "Parity": 1,
        "Days_In_Milk": 60, "Previous_Mastitis_History": 0, "Vaccination_Status": 1, "Body_Temperature_C": 38.4,
        "Udder_Temperature_C": 38.5, "Activity_Index": 82.0, "Rumination_Time_min": 510.0, "Feed_Intake_kgDM": 20.5,
        "Water_Intake_L": 92.0, "Ambient_Temperature_C": 22.0, "Humidity_pct": 50.0, "THI": 67.0,
        "Hygiene_Score": 1, "Bedding_Cleanliness_Score": 1, "Milking_Frequency": 3
    },
    "Scenario B: COW_102 — Normal Older Cow (Low Risk Demo)": {
        "cow_id": "COW_102_LOW_RISK", "Breed": "Gir", "Age_Years": 7.0, "Lactation_Number": 5, "Parity": 5,
        "Days_In_Milk": 180, "Previous_Mastitis_History": 0, "Vaccination_Status": 1, "Body_Temperature_C": 38.6,
        "Udder_Temperature_C": 38.7, "Activity_Index": 70.0, "Rumination_Time_min": 470.0, "Feed_Intake_kgDM": 18.0,
        "Water_Intake_L": 84.0, "Ambient_Temperature_C": 25.0, "Humidity_pct": 55.0, "THI": 72.0,
        "Hygiene_Score": 2, "Bedding_Cleanliness_Score": 2, "Milking_Frequency": 2
    },
    "Scenario C: COW_103 — Moderate Risk (History & Hygiene Demo)": {
        "cow_id": "COW_103_MEDIUM_RISK", "Breed": "Sahiwal", "Age_Years": 6.0, "Lactation_Number": 4, "Parity": 4,
        "Days_In_Milk": 250, "Previous_Mastitis_History": 1, "Vaccination_Status": 0, "Body_Temperature_C": 38.8,
        "Udder_Temperature_C": 38.9, "Activity_Index": 58.0, "Rumination_Time_min": 420.0, "Feed_Intake_kgDM": 15.5,
        "Water_Intake_L": 70.0, "Ambient_Temperature_C": 25.0, "Humidity_pct": 66.0, "THI": 73.0,
        "Hygiene_Score": 5, "Bedding_Cleanliness_Score": 5, "Milking_Frequency": 2
    },
    "Scenario D: COW_104 — High Risk (Elevated Fever & Lethargy Demo)": {
        "cow_id": "COW_104_HIGH_RISK", "Breed": "Holstein_Friesian", "Age_Years": 4.5, "Lactation_Number": 2, "Parity": 2,
        "Days_In_Milk": 45, "Previous_Mastitis_History": 0, "Vaccination_Status": 1, "Body_Temperature_C": 39.6,
        "Udder_Temperature_C": 39.4, "Activity_Index": 48.0, "Rumination_Time_min": 380.0, "Feed_Intake_kgDM": 15.0,
        "Water_Intake_L": 65.0, "Ambient_Temperature_C": 24.0, "Humidity_pct": 60.0, "THI": 72.0,
        "Hygiene_Score": 2, "Bedding_Cleanliness_Score": 2, "Milking_Frequency": 2
    },
    "Scenario E: COW_105 — Very High Risk (Udder Heat & Acute Symptoms Demo)": {
        "cow_id": "COW_105_ACUTE_RISK", "Breed": "Holstein_Friesian", "Age_Years": 5.5, "Lactation_Number": 4, "Parity": 4,
        "Days_In_Milk": 120, "Previous_Mastitis_History": 1, "Vaccination_Status": 1, "Body_Temperature_C": 39.8,
        "Udder_Temperature_C": 40.2, "Activity_Index": 40.0, "Rumination_Time_min": 310.0, "Feed_Intake_kgDM": 12.0,
        "Water_Intake_L": 55.0, "Ambient_Temperature_C": 28.0, "Humidity_pct": 75.0, "THI": 79.0,
        "Hygiene_Score": 4, "Bedding_Cleanliness_Score": 4, "Milking_Frequency": 2
    }
}


# ── SECTION 1 — HEADER ────────────────────────────────────────────────────────
st.markdown("""
<div class="header-container">
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem;">
        <div>
            <h1 class="header-title">🐄 MastitisAI</h1>
            <div class="header-subtitle">Bovine Mastitis Early-Risk Monitoring System · SIH Prototype</div>
        </div>
        <div style="display: flex; gap: 0.6rem; align-items: center;">
            <span class="status-pill"><span style="font-size:10px;">●</span> AI Model Online</span>
            <span class="tag-pill">Prototype | Synthetic Data</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# ── SECTION 2 — FARM OVERVIEW (DEMO METRICS) ─────────────────────────────────
st.markdown('<div class="section-head">📊 Demo Farm Overview</div>', unsafe_allow_html=True)

ov_col1, ov_col2, ov_col3, ov_col4 = st.columns(4)
with ov_col1:
    st.markdown("""
    <div class="overview-card">
        <div class="overview-val">120</div>
        <div class="overview-lbl">DEMO COWS TOTAL</div>
    </div>
    """, unsafe_allow_html=True)
with ov_col2:
    st.markdown("""
    <div class="overview-card" style="border-top: 3px solid #22c55e;">
        <div class="overview-val" style="color: #15803d;">85</div>
        <div class="overview-lbl">LOW RISK (DEMO)</div>
    </div>
    """, unsafe_allow_html=True)
with ov_col3:
    st.markdown("""
    <div class="overview-card" style="border-top: 3px solid #eab308;">
        <div class="overview-val" style="color: #854d0e;">25</div>
        <div class="overview-lbl">MEDIUM RISK (DEMO)</div>
    </div>
    """, unsafe_allow_html=True)
with ov_col4:
    st.markdown("""
    <div class="overview-card" style="border-top: 3px solid #ef4444;">
        <div class="overview-val" style="color: #b91c1c;">10</div>
        <div class="overview-lbl">HIGH RISK (DEMO)</div>
    </div>
    """, unsafe_allow_html=True)

st.caption("⚠️ *Note: Numbers above are demonstration figures for UI visualization.*")
st.markdown("<br>", unsafe_allow_html=True)


# ── SECTION 3 — COW ANALYSIS (SIDEBAR / INPUT SETUP) ─────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Cow Selection & Input Setup")
    selected_preset = st.selectbox(
        "Load Demonstration Presets",
        list(PRESET_SCENARIOS.keys()),
        index=0
    )
    preset_data = PRESET_SCENARIOS[selected_preset]

    st.markdown("---")
    st.markdown("#### Cow Metadata")
    cow_id_val = st.text_input("Cow ID / Tag Number", value=preset_data.get("cow_id", "COW_001") if preset_data else "COW_001")

    # 1. Cow Profile
    with st.expander("👤 1. Cow Profile", expanded=True):
        breed_opts = ["Holstein_Friesian", "Gir", "Sahiwal"]
        b_idx = breed_opts.index(preset_data["Breed"]) if preset_data else 0
        breed = st.selectbox("Breed", breed_opts, index=b_idx)
        age = st.number_input("Age (Years)", 1.0, 20.0, preset_data.get("Age_Years", 5.5) if preset_data else 5.5, 0.5)
        lac = st.number_input("Lactation Number", 1, 10, preset_data.get("Lactation_Number", 4) if preset_data else 4)
        par = st.number_input("Parity", 1, 10, preset_data.get("Parity", 4) if preset_data else 4)
        dim = st.number_input("Days In Milk", 1, 400, preset_data.get("Days_In_Milk", 120) if preset_data else 120)

    # 2. Health History
    with st.expander("📋 2. Health History", expanded=False):
        prev = st.selectbox("Previous Mastitis History", [0, 1], format_func=lambda x: "Yes" if x else "No", index=preset_data.get("Previous_Mastitis_History", 1) if preset_data else 1)
        vacc = st.selectbox("Vaccination Status", [0, 1], format_func=lambda x: "Vaccinated" if x else "Not Vaccinated", index=preset_data.get("Vaccination_Status", 0) if preset_data else 0)

    # 3. Physiological & Behavioural
    with st.expander("🌡️ 3. Physiological & Behavioral", expanded=True):
        body_temp  = st.number_input("Body Temp (°C)", 35.0, 42.0, preset_data.get("Body_Temperature_C", 39.5) if preset_data else 39.5, 0.1)
        udder_temp = st.number_input("Udder Temp (°C)", 35.0, 42.0, preset_data.get("Udder_Temperature_C", 39.8) if preset_data else 39.8, 0.1)
        activity   = st.number_input("Activity Index", 0.0, 150.0, preset_data.get("Activity_Index", 45.0) if preset_data else 45.0, 1.0)
        rumination = st.number_input("Rumination Time (min)", 0.0, 700.0, preset_data.get("Rumination_Time_min", 350.0) if preset_data else 350.0, 10.0)
        feed       = st.number_input("Feed Intake (kgDM)", 0.0, 35.0, preset_data.get("Feed_Intake_kgDM", 14.5) if preset_data else 14.5, 0.5)
        water      = st.number_input("Water Intake (L)", 0.0, 160.0, preset_data.get("Water_Intake_L", 60.0) if preset_data else 60.0, 1.0)

    # 4. Environmental
    with st.expander("⛅ 4. Environmental Factors", expanded=False):
        amb_temp = st.number_input("Ambient Temp (°C)", -10.0, 50.0, preset_data.get("Ambient_Temperature_C", 28.0) if preset_data else 28.0, 0.5)
        humidity = st.number_input("Humidity (%)", 0.0, 100.0, preset_data.get("Humidity_pct", 70.0) if preset_data else 70.0, 1.0)
        thi      = st.number_input("THI Index", 0.0, 120.0, preset_data.get("THI", 78.5) if preset_data else 78.5, 0.5)

    # 5. Farm Management
    with st.expander("🧹 5. Farm Management", expanded=False):
        hygiene  = st.number_input("Hygiene Score (1-5)", 1, 5, preset_data.get("Hygiene_Score", 3) if preset_data else 3)
        bedding  = st.number_input("Bedding Cleanliness (1-5)", 1, 5, preset_data.get("Bedding_Cleanliness_Score", 3) if preset_data else 3)
        milkfreq = st.number_input("Milking Freq (/day)", 1, 5, preset_data.get("Milking_Frequency", 2) if preset_data else 2)

    st.markdown("<br>", unsafe_allow_html=True)
    analyze_btn = st.button("🔍  ANALYZE MASTITIS RISK", type="primary", use_container_width=True)

# Payload Construction
sensor_payload = {
    'cow_id': cow_id_val,
    'timestamp': "2026-08-28T14:30:00Z",
    'Breed': breed, 'Age_Years': age, 'Lactation_Number': lac, 'Parity': par, 'Days_In_Milk': dim,
    'Previous_Mastitis_History': prev, 'Vaccination_Status': vacc,
    'Body_Temperature_C': body_temp, 'Udder_Temperature_C': udder_temp,
    'Activity_Index': activity, 'Rumination_Time_min': rumination,
    'Feed_Intake_kgDM': feed, 'Water_Intake_L': water,
    'Ambient_Temperature_C': amb_temp, 'Humidity_pct': humidity, 'THI': thi,
    'Hygiene_Score': hygiene, 'Bedding_Cleanliness_Score': bedding, 'Milking_Frequency': milkfreq,
}


# ── MAIN LAYOUT (2 COLUMNS: ANALYSIS RESULT & SYSTEM INFO) ─────────────────
col_main, col_side = st.columns([7, 5], gap="large")

with col_main:
    st.markdown(f'<div class="section-head">🔎 Analysis Result for Cow: <code>{cow_id_val}</code></div>', unsafe_allow_html=True)

    # Execute Hardware-to-ML Prediction
    try:
        res = process_sensor_reading(sensor_payload)
        prob = res["mastitis_probability"]
        healthy_prob = res["healthy_probability"]
        risk_level = res["risk_level"]
        risk_label = res["risk_label"]
        factors = res["contributing_factors"]
        action = res["recommended_action"]

        prob_pct = prob * 100
        color_cls = "prob-low" if risk_level == "LOW" else ("prob-medium" if risk_level == "MEDIUM" else "prob-high")
        badge_cls = f"badge-{risk_level.lower()}"

        # SECTION 4 — AI RESULT CARD (VISUAL CENTERPIECE)
        st.markdown(f"""
        <div class="result-card">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap;">
                <div>
                    <div style="font-size: 0.85rem; font-weight: 700; color: #64748b; text-transform: uppercase; letter-spacing: 0.05em;">MASTITIS RISK PROBABILITY</div>
                    <div class="prob-large {color_cls}">{prob_pct:.1f}%</div>
                </div>
                <div style="text-align: right; margin-top: 0.5rem;">
                    <span class="{badge_cls}">{risk_level} RISK</span>
                    <div style="font-size: 0.82rem; font-weight: 600; color: #64748b; margin-top: 0.4rem;">{risk_label}</div>
                </div>
            </div>
            <hr style="margin: 1.2rem 0 0.8rem 0; border: 0; border-top: 1px solid #f1f5f9;">
            <div style="display: flex; gap: 2rem; font-size: 0.88rem; color: #475569;">
                <div><b>Mastitis Probability:</b> {prob_pct:.1f}%</div>
                <div><b>Healthy Probability:</b> {healthy_prob*100:.1f}%</div>
                <div><b>Category:</b> {risk_level}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # SECTION 5 — "WHY THIS PREDICTION?" (EXPLAINABILITY)
        st.markdown('<div class="section-head">❓ Why is this cow at risk?</div>', unsafe_allow_html=True)
        st.caption("⚠️ *Model-associated contributing factors (scaled value × coefficient) — not causal biological explanations.*")

        for f in factors[:5]:
            contrib_abs = abs(f['contribution'])
            # Create a simple visual bar using block characters
            bar_len = min(15, max(2, int(contrib_abs * 6)))
            bar_str = "█" * bar_len

            if f["direction"] == "increases_risk":
                st.markdown(f"""
                <div class="factor-card-risk">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-weight: 600; color: #991b1b;">▲ {f['label']}</span>
                        <span style="font-family: monospace; font-weight: 700; color: #dc2626;">+{f['contribution']:.4f}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 0.2rem; font-size: 0.78rem; color: #7f1d1d;">
                        <span style="letter-spacing: -1px; color: #ef4444;">{bar_str}</span>
                        <span>Increasing Risk</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="factor-card-protective">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-weight: 600; color: #166534;">▼ {f['label']}</span>
                        <span style="font-family: monospace; font-weight: 700; color: #16a34a;">{f['contribution']:.4f}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 0.2rem; font-size: 0.78rem; color: #14532d;">
                        <span style="letter-spacing: -1px; color: #22c55e;">{bar_str}</span>
                        <span>Decreasing Risk (Protective)</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # SECTION 7 — RECOMMENDED ACTION
        st.markdown('<div class="section-head">📋 Recommended Action</div>', unsafe_allow_html=True)
        act_class = f"action-banner-{risk_level.lower()}"
        icon = "✅" if risk_level == "LOW" else ("⚠️" if risk_level == "MEDIUM" else "🚨")
        
        st.markdown(f"""
        <div class="{act_class}">
            <div style="font-weight: 700; font-size: 1rem; margin-bottom: 0.2rem;">{icon} Decision Support Recommendation</div>
            <div style="font-size: 0.9rem; line-height: 1.4;">{action}</div>
        </div>
        """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Error evaluating prediction pipeline: {e}")


# ── RIGHT COLUMN: SENSOR DATA, CHARTS, METRICS & ARCHITECTURE ─────────────────
with col_side:
    # SECTION 6 — CURRENT SENSOR DATA READINGS
    st.markdown('<div class="section-head">📡 Current Sensor Data</div>', unsafe_allow_html=True)
    st.caption("Data Source: **Demo / Manual Input** *(Ready for IoT Hardware Stream)*")

    sd_col1, sd_col2 = st.columns(2)
    with sd_col1:
        st.metric("Body Temperature", f"{body_temp:.1f} °C")
        st.metric("Udder Temperature", f"{udder_temp:.1f} °C")
        st.metric("Activity Index", f"{activity:.0f}")
        st.metric("Rumination Time", f"{rumination:.0f} min")
    with sd_col2:
        st.metric("Feed Intake", f"{feed:.1f} kgDM")
        st.metric("Water Intake", f"{water:.1f} L")
        st.metric("Ambient Temp", f"{amb_temp:.1f} °C")
        st.metric("THI Index", f"{thi:.1f}")

    st.markdown("<br>", unsafe_allow_html=True)

    # SECTION 8 — RISK DISTRIBUTION CHART
    st.markdown('<div class="section-head">📈 Demonstration Herd Risk Distribution</div>', unsafe_allow_html=True)
    
    chart_df = pd.DataFrame({
        'Risk Category': ['LOW', 'MEDIUM', 'HIGH'],
        'Count': [85, 25, 10]
    }).set_index('Risk Category')
    
    st.bar_chart(chart_df, height=180)
    st.caption("⚠️ *Synthetic Demonstration Data Distribution — Not live farm statistics.*")

    st.markdown("<br>", unsafe_allow_html=True)

    # SECTION 9 — MODEL PERFORMANCE
    with st.expander("📊 Model Performance Metrics", expanded=False):
        st.markdown("""
        **Classifier:** Logistic Regression (`class_weight='balanced'`)  
        **Input Features:** 19 Non-Diagnostic Measurements  

        | Metric | Score | Note |
        |---|---|---|
        | **Accuracy** | 85.0% | Overall correct predictions |
        | **Precision** | 60.9% | Correct positive rate |
        | **Recall** | **82.4%** | **Primary metric (Sensitivity)** |
        | **F1 Score** | 70.0% | Harmonic mean |
        | **ROC-AUC** | **90.1%** | Discrimination ability |

        > **Why Recall is Prioritized:**  
        > *Recall is prioritized because missing a potentially high-risk cow is far more concerning than generating some additional screening alerts.*
        """)

    # SECTION 10 — SYSTEM ARCHITECTURE
    with st.expander("🏗️ Hardware-to-ML System Architecture", expanded=False):
        st.markdown("""
        <div class="flow-box">
┌───────────────────────────────────────────┐<br>
│ 1. Cow Sensors / Farm Data Input          │<br>
└─────────────────────┬─────────────────────┘<br>
                      │<br>
                      ▼<br>
┌───────────────────────────────────────────┐<br>
│ 2. JSON Sensor Payload / API              │<br>
└─────────────────────┬─────────────────────┘<br>
                      │<br>
                      ▼<br>
┌───────────────────────────────────────────┐<br>
│ 3. Input Validation                       │<br>
└─────────────────────┬─────────────────────┘<br>
                      │<br>
                      ▼<br>
┌───────────────────────────────────────────┐<br>
│ 4. Preprocessing Pipeline                 │<br>
│    (Imputation + Scaling + OneHot)        │<br>
└─────────────────────┬─────────────────────┘<br>
                      │<br>
                      ▼<br>
┌───────────────────────────────────────────┐<br>
│ 5. Strict Logistic Regression Model       │<br>
└─────────────────────┬─────────────────────┘<br>
                      │<br>
                      ▼<br>
┌───────────────────────────────────────────┐<br>
│ 6. Output Generation                      │<br>
│    • Mastitis Risk Probability %          │<br>
│    • Risk Level (LOW / MEDIUM / HIGH)     │<br>
│    • Explainability / Factors             │<br>
└─────────────────────┬─────────────────────┘<br>
                      │<br>
                      ▼<br>
┌───────────────────────────────────────────┐<br>
│ 7. Dashboard Alert / Action Recommendation│<br>
└───────────────────────────────────────────┘
        </div>
        """, unsafe_allow_html=True)


# ── SECTION 11 — DISCLAIMER & FOOTER ─────────────────────────────────────────
st.markdown("""
<div class="disclaimer-card">
    <b>Prototype Notice & Legal Disclaimer:</b><br>
    This system is an AI-based software prototype evaluated using synthetic/enriched data. 
    The current model estimates mastitis risk probability from the supplied input factors and does not constitute a veterinary diagnosis 
    or demonstrate validated 7–14 day clinical forecasting. Real-world deployment requires field validation using genuine farm and sensor data.
</div>
""", unsafe_allow_html=True)
