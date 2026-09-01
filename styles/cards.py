import streamlit as st

# ==========================================================
# SECTION HEADER
# ==========================================================

def section(title, description=""):
    st.markdown(f"## {title}")
    if description:
        st.caption(description)
    st.write("")

# ==========================================================
# KPI CARD (NO HTML)
# ==========================================================

def kpi(title, value, subtitle=""):
    with st.container(border=True):
        st.caption(title)
        st.markdown(f"### {value}")
        if subtitle:
            st.caption(subtitle)

# ==========================================================
# DATASET CARD
# ==========================================================

def dataset_card(name, dtype, rows):
    with st.container(border=True):
        st.markdown("### Active Workforce Dataset")

        c1, c2, c3 = st.columns(3)

        c1.metric("Dataset Name", name)
        c2.metric("Dataset Type", dtype)
        c3.metric("Records", f"{rows:,}")

# ==========================================================
# FILTER PANEL
# ==========================================================

def filter_panel():
    with st.container(border=True):
        st.markdown("#### Dashboard Filters")
        st.caption(
            "Filter employees by department, city, gender, employment type and performance."
        )

# ==========================================================
# INSIGHT BOX
# ==========================================================

def insight(title, insight, recommendation=""):
    with st.container(border=True):
        st.markdown(f"#### {title}")

        st.markdown("**Business Insight**")
        st.write(insight)

        if recommendation:
            st.markdown("---")
            st.markdown("**Business Recommendation**")
            st.write(recommendation)

# ==========================================================
# AI SUMMARY
# ==========================================================

def ai_summary(summary):
    with st.container(border=True):
        st.markdown("### AI Workforce Executive Summary")
        st.write(summary)

# ==========================================================
# EMPTY STATE
# ==========================================================

def empty_state(message):
    st.info(message)