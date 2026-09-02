import streamlit as st
import pandas as pd

from styles.theme import load_theme, hero, footer
from styles.cards import section, insight, empty_state
from modules.data_loader import get_active_dataset
from components.sidebar import enterprise_sidebar

enterprise_sidebar()


st.set_page_config(
    page_title="SQL & Power BI Center",
    layout="wide"
)

load_theme()

hero(
    "SQL & Power BI Analytics Center",
    "Generate PostgreSQL queries, Power BI DAX measures and BI-ready workforce reports."
)


df = get_active_dataset()

if df is None or df.empty:
    empty_state("No workforce dataset available.")
    footer()
    st.stop()


numeric_cols = [
    "Salary",
    "Attendance_Percentage",
    "Performance_Rating",
    "Experience_Years",
    "Training_Hours",
    "Overtime_Hours",
    "Age"
]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)


tab1, tab2, tab3, tab4 = st.tabs([
    "PostgreSQL Queries",
    "Power BI DAX Studio",
    "HR KPI Formula Library",
    "Business Intelligence Guide"
])


with tab1:

    section(
        "Enterprise SQL Query Generator",
        "Ready-to-use PostgreSQL queries for HR analytics dashboards."
    )

    sql_option = st.selectbox(
        "Select HR Business Query",
        [
            "Top Paid Employees",
            "Average Salary by Department",
            "Department Employee Count",
            "Employees with Low Attendance",
            "Attrition Employees",
            "Promotion Eligible Employees",
            "Top Performers",
            "Training Hours by Department",
            "Overtime Analysis",
            "Hiring Trend by Year"
        ]
    )

    SQL_LIBRARY = {

        "Top Paid Employees":
"""
SELECT employee_name,
       department,
       salary
FROM fact_workforce
ORDER BY salary DESC
LIMIT 10;
""",

        "Average Salary by Department":
"""
SELECT department,
ROUND(AVG(salary),2) AS average_salary
FROM fact_workforce
GROUP BY department
ORDER BY average_salary DESC;
""",

        "Department Employee Count":
"""
SELECT department,
COUNT(*) AS employees
FROM fact_workforce
GROUP BY department
ORDER BY employees DESC;
""",

        "Employees with Low Attendance":
"""
SELECT employee_name,
department,
attendance_percentage
FROM fact_workforce
WHERE attendance_percentage < 75
ORDER BY attendance_percentage ASC;
""",

        "Attrition Employees":
"""
SELECT employee_name,
department,
city,
salary
FROM fact_workforce
WHERE LOWER(attrition_status)='left';
""",

        "Promotion Eligible Employees":
"""
SELECT employee_name,
department,
performance_rating,
attendance_percentage
FROM fact_workforce
WHERE performance_rating >=4.5
AND attendance_percentage >=90;
""",

        "Top Performers":
"""
SELECT employee_name,
department,
performance_rating
FROM fact_workforce
ORDER BY performance_rating DESC
LIMIT 20;
""",

        "Training Hours by Department":
"""
SELECT department,
ROUND(AVG(training_hours),1) AS avg_training_hours
FROM fact_workforce
GROUP BY department
ORDER BY avg_training_hours DESC;
""",

        "Overtime Analysis":
"""
SELECT employee_name,
department,
overtime_hours,
performance_rating
FROM fact_workforce
ORDER BY overtime_hours DESC;
""",

        "Hiring Trend by Year":
"""
SELECT joining_year,
COUNT(*) AS employees_joined
FROM fact_workforce
GROUP BY joining_year
ORDER BY joining_year;
"""
    }

    sql = SQL_LIBRARY[sql_option]

    st.code(sql, language="sql")

    st.download_button(
        "Download SQL Query",
        sql,
        file_name="workforce_query.sql",
        use_container_width=True
    )

    insight(
        "Business Usage",
        "These PostgreSQL queries can be executed directly against the InsightForge AI warehouse for reporting and dashboard development."
    )


