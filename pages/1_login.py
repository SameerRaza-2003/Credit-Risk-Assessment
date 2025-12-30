import streamlit as st
from auth import get_authenticator

st.title("🔐 Credit Risk System Login")

authenticator = get_authenticator()

# 🔑 This renders the login form
authenticator.login(location="main")

# ✅ Read auth state from session
if st.session_state.get("authentication_status"):
    st.session_state["authenticated"] = True
    st.session_state["user"] = st.session_state.get("username")
    st.success(f"Welcome {st.session_state.get('name')}")
    st.switch_page("pages/2_input_step1.py")

elif st.session_state.get("authentication_status") is False:
    st.error("Invalid username or password")

else:
    st.info("Please enter your credentials")
