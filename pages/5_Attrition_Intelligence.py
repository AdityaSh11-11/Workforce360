import streamlit as st
import pandas as pd
import plotly.express as px

from styles.theme import load_theme, hero, footer
from styles.cards import section, filter_panel, insight, empty_state
from modules.data_loader import get_active_dataset
from components.sidebar import enterprise_sidebar

enterprise_sidebar()

st.set_page_config(page_title="Attrition Intelligence", layout="wide")
load_theme()

hero(
    "Attrition Intelligence Dashboard",
    "Identify employee attrition patterns, retention risks and workforce stability using business intelligence."
)

df = get_active_dataset()

if df is None or df.empty:
    empty_state("No workforce dataset available.")
    footer()
    st.stop()

numeric_cols = [
    "Salary",
    "Experience_Years",
    "Performance_Rating",
    "Attendance_Percentage",
    "Training_Hours",
    "Overtime_Hours",
]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

df["Attrition_Status"] = df["Attrition_Status"].fillna("Active").astype(str)


section(
    "Attrition Filters",
    "Filter attrition analytics by department, city and employment type."
)

filter_panel()

c1, c2, c3 = st.columns(3)

department = c1.selectbox(
    "Department",
    ["All"] + sorted(df["Department"].dropna().unique())
)

city = c2.selectbox(
    "City",
    ["All"] + sorted(df["City"].dropna().unique())
)

employment = c3.selectbox(
    "Employment Type",
    ["All"] + sorted(df["Employment_Type"].dropna().unique())
)

filtered = df.copy()

if department != "All":
    filtered = filtered[filtered["Department"] == department]

if city != "All":
    filtered = filtered[filtered["City"] == city]

if employment != "All":
    filtered = filtered[filtered["Employment_Type"] == employment]

section(
    "Attrition KPI Overview",
    "Executive view of workforce retention and employee exits."
)

employees = len(filtered)
active = filtered["Attrition_Status"].str.lower().eq("active").sum()
left = employees - active

attrition_rate = round((left / employees) * 100, 2) if employees else 0

r1 = st.columns(4)

r1[0].metric("Employees", employees)
r1[1].metric("Active Employees", active)
r1[2].metric("Employees Left", left)
r1[3].metric("Attrition Rate", f"{attrition_rate}%")

st.divider()

section(
    "Attrition Status Distribution",
    "Overall workforce retention status."
)

status_df = (
    filtered.groupby("Attrition_Status")
    .size()
    .reset_index(name="Employees")
)

fig = px.pie(
    status_df,
    names="Attrition_Status",
    values="Employees",
    title="Employee Attrition Distribution"
)

fig.update_layout(template="plotly_dark", height=450)

st.plotly_chart(fig, use_container_width=True)

insight(
    "Attrition Insight",
    "This chart shows the percentage of active employees versus employees who have left the organization.",
    "A rising attrition percentage should trigger department-level retention analysis."
)

st.divider()

section(
    "Attrition by Department",
    "Departments experiencing the highest employee exits."
)

dept_attr = (
    filtered.groupby(["Department", "Attrition_Status"])
    .size()
    .reset_index(name="Employees")
)

fig = px.bar(
    dept_attr,
    x="Department",
    y="Employees",
    color="Attrition_Status",
    barmode="group",
    title="Department-wise Attrition"
)

fig.update_layout(template="plotly_dark", height=500)

st.plotly_chart(fig, use_container_width=True)

insight(
    "Department Attrition Insight",
    "Departments with higher employee exits may indicate workload imbalance, compensation issues or leadership challenges.",
    "Review HR interventions in departments with above-average attrition."
)

st.divider()

section(
    "Attrition by Location",
    "Geographic analysis of employee exits."
)

city_attr = (
    filtered.groupby(["City", "Attrition_Status"])
    .size()
    .reset_index(name="Employees")
)

fig = px.bar(
    city_attr,
    x="City",
    y="Employees",
    color="Attrition_Status",
    title="City-wise Attrition"
)

fig.update_layout(template="plotly_dark", height=500)

st.plotly_chart(fig, use_container_width=True)

insight(
    "Location Attrition Insight",
    "Identify business locations experiencing higher workforce turnover.",
    "Cities with consistently higher exits should be reviewed for employee engagement and hiring quality."
)

st.divider()

