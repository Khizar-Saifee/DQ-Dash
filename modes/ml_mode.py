import streamlit as st
import pandas as pd
import joblib
import seaborn as sns
import matplotlib.pyplot as plt
from utils.db_helper import save_ml_result

from utils.ml_helper import (
    prepare_data,
    detect_task,
    train_classification_models,
    train_regression_models
)


def run_ml_mode():

    st.header("🧠 ML Algorithm Recommendation Mode")

    uploaded_file = st.file_uploader("Upload CSV File for ML", type=["csv"])

    if uploaded_file is None:
        st.info("Please upload a CSV file.")
        return

    df = pd.read_csv(uploaded_file)

    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    # Filter possible target columns
    filtered_columns = [
        col for col in df.columns
        if df[col].nunique() < len(df) * 0.95
    ]

    if not filtered_columns:
        st.error("No suitable target column detected.")
        return

    target_column = st.selectbox("Select Target Column", filtered_columns)

    auto_detect = st.checkbox("Auto Detect Task Type", value=True)

    if auto_detect:
        task = detect_task(df[target_column])
        st.info(f"Detected Task: {task}")
    else:
        task = st.selectbox("Select Task Type", ["Classification", "Regression"])

    # TRAIN BUTTON
    if st.button("Train Models"):

        try:

            X_train, X_test, y_train, y_test = prepare_data(
                df, target_column
            )

            # store for feature importance
            st.session_state.X_train_columns = X_train.columns

            if task == "Classification":
                results = train_classification_models(
                    X_train, X_test, y_train, y_test
                )
            else:
                results = train_regression_models(
                    X_train, X_test, y_train, y_test
                )

            st.session_state.ml_results = results
            st.session_state.ml_task = task

        except Exception as e:
            st.error(f"Model training failed: {e}")
            return

    # SHOW RESULTS
    if "ml_results" in st.session_state:

        results = st.session_state.ml_results
        task = st.session_state.ml_task

        results_table = []

        for name, result in results.items():

            row = {"Model": name}

            for metric, value in result.items():
                if metric not in ["Model", "Confusion Matrix"]:
                    row[metric] = value

            results_table.append(row)

        comparison_df = pd.DataFrame(results_table)

        st.subheader("📊 Model Comparison Table")
        st.dataframe(comparison_df)

        if task == "Classification":
            comparison_df = comparison_df.sort_values(
                by="Accuracy", ascending=False
            )
            best_model_name = comparison_df.iloc[0]["Model"]
        else:
            comparison_df = comparison_df.sort_values(
                by="R2 Score", ascending=False
            )
            best_model_name = comparison_df.iloc[0]["Model"]

        best_model = results[best_model_name]["Model"]

        st.markdown(
            f"""
            <div style="background-color:#1f6f3d;padding:20px;border-radius:10px;">
            <h3 style="color:white;">🏆 Best Model Selected</h3>
            <h2 style="color:white;">{best_model_name}</h2>
            </div>
            """,
            unsafe_allow_html=True
        )

        # PERFORMANCE CHART
        st.subheader("📈 Model Performance Comparison")

        metric_name = (
            "Accuracy" if task == "Classification" else "R2 Score"
        )

        st.bar_chart(
            comparison_df.set_index("Model")[metric_name]
        )

        # ---------------- SAVE ML ACTIVITY ---------------- #

        best_score = float(comparison_df.iloc[0][metric_name])

        if "ml_saved" not in st.session_state:
            save_ml_result(
                st.session_state.username,
                uploaded_file.name,
                target_column,
                best_model_name,
                best_score
            )
            st.session_state.ml_saved = True

        # CONFUSION MATRIX
        if task == "Classification":

            best_cm = results[best_model_name]["Confusion Matrix"]

            st.subheader("📊 Confusion Matrix")

            fig, ax = plt.subplots(figsize=(4, 3))

            sns.heatmap(
                best_cm,
                annot=True,
                fmt="d",
                cmap="Blues",
                cbar=False,
                square=True,
                ax=ax
            )

            ax.set_xlabel("Predicted")
            ax.set_ylabel("Actual")

            plt.tight_layout()

            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.pyplot(fig, use_container_width=False)

        # FEATURE IMPORTANCE
        if hasattr(best_model, "feature_importances_") and "X_train_columns" in st.session_state:

            st.subheader("📈 Feature Importance")

            importance_df = pd.DataFrame({
                "Feature": st.session_state.X_train_columns,
                "Importance": best_model.feature_importances_
            }).sort_values(by="Importance", ascending=False).head(10)

            fig_imp, ax_imp = plt.subplots(figsize=(5, 3))

            ax_imp.barh(
                importance_df["Feature"],
                importance_df["Importance"]
            )

            ax_imp.invert_yaxis()
            ax_imp.set_xlabel("Importance Score")

            plt.tight_layout()

            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.pyplot(fig_imp, use_container_width=False)

        # DOWNLOAD MODEL
        joblib.dump(best_model, "best_model.pkl")

        with open("best_model.pkl", "rb") as f:
            st.download_button(
                "⬇ Download Best Model",
                f,
                file_name="best_model.pkl"
            )