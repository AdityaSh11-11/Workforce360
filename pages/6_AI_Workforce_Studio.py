import streamlit as st
import pandas as pd

from styles.theme import load_theme, hero, footer
from styles.cards import section, insight, empty_state
from modules.data_loader import get_active_dataset
from components.sidebar import enterprise_sidebar
enterprise_sidebar()
# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(page_title="AI Workforce Studio", layout="wide")
load_theme()

hero(
    "AI Workforce Studio",
    "Generate HR insights, executive summaries, SQL queries and Power BI DAX formulas using your workforce dataset."
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
# CLEAN DATA
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

# ==========================================================
# TABS
# ==========================================================

tabs = st.tabs([
    "Executive Summary",
    "HR Recommendations",
    "SQL Generator",
    "Power BI DAX Generator",
    "Workforce Insights"
])

# ==========================================================
# TAB 1 : EXECUTIVE SUMMARY
# ==========================================================

with tabs[0]:

    section(
        "AI Executive Workforce Summary",
        "Automatically summarize workforce health for leadership."
    )

    employees = len(df)
    payroll = df["Salary"].sum()
    avg_salary = df["Salary"].mean()
    attendance = df["Attendance_Percentage"].mean()
    performance = df["Performance_Rating"].mean()

    attrition = (
        df["Attrition_Status"]
        .astype(str)
        .str.lower()
        .eq("left")
        .sum()
    )

    attrition_rate = round(attrition / employees * 100, 2)

    st.markdown(f"""
### Executive Summary

The workforce currently contains **{employees:,} employees** across
**{df['Department'].nunique()} departments** and
**{df['City'].nunique()} cities**.

**Key Workforce Indicators**

- Total Payroll: **₹ {payroll:,.0f}**
- Average Salary: **₹ {avg_salary:,.0f}**
- Average Attendance: **{attendance:.1f}%**
- Average Performance Rating: **{performance:.2f}/5**
- Attrition Rate: **{attrition_rate}%**

**Business Interpretation**

The organization maintains overall workforce productivity through attendance and performance metrics while attrition monitoring helps identify retention opportunities across departments.
""")

# ==========================================================
# TAB 2 : HR RECOMMENDATIONS
# ==========================================================

with tabs[1]:

    section(
        "AI HR Recommendations",
        "Business recommendations generated from workforce KPIs."
    )

    recommendations = []

    if attendance < 85:
        recommendations.append(
            "Improve attendance through flexible work policies and employee engagement initiatives."
        )

    if performance < 3.5:
        recommendations.append(
            "Launch department-specific coaching and training programs for underperforming employees."
        )

    if attrition_rate > 20:
        recommendations.append(
            "Implement retention interviews and salary benchmarking for high-risk departments."
        )

    if df["Training_Hours"].mean() < 20:
        recommendations.append(
            "Increase employee learning hours through structured development programs."
        )

    if len(recommendations) == 0:
        recommendations.append(
            "Current workforce indicators are healthy. Continue monitoring department-level trends."
        )

    for i, rec in enumerate(recommendations, start=1):
        st.markdown(f"**Recommendation {i}**")
        st.write(rec)
        st.divider()

# ==========================================================
# TAB 3 : SQL GENERATOR
# ==========================================================

with tabs[2]:

    section(
        "SQL Query Generator",
        "Generate PostgreSQL queries for common HR business questions."
    )

    query_type = st.selectbox(
        "Choose Business Query",
        [
            "Top Paid Employees",
            "Department Salary Average",
            "Employees with Low Attendance",
            "Attrition Employees",
            "Performance Leaders"
        ]
    )

    sql_queries = {
        "Top Paid Employees": """
SELECT employee_name, department, salary
FROM fact_workforce
ORDER BY salary DESC
LIMIT 10;
""",
        "Department Salary Average": """
SELECT department,
       ROUND(AVG(salary),2) AS average_salary
FROM fact_workforce
GROUP BY department
ORDER BY average_salary DESC;
""",
        "Employees with Low Attendance": """
SELECT employee_name,
       department,
       attendance_percentage
FROM fact_workforce
WHERE attendance_percentage < 75
ORDER BY attendance_percentage;
""",
        "Attrition Employees": """
SELECT employee_name,
       department,
       city,
       salary
FROM fact_workforce
WHERE LOWER(attrition_status)='left';
""",
        "Performance Leaders": """
SELECT employee_name,
       department,
       performance_rating
FROM fact_workforce
ORDER BY performance_rating DESC
LIMIT 20;
"""
    }

    st.code(sql_queries[query_type], language="sql")

    st.download_button(
        "Download SQL Query",
        sql_queries[query_type],
        file_name="hr_business_query.sql",
        use_container_width=True
    )

# ==========================================================
# TAB 4 : POWER BI DAX
# ==========================================================

with tabs[3]:

    section(
        "Power BI DAX Generator",
        "Generate reusable DAX measures for HR dashboards."
    )

    dax_type = st.selectbox(
        "Select DAX Measure",
        [
            "Average Salary",
            "Attrition Rate",
            "Average Attendance",
            "Average Performance",
            "Total Employees"
        ]
    )

    dax = {
        "Average Salary":
"""Average Salary =
AVERAGE(fact_workforce[salary])""",

        "Attrition Rate":
"""Attrition Rate =
DIVIDE(
CALCULATE(COUNTROWS(fact_workforce),
fact_workforce[attrition_status]="Left"),
COUNTROWS(fact_workforce)
)""",

        "Average Attendance":
"""Average Attendance =
AVERAGE(fact_workforce[attendance_percentage])""",

        "Average Performance":
"""Average Performance =
AVERAGE(fact_workforce[performance_rating])""",

        "Total Employees":
"""Total Employees =
COUNTROWS(fact_workforce)"""
    }

    st.code(dax[dax_type], language="sql")

    st.download_button(
        "Download DAX Measure",
        dax[dax_type],
        file_name="powerbi_measure.dax",
        use_container_width=True
    )

# ==========================================================
# TAB 5 : WORKFORCE INSIGHTS
# ==========================================================

with tabs[4]:

    section(
        "AI Workforce Insights",
        "Automatically identify workforce strengths and risks."
    )

    high_perf = (
        df["Performance_Rating"] >= 4.5
    ).sum()

    low_att = (
        df["Attendance_Percentage"] < 75
    ).sum()

    overtime = (
        df["Overtime_Hours"] > 30
    ).sum()

    promotion = (
        df["Promotion_Status"]
        .astype(str)
        .str.lower()
        .eq("promoted")
        .sum()
    )

    c1, c2 = st.columns(2)

    with c1:

        st.metric("High Performers", high_perf)
        st.metric("Low Attendance Employees", low_att)

    with c2:

        st.metric("High Overtime Employees", overtime)
        st.metric("Promoted Employees", promotion)

    st.divider()

    insight(
        "AI Workforce Interpretation",
        f"""
**High Performing Employees:** {high_perf}

**Low Attendance Employees:** {low_att}

**Employees with High Overtime:** {overtime}

**Promoted Employees:** {promotion}

These metrics highlight workforce productivity, employee engagement and potential burnout indicators.
        """,
        """
Use these indicators during monthly HR reviews to identify promotion candidates,
retention risks and workload balancing opportunities.
        """
    )

footer()