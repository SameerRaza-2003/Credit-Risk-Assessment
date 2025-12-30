import streamlit as st

# 🔐 Guards
if not st.session_state.get("authenticated", False):
    st.switch_page("pages/1_login.py")

if "step1" not in st.session_state:
    st.switch_page("pages/2_input_step1.py")

st.title("💰 Financial Information")
st.caption("Step 2 of 2 • Financial position & performance")

with st.form("financials_form"):
    st.subheader("📊 Balance Sheet")

    col1, col2 = st.columns(2)

    with col1:
        total_assets = st.number_input(
            "Total Assets",
            min_value=0.0,
            step=100000.0
        )

        total_liabilities = st.number_input(
            "Total Liabilities",
            min_value=0.0,
            step=100000.0
        )

        working_capital = st.number_input(
            "Working Capital",
            step=100000.0,
            help="Can be negative"
        )

    with col2:
        average_bank_balance = st.number_input(
            "Average Bank Balance",
            min_value=0.0,
            step=50000.0
        )

        sales = st.number_input(
            "Sales / Revenue",
            min_value=0.0,
            step=100000.0
        )

    st.divider()
    st.subheader("📈 Income Statement")

    col3, col4 = st.columns(2)

    with col3:
        ebit = st.number_input(
            "EBIT",
            step=100000.0
        )

    with col4:
        net_income = st.number_input(
            "Net Income",
            step=100000.0
        )

    interest_expense = st.number_input(
        "Interest Expense",
        min_value=0.0,
        step=50000.0
    )

    st.divider()
    st.subheader("⏱ Credit Behaviour")

    dpd_flags = st.text_input(
        "Days Past Due (30/60/90 flags)",
        placeholder="e.g. Regular: 0 | 1 to 89 DPD: 3 | 90+DPD: 1",
        help="Free-text as per bank records"
    )

    submit = st.form_submit_button("🚀 Calculate Risk")

if submit:
    raw_financials = {
        "Total Assets": total_assets,
        "Total Liabilities": total_liabilities,
        "Working Capital": working_capital,
        "Average Bank Balance": average_bank_balance,
        "Sales/Revenue": sales,
        "EBIT": ebit,
        "Net Income": net_income,
        "Interest Expense": interest_expense,
        "Days Past Due (30/60/90 flags)": dpd_flags,
    }

    # Merge step1 + step2
    st.session_state["financials"] = {
        **st.session_state["step1"],
        **raw_financials
    }

    st.switch_page("pages/4_results.py")
