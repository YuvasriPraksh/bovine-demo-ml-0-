"""
streamlit_app.py
----------------
Pashu Sanjeevani AI — National Bovine Mastitis Early-Warning & Risk Surveillance Portal
Government of India · Ministry of Fisheries, Animal Husbandry & Dairying
"""

import sys
import os
import json
import time
import numpy as np
import pandas as pd
import streamlit as st

# Ensure src directory is in Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from hardware_interface import process_sensor_reading
from predict import predict_mastitis_risk, predict_mastitis_risk_batch

# ── 1. PAGE CONFIGURATION ─────────────────────────────────────────────────────
st.set_page_config(
    page_title="Pashu Sanjeevani AI — Mastitis Early-Warning Portal",
    page_icon="🐄",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── 2. STATE-OF-THE-ART GOVERNMENT AGRI-TECH UI/UX STYLING ─────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
    color: #1e293b;
    background-color: #f8fafc;
}

/* Global Container Width */
.main .block-container {
    padding-top: 0.8rem;
    padding-bottom: 2.5rem;
    max-width: 1280px;
}

/* Government Tricolor Top Accent Line */
.tricolor-stripe {
    height: 4px;
    width: 100%;
    background: linear-gradient(90deg, #ff9933 0%, #ff9933 33.3%, #ffffff 33.3%, #ffffff 66.6%, #128807 66.6%, #128807 100%);
    border-radius: 4px 4px 0 0;
}

/* Header Container */
.gov-header {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
    color: #ffffff;
    padding: 1.5rem 2rem;
    border-radius: 0 0 16px 16px;
    box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.25);
    margin-bottom: 1.8rem;
    position: relative;
    overflow: hidden;
}
.gov-header::after {
    content: '';
    position: absolute;
    top: -50%;
    right: -10%;
    width: 350px;
    height: 350px;
    background: radial-gradient(circle, rgba(56, 189, 248, 0.08) 0%, rgba(255, 255, 255, 0) 70%);
    pointer-events: none;
}
.gov-title {
    font-family: 'Outfit', sans-serif;
    font-size: 2.1rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    color: #ffffff;
    margin: 0;
    display: flex;
    align-items: center;
    gap: 0.75rem;
}
.gov-subtitle {
    font-size: 0.95rem;
    color: #94a3b8;
    margin-top: 0.25rem;
    font-weight: 400;
}

/* Status & Emblem Badges */
.status-pill-online {
    background: rgba(34, 197, 94, 0.15);
    color: #4ade80;
    border: 1px solid rgba(74, 222, 128, 0.3);
    padding: 4px 14px;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 600;
    display: inline-flex;
    align-items: center;
    gap: 7px;
}
.pulse-dot {
    width: 8px;
    height: 8px;
    background-color: #22c55e;
    border-radius: 50%;
    box-shadow: 0 0 0 0 rgba(34, 197, 94, 0.7);
    animation: pulse 1.6s infinite;
}
@keyframes pulse {
    0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(34, 197, 94, 0.7); }
    70% { transform: scale(1); box-shadow: 0 0 0 8px rgba(34, 197, 94, 0); }
    100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(34, 197, 94, 0); }
}

.gov-badge {
    background: rgba(255, 153, 51, 0.15);
    color: #ffb74d;
    border: 1px solid rgba(255, 153, 51, 0.3);
    padding: 4px 14px;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 600;
}

/* Glassmorphism Metric Cards */
.metric-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    padding: 1.25rem 1.4rem;
    text-align: center;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    transition: all 0.25s ease-in-out;
}
.metric-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 20px -5px rgba(0, 0, 0, 0.08);
}
.metric-val {
    font-family: 'Outfit', sans-serif;
    font-size: 2rem;
    font-weight: 700;
    line-height: 1.1;
}
.metric-lbl {
    font-size: 0.75rem;
    font-weight: 700;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-top: 0.4rem;
}

