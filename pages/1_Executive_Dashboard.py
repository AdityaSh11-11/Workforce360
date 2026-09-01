import streamlit as st
import pandas as pd
import plotly.express as px

from styles.theme import load_theme, hero, footer
from styles.cards import section, kpi, filter_panel, insight, empty_state
from modules.data_loader import get_active_dataset
from components.sidebar import enterprise_sidebar

enterprise_sidebar()
# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(page_title="Executive Dashboard", layout="wide")
load_theme()

hero(
    "Executive Workforce Dashboard",
    "Enterprise-level workforce KPIs, payroll analytics, hiring trends and business intelligence."
)

# ==========================================================
# LOAD DATASET
# ==========================================================

df = get_active_dataset()

if df is None or df.empty:
    empty_state("No Workforce Dataset Available")
    footer()
    st.stop()

# ==========================================================
# CLEAN NUMERIC COLUMNS
# ==========================================================

numeric_cols = [
    "Salary",
    "Attendance_Percentage",
    "Performance_Rating",
    "Experience_Years",
    "Training_Hours",
    "Overtime_Hours",
]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

df["Joining_Date"] = pd.to_datetime(df["Joining_Date"], errors="coerce")

# ==========================================================
# FILTERS
# ==========================================================

section(
    "Executive Filters",
    "Filter workforce metrics by department, city and employment type."
)

filter_panel()

c1, c2, c3 = st.columns(3)

with c1:
    department = st.selectbox(
        "Department",
        ["All"] + sorted(df["Department"].dropna().unique().tolist())
    )

with c2:
    city = st.selectbox(
        "City",
        ["All"] + sorted(df["City"].dropna().unique().tolist())
    )

with c3:
    emp_type = st.selectbox(
        "Employment Type",
        ["All"] + sorted(df["Employment_Type"].dropna().unique().tolist())
    )

filtered = df.copy()

if department != "All":
    filtered = filtered[filtered["Department"] == department]

if city != "All":
    filtered = filtered[filtered["City"] == city]

if emp_type != "All":
    filtered = filtered[filtered["Employment_Type"] == emp_type]

# ==========================================================
# KPI SECTION
# ==========================================================

section(
    "Executive Workforce Snapshot",
    "Organization-wide workforce health indicators."
)

employees = len(filtered)
payroll = filtered["Salary"].sum()
avg_salary = filtered["Salary"].mean()
attendance = filtered["Attendance_Percentage"].mean()
performance = filtered["Performance_Rating"].mean()

active = (
    filtered["Attrition_Status"]
    .astype(str)
    .str.lower()
    .eq("active")
    .sum()
)

attrition = round(((employees - active) / employees) * 100, 2) if employees else 0

r1 = st.columns(3)
r2 = st.columns(3)

with r1[0]:
    kpi("Total Employees", f"{employees:,}", "Employees After Filters")

with r1[1]:
    kpi("Average Salary", f"₹ {avg_salary:,.0f}", "Average Compensation")

with r1[2]:
    kpi("Total Payroll", f"₹ {payroll:,.0f}", "Current Payroll")

with r2[0]:
    kpi("Attendance", f"{attendance:.1f}%", "Average Attendance")

with r2[1]:
    kpi("Performance", f"{performance:.2f}/5", "Average Performance Rating")

with r2[2]:
    kpi("Attrition Rate", f"{attrition:.1f}%", "Current Attrition")

st.divider()

# ==========================================================
# CHARTS ROW 1
# ==========================================================

section(
    "Department & Payroll Analytics",
    "Compare workforce size and compensation across departments."
)

left, right = st.columns(2)

with left:

    dept = (
        filtered.groupby("Department")
        .size()
        .reset_index(name="Employees")
        .sort_values("Employees", ascending=False)
    )

    fig = px.bar(
        dept,
        x="Department",
        y="Employees",
        color="Employees",
        title="Employees by Department"
    )

    fig.update_layout(template="plotly_dark", height=450)

    st.plotly_chart(fig, use_container_width=True)

    insight(
        "Department Workforce Insight",
        "Shows workforce distribution across business departments.",
        "Departments with unusually low headcount may require hiring or resource planning."
    )

with right:

    salary = (
        filtered.groupby("Department")["Salary"]
        .mean()
        .reset_index()
        .sort_values("Salary", ascending=False)
    )

    fig = px.bar(
        salary,
        x="Department",
        y="Salary",
        color="Salary",
        title="Average Salary by Department"
    )

    fig.update_layout(template="plotly_dark", height=450)

    st.plotly_chart(fig, use_container_width=True)

    insight(
        "Department Salary Insight",
        "Highlights compensation differences across departments.",
        "Review departments with significantly higher or lower average salaries for compensation benchmarking."
    )

st.divider()

# ==========================================================
# CHARTS ROW 2
# ==========================================================

section(
    "Geographic Workforce Analytics",
    "Understand employee distribution across cities."
)

city_df = (
    filtered.groupby("City")
    .size()
    .reset_index(name="Employees")
    .sort_values("Employees", ascending=False)
)

fig = px.bar(
    city_df,
    x="City",
    y="Employees",
    color="Employees",
    title="Employees by City"
)

fig.update_layout(template="plotly_dark", height=500)

st.plotly_chart(fig, use_container_width=True)

insight(
    "Location Insight",
    "Displays workforce concentration across operating locations.",
    "Cities with rapid workforce growth may require additional HR support and infrastructure."
)

st.divider()

# ==========================================================
# PERFORMANCE VS ATTENDANCE
# ==========================================================

section(
    "Attendance and Performance Intelligence",
    "Relationship between attendance and employee performance."
)

scatter_df = filtered.copy()

scatter_df["Training_Hours"] = scatter_df["Training_Hours"].clip(lower=1)

fig = px.scatter(
    scatter_df,
    x="Attendance_Percentage",
    y="Performance_Rating",
    color="Department",
    size="Training_Hours",
    hover_name="Employee_Name",
    title="Attendance vs Performance vs Training Hours"
)

fig.update_layout(template="plotly_dark", height=550)

st.plotly_chart(fig, use_container_width=True)

insight(
    "Performance Insight",
    "Each employee is represented by a bubble where bubble size indicates training investment.",
    "Employees with strong attendance but weak performance should receive targeted coaching."
)

st.divider()

# ==========================================================
# EXPERIENCE ANALYTICS
# ==========================================================

section(
    "Experience Distribution",
    "Workforce experience segmentation."
)

exp = (
    filtered.groupby("Experience_Group")
    .size()
    .reset_index(name="Employees")
)

fig = px.pie(
    exp,
    names="Experience_Group",
    values="Employees",
    title="Employees by Experience Group"
)

fig.update_layout(template="plotly_dark", height=480)

st.plotly_chart(fig, use_container_width=True)

insight(
    "Experience Insight",
    "Shows workforce maturity across experience bands.",
    "Balance hiring across junior and experienced employees to maintain succession planning."
)

st.divider()

# ==========================================================
# JOINING TREND
# ==========================================================

section(
    "Hiring Trend Analysis",
    "Employee joining trend across years."
)

trend = (
    filtered.groupby("Joining_Year")
    .size()
    .reset_index(name="Employees")
)

fig = px.line(
    trend,
    x="Joining_Year",
    y="Employees",
    markers=True,
    title="Hiring Trend by Joining Year"
)

fig.update_layout(template="plotly_dark", height=500)

st.plotly_chart(fig, use_container_width=True)

insight(
    "Hiring Trend Insight",
    "Displays recruitment volume across years.",
    "Hiring spikes indicate expansion periods while declining hiring may indicate workforce stabilization."
)

footer()