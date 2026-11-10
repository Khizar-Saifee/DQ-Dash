import streamlit as st
from auth.auth_utils import init_db, register_user, login_user
from utils.db_helper import init_activity_db
from modes.activity_mode import run_activity_mode
from modes.dashboard_mode import run_dashboard_mode

# Run database initialization once
if "db_initialized" not in st.session_state:
    init_db()
    init_activity_db()
    st.session_state.db_initialized = True

st.set_page_config(page_title="DQDash", layout="wide")

# Session state for login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

st.title("📊 DQDash - AI Data Quality Assistant")

# -----------------------------
# USER NOT LOGGED IN
# -----------------------------
if not st.session_state.logged_in:

    menu = st.sidebar.selectbox("Account", ["Login", "Register"])

    if menu == "Register":

        st.subheader("Create Account")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Register"):

            if not username or not password:
                st.warning("Please enter username and password.")
            else:
                if register_user(username, password):
                    st.success("Account created successfully! Please login.")
                else:
                    st.error("Username already exists.")

    elif menu == "Login":

        st.subheader("Login")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):

            if login_user(username, password):

                st.session_state.logged_in = True
                st.session_state.username = username   # ADD THIS LINE

                st.success("Login successful")
                st.rerun()

            else:
                st.error("Invalid credentials")

# -----------------------------
# USER LOGGED IN
# -----------------------------
else:

    st.sidebar.success("Logged in")

    st.sidebar.title("DQDash Navigation")

    mode = st.sidebar.selectbox(
        "Select Mode",
        [
            "Preventive Mode",
            "Corrective Mode",
            "ML Mode",
            "User Activity",
            "Dashboard"
        ]
    )

    if st.sidebar.button("Logout"):

        st.session_state.logged_in = False
        st.rerun()

    # Preventive Mode
    if mode == "Preventive Mode":

        from modes.preventive_mode import run_preventive_mode
        run_preventive_mode()

    # Corrective Mode
    elif mode == "Corrective Mode":

        from modes.corrective_mode import run_corrective_mode
        run_corrective_mode()

    # ML Mode
    elif mode == "ML Mode":

        from modes.ml_mode import run_ml_mode
        run_ml_mode()

    # User Activity Mode
    elif mode == "User Activity":

        from modes.activity_mode import run_activity_mode
        run_activity_mode()

    # Dashboard
    elif mode == "Dashboard":

        from modes.dashboard_mode import run_dashboard_mode
        run_dashboard_mode()       
 

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.caption("DQDash – AI Data Quality Assistant | Final Year Project 2025-26| By Saifee Khizar & Dhina Chelliah")
