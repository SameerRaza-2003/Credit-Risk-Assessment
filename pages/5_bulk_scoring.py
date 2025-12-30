import streamlit as st
import pandas as pd

from models.feature_engineering import build_model_input
from models.logistic_pd import score_pd
from models.altman_z import compute_altman_z

# -------------------------------------------------
# Guards
# -------------------------------------------------
if not st.session_state.get("authenticated", False):
    st.switch_page("pages/1_login.py")

st.title("📂 Bulk PD Scoring")
st.caption("Upload a CSV and drill down into individual risk reports")

uploaded = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded:
    df = pd.read_csv(uploaded)

    results = []

    for idx, row in df.iterrows():
        raw = row.to_dict()
        model_input = build_model_input(raw)

        pd_val, elog = score_pd(model_input)
        z_score = compute_altman_z(raw)

        results.append({
            "Row_ID": idx,
            **raw,
            "PD": pd_val,
            "E_log": elog,
            "Altman_Z": z_score
        })

    scored_df = pd.DataFrame(results)

    st.success("✅ Bulk scoring completed")

    # -----------------------------
    # Summary table
    # -----------------------------
    display_cols = [
        "Row_ID",
        "Business Type",
        "Industry/Sector",
        "Loan Amount",
        "PD",
        "Altman_Z"
    ]

    st.subheader("📊 Scoring Summary")
    st.dataframe(scored_df[display_cols])

    # -----------------------------
    # Row selector
    # -----------------------------
    st.divider()
    st.subheader("🔍 View Detailed Risk Report")

    selected_row = st.selectbox(
        "Select a borrower (by Row ID)",
        scored_df["Row_ID"]
    )

    if st.button("📄 Open Detailed Results"):
        selected_data = scored_df.loc[
            scored_df["Row_ID"] == selected_row
        ].iloc[0].to_dict()

        # Store selected borrower as if it was single input
        st.session_state["financials"] = {
            k: selected_data[k]
            for k in df.columns  # ONLY raw inputs
        }

        st.switch_page("pages/4_results.py")

    # -----------------------------
    # Download full scored file
    # -----------------------------
    st.divider()
    st.download_button(
        "⬇️ Download Full Scored File",
        scored_df.to_csv(index=False),
        "pd_bulk_scored.csv",
        "text/csv"
    )
