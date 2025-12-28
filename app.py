import streamlit as st
import pandas as pd
import numpy as np
import joblib
import json
import warnings

# ============================================================
# SUPPRESS KNOWN SAFE WARNINGS
# ============================================================
warnings.filterwarnings(
    "ignore",
    message="Found unknown categories"
)

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Probability of Default Dashboard",
    page_icon="📊",
    layout="centered"
)

# ============================================================
# LOAD CATEGORY METADATA
# ============================================================
@st.cache_resource
def load_category_metadata():
    with open("categorical_metadata.json", "r") as f:
        return json.load(f)

cat_meta = load_category_metadata()

# ============================================================
# LOAD CALIBRATED MODEL
# ============================================================
@st.cache_resource
def load_model():
    return joblib.load("pd_logistic_model_calibrated.joblib")

model = load_model()

# ============================================================
# HEADER
# ============================================================
st.markdown(
    """
    <h1 style="text-align:center;">📊 Probability of Default (PD)</h1>
    <p style="text-align:center; color: gray;">
    Bank-grade, calibrated, interpretable credit risk scoring
    </p>
    """,
    unsafe_allow_html=True
)

st.divider()

# ============================================================
# BULK CSV PREDICTION
# ============================================================
st.subheader("📂 Bulk PD Prediction (CSV Upload)")

uploaded_file = st.file_uploader(
    "Upload CSV file with borrower data",
    type=["csv"]
)

REQUIRED_COLS = [
    "Business Age (Years)",
    "Total Assets",
    "Total Liabilities",
    "Sales/Revenue",
    "Net Income",
    "EBIT",
    "Interest Expense",
    "Loan Amount",
    "Installment Amount",
    "Number of Previous Loans",
    "Tenure (Months)",
    "Interest Rate",
    "Industry/Sector",
    "Loan Type",
    "Repayment Frequency",
    "Business Type",
    "Collateral Type & Value"
]

if uploaded_file is not None:
    bulk_df = pd.read_csv(uploaded_file)

    missing = set(REQUIRED_COLS) - set(bulk_df.columns)
    if missing:
        st.error(f"❌ Missing required columns: {missing}")
    else:
        # Feature engineering
        bulk_df["debt_to_assets"] = bulk_df["Total Liabilities"] / bulk_df["Total Assets"]
        bulk_df["interest_coverage"] = bulk_df["EBIT"] / (bulk_df["Interest Expense"] + 1e-6)
        bulk_df["profit_margin"] = bulk_df["Net Income"] / bulk_df["Sales/Revenue"]
        bulk_df["wc_ratio"] = (
            bulk_df["Total Assets"] - bulk_df["Total Liabilities"]
        ) / bulk_df["Total Assets"]

        bulk_df.replace([np.inf, -np.inf], 0, inplace=True)
        bulk_df.fillna(0, inplace=True)

        # Predict + CAP PD (bank-standard)
        raw_pd = model.predict_proba(bulk_df)[:, 1]
        bulk_df["PD"] = np.clip(raw_pd, 0.05, 0.95)
        bulk_df["PD (%)"] = (bulk_df["PD"] * 100).round(2)

        def risk_band(pd):
            if pd < 0.20:
                return "Low"
            elif pd < 0.50:
                return "Medium"
            else:
                return "High"

        bulk_df["Risk Band"] = bulk_df["PD"].apply(risk_band)

        st.success("✅ Bulk prediction completed")

        st.dataframe(
            bulk_df[[
                "PD (%)",
                "Risk Band",
                "Business Age (Years)",
                "Industry/Sector",
                "Loan Amount",
                "Interest Rate"
            ]]
        )

        st.download_button(
            "⬇️ Download Results CSV",
            bulk_df.to_csv(index=False),
            "pd_results.csv",
            "text/csv"
        )

st.divider()

# ============================================================
# SINGLE BORROWER FORM
# ============================================================
with st.form("pd_form"):
    st.subheader("📌 Borrower & Loan Information")

    col1, col2 = st.columns(2)

    with col1:
        business_age = st.number_input("Business Age (Years)", 0, 50, 8)
        total_assets = st.number_input("Total Assets", value=5_000_000.0)
        total_liabilities = st.number_input("Total Liabilities", value=3_000_000.0)
        sales = st.number_input("Sales / Revenue", value=7_000_000.0)
        net_income = st.number_input("Net Income", value=600_000.0)
        ebit = st.number_input("EBIT", value=850_000.0)

    with col2:
        interest_expense = st.number_input("Interest Expense", value=180_000.0)
        loan_amount = st.number_input("Loan Amount", value=1_200_000.0)
        installment_amount = st.number_input("Installment Amount", value=45_000.0)
        num_prev_loans = st.number_input("Number of Previous Loans", 0, 10, 2)
        tenure = st.number_input("Loan Tenure (Months)", 1, 120, 36)
        interest_rate = st.number_input("Interest Rate (%)", 0.0, 50.0, 14.5)

    st.subheader("🏢 Business Details")

    industry = st.selectbox("Industry / Sector", cat_meta["Industry/Sector"])
    loan_type = st.selectbox("Loan Type", cat_meta["Loan Type"])
    repayment_freq = st.selectbox("Repayment Frequency", cat_meta["Repayment Frequency"])
    business_type = st.selectbox("Business Type", cat_meta["Business Type"])
    collateral = st.selectbox("Collateral Type & Value", cat_meta["Collateral Type & Value"])

    submitted = st.form_submit_button("🔍 Predict Probability of Default")

# ============================================================
# SINGLE PREDICTION LOGIC
# ============================================================
if submitted:
    df = pd.DataFrame([{
        "Business Age (Years)": business_age,
        "Total Assets": total_assets,
        "Total Liabilities": total_liabilities,
        "Sales/Revenue": sales,
        "Net Income": net_income,
        "EBIT": ebit,
        "Interest Expense": interest_expense,
        "Loan Amount": loan_amount,
        "Installment Amount": installment_amount,
        "Number of Previous Loans": num_prev_loans,
        "Tenure (Months)": tenure,
        "Interest Rate": interest_rate,
        "Industry/Sector": industry,
        "Loan Type": loan_type,
        "Repayment Frequency": repayment_freq,
        "Business Type": business_type,
        "Collateral Type & Value": collateral
    }])

    # Feature engineering
    df["debt_to_assets"] = df["Total Liabilities"] / df["Total Assets"]
    df["interest_coverage"] = df["EBIT"] / (df["Interest Expense"] + 1e-6)
    df["profit_margin"] = df["Net Income"] / df["Sales/Revenue"]
    df["wc_ratio"] = (df["Total Assets"] - df["Total Liabilities"]) / df["Total Assets"]

    df.replace([np.inf, -np.inf], 0, inplace=True)
    df.fillna(0, inplace=True)

    # Predict + cap PD
    raw_pd = model.predict_proba(df)[0, 1]
    pd_prob = min(max(raw_pd, 0.05), 0.95)

    if pd_prob < 0.20:
        risk = "🟢 Low Risk"
    elif pd_prob < 0.50:
        risk = "🟠 Medium Risk"
    else:
        risk = "🔴 High Risk"

    st.divider()
    st.subheader("📈 PD Result")

    st.metric(
        "Probability of Default",
        f"{pd_prob * 100:.2f}%",
        risk
    )

    st.progress(pd_prob)

    st.caption(
        "PD is a calibrated and capped probability estimate, "
        "aligned with industry-standard credit risk practices."
    )
