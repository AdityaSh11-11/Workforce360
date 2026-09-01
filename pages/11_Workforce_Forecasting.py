import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

from styles.theme import load_theme, hero, footer
from styles.cards import section, insight, empty_state
from modules.data_loader import get_active_dataset
from components.sidebar import enterprise_sidebar

enterprise_sidebar()
# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Workforce Forecasting",
    layout="wide"
)

load_theme()

hero(
    "Workforce Forecasting Dashboard",
    "Predict hiring demand, attrition trends, payroll growth and workforce planning for future business expansion."
)

# ==========================================================
# LOAD DATASET
# ==========================================================

df = get_active_dataset()

if df is None or df.empty:
    empty_state("No workforce dataset available.")
    footer()
    st.stop()

# ==========================================================
# CLEAN DATA (NaN SAFE)
# ==========================================================

numeric_cols = [
    "Salary",
    "Performance_Rating",
    "Attendance_Percentage",
    "Experience_Years",
    "Training_Hours",
    "Overtime_Hours"
]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

employees = len(df)
departments = df["Department"].nunique()
avg_salary = df["Salary"].mean()

current_attrition = (
    df["Attrition_Status"]
    .astype(str)
    .str.lower()
    .eq("left")
    .mean()
) * 100

avg_salary = 0 if np.isnan(avg_salary) else avg_salary
current_attrition = round(current_attrition, 2)

# ==========================================================
# KPI SECTION
# ==========================================================

section(
    "Executive Forecast Snapshot",
    "Current workforce metrics used as the baseline for forecasting models."
)

c1, c2, c3, c4 = st.columns(4)

c1.metric("Current Employees", employees)
c2.metric("Departments", departments)
c3.metric("Average Salary", f"₹ {avg_salary:,.0f}")
c4.metric("Current Attrition", f"{current_attrition}%")

st.divider()

# ==========================================================
# FORECAST SETTINGS
# ==========================================================

section(
    "Forecast Configuration",
    "Adjust business assumptions to generate hiring and payroll forecasts."
)

col1, col2, col3 = st.columns(3)

forecast_months = col1.slider(
    "Forecast Period (Months)",
    3,
    24,
    12
)

growth_rate = col2.slider(
    "Hiring Growth (%)",
    0,
    30,
    10
)

salary_growth = col3.slider(
    "Annual Salary Increment (%)",
    0,
    20,
    8
)

months = np.arange(1, forecast_months + 1)

# ==========================================================
# HIRING FORECAST
# ==========================================================

section(
    "Projected Hiring Forecast",
    "Expected workforce growth based on hiring assumptions."
)

projected_employees = [
    round(employees * (1 + (growth_rate / 100) * (m / forecast_months)))
    for m in months
]

forecast_df = pd.DataFrame({
    "Month": months,
    "Projected Employees": projected_employees
})

fig = px.line(
    forecast_df,
    x="Month",
    y="Projected Employees",
    markers=True,
    title="Projected Workforce Growth"
)

fig.update_layout(template="plotly_dark", height=450)

st.plotly_chart(fig, use_container_width=True)

insight(
    "Hiring Forecast Insight",
    f"With a projected hiring growth of {growth_rate}%, the workforce is expected to grow from {employees:,} employees to approximately {projected_employees[-1]:,} employees within {forecast_months} months.",
    "Use projected hiring demand for recruitment budgeting and workforce planning."
)

st.divider()

# ==========================================================
# ATTRITION FORECAST
# ==========================================================

section(
    "Projected Attrition Forecast",
    "Forecast expected workforce attrition over upcoming months."
)

future_attrition = [
    max(0, round(current_attrition + np.sin(m / 2) * 1.2, 2))
    for m in months
]

attrition_df = pd.DataFrame({
    "Month": months,
    "Projected Attrition Rate": future_attrition
})

fig = px.line(
    attrition_df,
    x="Month",
    y="Projected Attrition Rate",
    markers=True,
    title="Projected Attrition Trend"
)

fig.update_layout(template="plotly_dark", height=450)

st.plotly_chart(fig, use_container_width=True)

insight(
    "Attrition Forecast Insight",
    "The projected attrition curve estimates workforce exits over the planning period using the current attrition baseline.",
    "Prepare retention initiatives before projected attrition peaks."
)

st.divider()

# ==========================================================
# SALARY FORECAST
# ==========================================================

section(
    "Salary Growth Forecast",
    "Estimate average salary growth using annual increment assumptions."
)

salary_forecast = [
    avg_salary * (1 + salary_growth / 100 * (m / 12))
    for m in months
]

salary_df = pd.DataFrame({
    "Month": months,
    "Average Salary Forecast": salary_forecast
})

fig = px.line(
    salary_df,
    x="Month",
    y="Average Salary Forecast",
    markers=True,
    title="Projected Average Salary Trend"
)