section(
    "Experience and Attrition",
    "Attrition distribution across workforce experience groups."
)

exp_attr = (
    filtered.groupby(["Experience_Group", "Attrition_Status"])
    .size()
    .reset_index(name="Employees")
)

fig = px.bar(
    exp_attr,
    x="Experience_Group",
    y="Employees",
    color="Attrition_Status",
    barmode="group",
    title="Attrition by Experience Group"
)

fig.update_layout(template="plotly_dark", height=480)

st.plotly_chart(fig, use_container_width=True)

insight(
    "Experience Attrition Insight",
    "Early-career employees often contribute a larger share of attrition.",
    "Strengthen onboarding, mentoring and career progression programs for junior employees."
)

st.divider()

section(
    "Salary Band Attrition",
    "Relationship between salary bands and employee exits."
)

salary_attr = (
    filtered.groupby(["Salary_Band", "Attrition_Status"])
    .size()
    .reset_index(name="Employees")
)

fig = px.bar(
    salary_attr,
    x="Salary_Band",
    y="Employees",
    color="Attrition_Status",
    barmode="group",
    title="Attrition by Salary Band"
)

fig.update_layout(template="plotly_dark", height=450)

st.plotly_chart(fig, use_container_width=True)

insight(
    "Salary Attrition Insight",
    "Lower salary bands may experience higher turnover because of compensation competition.",
    "Review compensation strategy for departments with persistent low-band attrition."
)

st.divider()

section(
    "Performance and Attrition",
    "Compare employee performance ratings with attrition status."
)

fig = px.box(
    filtered,
    x="Attrition_Status",
    y="Performance_Rating",
    color="Attrition_Status",
    title="Performance Rating by Attrition Status"
)

fig.update_layout(template="plotly_dark", height=480)

st.plotly_chart(fig, use_container_width=True)

insight(
    "Performance Attrition Insight",
    "Employees leaving despite high performance ratings represent potential retention risks.",
    "Create retention strategies for high-performing employees before resignation."
)

st.divider()

section(
    "Overtime Impact on Attrition",
    "Relationship between overtime workload and employee exits."
)

fig = px.scatter(
    filtered,
    x="Overtime_Hours",
    y="Performance_Rating",
    color="Attrition_Status",
    hover_name="Employee_Name",
    title="Overtime Hours vs Performance Rating"
)

fig.update_layout(template="plotly_dark", height=520)

st.plotly_chart(fig, use_container_width=True)

insight(
    "Overtime Insight",
    "Employees working excessive overtime with declining performance may be at burnout risk.",
    "Monitor workload and introduce work-life balance initiatives."
)

st.divider()

section(
    "Retention Risk Watchlist",
    "Employees showing characteristics commonly associated with attrition."
)

risk = filtered[
    (
        (filtered["Attendance_Percentage"] < 75)
        | (filtered["Performance_Rating"] < 2.5)
        | (filtered["Overtime_Hours"] > 40)
    )
]

st.dataframe(
    risk[
        [
            "Employee_Name",
            "Department",
            "City",
            "Salary",
            "Attendance_Percentage",
            "Performance_Rating",
            "Overtime_Hours",
            "Attrition_Status",
        ]
    ],
    use_container_width=True,
    hide_index=True,
)

insight(
    "Retention Watchlist Insight",
    "Employees in this list show one or more potential attrition indicators including low attendance, low performance or excessive overtime.",
    "HR managers should schedule engagement conversations and development plans for these employees."
)

st.divider()

section(
    "Executive Attrition Summary",
    "AI-style business summary generated from current workforce metrics."
)

summary = f"""
**Current Workforce Overview**

- Total Employees: **{employees:,}**
- Active Employees: **{active:,}**
- Employees Left: **{left:,}**
- Attrition Rate: **{attrition_rate}%**

**Key Business Findings**

- Departments with higher exits require targeted retention initiatives.
- Salary competitiveness and workload balance are major retention indicators.
- Early-career employees show stronger attrition trends than experienced employees.
- High-performing employees leaving the organization represent significant business risk.

**Recommended HR Actions**

1. Launch department-level retention programs.
2. Review salary bands with high employee exits.
3. Reduce excessive overtime in high-risk teams.
4. Increase career development and learning opportunities.
"""

st.markdown(summary)

footer()
