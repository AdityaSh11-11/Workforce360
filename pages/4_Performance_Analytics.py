import streamlit as st
import pandas as pd
import plotly.express as px

from styles.theme import load_theme, hero, footer
from styles.cards import section, kpi, filter_panel, insight, empty_state
from modules.data_loader import get_active_dataset
from components.sidebar import enterprise_sidebar

enterprise_sidebar()

st.set_page_config(page_title="Performance Analytics", layout="wide")
load_theme()

hero(
    "Performance Analytics Dashboard",
    "Employee performance, attendance, training effectiveness and productivity intelligence."
)
df = get_active_dataset()

if df is None or df.empty:
    empty_state("No workforce dataset available.")
    footer()
    st.stop()

numeric_cols = [
    "Performance_Rating",
    "Attendance_Percentage",
    "Training_Hours",
    "Overtime_Hours",
    "Salary",
    "Experience_Years"
]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

# Prevent Plotly NaN size errors
df["Training_Hours"] = df["Training_Hours"].clip(lower=1)

section(
    "Performance Filters",
    "Analyze workforce productivity using business filters."
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

rating_filter = c3.slider(
    "Minimum Performance Rating",
    1.0,
    5.0,
    1.0
)

filtered = df.copy()

if department != "All":
    filtered = filtered[filtered["Department"] == department]

if city != "All":
    filtered = filtered[filtered["City"] == city]

filtered = filtered[
    filtered["Performance_Rating"] >= rating_filter
]


section(
    "Performance KPI Overview",
    "Summary metrics for workforce productivity."
)

r1 = st.columns(4)

r1[0].metric(
    "Employees",
    len(filtered)
)

r1[1].metric(
    "Average Rating",
    f"{filtered['Performance_Rating'].mean():.2f}/5"
)

r1[2].metric(
    "Average Attendance",
    f"{filtered['Attendance_Percentage'].mean():.1f}%"
)

r1[3].metric(
    "Average Training Hours",
    f"{filtered['Training_Hours'].mean():.1f}"
)

st.divider()

section(
    "Performance Rating Distribution",
    "Distribution of employee performance ratings."
)

fig = px.histogram(
    filtered,
    x="Performance_Rating",
    nbins=8,
    color="Department",
    title="Performance Rating Distribution"
)

fig.update_layout(
    template="plotly_dark",
    height=480
)

st.plotly_chart(fig, use_container_width=True)

insight(
    "Performance Insight",
    "Performance ratings indicate workforce productivity distribution across departments.",
    "Departments with consistently lower ratings may require leadership review or training programs."
)

st.divider()


section(
    "Department Performance Comparison",
    "Average performance rating by department."
)

dept_perf = (
    filtered.groupby("Department")["Performance_Rating"]
    .mean()
    .reset_index()
    .sort_values("Performance_Rating", ascending=False)
)

fig = px.bar(
    dept_perf,
    x="Department",
    y="Performance_Rating",
    color="Performance_Rating",
    title="Average Performance Rating by Department"
)

fig.update_layout(
    template="plotly_dark",
    height=480
)

st.plotly_chart(fig, use_container_width=True)

st.divider()


section(
    "Attendance vs Performance",
    "Relationship between attendance, performance and training."
)

fig = px.scatter(
    filtered,
    x="Attendance_Percentage",
    y="Performance_Rating",
    size="Training_Hours",
    color="Department",
    hover_name="Employee_Name",
    title="Attendance vs Performance"
)

fig.update_layout(
    template="plotly_dark",
    height=550
)

st.plotly_chart(fig, use_container_width=True)

insight(
    "Attendance Insight",
    "Bubble size represents employee training hours completed.",
    "High attendance with low ratings indicates coaching opportunities. High attendance with high ratings indicates high-performing employees."
)

st.divider()


section(
    "Training Effectiveness Analysis",
    "Compare training hours against employee performance."
)

fig = px.scatter(
    filtered,
    x="Training_Hours",
    y="Performance_Rating",
    color="Department",
    hover_name="Employee_Name",
    title="Training Hours vs Performance Rating"
)

fig.update_layout(
    template="plotly_dark",
    height=520
)

st.plotly_chart(fig, use_container_width=True)

insight(
    "Training Effectiveness Insight",
    "Employees receiving more training should demonstrate performance improvement over time.",
    "Departments with high training investment but low performance should review training quality."
)

st.divider()


section(
    "Overtime Analysis",
    "Relationship between overtime workload and employee performance."
)

fig = px.scatter(
    filtered,
    x="Overtime_Hours",
    y="Performance_Rating",
    color="Department",
    hover_name="Employee_Name",
    title="Overtime Hours vs Performance Rating"
)

fig.update_layout(
    template="plotly_dark",
    height=520
)

st.plotly_chart(fig, use_container_width=True)

insight(
    "Overtime Insight",
    "This visualization helps identify whether excessive overtime impacts employee productivity.",
    "Employees with excessive overtime and declining ratings may be at burnout risk."
)

st.divider()


section(
    "Experience vs Performance",
    "Compare employee experience against performance ratings."
)

fig = px.box(
    filtered,
    x="Experience_Group",
    y="Performance_Rating",
    color="Experience_Group",
    title="Performance by Experience Group"
)

fig.update_layout(
    template="plotly_dark",
    height=500
)

st.plotly_chart(fig, use_container_width=True)

st.divider()


section(
    "Top Performing Employees",
    "Employees with the highest performance ratings."
)

top = filtered.sort_values(
    ["Performance_Rating", "Attendance_Percentage"],
    ascending=False
).head(15)

st.dataframe(
    top[
        [
            "Employee_Name",
            "Department",
            "City",
            "Performance_Rating",
            "Attendance_Percentage",
            "Training_Hours",
            "Salary",
        ]
    ],
    use_container_width=True,
    hide_index=True,
)

insight(
    "Top Performer Insight",
    "These employees consistently demonstrate strong attendance and high performance.",
    "Consider these employees for promotion planning, mentoring and leadership development."
)

st.divider()


section(
    "Performance Watchlist",
    "Employees requiring performance improvement attention."
)

watchlist = filtered[
    (filtered["Performance_Rating"] <= 2.5)
    | (filtered["Attendance_Percentage"] <= 70)
]

st.dataframe(
    watchlist[
        [
            "Employee_Name",
            "Department",
            "City",
            "Attendance_Percentage",
            "Performance_Rating",
            "Training_Hours",
            "Overtime_Hours",
        ]
    ],
    use_container_width=True,
    hide_index=True,
)

insight(
    "Watchlist Insight",
    "Employees on this list show lower attendance or lower performance ratings.",
    "HR managers should initiate coaching, training or workload reviews for these employees."
)

footer()