fig.update_layout(template="plotly_dark", height=450)

st.plotly_chart(fig, use_container_width=True)

insight(
    "Salary Forecast Insight",
    f"Assuming an annual salary increment of {salary_growth}%, the average employee salary is expected to reach approximately ₹ {salary_forecast[-1]:,.0f}.",
    "Use salary forecasting while planning compensation budgets."
)

st.divider()

# ==========================================================
# DEPARTMENT HIRING PLAN
# ==========================================================

section(
    "Department Hiring Recommendations",
    "AI-generated hiring demand across departments."
)

dept = (
    df.groupby("Department")
    .size()
    .reset_index(name="Current Employees")
)

dept["Suggested Hiring"] = (
    dept["Current Employees"] * growth_rate / 100
).round().astype(int)

dept["Future Headcount"] = (
    dept["Current Employees"] + dept["Suggested Hiring"]
)

fig = px.bar(
    dept.sort_values("Suggested Hiring", ascending=False),
    x="Department",
    y="Suggested Hiring",
    color="Suggested Hiring",
    text="Suggested Hiring",
    title="Suggested Hiring by Department"
)

fig.update_layout(template="plotly_dark", height=500)

st.plotly_chart(fig, use_container_width=True)

st.dataframe(dept, use_container_width=True, hide_index=True)

insight(
    "Department Hiring Insight",
    "Departments with the highest suggested hiring numbers represent the largest workforce expansion opportunities.",
    "Prioritize recruitment budgets for departments with future workforce shortages."
)

st.divider()

# ==========================================================
# HEADCOUNT COMPARISON
# ==========================================================

section(
    "Current vs Future Headcount",
    "Compare existing workforce against projected department headcount."
)

fig = px.bar(
    dept,
    x="Department",
    y=["Current Employees", "Future Headcount"],
    barmode="group",
    title="Current vs Future Workforce Planning"
)

fig.update_layout(template="plotly_dark", height=520)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# ==========================================================
# PROMOTION FORECAST
# ==========================================================

section(
    "Promotion Forecast",
    "Identify employees eligible for promotion using attendance and performance criteria."
)

eligible = df[
    (df["Performance_Rating"] >= 4.5)
    & (df["Attendance_Percentage"] >= 90)
]

promotion_count = len(eligible)
promotion_rate = (
    round((promotion_count / employees) * 100, 2)
    if employees else 0
)

c1, c2 = st.columns(2)

c1.metric("Promotion Eligible Employees", promotion_count)
c2.metric("Promotion Eligibility Rate", f"{promotion_rate}%")

st.dataframe(
    eligible[
        [
            "Employee_Name",
            "Department",
            "Performance_Rating",
            "Attendance_Percentage",
            "Salary"
        ]
    ],
    use_container_width=True,
    hide_index=True
)

st.divider()

# ==========================================================
# PAYROLL FORECAST
# ==========================================================

section(
    "Payroll Budget Forecast",
    "Estimate payroll growth after hiring expansion and salary increments."
)

current_payroll = df["Salary"].sum()

projected_payroll = current_payroll * (
    1 + growth_rate / 100
) * (
    1 + salary_growth / 100
)

budget_df = pd.DataFrame({
    "Scenario": [
        "Current Payroll",
        "Projected Payroll"
    ],
    "Payroll Amount": [
        current_payroll,
        projected_payroll
    ]
})

fig = px.bar(
    budget_df,
    x="Scenario",
    y="Payroll Amount",
    color="Scenario",
    text_auto=True,
    title="Payroll Budget Forecast"
)

fig.update_layout(template="plotly_dark", height=450)

st.plotly_chart(fig, use_container_width=True)

insight(
    "Payroll Forecast Insight",
    f"The payroll budget increases from ₹ {current_payroll:,.0f} to approximately ₹ {projected_payroll:,.0f} under the selected hiring and salary assumptions.",
    "Plan compensation budgets and finance approvals using projected payroll scenarios."
)

st.divider()

# ==========================================================
# EXECUTIVE AI SUMMARY
# ==========================================================

section(
    "Executive Workforce Planning Summary",
    "Business-ready summary of future workforce planning decisions."
)

top_dept = dept.sort_values(
    "Suggested Hiring",
    ascending=False
).iloc[0]["Department"]

st.markdown(f"""
### Workforce Planning Summary

**Forecast Period:** {forecast_months} Months

**Hiring Growth:** {growth_rate}%

**Projected Workforce Size:** {projected_employees[-1]:,} Employees

**Projected Payroll Budget:** ₹ {projected_payroll:,.0f}

### Key Business Recommendations

1. Prioritize hiring in **{top_dept}**.
2. Allocate recruitment budget based on projected workforce growth.
3. Increase retention efforts before projected attrition rises.
4. Fast-track promotion-ready employees to improve internal retention.
5. Align compensation planning with projected payroll growth.
""")

footer()