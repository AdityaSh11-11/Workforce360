import streamlit as st
import pandas as pd
from io import BytesIO

from styles.theme import load_theme, hero, footer
from styles.cards import section, empty_state
from modules.data_loader import get_active_dataset
from components.sidebar import enterprise_sidebar

enterprise_sidebar()

st.set_page_config(
    page_title="Export Center",
    layout="wide"
)

load_theme()

hero(
    "Workforce Export Center",
    "Export workforce datasets, executive reports and Power BI-ready files."
)

df = get_active_dataset()

if df is None or df.empty:
    empty_state("No workforce dataset available.")
    footer()
    st.stop()

def create_excel(dataframe):
    output = BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        dataframe.to_excel(
            writer,
            sheet_name="Workforce_Data",
            index=False
        )

    output.seek(0)
    return output

csv_data = df.to_csv(index=False).encode("utf-8")
excel_data = create_excel(df)

section(
    "Dataset Export",
    "Download workforce datasets in multiple business-ready formats."
)

c1, c2 = st.columns(2)

with c1:
    st.download_button(
        "Download Workforce CSV",
        csv_data,
        "workforce_dataset.csv",
        "text/csv",
        use_container_width=True
    )

with c2:
    st.download_button(
        "Download Workforce Excel",
        excel_data,
        "workforce_dataset.xlsx",
        use_container_width=True
    )

st.divider()

section(
    "Executive Workforce Report",
    "Download an executive KPI summary for business stakeholders."
)

salary = pd.to_numeric(df["Salary"], errors="coerce").fillna(0)
attendance = pd.to_numeric(df["Attendance_Percentage"], errors="coerce").fillna(0)
performance = pd.to_numeric(df["Performance_Rating"], errors="coerce").fillna(0)

employees = len(df)
avg_salary = salary.mean()
payroll = salary.sum()
avg_attendance = attendance.mean()
avg_performance = performance.mean()

active = (
    df["Attrition_Status"]
    .astype(str)
    .str.lower()
    .eq("active")
    .sum()
)

attrition_rate = round(((employees - active) / employees) * 100, 2)

summary_df = pd.DataFrame({
    "Metric": [
        "Total Employees",
        "Departments",
        "Cities",
        "Total Payroll",
        "Average Salary",
        "Average Attendance",
        "Average Performance Rating",
        "Attrition Rate"
    ],
    "Value": [
        employees,
        df["Department"].nunique(),
        df["City"].nunique(),
        f"₹ {payroll:,.0f}",
        f"₹ {avg_salary:,.0f}",
        f"{avg_attendance:.1f}%",
        f"{avg_performance:.2f}/5",
        f"{attrition_rate}%"
    ]
})

st.dataframe(summary_df, use_container_width=True, hide_index=True)

summary_excel = create_excel(summary_df)

st.download_button(
    "Download Executive KPI Report (Excel)",
    summary_excel,
    "executive_workforce_report.xlsx",
    use_container_width=True
)

st.divider()

section(
    "Power BI Export",
    "Export a clean workforce table optimized for Microsoft Power BI."
)

powerbi_df = df.copy()

powerbi_df.columns = [
    c.lower().replace(" ", "_")
    for c in powerbi_df.columns
]

powerbi_csv = powerbi_df.to_csv(index=False).encode("utf-8")

st.download_button(
    "Download Power BI Dataset",
    powerbi_csv,
    "powerbi_workforce_dataset.csv",
    "text/csv",
    use_container_width=True
)

st.caption(
    "This dataset is formatted for direct import into Microsoft Power BI."
)

st.divider()
section(
    "Department-wise Reports",
    "Export individual department datasets."
)

departments = sorted(df["Department"].dropna().unique())

selected_dept = st.selectbox(
    "Select Department",
    departments
)

dept_df = df[df["Department"] == selected_dept]

st.dataframe(
    dept_df.head(15),
    use_container_width=True,
    hide_index=True
)

dept_csv = dept_df.to_csv(index=False).encode("utf-8")

st.download_button(
    f"Download {selected_dept} Dataset",
    dept_csv,
    f"{selected_dept.lower() if selected_dept else 'department'}_employees.csv",
    "text/csv",
    use_container_width=True
)

st.divider()

section(
    "Location-wise Reports",
    "Export workforce records for a selected city."
)

cities = sorted(df["City"].dropna().unique())

selected_city = st.selectbox(
    "Select City",
    cities
)

city_df = df[df["City"] == selected_city]

st.dataframe(
    city_df.head(15),
    use_container_width=True,
    hide_index=True
)

city_csv = city_df.to_csv(index=False).encode("utf-8")

st.download_button(
    f"Download {selected_city} Workforce",
    city_csv,
    f"{selected_city.lower() if selected_city else 'city'}_workforce.csv",
    "text/csv",
    use_container_width=True
)

st.divider()

section(
    "Attrition Report",
    "Download only employees marked as Left."
)

attrition_df = df[
    df["Attrition_Status"].astype(str).str.lower() == "left"
]

st.dataframe(
    attrition_df.head(15),
    use_container_width=True,
    hide_index=True
)

attrition_csv = attrition_df.to_csv(index=False).encode("utf-8")

st.download_button(
    "Download Attrition Dataset",
    attrition_csv,
    "attrition_employees.csv",
    "text/csv",
    use_container_width=True
)

st.divider()

section(
    "Current Active Dataset",
    "Preview the active workforce dataset before exporting."
)

st.dataframe(
    df.head(20),
    use_container_width=True,
    hide_index=True
)

footer()
