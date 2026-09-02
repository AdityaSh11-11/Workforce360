import streamlit as st
import pandas as pd
from datetime import datetime

from styles.theme import load_theme, hero, footer
from styles.cards import section, kpi, dataset_card, ai_summary, empty_state
from modules.data_loader import get_active_dataset
from components.sidebar import enterprise_sidebar

st.set_page_config(
    page_title="InsightForge AI",
    layout="wide",
    initial_sidebar_state="expanded"
)
enterprise_sidebar()
load_theme()

df = get_active_dataset()

dataset_name = st.session_state.get("dataset_name", "No Dataset Loaded")
dataset_type = st.session_state.get("dataset_type", "None")
quality = st.session_state.get("quality", {"score": 0})


hero(
    "InsightForge AI Workforce Intelligence Platform",
    "Enterprise HR Analytics Platform powered by AI, PostgreSQL and Interactive Workforce Dashboards."
)

st.caption(
    f"Environment: Production Preview • Last Updated: {datetime.now().strftime('%d %b %Y %I:%M %p')}"
)

st.divider()


section(
    "Current Dataset",
    "Information about the dataset currently active across all dashboards."
)

if df is not None and not df.empty:
    dataset_card(dataset_name, dataset_type, len(df))
else:
    empty_state("No Workforce Dataset Available")


section(
    "Executive Workforce Snapshot",
    "Organization-wide workforce indicators generated from the active dataset."
)

# Initialize variables
total_employees = 0
avg_salary = 0
payroll = 0
avg_attendance = 0
avg_performance = 0
attrition_rate = 0

if df is not None and not df.empty:

    salary = pd.to_numeric(df["Salary"], errors="coerce").fillna(0)
    attendance = pd.to_numeric(df["Attendance_Percentage"], errors="coerce").fillna(0)
    performance = pd.to_numeric(df["Performance_Rating"], errors="coerce").fillna(0)

    total_employees = len(df)
    avg_salary = salary.mean()
    payroll = salary.sum()
    avg_attendance = attendance.mean()
    avg_performance = performance.mean()

    active_emp = (
        df["Attrition_Status"]
        .astype(str)
        .str.lower()
        .eq("active")
        .sum()
    )

    attrition_rate = round(
        ((total_employees - active_emp) / total_employees) * 100,
        2,
    )

else:
    avg_salary = 0
    payroll = 0
    avg_attendance = 0
    avg_performance = 0
    attrition_rate = 0

if df is not None and not df.empty:

    r1 = st.columns(3)
    r2 = st.columns(3)

    with r1[0]:
        kpi("Total Employees", f"{total_employees:,}", "Employees in Dataset")

    with r1[1]:
        kpi("Average Salary", f"₹ {avg_salary:,.0f}", "Average Compensation")

    with r1[2]:
        kpi("Total Payroll", f"₹ {payroll:,.0f}", "Overall Payroll")

    with r2[0]:
        kpi("Attendance Rate", f"{avg_attendance:.1f}%", "Organization Attendance")

    with r2[1]:
        kpi("Performance Rating", f"{avg_performance:.2f}/5", "Average Performance")

    with r2[2]:
        kpi("Attrition Rate", f"{attrition_rate:.1f}%", "Current Attrition")

else:

    cols = st.columns(3)
    cols2 = st.columns(3)

    for c, title in zip(
        cols + cols2,
        [
            "Total Employees",
            "Average Salary",
            "Total Payroll",
            "Attendance Rate",
            "Performance Rating",
            "Attrition Rate",
        ],
    ):
        with c:
            kpi(title, "--", "Dataset Required")

st.divider()


section(
    "Platform Modules",
    "InsightForge AI consists of interconnected analytics modules built for HR leaders."
)

modules = [
    ("Data Ingestion", "Upload CSV, Excel or manually enter employee records."),
    ("Executive Dashboard", "High-level workforce KPIs and payroll insights."),
    ("Employee Analytics", "Employee demographics, location and department analysis."),
    ("Performance Analytics", "Performance, attendance, overtime and training insights."),
    ("Attrition Intelligence", "Identify retention risks and workforce churn patterns."),
    ("AI Workforce Studio", "Generate AI recommendations, SQL and Power BI DAX."),
    ("AI Workforce Chat", "Ask HR questions using natural language."),
    ("Export Center", "Download Excel, CSV and Power BI ready datasets."),
    ("Audit Log", "Track ingestion history and warehouse activity.")
]

for i in range(0, len(modules), 3):
    cols = st.columns(3)

    for col, module in zip(cols, modules[i:i + 3]):
        with col:
            st.container(border=True)

            st.markdown(f"#### {module[0]}")
            st.caption(module[1])

st.divider()


section(
    "Dataset Preview",
    "First 15 rows from the currently active workforce dataset."
)

if df is not None and not df.empty:

    st.dataframe(
        df.head(15),
        use_container_width=True,
        hide_index=True,
    )

    st.caption(
        f"Rows : {len(df):,} | Columns : {len(df.columns)} | Quality Score : {quality.get('score',100)}%"
    )

else:

    st.info("Upload a dataset from the Data Ingestion page.")

st.divider()


section(
    "Business Objectives",
    "Primary business decisions supported by InsightForge AI."
)

col1, col2 = st.columns(2)

with col1:

    st.markdown("""
    **Workforce Monitoring**

    - Department-wise workforce distribution.
    - Employee demographic analytics.
    - Payroll visibility.
    - Attendance monitoring.
    - Hiring trend analysis.
    """)

    st.markdown("""
    **HR Decision Support**

    - Attrition monitoring.
    - Promotion readiness.
    - Employee engagement indicators.
    - Performance benchmarking.
    """)

with col2:

    st.markdown("""
    **Executive Intelligence**

    - AI-generated workforce summaries.
    - Compensation insights.
    - Workforce productivity analysis.
    - Retention strategy recommendations.
    """)

    st.markdown("""
    **Business Intelligence Integration**

    - PostgreSQL Warehouse.
    - Microsoft Power BI exports.
    - SQL analytics.
    - Audit logging.
    """)

st.divider()


section(
    "AI Executive Workforce Summary",
    "Automatically generated overview for business stakeholders."
)

if df is not None and not df.empty:

    dept = df["Department"].nunique()
    city = df["City"].nunique()

    summary = f"""
    The organization currently has **{len(df):,} employees** distributed across **{dept} departments**
    and **{city} cities**.

    Average attendance is **{avg_attendance:.1f}%**, while workforce performance averages
    **{avg_performance:.2f}/5**. Overall payroll stands at **₹ {payroll:,.0f}**
    with an average employee salary of **₹ {avg_salary:,.0f}**.

    Current attrition is **{attrition_rate:.1f}%**, indicating opportunities for targeted
    retention strategies and performance improvement initiatives.
    """

    ai_summary(summary)

else:

    ai_summary(
        "Upload a workforce dataset to generate an AI-powered executive workforce summary."
    )

st.divider()


section(
    "Technology Stack",
    "Architecture powering the Workforce Intelligence Platform."
)

tech1, tech2 = st.columns(2)

with tech1:

    st.markdown("""
    **Backend**

    - Python
    - Streamlit
    - SQLAlchemy
    - PostgreSQL
    - Pandas
    """)

with tech2:

    st.markdown("""
    **Analytics**

    - Plotly
    - AI Workforce Studio
    - AI Chat Assistant
    - Power BI Integration
    - Audit Logging
    """)

footer()
