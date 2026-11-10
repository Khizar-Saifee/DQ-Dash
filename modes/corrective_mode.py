import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils.db_helper import save_corrective_activity

from utils.data_quality import (
    calculate_data_quality,
    detect_outliers,
    remove_outliers_iqr
)
from utils.cleaning import remove_duplicates, fill_missing


def run_corrective_mode():

    st.header("🔧 Corrective Mode - Data Quality Assessment")

    uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])

    if uploaded_file is None:
        st.info("Please upload a CSV file.")
        return

    df = pd.read_csv(uploaded_file)

    # Initialize session state only once
    if "cleaned_df" not in st.session_state:
        st.session_state.cleaned_df = df.copy()

    df_display = st.session_state.cleaned_df

    st.subheader("📄 Dataset Preview")
    st.dataframe(df_display.head())

    if df_display.empty:
        st.error("Dataset is empty after cleaning.")
        return

    # DATA QUALITY METRICS
    st.subheader("📊 Data Quality Metrics")

    metrics = calculate_data_quality(df_display)

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Rows", metrics["Total Rows"])
    col1.metric("Total Columns", metrics["Total Columns"])

    col2.metric("Missing Values", metrics["Missing Values"])
    col2.metric("Duplicate Rows", metrics["Duplicate Rows"])

    col3.metric("Completeness (%)", metrics["Completeness (%)"])
    col3.metric("Overall Quality Score", metrics["Overall Quality Score"])

    # ---------------- SAVE ACTIVITY ---------------- #

    quality_score = metrics["Overall Quality Score"]

    if "corrective_saved" not in st.session_state:
        save_corrective_activity(
            st.session_state.username,
            uploaded_file.name,
            df.shape[0],
            df.shape[1],
            quality_score
        )
        st.session_state.corrective_saved = True

    # QUALITY GAUGE
    st.subheader("🎯 Quality Score Gauge")

    score = metrics["Overall Quality Score"]

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        title={'text': "Data Quality Score"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "green"},
            'steps': [
                {'range': [0, 50], 'color': "red"},
                {'range': [50, 75], 'color': "yellow"},
                {'range': [75, 100], 'color': "lightgreen"},
            ],
        }
    ))

    fig.update_layout(height=300, width=450)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.plotly_chart(fig, use_container_width=False)

    # MISSING VALUES
    st.subheader("📊 Missing Values per Column")

    missing_data = df_display.isnull().sum()
    missing_data = missing_data[missing_data > 0]

    if not missing_data.empty:
        st.bar_chart(missing_data)
    else:
        st.success("No missing values detected.")

    # OUTLIER DETECTION
    st.subheader("🔍 Outlier Detection")

    outliers = detect_outliers(df_display)

    has_outliers = False

    for col, count in outliers.items():
        if count > 0:
            st.write(f"{col}: {count} outliers")
            has_outliers = True

    if not has_outliers:
        st.success("No outliers detected.")

    # CLEANING OPTIONS
    st.subheader("🧹 Cleaning Options")

    if st.button("Remove Duplicates"):

        st.session_state.cleaned_df = remove_duplicates(
            st.session_state.cleaned_df
        )

        st.success("Duplicates removed!")

    if st.button("Fill Missing Values (Mean/Unknown)"):

        st.session_state.cleaned_df = fill_missing(
            st.session_state.cleaned_df
        )

        st.success("Missing values handled!")

    if st.button("Remove Outliers (IQR Method)"):

        st.session_state.cleaned_df = remove_outliers_iqr(
            st.session_state.cleaned_df
        )

        st.success("Outliers removed!")

    # DOWNLOAD CLEANED DATA
    st.subheader("📥 Download Cleaned Data")

    original_name = uploaded_file.name.replace(".csv", "")
    new_filename = f"{original_name}_cleaned.csv"

    csv = st.session_state.cleaned_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download Cleaned CSV",
        data=csv,
        file_name=new_filename,
        mime="text/csv",
    )