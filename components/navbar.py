import streamlit as st

def render_navbar(active_page: str):
    """
    active_page: one of ["input", "results"]
    """

    st.markdown(
        """
        <style>
        .nav-container {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 12px 20px;
            border-bottom: 1px solid #e6e6e6;
            margin-bottom: 25px;
        }
        .nav-left {
            font-size: 22px;
            font-weight: 600;
        }
        .nav-right button {
            margin-left: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns([3, 2])

    with col1:
        st.markdown("### 📊 Credit Risk Assessment System")

    with col2:
        c1, c2, c3 = st.columns(3)

        with c1:
            if st.button(
                "🏠 Input",
                disabled=(active_page == "input"),
                use_container_width=True
            ):
                st.switch_page("pages/2_input_step1.py")

        with c2:
            if st.button(
                "📈 Results",
                disabled=(active_page == "results"),
                use_container_width=True
            ):
                st.switch_page("pages/4_results.py")

        with c3:
            if st.button(
                "🚪 Logout",
                use_container_width=True
            ):
                st.session_state.clear()
                st.switch_page("pages/1_login.py")

    st.divider()
