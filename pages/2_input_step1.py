import streamlit as st
import pandas as pd

from models.feature_engineering import build_model_input
from models.logistic_pd import score_pd
from models.altman_z import compute_altman_z
from components.navbar import render_navbar

# -------------------------------------------------
# NAVBAR
# -------------------------------------------------
render_navbar(active_page="input")

# -------------------------------------------------
# AUTH GUARD
# -------------------------------------------------
if not st.session_state.get("authenticated", False):
    st.switch_page("pages/1_login.py")

st.title("📋 Borrower & Loan Information")
st.caption("Choose single borrower entry or bulk CSV upload")

# -------------------------------------------------
# MODE SELECTION
# -------------------------------------------------
mode = st.radio(
    "Select Input Mode",
    ["Single Borrower", "Bulk CSV Upload"],
    horizontal=True
)

# =================================================
# SINGLE BORROWER MODE
# =================================================
if mode == "Single Borrower":

    with st.form("single_borrower_form"):
        st.subheader("🏢 Borrower Profile")

        col1, col2 = st.columns(2)

        with col1:
            business_type = st.selectbox(
                "Business Type",
                [
                    "SMALL ENTERPRISES",
                    "MEDIUM ENTERPRISES",
                    "PROPRIETORSHIP",
                    "PARTNERSHIP",
                    "PRIVATE LIMITED",
                    "INDIVIDUAL"
                ]
            )

            industry = st.text_input(
                "Industry / Sector",
                placeholder="e.g. Manufacturing, Trading, Services"
            )

        with col2:
            business_age = st.number_input(
                "Business Age (Years)",
                min_value=0,
                step=1
            )

            bank = st.selectbox(
                "Bank",
                ["Allied Bank", "HBL", "NBP", "BOP", "ALHabib"]
            )

        st.divider()
        st.subheader("💳 Loan Details")

        col3, col4 = st.columns(2)

        with col3:
            loan_amount = st.number_input(
                "Loan Amount",
                min_value=0.0,
                step=100000.0
            )

            tenure = st.number_input(
                "Tenure (Months)",
                min_value=1,
                step=1
            )

        with col4:
            repayment_frequency = st.selectbox(
                "Repayment Frequency",
                ["Monthly", "Quarterly", "Annually"]
            )

            interest_rate = st.number_input(
                "Interest Rate (%)",
                min_value=0.0,
                step=0.1
            )

        submitted = st.form_submit_button("Next ➡️ Financial Information")

    if submitted:
        st.session_state["financials"] = {
            "Business Type": business_type,
            "Industry/Sector": industry,
            "Business Age (Years)": business_age,
            "Bank": bank,
            "Loan Amount": loan_amount,
            "Tenure (Months)": tenure,
            "Repayment Frequency": repayment_frequency,
            "Interest Rate": interest_rate
        }
        st.switch_page("pages/3_input_step2.py")

# =================================================
# BULK CSV MODE (PRODUCTION-SAFE)
# =================================================
else:
    st.subheader("📂 Bulk Borrower Upload")

    uploaded = st.file_uploader(
        "Upload CSV file",
        type=["csv"],
        help="Upload borrower-level CSV"
    )

    # ----------------------------------------------
    # PROCESS FILE ONLY ONCE
    # ----------------------------------------------
    if uploaded and "bulk_scored_df" not in st.session_state:
        df = pd.read_csv(uploaded)

        results = []

        with st.spinner("Scoring borrowers..."):
            for idx, row in df.iterrows():
                raw = row.to_dict()

                model_input = build_model_input(raw)
                pd_val, elog = score_pd(model_input)
                z_score = compute_altman_z(raw)

                results.append({
                    "Row_Index": idx,
                    **raw,
                    "PD": pd_val,
                    "E_log": elog,
                    "Altman_Z": z_score
                })

        st.session_state["bulk_scored_df"] = pd.DataFrame(results)
        st.success("✅ Bulk scoring completed")

    # ----------------------------------------------
    # DISPLAY BULK RESULTS (FROM SESSION)
    # ----------------------------------------------
    if "bulk_scored_df" in st.session_state:
        scored_df = st.session_state["bulk_scored_df"]

        st.subheader("📊 Bulk Scoring Summary")
        st.dataframe(
            scored_df[["Row_Index", "Business Type", "Loan Amount", "PD", "Altman_Z"]],
            width="stretch"
        )

        st.divider()
        st.subheader("🔍 View Individual Risk Report")

        selected_idx = st.selectbox(
            "Select Borrower (Row Index)",
            scored_df["Row_Index"],
            index=0
        )

        if st.button("📄 Open Detailed Results"):
            row = scored_df[scored_df["Row_Index"] == selected_idx].iloc[0]

            st.session_state["financials"] = {
                k: row[k]
                for k in scored_df.columns
                if k not in ["PD", "E_log", "Altman_Z", "Row_Index"]
            }

            st.session_state["bulk_row_index"] = selected_idx
            st.switch_page("pages/4_results.py")

        st.divider()
        st.download_button(
            "⬇️ Download Full Scored File",
            scored_df.to_csv(index=False),
            "pd_bulk_scored.csv",
            "text/csv"
        )
