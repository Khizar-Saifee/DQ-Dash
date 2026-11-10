import streamlit as st
from utils.db_helper import (
    get_preventive_history,
    get_corrective_history,
    get_ml_history
)


def run_activity_mode():

    st.header("📊 User Activity History")

    st.write("Track previous AI reports, dataset analysis, and ML experiments.")

    st.divider()

    # ---------------- PREVENTIVE HISTORY ---------------- #

    st.subheader("🛡 Preventive Mode Reports")

    preventive = get_preventive_history()

    if not preventive.empty:
        st.dataframe(preventive)
    else:
        st.info("No preventive reports generated yet.")

    st.divider()

    # ---------------- CORRECTIVE HISTORY ---------------- #

    st.subheader("🔧 Corrective Mode Activity")

    corrective = get_corrective_history()

    if not corrective.empty:
        st.dataframe(corrective)
    else:
        st.info("No corrective analysis recorded yet.")

    st.divider()

    # ---------------- ML HISTORY ---------------- #

    st.subheader("🧠 ML Model Experiments")

    ml = get_ml_history()

    if not ml.empty:
        st.dataframe(ml)
    else:
        st.info("No ML experiments recorded yet.")