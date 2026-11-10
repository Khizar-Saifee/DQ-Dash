import streamlit as st
from utils.db_helper import get_system_stats


def run_dashboard_mode():

    st.header("📊 DQDash System Analytics")

    stats = get_system_stats()

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "🛡 Preventive Reports",
        stats["preventive"]
    )

    col2.metric(
        "🔧 Datasets Analyzed",
        stats["corrective"]
    )

    col3.metric(
        "🧠 ML Experiments",
        stats["ml"]
    )

    st.divider()

    st.info(
        "This dashboard shows overall activity across the DQDash system."
    )