/* Main Risk Display Card */
.risk-card-container {
    background: #ffffff;
    border-radius: 18px;
    padding: 1.8rem 2.2rem;
    border: 1px solid #e2e8f0;
    box-shadow: 0 10px 30px -10px rgba(15, 23, 42, 0.08);
    margin-bottom: 1.5rem;
    transition: all 0.3s ease;
}
.risk-prob-text {
    font-family: 'Outfit', sans-serif;
    font-size: 4.5rem;
    font-weight: 800;
    line-height: 1;
    letter-spacing: -0.03em;
}
.risk-prob-low { color: #059669; }
.risk-prob-med { color: #d97706; }
.risk-prob-high { color: #dc2626; }

.badge-low {
    background: #d1fae5; color: #047857; font-weight: 700; padding: 6px 20px; border-radius: 30px; font-size: 0.95rem; display: inline-block;
}
.badge-med {
    background: #fef3c7; color: #b45309; font-weight: 700; padding: 6px 20px; border-radius: 30px; font-size: 0.95rem; display: inline-block;
}
.badge-high {
    background: #fee2e2; color: #b91c1c; font-weight: 700; padding: 6px 20px; border-radius: 30px; font-size: 0.95rem; display: inline-block;
}

/* Factor Contribution Bars */
.factor-box-risk {
    background: #fff1f2;
    border-left: 4px solid #f43f5e;
    border-radius: 8px;
    padding: 0.8rem 1rem;
    margin-bottom: 0.6rem;
    font-size: 0.9rem;
    transition: transform 0.2s ease;
}
.factor-box-risk:hover { transform: translateX(4px); }
.factor-box-protective {
    background: #ecfdf5;
    border-left: 4px solid #10b981;
    border-radius: 8px;
    padding: 0.8rem 1rem;
    margin-bottom: 0.6rem;
    font-size: 0.9rem;
    transition: transform 0.2s ease;
}
.factor-box-protective:hover { transform: translateX(4px); }

/* Section Headings */
.sec-title {
    font-family: 'Outfit', sans-serif;
    font-size: 1.25rem;
    font-weight: 700;
    color: #0f172a;
    margin-top: 1.2rem;
    margin-bottom: 0.9rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

/* Custom Streamlit Tab Styling */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background-color: #f1f5f9;
    padding: 6px;
    border-radius: 12px;
}
.stTabs [data-baseweb="tab"] {
    height: 44px;
    border-radius: 8px;
    font-family: 'Outfit', sans-serif;
    font-weight: 600;
    font-size: 0.92rem;
    color: #475569;
    padding: 0 18px;
}
.stTabs [aria-selected="true"] {
    background-color: #ffffff !important;
    color: #0f172a !important;
    box-shadow: 0 2px 6px rgba(0,0,0,0.06);
}
</style>
""", unsafe_allow_html=True)

# ── 3. PRESET SCENARIO DATA ───────────────────────────────────────────────────
PRESET_SCENARIOS = {
    "Custom Input (Manual Form Setup)": None,
    "Scenario A: COW_101 — Healthy Baseline (Low Risk)": {
        "cow_id": "COW_101_HEALTHY", "breed": "Holstein_Friesian", "age_years": 3.0,
        "previous_mastitis_history": 0, "vaccinated": 1, "chronic_disease_flag": 0,
        "body_temperature_c": 38.4, "udder_surface_temperature_c": 38.5,
        "activity_score": 82.0, "rumination_min_day": 510.0, "feed_intake_kg_day": 20.5,
        "water_intake_l_day": 92.0, "milk_yield_kg_day": 24.0, "milk_conductivity_mS_cm": 4.5,
        "ambient_temperature_c": 22.0, "relative_humidity_pct": 50.0,
        "environment_total_mastitis_pathogen_load_log10": 2.1,
        "S_aureus_load_log10_cfu_equiv": 1.5, "S_uberis_load_log10_cfu_equiv": 1.8,
        "E_coli_load_log10_cfu_equiv": 1.2, "K_pneumoniae_load_log10_cfu_equiv": 1.1,
        "S_agalactiae_load_log10_cfu_equiv": 1.0, "dominant_environment_pathogen": "S. uberis",
        "hygiene_score_0_100": 85.0
    },
    "Scenario B: COW_102 — Normal Indigenous Cow (Low Risk)": {
        "cow_id": "COW_102_LOW_RISK", "breed": "Gir", "age_years": 7.0,
        "previous_mastitis_history": 0, "vaccinated": 1, "chronic_disease_flag": 0,
        "body_temperature_c": 38.6, "udder_surface_temperature_c": 38.7,
        "activity_score": 70.0, "rumination_min_day": 470.0, "feed_intake_kg_day": 18.0,
        "water_intake_l_day": 84.0, "milk_yield_kg_day": 19.5, "milk_conductivity_mS_cm": 4.7,
        "ambient_temperature_c": 25.0, "relative_humidity_pct": 55.0,
        "environment_total_mastitis_pathogen_load_log10": 2.5,
        "S_aureus_load_log10_cfu_equiv": 2.0, "S_uberis_load_log10_cfu_equiv": 2.2,
        "E_coli_load_log10_cfu_equiv": 1.8, "K_pneumoniae_load_log10_cfu_equiv": 1.5,
        "S_agalactiae_load_log10_cfu_equiv": 1.2, "dominant_environment_pathogen": "S. uberis",
        "hygiene_score_0_100": 70.0
    },
    "Scenario C: COW_103 — Subclinical Warning (Medium Risk)": {
        "cow_id": "COW_103_MEDIUM_RISK", "breed": "Sahiwal", "age_years": 6.0,
        "previous_mastitis_history": 1, "vaccinated": 0, "chronic_disease_flag": 0,
        "body_temperature_c": 38.8, "udder_surface_temperature_c": 38.9,
        "activity_score": 58.0, "rumination_min_day": 420.0, "feed_intake_kg_day": 15.5,
        "water_intake_l_day": 70.0, "milk_yield_kg_day": 16.0, "milk_conductivity_mS_cm": 5.4,
        "ambient_temperature_c": 26.0, "relative_humidity_pct": 66.0,
        "environment_total_mastitis_pathogen_load_log10": 3.8,
        "S_aureus_load_log10_cfu_equiv": 3.2, "S_uberis_load_log10_cfu_equiv": 3.5,
        "E_coli_load_log10_cfu_equiv": 2.9, "K_pneumoniae_load_log10_cfu_equiv": 2.5,
        "S_agalactiae_load_log10_cfu_equiv": 2.2, "dominant_environment_pathogen": "S. aureus",
        "hygiene_score_0_100": 45.0
    },
    "Scenario D: COW_104 — High Environmental Pathogen Risk": {
        "cow_id": "COW_104_HIGH_RISK", "breed": "Holstein_Friesian", "age_years": 4.5,
        "previous_mastitis_history": 0, "vaccinated": 1, "chronic_disease_flag": 0,
        "body_temperature_c": 39.6, "udder_surface_temperature_c": 39.5,
        "activity_score": 48.0, "rumination_min_day": 380.0, "feed_intake_kg_day": 15.0,
        "water_intake_l_day": 65.0, "milk_yield_kg_day": 14.0, "milk_conductivity_mS_cm": 6.2,
        "ambient_temperature_c": 28.0, "relative_humidity_pct": 72.0,
        "environment_total_mastitis_pathogen_load_log10": 4.8,
        "S_aureus_load_log10_cfu_equiv": 4.5, "S_uberis_load_log10_cfu_equiv": 4.1,
        "E_coli_load_log10_cfu_equiv": 3.8, "K_pneumoniae_load_log10_cfu_equiv": 3.2,
        "S_agalactiae_load_log10_cfu_equiv": 3.0, "dominant_environment_pathogen": "S. aureus",
        "hygiene_score_0_100": 40.0
    },
    "Scenario E: COW_105 — Acute Udder Fever & High Conductivity": {
        "cow_id": "COW_105_ACUTE_RISK", "breed": "Holstein_Friesian", "age_years": 5.5,
        "previous_mastitis_history": 1, "vaccinated": 1, "chronic_disease_flag": 1,
        "body_temperature_c": 39.8, "udder_surface_temperature_c": 40.2,
        "activity_score": 40.0, "rumination_min_day": 310.0, "feed_intake_kg_day": 12.0,
        "water_intake_l_day": 55.0, "milk_yield_kg_day": 10.5, "milk_conductivity_mS_cm": 7.1,
        "ambient_temperature_c": 31.0, "relative_humidity_pct": 78.0,
        "environment_total_mastitis_pathogen_load_log10": 5.5,
        "S_aureus_load_log10_cfu_equiv": 5.2, "S_uberis_load_log10_cfu_equiv": 4.8,
        "E_coli_load_log10_cfu_equiv": 4.5, "K_pneumoniae_load_log10_cfu_equiv": 4.0,
        "S_agalactiae_load_log10_cfu_equiv": 3.8, "dominant_environment_pathogen": "E. coli",
        "hygiene_score_0_100": 30.0
    }
}

# ── 4. OFFICIAL GOVERNMENT HEADER ─────────────────────────────────────────────
st.markdown('<div class="tricolor-stripe"></div>', unsafe_allow_html=True)
st.markdown("""
<div class="gov-header">
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1.2rem;">
        <div>
            <div style="display: flex; align-items: center; gap: 0.6rem; margin-bottom: 0.3rem;">
                <span class="gov-badge">🇮🇳 PASHU SANJEEVANI AI PORTAL</span>
                <span style="color: #94a3b8; font-size: 0.8rem;">| DAHD National Early-Warning Grid</span>
            </div>
            <h1 class="gov-title">🐄 Rashtriya Bovine Mastitis Risk AI System</h1>
            <div class="gov-subtitle">Department of Animal Husbandry & Dairying · Ministry of Fisheries, Animal Husbandry & Dairying</div>
        </div>
        <div style="display: flex; gap: 0.8rem; align-items: center;">
            <span class="status-pill-online"><span class="pulse-dot"></span> AI Risk Grid Online</span>
            <span style="background: rgba(255,255,255,0.1); color: #cbd5e1; border: 1px solid rgba(255,255,255,0.2); padding: 4px 14px; border-radius: 20px; font-size: 0.8rem; font-weight: 500;">
                XGBoost 23-Factor Core
            </span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── 5. SIDEBAR CONTROL PANEL ──────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Pashu Selection & IoT Setup")
    selected_preset = st.selectbox(
        "Load Official Demonstration Presets",
        list(PRESET_SCENARIOS.keys()),
        index=0
    )
    preset_data = PRESET_SCENARIOS[selected_preset]

    st.markdown("---")
    st.markdown("#### Livestock Identification")
    cow_id_val = st.text_input("Pashu Tag Number / Cow ID", value=preset_data.get("cow_id", "COW_001") if preset_data else "COW_001")

    # 1. Profile & History
    with st.expander("👤 1. Breed Profile & Health History", expanded=True):
        breed_opts = ["Holstein_Friesian", "Gir", "Sahiwal"]
        b_idx = breed_opts.index(preset_data.get("breed", "Holstein_Friesian")) if preset_data else 0
        breed = st.selectbox("Livestock Breed", breed_opts, index=b_idx)
        age = st.number_input("Age (Years)", 1.0, 20.0, float(preset_data.get("age_years", 4.5)) if preset_data else 4.5, 0.5)
        prev = st.selectbox("Prior Mastitis History", [0, 1], format_func=lambda x: "Yes (1)" if x else "No (0)", index=int(preset_data.get("previous_mastitis_history", 0)) if preset_data else 0)
        vacc = st.selectbox("Vaccination Status", [0, 1], format_func=lambda x: "Vaccinated (1)" if x else "Not Vaccinated (0)", index=int(preset_data.get("vaccinated", 1)) if preset_data else 1)
        chronic = st.selectbox("Chronic Health Condition", [0, 1], format_func=lambda x: "Present (1)" if x else "None (0)", index=int(preset_data.get("chronic_disease_flag", 0)) if preset_data else 0)

    # 2. Vitals & Sensors
    with st.expander("🌡️ 2. Vitals & Pedometer Sensors", expanded=True):
        body_temp  = st.number_input("Body Temperature (°C)", 35.0, 42.0, float(preset_data.get("body_temperature_c", 38.6)) if preset_data else 38.6, 0.1)
        udder_temp = st.number_input("Udder Thermography (°C)", 35.0, 42.0, float(preset_data.get("udder_surface_temperature_c", 38.3)) if preset_data else 38.3, 0.1)
        activity   = st.number_input("Activity Index (Pedometer)", 0.0, 150.0, float(preset_data.get("activity_score", 65.0)) if preset_data else 65.0, 1.0)
        rumination = st.number_input("Rumination Time (min/day)", 0.0, 700.0, float(preset_data.get("rumination_min_day", 480.0)) if preset_data else 480.0, 10.0)
        feed       = st.number_input("Feed Intake (kgDM/day)", 0.0, 35.0, float(preset_data.get("feed_intake_kg_day", 18.0)) if preset_data else 18.0, 0.5)
        water      = st.number_input("Water Intake (L/day)", 0.0, 160.0, float(preset_data.get("water_intake_l_day", 85.0)) if preset_data else 85.0, 1.0)

    # 3. Milk Quality & Conductivity
    with st.expander("🥛 3. Inline Milk Sensor Quality", expanded=True):
        milk_yield = st.number_input("Milk Yield (kg/day)", 0.0, 60.0, float(preset_data.get("milk_yield_kg_day", 22.0)) if preset_data else 22.0, 0.5)
        milk_cond  = st.number_input("Electrical Conductivity (mS/cm)", 2.0, 12.0, float(preset_data.get("milk_conductivity_mS_cm", 4.8)) if preset_data else 4.8, 0.1)

    # 4. Pathogen Microbiology
    with st.expander("🦠 4. Microbial Pathogen Loads", expanded=False):
        pathogen_opts = ["S. uberis", "S. aureus", "E. coli", "K. pneumoniae", "S. agalactiae"]
        dom_idx = pathogen_opts.index(preset_data.get("dominant_environment_pathogen", "S. uberis")) if preset_data and preset_data.get("dominant_environment_pathogen") in pathogen_opts else 0
        dom_pathogen = st.selectbox("Dominant Pathogen Type", pathogen_opts, index=dom_idx)
        total_path = st.number_input("Total Env Pathogen Load (log10)", 0.0, 10.0, float(preset_data.get("environment_total_mastitis_pathogen_load_log10", 3.5)) if preset_data else 3.5, 0.1)
        s_aureus   = st.number_input("S. aureus Load (log10 CFU)", 0.0, 10.0, float(preset_data.get("S_aureus_load_log10_cfu_equiv", 2.5)) if preset_data else 2.5, 0.1)
        s_uberis   = st.number_input("S. uberis Load (log10 CFU)", 0.0, 10.0, float(preset_data.get("S_uberis_load_log10_cfu_equiv", 2.8)) if preset_data else 2.8, 0.1)
        e_coli     = st.number_input("E. coli Load (log10 CFU)", 0.0, 10.0, float(preset_data.get("E_coli_load_log10_cfu_equiv", 2.2)) if preset_data else 2.2, 0.1)
        k_pneum    = st.number_input("K. pneumoniae Load (log10 CFU)", 0.0, 10.0, float(preset_data.get("K_pneumoniae_load_log10_cfu_equiv", 2.1)) if preset_data else 2.1, 0.1)
        s_agal     = st.number_input("S. agalactiae Load (log10 CFU)", 0.0, 10.0, float(preset_data.get("S_agalactiae_load_log10_cfu_equiv", 2.0)) if preset_data else 2.0, 0.1)

    # 5. Environment & Hygiene
    with st.expander("⛅ 5. Barn Environment & Hygiene", expanded=False):
        amb_temp = st.number_input("Ambient Temp (°C)", -10.0, 50.0, float(preset_data.get("ambient_temperature_c", 28.0)) if preset_data else 28.0, 0.5)
        humidity = st.number_input("Relative Humidity (%)", 0.0, 100.0, float(preset_data.get("relative_humidity_pct", 65.0)) if preset_data else 65.0, 1.0)
        hygiene  = st.number_input("Farm Hygiene Index (0-100)", 0.0, 100.0, float(preset_data.get("hygiene_score_0_100", 60.0)) if preset_data else 60.0, 5.0)

    st.markdown("<br>", unsafe_allow_html=True)
    analyze_btn = st.button("🔍  RUN AI DIAGNOSTIC EVALUATION", type="primary", use_container_width=True)

# Sensor Payload Construction
sensor_payload = {
    'cow_id': cow_id_val,
    'timestamp': time.strftime("%Y-%m-%dT%H:%M:%SZ"),
    'breed': breed, 'age_years': age,
    'previous_mastitis_history': prev, 'vaccinated': vacc, 'chronic_disease_flag': chronic,
    'body_temperature_c': body_temp, 'udder_surface_temperature_c': udder_temp,
    'activity_score': activity, 'rumination_min_day': rumination,
    'feed_intake_kg_day': feed, 'water_intake_l_day': water,
    'milk_yield_kg_day': milk_yield, 'milk_conductivity_mS_cm': milk_cond,
    'ambient_temperature_c': amb_temp, 'relative_humidity_pct': humidity,
    'environment_total_mastitis_pathogen_load_log10': total_path,
    'S_aureus_load_log10_cfu_equiv': s_aureus, 'S_uberis_load_log10_cfu_equiv': s_uberis,
    'E_coli_load_log10_cfu_equiv': e_coli, 'K_pneumoniae_load_log10_cfu_equiv': k_pneum,
    'S_agalactiae_load_log10_cfu_equiv': s_agal, 'dominant_environment_pathogen': dom_pathogen,
    'hygiene_score_0_100': hygiene
}


# ── 6. MAIN PORTAL NAVIGATION TABS ───────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Pashu Diagnostic Center",
    "🐄 Herd Risk Radar & Surveillance",
    "🦠 Pathogen & Milk Biomarkers",
    "📡 IoT Edge Gateway Console",
    "📋 Farmer Guidelines & Veterinary Protocol"
])

# Process AI Inference Result
try:
    res = process_sensor_reading(sensor_payload)
    prob = res["mastitis_probability"]
    healthy_prob = res["healthy_probability"]
    risk_level = res["risk_level"]
    risk_label = res["risk_label"]
    factors = res.get("contributing_factors", [])
    action = res.get("recommended_action", "")

    prob_pct = prob * 100
    prob_cls = "risk-prob-low" if risk_level == "LOW" else ("risk-prob-med" if risk_level == "MEDIUM" else "risk-prob-high")
    badge_cls = f"badge-{risk_level.lower()[:4]}"
except Exception as e:
    st.error(f"Inference error: {e}")
    res = {}
    prob_pct = 0.0
    risk_level = "ERROR"
    badge_cls = "badge-high"
    prob_cls = "risk-prob-high"
    factors = []
    action = "Check input schema."


# ── TAB 1: PASHU DIAGNOSTIC CENTER ───────────────────────────────────────────
with tab1:
    col_diag_main, col_diag_side = st.columns([7, 5], gap="large")

    with col_diag_main:
        st.markdown(f'<div class="sec-title">🔎 Pashu Diagnostic Evaluation for: <code>{cow_id_val}</code></div>', unsafe_allow_html=True)

        # AI Diagnostic Result Glassmorphic Card
        st.markdown(f"""
        <div class="risk-card-container">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap;">
                <div>
                    <div style="font-size: 0.8rem; font-weight: 700; color: #64748b; text-transform: uppercase; letter-spacing: 0.05em;">ESTIMATED MASTITIS RISK PROBABILITY</div>
                    <div class="risk-prob-text {prob_cls}">{prob_pct:.1f}%</div>
                </div>
                <div style="text-align: right; margin-top: 0.5rem;">
                    <span class="{badge_cls}">{risk_level} RISK STATUS</span>
                    <div style="font-size: 0.85rem; font-weight: 600; color: #475569; margin-top: 0.4rem;">{risk_label}</div>
                </div>
            </div>
            <div style="margin-top: 1.2rem; background: #e2e8f0; height: 10px; border-radius: 5px; overflow: hidden;">
                <div style="background: {'#059669' if risk_level=='LOW' else ('#d97706' if risk_level=='MEDIUM' else '#dc2626')}; width: {prob_pct}%; height: 100%; border-radius: 5px; transition: width 0.8s ease;"></div>
            </div>
            <hr style="margin: 1.2rem 0 0.8rem 0; border: 0; border-top: 1px solid #f1f5f9;">
            <div style="display: flex; justify-content: space-between; font-size: 0.88rem; color: #475569; flex-wrap: wrap; gap: 1rem;">
                <div><b>Healthy Probability:</b> {healthy_prob*100:.1f}%</div>
                <div><b>Risk Category:</b> {risk_level}</div>
                <div><b>Evaluation Method:</b> 23-Factor XGBoost Model</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Explainability Section ("Why is this cow at risk?")
        st.markdown('<div class="sec-title">🧠 AI Explainability: Key Risk Drivers</div>', unsafe_allow_html=True)
        st.caption("Model-associated factor contributions based on feature values and trained XGBoost weights.")

        if factors:
            for f in factors[:5]:
                box_cls = "factor-box-risk" if f['direction'] == 'risk' else "factor-box-protective"
                icon = "🔺 INCREASES RISK" if f['direction'] == 'risk' else "🛡️ PROTECTIVE FACTOR"
                st.markdown(f"""
                <div class="{box_cls}">
                    <div style="display: flex; justify-content: space-between; font-weight: 600; color: #0f172a;">
                        <span>{f['label']}</span>
                        <span style="font-size: 0.8rem; opacity: 0.8;">{icon}</span>
                    </div>
                    <div style="font-size: 0.82rem; color: #475569; margin-top: 0.2rem;">
                        Impact Score: <b>{f['contribution']:+.4f}</b>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        # Veterinary Protocol Banner
        st.markdown('<div class="sec-title">🩺 Recommended Action Protocol</div>', unsafe_allow_html=True)
        banner_bg = "#f0fdf4" if risk_level == "LOW" else ("#fefce8" if risk_level == "MEDIUM" else "#fff1f2")
        banner_border = "#bbf7d0" if risk_level == "LOW" else ("#fef08a" if risk_level == "MEDIUM" else "#fecdd3")
        banner_text = "#166534" if risk_level == "LOW" else ("#854d0e" if risk_level == "MEDIUM" else "#9f1239")

        st.markdown(f"""
        <div style="background: {banner_bg}; border: 1px solid {banner_border}; color: {banner_text}; border-radius: 14px; padding: 1.2rem 1.4rem;">
            <div style="font-weight: 700; font-size: 1rem; margin-bottom: 0.3rem;">OPERATIONAL ADVISORY ({risk_level} RISK):</div>
            <div style="font-size: 0.9rem; line-height: 1.5;">{action}</div>
        </div>
        """, unsafe_allow_html=True)

    with col_diag_side:
        st.markdown('<div class="sec-title">📡 Real-Time Vitals Grid</div>', unsafe_allow_html=True)

        mcol1, mcol2 = st.columns(2)
        with mcol1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-val" style="color: {'#dc2626' if body_temp>39.2 else '#0f172a'};">{body_temp:.1f} °C</div>
                <div class="metric-lbl">Body Temp</div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-val" style="color: {'#dc2626' if udder_temp>39.5 else '#0f172a'};">{udder_temp:.1f} °C</div>
                <div class="metric-lbl">Udder Temp</div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-val" style="color: {'#d97706' if activity<50 else '#0f172a'};">{activity:.0f}</div>
                <div class="metric-lbl">Activity Index</div>
            </div>
            """, unsafe_allow_html=True)
        with mcol2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-val" style="color: {'#dc2626' if milk_cond>5.5 else '#0f172a'};">{milk_cond:.1f}</div>
                <div class="metric-lbl">Conductivity (mS/cm)</div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-val" style="color: #0f172a;">{milk_yield:.1f} kg</div>
                <div class="metric-lbl">Daily Milk Yield</div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-val" style="color: {'#d97706' if rumination<400 else '#0f172a'};">{rumination:.0f} min</div>
                <div class="metric-lbl">Rumination Time</div>
            </div>
            """, unsafe_allow_html=True)


# ── TAB 2: HERD SURVEILLANCE & REGIONAL RADAR ────────────────────────────────
with tab2:
    st.markdown('<div class="sec-title">🐄 National Dairy Herd Surveillance Radar</div>', unsafe_allow_html=True)
    st.caption("Live aggregate health indicators across monitored demonstration dairy units.")

    hcol1, hcol2, hcol3, hcol4 = st.columns(4)
    with hcol1:
        st.markdown('<div class="metric-card"><div class="metric-val">120</div><div class="metric-lbl">TOTAL MONITORED HERD</div></div>', unsafe_allow_html=True)
    with hcol2:
        st.markdown('<div class="metric-card" style="border-top:3px solid #059669;"><div class="metric-val" style="color:#059669;">85</div><div class="metric-lbl">LOW RISK COWS</div></div>', unsafe_allow_html=True)
    with hcol3:
        st.markdown('<div class="metric-card" style="border-top:3px solid #d97706;"><div class="metric-val" style="color:#d97706;">25</div><div class="metric-lbl">MEDIUM RISK COWS</div></div>', unsafe_allow_html=True)
    with hcol4:
        st.markdown('<div class="metric-card" style="border-top:3px solid #dc2626;"><div class="metric-val" style="color:#dc2626;">10</div><div class="metric-lbl">HIGH RISK COWS</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    rcol1, rcol2 = st.columns([6, 6])
    with rcol1:
        st.markdown("#### Herd Risk Distribution Breakdown")
        dist_df = pd.DataFrame({
            "Risk Category": ["LOW", "MEDIUM", "HIGH"],
            "Cows": [85, 25, 10]
        }).set_index("Risk Category")
        st.bar_chart(dist_df, height=220)
    with rcol2:
        st.markdown("#### Regional Environmental THI Monitoring")
        env_df = pd.DataFrame({
            "Region": ["North Zone", "West Zone", "Central Zone", "South Zone"],
            "Ambient Temp (°C)": [28.5, 31.0, 29.2, 27.8],
            "Humidity (%)": [65, 78, 70, 62]
        }).set_index("Region")
        st.line_chart(env_df, height=220)


# ── TAB 3: PATHOGEN & MILK BIOMARKERS ─────────────────────────────────────────
with tab3:
    st.markdown('<div class="sec-title">🦠 Microbial Pathogen Burden & Milk Conductance Biomarkers</div>', unsafe_allow_html=True)
    st.caption("Quantitative pathogen CFU equivalent concentrations and milk electrical conductivity thresholds.")

    pcol1, pcol2 = st.columns([6, 6])
    with pcol1:
        st.markdown("#### Pathogen Load Profile (log10 CFU equiv)")
        path_df = pd.DataFrame({
            "Pathogen Strain": ["S. aureus", "S. uberis", "E. coli", "K. pneumoniae", "S. agalactiae"],
            "Load (log10 CFU)": [s_aureus, s_uberis, e_coli, k_pneum, s_agal]
        }).set_index("Pathogen Strain")
        st.bar_chart(path_df, height=240)
    with pcol2:
        st.markdown("#### Dominant Pathogen Analysis")
        st.info(f"**Primary Dominant Strain:** `{dom_pathogen}`")
        st.write(f"- **Total Environmental Pathogen Pressure:** `{total_path:.1f} log10 CFU`")
        st.write(f"- **Milk Electrical Conductivity:** `{milk_cond:.1f} mS/cm` (Normal range: 4.0 – 5.0 mS/cm)")
        if milk_cond > 5.5:
            st.error("⚠️ Elevated milk electrical conductivity detected — indicates ion flux due to udder tissue inflammation.")
        else:
            st.success("✅ Milk electrical conductivity within normal physiological range.")


# ── TAB 4: IOT EDGE GATEWAY CONSOLE ───────────────────────────────────────────
with tab4:
    st.markdown('<div class="sec-title">📡 IoT Edge Hardware Gateway Interface</div>', unsafe_allow_html=True)
    st.caption("Developer payload inspector for MQTT / Serial / HTTP REST hardware nodes.")

    st.code(json.dumps(sensor_payload, indent=2), language="json")

    st.markdown("#### Direct API Invocation Code Snippet")
    st.code(f"""
import requests

hardware_payload = {json.dumps(sensor_payload, indent=2)}

# Send POST request to Pashu Sanjeevani AI API Gateway
response = requests.post("http://api.pashusanjeevani.gov.in/v1/predict", json=hardware_payload)
print(response.json())
""", language="python")


# ── TAB 5: FARMER GUIDELINES & PROTOCOL ───────────────────────────────────────
with tab5:
    st.markdown('<div class="sec-title">📋 Government Advisory Guidelines (SOP) for Farmers & Vets</div>', unsafe_allow_html=True)

    gcol1, gcol2 = st.columns(2)
    with gcol1:
        st.markdown("""
        ### 🐄 Preventive Biosecurity SOP
        1. **Teat Dip Sanitation:** Apply post-milking teat dip (0.5% Iodine or Chlorhexidine) within 15 seconds after milking.
        2. **Bedding Management:** Maintain dry, clean bedding (change sand/straw twice daily) to minimize *S. uberis* pathogen load.
        3. **Milking Order:** Always milk healthy cows first, older/history cows second, and mastitis-suspected cows last.
        """)
    with gcol2:
        st.markdown("""
        ### 📞 Emergency Support & Helplines
        - **National Pashu Sanjeevani Helpline:** `1800-180-1551` (Toll Free)
        - **DAHD Veterinary Emergency Support:** Contact Local Block Veterinary Officer (BVO).
        - **Mobile Veterinary Unit (MVU):** Available 24x7 via Pashu Sanjeevani App.
        """)

st.markdown("<br><hr>", unsafe_allow_html=True)
st.caption("🇮🇳 *Pashu Sanjeevani AI — Official Early-Warning System Prototype · Department of Animal Husbandry & Dairying, Ministry of Fisheries, Animal Husbandry & Dairying, Govt. of India.*")
