import streamlit as st

# -------------------------------------------------
# Page config
# -------------------------------------------------
st.set_page_config(
    page_title="Credit Risk Assessment System",
    page_icon="📊",
    layout="centered"
)

# -------------------------------------------------
# Session initialization
# -------------------------------------------------
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# -------------------------------------------------
# Minimal landing UI (prevents ugly flash)
# -------------------------------------------------
st.markdown(
    """
    <div style="text-align: center; margin-top: 120px;">
        <h1>📊 Credit Risk Assessment System</h1>
        <p style="color: grey; font-size: 16px;">
            SME Probability of Default & Financial Risk Evaluation
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("<br><br>", unsafe_allow_html=True)

with st.spinner("Loading application..."):
    # -------------------------------------------------
    # Routing logic (UNCHANGED)
    # -------------------------------------------------
    if not st.session_state["authenticated"]:
        st.switch_page("pages/1_login.py")
    else:
        st.switch_page("pages/2_input_step1.py")
