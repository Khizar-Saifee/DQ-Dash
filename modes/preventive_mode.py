import streamlit as st
from utils.llm_helper import generate_database_design
from utils.db_helper import save_preventive_report



def run_preventive_mode():

    # Session state initialization
    if "ai_result" not in st.session_state:
        st.session_state.ai_result = None

    st.header("🛡 Preventive Mode - AI Database Design Advisor")

    st.write(
        "Describe your business idea and the system will suggest "
        "an optimized database schema."
    )

    business_description = st.text_area(
        "Enter Business Description",
        height=200,
        placeholder="Example: Online food delivery app with users, restaurants, orders, payments..."
    )

    model_choice = st.selectbox(
        "Select LLM Model",
        ["phi3"]
    )

    # Generate design
    if st.button("Generate Database Design"):

        if not business_description.strip():
            st.warning("Please enter a business description.")
            return

        with st.spinner("Generating database architecture..."):
            st.session_state.ai_result = generate_database_design(
                business_description,
                model=model_choice
            )

    # Get stored result
    result = st.session_state.ai_result

    if result and "preventive_saved" not in st.session_state:

        save_preventive_report(
            st.session_state.username,
            business_description,
            result
        )

        st.session_state.preventive_saved = True

    # Display results if available
    if result:

        st.subheader("📋 AI Generated Database Design")

        st.info(
            "⚠ This AI-generated schema is a draft recommendation. "
            "Final validation by a database architect is recommended."
        )

        # Clear button
        if st.button("Clear Result"):
            st.session_state.ai_result = None
            st.rerun()

        # Extract sections robustly

        design = ""
        sql_script = ""
        er_diagram = ""

        if "SECTION 1:" in result:
            try:
                design = result.split("SECTION 1:")[1].split("SECTION 2:")[0].strip()
            except:
                design = ""

        if "SECTION 2:" in result:
            try:
                sql_script = result.split("SECTION 2:")[1].split("SECTION 3:")[0].strip()
            except:
                sql_script = ""

        if "SECTION 3:" in result:
            try:
                er_diagram = result.split("SECTION 3:")[1].strip()
            except:
                er_diagram = ""

        # Display sections
        if design:
            st.markdown("### Database Design")
            st.markdown(design)

        if sql_script:
            st.markdown("### SQL Script")
            st.code(sql_script, language="sql")

        if er_diagram:
            st.markdown("### ER Diagram (Text)")
            st.markdown(er_diagram)

        # SQL Download
        if sql_script:
            st.download_button(
                label="⬇ Download SQL Schema",
                data=sql_script,
                file_name="database_schema.sql",
                mime="text/plain"
            )

        # ER Diagram Download
        if er_diagram:
            st.download_button(
                label="⬇ Download ER Diagram Text",
                data=er_diagram,
                file_name="er_diagram.txt",
                mime="text/plain"
            )

        # Raw AI Report Download
        st.download_button(
            label="⬇ Download Design Report",
            data=result,
            file_name="database_design_report.txt",
            mime="text/plain"
        )

        # Full Architecture Report
        full_report = f"""
==============================
DQDash - AI Database Architect
==============================

BUSINESS DESCRIPTION
--------------------
{business_description}

==============================
DATABASE DESIGN
==============================
{design if design else "Not generated"}

==============================
SQL SCHEMA
==============================
{sql_script if sql_script else "Not generated"}

==============================
ER DIAGRAM
==============================
{er_diagram if er_diagram else "Not generated"}
"""

        st.divider()
        st.subheader("⬇ Download Options")

        st.download_button(
            label="⬇ Download Full Architecture Report",
            data=full_report,
            file_name="database_architecture_report.txt",
            mime="text/plain"
        )