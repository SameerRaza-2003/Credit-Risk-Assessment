import streamlit as st
import pandas as pd

from models.feature_engineering import build_model_input
from models.logistic_pd import score_pd
from utils.validators import validate_inputs
from models.altman_z import compute_altman_z
from components.navbar import render_navbar

# -------------------------------------------------
# NAVBAR
# -------------------------------------------------
render_navbar(active_page="results")

# -------------------------------------------------
# AUTH GUARD
# -------------------------------------------------
if not st.session_state.get("authenticated", False):
    st.switch_page("pages/1_login.py")

st.title("📊 Risk Assessment Results")

# -------------------------------------------------
# DETECT MODE (SINGLE vs BULK)
# -------------------------------------------------
bulk_mode = "bulk_scored_df" in st.session_state

if bulk_mode:
    scored_df = st.session_state["bulk_scored_df"]

    st.subheader("📂 Bulk Results Navigation")

    selected_idx = st.selectbox(
        "Select Borrower (Row Index)",
        scored_df["Row_Index"],
        index=list(scored_df["Row_Index"]).index(
            st.session_state.get(
                "bulk_row_index",
                scored_df["Row_Index"].iloc[0]
            )
        )
    )

    # Persist selection
    st.session_state["bulk_row_index"] = selected_idx

    row = scored_df[scored_df["Row_Index"] == selected_idx].iloc[0]

    raw = {
        k: row[k]
        for k in scored_df.columns
        if k not in ["PD", "E_log", "Altman_Z", "Row_Index"]
    }

    st.info(f"📌 Viewing Bulk CSV — Row Index: {selected_idx}")

else:
    if "financials" not in st.session_state:
        st.switch_page("pages/3_input_step2.py")

    raw = st.session_state["financials"]

# -------------------------------------------------
# VALIDATION WARNINGS (OPTIONAL UX)
# -------------------------------------------------
warnings = validate_inputs(raw)
if warnings:
    with st.expander("⚠️ Input Validation Warnings"):
        for w in warnings:
            st.write(f"• {w}")

# -------------------------------------------------
# FEATURE ENGINEERING
# -------------------------------------------------
model_input = build_model_input(raw)

# -------------------------------------------------
# MODEL SCORING
# -------------------------------------------------
pd_val, elog = score_pd(model_input)
z_score = compute_altman_z(raw)

# -------------------------------------------------
# VIEW TOGGLE
# -------------------------------------------------
st.divider()
view = st.radio(
    "Select Risk Assessment Method",
    ["Logistic Regression (PD)", "Altman Z-Score"],
    horizontal=True
)

# =================================================
# LOGISTIC REGRESSION VIEW
# =================================================
if view == "Logistic Regression (PD)":

    st.subheader("📈 Logistic Regression – Probability of Default")

    col1, col2 = st.columns(2)
    col1.metric("Probability of Default (PD)", f"{pd_val:.2%}")
    col2.metric("E-log (Score)", round(elog, 3))

    # PD Banding
    def pd_band(pd):
        if pd < 0.10:
            return "A"
        elif pd < 0.20:
            return "B"
        elif pd < 0.30:
            return "C1"
        elif pd < 0.40:
            return "C2"
        elif pd < 0.50:
            return "C3"
        elif pd < 0.70:
            return "D"
        else:
            return "E"

    band = pd_band(pd_val)

    risk_map = {
        "A": "Very Low Risk",
        "B": "Low Risk",
        "C1": "Moderate Risk",
        "C2": "Elevated Risk",
        "C3": "High Risk",
        "D": "Very High Risk",
        "E": "Severe Risk"
    }

    st.success(f"**PD Band:** {band}  →  **{risk_map[band]}**")

    st.divider()
    st.subheader("📋 PD Band Reference")

    pd_table = pd.DataFrame({
        "PD Band": ["A", "B", "C1", "C2", "C3", "D", "E"],
        "PD Range": ["<10%", "10–20%", "20–30%", "30–40%", "40–50%", "50–70%", ">70%"],
        "Risk Meaning": [
            "Very Low Risk",
            "Low Risk",
            "Moderate Risk",
            "Elevated Risk",
            "High Risk",
            "Very High Risk",
            "Severe Risk"
        ]
    })

    st.table(pd_table)

# =================================================
# ALTMAN Z-SCORE VIEW
# =================================================
else:
    st.subheader("🏦 Altman Z-Score – Financial Distress Indicator")

    st.metric("Altman Z-Score", round(z_score, 2))

    if z_score < 3:
        z_label = "Severe Financial Distress"
        z_icon = "❌"
    elif z_score < 6:
        z_label = "High Risk"
        z_icon = "⚠️"
    elif z_score < 10:
        z_label = "Moderate Risk"
        z_icon = "🟡"
    else:
        z_label = "Low Risk / Financially Stable"
        z_icon = "✅"

    st.info(f"{z_icon} **Z-Score Interpretation:** {z_label}")

    st.divider()
    st.subheader("📋 Altman Z-Score Reference")

    z_table = pd.DataFrame({
        "Z-Score Range": ["< 3", "3 – 6", "6 – 10", "≥ 10"],
        "Financial Meaning": [
            "Severe Financial Distress",
            "High Risk",
            "Moderate Risk",
            "Low Risk / Financially Stable"
        ]
    })

    st.table(z_table)

# -------------------------------------------------
# LOGOUT
# -------------------------------------------------
if st.sidebar.button("Logout"):
    st.session_state.clear()
    st.switch_page("pages/1_login.py")
