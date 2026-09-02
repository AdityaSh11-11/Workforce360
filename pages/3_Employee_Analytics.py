import streamlit as st
import pandas as pd
import plotly.express as px

from styles.theme import load_theme, hero, footer
from styles.cards import section, kpi, filter_panel, insight, empty_state
from modules.data_loader import get_active_dataset
from components.sidebar import enterprise_sidebar

enterprise_sidebar()

st.set_page_config(page_title="Employee Analytics", layout="wide")
load_theme()

hero(
    "Employee Analytics",
    "Explore employee demographics, salary, attendance, experience and individual workforce profiles."
)


df = get_active_dataset()

if df is None or df.empty:
    empty_state("No workforce dataset available.")
    footer()
    st.stop()


numeric_cols = [
    "Age",
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


section(
    "Employee Filters",
    "Filter employees by department, city, gender and employment type."
)

filter_panel()

c1, c2, c3, c4 = st.columns(4)

department = c1.selectbox(
    "Department",
    ["All"] + sorted(df["Department"].dropna().unique().tolist())
)

city = c2.selectbox(
    "City",
    ["All"] + sorted(df["City"].dropna().unique().tolist())
)

gender = c3.selectbox(
    "Gender",
    ["All"] + sorted(df["Gender"].dropna().unique().tolist())
)

employment = c4.selectbox(
    "Employment Type",
    ["All"] + sorted(df["Employment_Type"].dropna().unique().tolist())
)

filtered = df.copy()

if department != "All":
    filtered = filtered[filtered["Department"] == department]

if city != "All":
    filtered = filtered[filtered["City"] == city]

if gender != "All":
    filtered = filtered[filtered["Gender"] == gender]

if employment != "All":
    filtered = filtered[filtered["Employment_Type"] == employment]

st.divider()


section(
    "Workforce Summary",
    "High-level employee metrics after applying filters."
)

r1 = st.columns(4)

with r1[0]:
    kpi("Employees", len(filtered), "Filtered Workforce")

with r1[1]:
    kpi("Average Age", round(filtered["Age"].mean(), 1))

with r1[2]:
    kpi("Average Salary", f"₹ {filtered['Salary'].mean():,.0f}")

with r1[3]:
    kpi("Average Experience", f"{filtered['Experience_Years'].mean():.1f} Years")

st.divider()

section(
    "Employee Demographics",
    "Understand workforce composition by gender and age."
)

left, right = st.columns(2)

with left:

    gender_df = (
        filtered.groupby("Gender")
        .size()
        .reset_index(name="Employees")
    )

    fig = px.pie(
        gender_df,
        names="Gender",
        values="Employees",
        title="Gender Distribution"
    )

    fig.update_layout(template="plotly_dark", height=420)

    st.plotly_chart(fig, use_container_width=True)

with right:

    fig = px.histogram(
        filtered,
        x="Age",
        nbins=20,
        title="Age Distribution"
    )

    fig.update_layout(template="plotly_dark", height=420)

    st.plotly_chart(fig, use_container_width=True)

insight(
    "Demographic Insight",
    "Age and gender distribution help HR teams monitor workforce diversity and workforce planning."
)

st.divider()

section(
    "Salary Intelligence",
    "Analyze salary distribution across departments and experience groups."
)

left, right = st.columns(2)

with left:

    dept_salary = (
        filtered.groupby("Department")["Salary"]
        .mean()
        .reset_index()
        .sort_values("Salary", ascending=False)
    )

    fig = px.bar(
        dept_salary,
        x="Department",
        y="Salary",
        color="Salary",
        title="Average Salary by Department"
    )

    fig.update_layout(template="plotly_dark", height=450)

    st.plotly_chart(fig, use_container_width=True)

with right:

    fig = px.box(
        filtered,
        x="Experience_Group",
        y="Salary",
        color="Experience_Group",
        title="Salary Distribution by Experience Group"
    )

    fig.update_layout(template="plotly_dark", height=450)

    st.plotly_chart(fig, use_container_width=True)

insight(
    "Salary Insight",
    "Departments with unusually high salary averages typically represent specialized roles or senior workforce segments.",
    "Use salary benchmarking for compensation planning and internal pay equity reviews."
)

st.divider()

section(
    "Attendance and Performance",
    "Compare employee attendance with performance ratings."
)

bubble = filtered.copy()

bubble["Training_Hours"] = bubble["Training_Hours"].clip(lower=1)

fig = px.scatter(
    bubble,
    x="Attendance_Percentage",
    y="Performance_Rating",
    color="Department",
    size="Training_Hours",
    hover_name="Employee_Name",
    title="Attendance vs Performance"
)

fig.update_layout(template="plotly_dark", height=550)

st.plotly_chart(fig, use_container_width=True)

insight(
    "Attendance Insight",
    "Employees with consistently high attendance but lower performance may require coaching rather than attendance interventions.",
    "Use this chart to identify high-potential employees with improving performance after training."
)

st.divider()



section(
    "Experience Distribution",
    "Employee distribution across experience categories."
)

exp = (
    filtered.groupby("Experience_Group")
    .size()
    .reset_index(name="Employees")
)

fig = px.bar(
    exp,
    x="Experience_Group",
    y="Employees",
    color="Employees",
    title="Employees by Experience Group"
)

fig.update_layout(template="plotly_dark", height=450)

st.plotly_chart(fig, use_container_width=True)

st.divider()


section(
    "Employee Directory",
    "Search and view individual employee profiles."
)

employee_name = st.selectbox(
    "Select Employee",
    sorted(filtered["Employee_Name"].dropna().unique().tolist())
)

emp = filtered[filtered["Employee_Name"] == employee_name].iloc[0]

c1, c2 = st.columns(2)

with c1:
    st.metric("Employee ID", emp["Employee_ID"])
    st.metric("Department", emp["Department"])
    st.metric("Job Role", emp["Job_Role"])
    st.metric("Employment Type", emp["Employment_Type"])

with c2:
    st.metric("Salary", f"₹ {emp['Salary']:,.0f}")
    st.metric("Experience", f"{emp['Experience_Years']} Years")
    st.metric("Attendance", f"{emp['Attendance_Percentage']}%")
    st.metric("Performance", f"{emp['Performance_Rating']}/5")

st.markdown("### Employee Information")

info = pd.DataFrame({
    "Attribute": [
        "Gender",
        "Age",
        "Email",
        "Phone",
        "City",
        "State",
        "Joining Date",
        "Promotion Status",
        "Attrition Status",
        "Training Hours",
        "Overtime Hours",
    ],
    "Value": [
        emp["Gender"],
        emp["Age"],
        emp["Email"],
        emp["Phone"],
        emp["City"],
        emp["State"],
        emp["Joining_Date"].date(),
        emp["Promotion_Status"],
        emp["Attrition_Status"],
        emp["Training_Hours"],
        emp["Overtime_Hours"],
    ]
})

st.dataframe(info, use_container_width=True, hide_index=True)

st.divider()


section(
    "Complete Employee Dataset",
    "View and search all employees currently available in the active dataset."
)

search = st.text_input("Search Employee Name")

table = filtered.copy()

if search:
    table = table[
        table["Employee_Name"].str.contains(search, case=False, na=False)
    ]

st.dataframe(table, use_container_width=True, hide_index=True)

footer()
