import streamlit as st
import pandas as pd
from modules.data_loader import get_active_dataset

# ==========================================================
# ENTERPRISE SIDEBAR
# ==========================================================

def enterprise_sidebar():

    with st.sidebar:

        st.title("InsightForge AI")
        st.caption("Enterprise Workforce Intelligence Platform")

        st.divider()

        # =========================
        # ACTIVE DATASET STATUS
        # =========================

        dataset = get_active_dataset()

        if dataset is not None and not dataset.empty:

            quality = st.session_state.get("quality", {})
            score = quality.get("score", 100)

            st.subheader("Active Dataset")

            st.metric(
                "Dataset",
                st.session_state.get("dataset_name", "Unknown")
            )

            st.metric(
                "Employees",
                len(dataset)
            )

            st.metric(
                "Quality Score",
                f"{score}%"
            )

            st.progress(min(score / 100, 1.0))

        else:

            st.subheader("Active Dataset")
            st.warning("No dataset loaded.")

        st.divider()

        # =========================
        # PLATFORM STATUS
        # =========================

        st.subheader("Platform Status")

        st.success("Application Running")

        db_status = st.session_state.get("db_status", "Connected")
        st.info(f"PostgreSQL : {db_status}")

        st.divider()

        # =========================
        # QUICK NAVIGATION
        # =========================

        st.subheader("Analytics Modules")

        st.page_link("app.py", label="Home")

        st.caption("Data Platform")

        st.divider()

        # =========================
        # QUICK STATS
        # =========================

        st.subheader("Quick Statistics")

        if dataset is not None and not dataset.empty:

            salary = pd.to_numeric(
                dataset["Salary"],
                errors="coerce"
            ).fillna(0)

            attendance = pd.to_numeric(
                dataset["Attendance_Percentage"],
                errors="coerce"
            ).fillna(0)

            st.metric(
                "Departments",
                dataset["Department"].nunique()
            )

            st.metric(
                "Cities",
                dataset["City"].nunique()
            )

            st.metric(
                "Average Salary",
                f"₹ {salary.mean():,.0f}"
            )

            st.metric(
                "Attendance",
                f"{attendance.mean():.1f}%"
            )

        st.divider()

        # =========================
        # SYSTEM INFORMATION
        # =========================

        st.caption("InsightForge AI v2.0")
        st.caption("Streamlit • PostgreSQL • Plotly • Pandas")