with tab2:

    section(
        "Power BI DAX Measure Generator",
        "Generate reusable DAX measures for HR dashboards."
    )

    dax_option = st.selectbox(
        "Select Power BI Measure",
        [
            "Total Employees",
            "Average Salary",
            "Total Payroll",
            "Average Attendance",
            "Average Performance Rating",
            "Attrition Rate",
            "Promotion Rate",
            "Average Training Hours",
            "Average Overtime Hours"
        ]
    )

    DAX_LIBRARY = {

        "Total Employees":
"""
Total Employees =
COUNTROWS(fact_workforce)
""",

        "Average Salary":
"""
Average Salary =
AVERAGE(fact_workforce[salary])
""",

        "Total Payroll":
"""
Total Payroll =
SUM(fact_workforce[salary])
""",

        "Average Attendance":
"""
Average Attendance =
AVERAGE(fact_workforce[attendance_percentage])
""",

        "Average Performance Rating":
"""
Average Performance =
AVERAGE(fact_workforce[performance_rating])
""",

        "Attrition Rate":
"""
Attrition Rate =
DIVIDE(
CALCULATE(
COUNTROWS(fact_workforce),
fact_workforce[attrition_status]="Left"
),
COUNTROWS(fact_workforce)
)
""",

        "Promotion Rate":
"""
Promotion Rate =
DIVIDE(
CALCULATE(
COUNTROWS(fact_workforce),
fact_workforce[promotion_status]="Promoted"
),
COUNTROWS(fact_workforce)
)
""",

        "Average Training Hours":
"""
Average Training Hours =
AVERAGE(fact_workforce[training_hours])
""",

        "Average Overtime Hours":
"""
Average Overtime Hours =
AVERAGE(fact_workforce[overtime_hours])
"""
    }

    dax = DAX_LIBRARY[dax_option]

    st.code(dax, language="sql")

    st.download_button(
        "Download DAX Measure",
        dax,
        file_name="powerbi_measure.dax",
        use_container_width=True
    )

    insight(
        "Business Usage",
        "Use these DAX measures directly in Microsoft Power BI visuals, KPI cards and executive dashboards."
    )


with tab3:

    section(
        "HR KPI Formula Library",
        "Common HR metrics used by enterprise dashboards."
    )

    formulas = pd.DataFrame({
        "KPI": [
            "Attrition Rate",
            "Promotion Rate",
            "Average Salary",
            "Average Attendance",
            "Payroll Cost",
            "Training Hours per Employee",
            "Average Performance Rating",
            "Department Headcount",
            "Retention Rate"
        ],

        "Business Formula": [
            "Employees Left ÷ Total Employees × 100",
            "Promoted Employees ÷ Total Employees × 100",
            "Total Salary ÷ Total Employees",
            "Average Attendance Percentage",
            "Sum of Employee Salaries",
            "Total Training Hours ÷ Total Employees",
            "Average Performance Rating",
            "Employees grouped by Department",
            "Active Employees ÷ Total Employees × 100"
        ]
    })

    st.dataframe(
        formulas,
        use_container_width=True,
        hide_index=True
    )

    csv = formulas.to_csv(index=False).encode("utf-8")

    st.download_button(
        "Download KPI Library",
        csv,
        file_name="hr_kpi_library.csv",
        mime="text/csv",
        use_container_width=True
    )


with tab4:

    section(
        "Business Intelligence Implementation Guide",
        "Recommended Power BI visuals for enterprise workforce analytics."
    )

    guide = pd.DataFrame({
        "Dashboard": [
            "Executive Dashboard",
            "Employee Analytics",
            "Performance Dashboard",
            "Attrition Intelligence",
            "Payroll Dashboard",
            "Training Dashboard",
            "Recruitment Dashboard"
        ],

        "Recommended Power BI Visuals": [
            "KPI Cards, Bar Charts, Line Charts",
            "Pie Charts, Maps, Tables",
            "Scatter Plot, Box Plot, Heatmap",
            "Donut Chart, Stacked Bar Chart",
            "Tree Map, Column Chart",
            "Scatter Plot, Histogram",
            "Line Chart, Area Chart"
        ],

        "Business Purpose": [
            "Organization-level workforce KPIs.",
            "Employee demographics and workforce composition.",
            "Employee productivity and performance benchmarking.",
            "Retention and employee exit analysis.",
            "Compensation and payroll monitoring.",
            "Learning effectiveness analysis.",
            "Hiring trend and workforce expansion analysis."
        ]
    })

    st.dataframe(
        guide,
        use_container_width=True,
        hide_index=True
    )

    st.markdown("---")

    st.markdown("### Recommended Power BI Pages")

    st.markdown("""
1. Executive Workforce Dashboard
2. Employee Demographics Dashboard
3. Department Performance Dashboard
4. Payroll & Compensation Dashboard
5. Attrition Intelligence Dashboard
6. Recruitment & Hiring Dashboard
7. AI Workforce Insights Dashboard
""")

    insight(
        "Power BI Deployment Recommendation",
        "Import the Power BI-ready CSV from Export Center and use these DAX measures to build executive dashboards with interactive slicers and KPI cards."
    )

footer()
