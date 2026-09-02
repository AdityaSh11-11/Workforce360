import streamlit as st
import pandas as pd
import plotly.express as px

from styles.theme import load_theme, hero, footer
from styles.cards import section, kpi, dataset_card, insight
from components.sidebar import enterprise_sidebar

from modules.data_loader import (
    load_dataset,
    save_session_dataset,
    dataset_quality
)

from modules.warehouse import (
    load_workforce,
    clear_workforce_data,
    warehouse_record_count
)

from modules.audit_engine import write_log
import streamlit.components.v1 as components
st.set_page_config(
    page_title="Workforce Data Ingestion",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

load_theme()
enterprise_sidebar()

hero(
    "Workforce Data Ingestion",
    "Enterprise ETL Pipeline • CSV & Excel Upload • PostgreSQL Warehouse • Power BI Integration"
)


default_session = {
    "dataset": None,
    "dataset_name": "No Dataset Loaded",
    "dataset_type": "Unknown",
    "quality": {},
    "ai_report": None
}

for key, value in default_session.items():
    if key not in st.session_state:
        st.session_state[key] = value


try:
    warehouse_records = warehouse_record_count()
    warehouse_status = "Connected"
except Exception:
    warehouse_records = 0
    warehouse_status = "Disconnected"

section(
    "Platform Warehouse Status",
    "Current PostgreSQL warehouse connection and storage overview."
)

c1, c2, c3, c4 = st.columns(4)

with c1:
    kpi("", "Warehouse Status", warehouse_status)

with c2:
    kpi("", "Stored Records", f"{warehouse_records:,}")

with c3:
    kpi("", "Upload Modes", "2 Available")

with c4:
    kpi("", "Power BI Sync", "Ready")

st.divider()


section(
    "Choose Dataset Loading Mode",
    "Select how the uploaded dataset should be used inside InsightForge AI."
)

upload_mode = st.radio(
    "Select Mode",
    [
        "Direct Upload (Dashboards Only)",
        "Upload into PostgreSQL Warehouse"
    ],
    horizontal=True
)

if upload_mode == "Direct Upload (Dashboards Only)":
    st.info(
        "The dataset will be stored only in the current Streamlit session. All dashboards will use this dataset instantly without writing anything into PostgreSQL."
    )
else:
    st.success(
        "The dataset will be permanently stored inside the PostgreSQL Workforce Warehouse and will automatically be available for Power BI after refresh."
    )

st.divider()

section(
    "Upload Workforce Dataset",
    "Supported formats: CSV (.csv), Excel (.xlsx, .xls). The application automatically validates and standardizes the uploaded dataset."
)

uploaded_file = st.file_uploader(
    "Select Workforce Dataset",
    type=["csv", "xlsx", "xls"],
    help="Upload a workforce dataset containing employee, salary, attendance, performance and attrition information."
)

if uploaded_file is not None:

    result = load_dataset(uploaded_file)

    if result["status"]:

        save_session_dataset(
            result["data"],
            uploaded_file.name,
            uploaded_file.name.split(".")[-1].upper()
        )

        st.session_state.quality = result["quality"]

        write_log(
            "Dataset Uploaded",
            uploaded_file.name,
            len(result["data"])
        )

        st.success(
            f"Dataset '{uploaded_file.name}' loaded successfully into InsightForge AI."
        )

    else:
        st.error(result["message"])

st.divider()


section(
    "Manual Employee Entry",
    "Create workforce records manually without uploading a CSV or Excel file."
)

with st.expander("Open Employee Registration Form", expanded=False):

    col1, col2 = st.columns(2)

    with col1:

        emp_id = st.text_input("Employee ID", placeholder="EMP10001")
        name = st.text_input("Employee Name", placeholder="John Smith")

        gender = st.selectbox(
            "Gender",
            ["Male", "Female", "Other"]
        )

        age = st.number_input(
            "Age",
            min_value=18,
            max_value=70,
            value=25
        )

        email = st.text_input(
            "Email",
            placeholder="john@email.com"
        )

        phone = st.text_input(
            "Phone Number",
            placeholder="+91XXXXXXXXXX"
        )

        department = st.selectbox(
            "Department",
            [
                "Engineering",
                "Sales",
                "Finance",
                "Marketing",
                "HR",
                "Operations",
                "Customer Support",
                "IT",
                "Legal",
                "Administration"
            ]
        )

        role = st.text_input(
            "Job Role",
            placeholder="Software Engineer"
        )

    with col2:

        city = st.text_input("City", placeholder="Bengaluru")
        state = st.text_input("State", placeholder="Karnataka")

        joining = st.date_input("Joining Date")

        employment = st.selectbox(
            "Employment Type",
            ["Full-Time", "Part-Time", "Contract", "Intern"]
        )

        salary = st.number_input(
            "Annual Salary (₹)",
            min_value=0,
            max_value=10000000,
            value=500000,
            step=50000
        )

        experience = st.number_input(
            "Experience (Years)",
            min_value=0.0,
            max_value=40.0,
            value=2.0,
            step=0.5
        )

        attendance = st.slider(
            "Attendance Percentage",
            0.0,
            100.0,
            95.0
        )

        performance = st.slider(
            "Performance Rating",
            1.0,
            5.0,
            4.0
        )

    st.markdown("---")

    c1, c2 = st.columns(2)

    with c1:
        training = st.number_input(
            "Training Hours",
            0.0,
            500.0,
            20.0
        )

    with c2:
        overtime = st.number_input(
            "Overtime Hours",
            0.0,
            300.0,
            5.0
        )

    promotion = st.selectbox(
        "Promotion Status",
        ["Promoted", "Not Promoted"]
    )

    attrition = st.selectbox(
        "Attrition Status",
        ["Active", "Left"]
    )

    st.markdown("")

    if st.button(
        "Add Employee to Current Dataset",
        use_container_width=True,
        type="primary"
    ):

        employee = pd.DataFrame([{
            "Employee_ID": emp_id,
            "Employee_Name": name,
            "Gender": gender,
            "Age": age,
            "Email": email,
            "Phone": phone,
            "Department": department,
            "Job_Role": role,
            "City": city,
            "State": state,
            "Joining_Date": joining,
            "Employment_Type": employment,
            "Salary": salary,
            "Experience_Years": experience,
            "Tenure_Years": experience,
            "Attendance_Percentage": attendance,
            "Performance_Rating": performance,
            "Training_Hours": training,
            "Overtime_Hours": overtime,
            "Promotion_Status": promotion,
            "Attrition_Status": attrition
        }])

        if st.session_state.dataset is None:

            save_session_dataset(
                employee,
                "Manual Workforce Dataset",
                "Manual"
            )

        else:

            updated_df = pd.concat(
                [st.session_state.dataset, employee],
                ignore_index=True
            )

            save_session_dataset(
                updated_df,
                "Manual Workforce Dataset",
                "Manual"
            )

        write_log(
            "Manual Employee Added",
            "Manual Workforce Dataset",
            1
        )

        st.success("Employee record added successfully.")

st.divider()


if st.session_state.dataset is not None:

    df = st.session_state.dataset.copy()
    quality = dataset_quality(df)
    st.session_state.quality = quality

    section(
        "Dataset Quality Overview",
        "Automatically generated quality assessment for the uploaded workforce dataset."
    )

    r1 = st.columns(4)

    with r1[0]:
        kpi("", "Total Records", f"{quality['rows']:,}")

    with r1[1]:
        kpi("", "Total Columns", str(quality["columns"]))

    with r1[2]:
        kpi("", "Missing Values", str(quality["missing_values"]))

    with r1[3]:
        kpi("", "Quality Score", f"{quality['score']}%")

    st.markdown("")

    dataset_card(
        st.session_state.dataset_name,
        st.session_state.dataset_type,
        len(df)
    )

    st.divider()


    section(
        "Dataset Information",
        "Basic metadata for the currently active workforce dataset."
    )

    info1, info2, info3 = st.columns(3)

    with info1:
        st.metric("Dataset Name", st.session_state.dataset_name)

    with info2:
        st.metric("Dataset Type", st.session_state.dataset_type)

    with info3:
        st.metric("Departments", df["Department"].nunique())

    info4, info5, info6 = st.columns(3)

    with info4:
        st.metric("Cities", df["City"].nunique())

    with info5:
        st.metric("Average Salary", f"₹ {int(df['Salary'].mean()):,}")

    with info6:
        st.metric(
            "Attrition Employees",
            int((df["Attrition_Status"] == "Left").sum())
        )

    st.divider()


    section(
        "Workforce Dataset Preview",
        "First 20 cleaned employee records after preprocessing."
    )

    st.dataframe(
        df.head(20),
        use_container_width=True,
        hide_index=True
    )

    st.divider()


    section(
        "Dataset Download Center",
        "Download the cleaned workforce dataset for Power BI, Excel or external reporting."
    )

    download_col1, download_col2 = st.columns(2)

    csv = df.to_csv(index=False).encode("utf-8")

    with download_col1:

        st.download_button(
            "Download Workforce Dataset (CSV)",
            data=csv,
            file_name="InsightForge_Workforce_Clean_Dataset.csv",
            mime="text/csv",
            use_container_width=True
        )

    with download_col2:

        st.download_button(
            "Download Preview Dataset",
            data=df.head(500).to_csv(index=False).encode("utf-8"),
            file_name="InsightForge_Workforce_Preview.csv",
            mime="text/csv",
            use_container_width=True
        )

    st.divider()


if st.session_state.dataset is not None:

    df = st.session_state.dataset.copy()

    section(
        "Workforce Data Quality Analytics",
        "Visual exploration of salary, attendance, performance, experience and attrition across the workforce."
    )


    col1, col2 = st.columns(2)

    with col1:

        fig = px.histogram(
            df,
            x="Salary",
            nbins=30,
            title="Salary Distribution",
            color_discrete_sequence=["#38BDF8"]
        )

        fig.update_layout(
            template="plotly_dark",
            height=360,
            margin=dict(l=20, r=20, t=60, b=20),
            paper_bgcolor="#111827",
            plot_bgcolor="#111827"
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:

        fig = px.histogram(
            df,
            x="Attendance_Percentage",
            nbins=20,
            title="Attendance Percentage Distribution",
            color_discrete_sequence=["#10B981"]
        )

        fig.update_layout(
            template="plotly_dark",
            height=360,
            margin=dict(l=20, r=20, t=60, b=20),
            paper_bgcolor="#111827",
            plot_bgcolor="#111827"
        )

        st.plotly_chart(fig, use_container_width=True)


    left, right = st.columns(2)

    with left:

        dept_salary = (
            df.groupby("Department", as_index=False)["Salary"]
            .mean()
            .sort_values("Salary", ascending=False)
        )

        fig = px.bar(
            dept_salary,
            x="Salary",
            y="Department",
            orientation="h",
            title="Average Salary by Department",
            color="Salary",
            color_continuous_scale="Blues"
        )

        fig.update_layout(
            template="plotly_dark",
            height=420,
            margin=dict(l=20, r=20, t=60, b=20),
            paper_bgcolor="#111827",
            plot_bgcolor="#111827",
            coloraxis_showscale=False
        )

        st.plotly_chart(fig, use_container_width=True)

    with right:

        dept_perf = (
            df.groupby("Department", as_index=False)["Performance_Rating"]
            .mean()
            .sort_values("Performance_Rating", ascending=False)
        )

        fig = px.bar(
            dept_perf,
            x="Department",
            y="Performance_Rating",
            title="Average Performance Rating by Department",
            color="Performance_Rating",
            color_continuous_scale="Tealgrn"
        )

        fig.update_layout(
            template="plotly_dark",
            height=420,
            margin=dict(l=20, r=20, t=60, b=20),
            paper_bgcolor="#111827",
            plot_bgcolor="#111827",
            coloraxis_showscale=False
        )

        st.plotly_chart(fig, use_container_width=True)

    section(
        "Attendance vs Performance Intelligence",
        "Bubble size represents employee training hours while color represents department."
    )

    scatter_df = df.copy()

    scatter_df["Training_Hours"] = pd.to_numeric(
        scatter_df["Training_Hours"], errors="coerce"
    ).fillna(1)

    scatter_df["Training_Hours"] = scatter_df["Training_Hours"].clip(lower=1)

    fig = px.scatter(
        scatter_df,
        x="Attendance_Percentage",
        y="Performance_Rating",
        size="Training_Hours",
        color="Department",
        hover_name="Employee_Name",
        title="Attendance, Performance & Training Relationship"
    )

    fig.update_layout(
        template="plotly_dark",
        height=560,
        margin=dict(l=20, r=20, t=60, b=20),
        paper_bgcolor="#111827",
        plot_bgcolor="#111827"
    )

    st.plotly_chart(fig, use_container_width=True)


    col1, col2 = st.columns(2)

    with col1:

        fig = px.scatter(
            df,
            x="Experience_Years",
            y="Salary",
            color="Department",
            size="Performance_Rating",
            hover_name="Employee_Name",
            title="Salary Growth vs Experience"
        )

        fig.update_layout(
            template="plotly_dark",
            height=420,
            margin=dict(l=20, r=20, t=60, b=20),
            paper_bgcolor="#111827",
            plot_bgcolor="#111827"
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:

        attrition = (
            df["Attrition_Status"]
            .value_counts()
            .reset_index()
        )

        attrition.columns = ["Status", "Employees"]

        fig = px.pie(
            attrition,
            names="Status",
            values="Employees",
            hole=0.65,
            title="Active vs Left Employees",
            color_discrete_sequence=["#10B981", "#EF4444"]
        )

        fig.update_layout(
            template="plotly_dark",
            height=420,
            margin=dict(l=20, r=20, t=60, b=20),
            paper_bgcolor="#111827",
            plot_bgcolor="#111827"
        )

        st.plotly_chart(fig, use_container_width=True)

    st.divider()


    section(
        "Business Insight Summary",
        "Automatically generated insights from the uploaded workforce dataset."
    )

    highest_salary_department = (
        df.groupby("Department")["Salary"]
        .mean()
        .idxmax()
    )

    highest_attrition_department = (
        df[df["Attrition_Status"] == "Left"]
        .groupby("Department")
        .size()
        .sort_values(ascending=False)
    )

    if len(highest_attrition_department) > 0:
        highest_attrition_department = highest_attrition_department.index[0]
    else:
        highest_attrition_department = "No Attrition"

    best_performance_department = (
        df.groupby("Department")["Performance_Rating"]
        .mean()
        .idxmax()
    )

    insight(
        "AI Workforce Quality Insights",
        f"""
• Highest Average Salary Department : **{highest_salary_department}**

• Highest Attrition Department : **{highest_attrition_department}**

• Best Performing Department : **{best_performance_department}**

• Average Workforce Salary : **₹ {int(df['Salary'].mean()):,}**

• Workforce Quality Score : **{st.session_state.quality['score']}%**
        """,
        """
HR leaders should prioritize retention strategies in departments with higher attrition,
expand learning programs for lower-performing teams, and use salary intelligence to balance payroll investments.
        """
    )

    st.divider()


    # section(
    #     "PostgreSQL Warehouse & Power BI Control Center",
    #     "Manage workforce data inside PostgreSQL and instantly access the Power BI Executive Dashboard."
    # )

    # records = warehouse_record_count()

    # status1, status2, status3 = st.columns(3)

    # with status1:
    #     kpi("", "Warehouse Records", f"{records:,}")

    # with status2:
    #     kpi("", "Warehouse Connection", "Connected")

    # with status3:
    #     kpi("", "Power BI Sync Status", "Ready")

    # st.markdown("---")

    # button1, button2, button3 = st.columns(3)


    # with button1:

    #     if st.button(
    #         "Load Dataset into PostgreSQL",
    #         use_container_width=True,
    #         type="primary"
    #     ):

    #         with st.spinner("Uploading workforce dataset into PostgreSQL Warehouse..."):

    #             dataset_id = load_workforce(
    #                 df,
    #                 st.session_state.dataset_name,
    #                 st.session_state.dataset_type,
    #                 float(st.session_state.quality["score"])
    #             )

    #         write_log(
    #             "Dataset Loaded into PostgreSQL",
    #             st.session_state.dataset_name,
    #             len(df)
    #         )

    #         st.success(
    #             f"Dataset successfully stored in PostgreSQL Warehouse. Dataset ID : {dataset_id}"
    #         )

    #         st.info(
    #             "Power BI will display the latest workforce data after clicking Refresh."
    #         )


    # with button2:

    #     if st.button(
    #         "Remove Dataset from PostgreSQL",
    #         use_container_width=True
    #     ):

    #         clear_workforce_data()

    #         write_log(
    #             "PostgreSQL Warehouse Cleared",
    #             "Workforce Warehouse",
    #             0
    #         )

    #         st.success(
    #             "All workforce records have been removed from PostgreSQL Warehouse."
    #         )

    #         st.warning(
    #             "After refreshing Power BI, the dashboard will become empty until a new dataset is uploaded."
    #         )

 

section(
    "Current Session Dataset Summary",
    "Quick overview of the dataset currently available inside Streamlit dashboards."
)

if st.session_state.dataset is not None:

    df = st.session_state.dataset.copy()

    summary = pd.DataFrame({
        "Dataset Property": [
            "Dataset Name",
            "Dataset Type",
            "Employees",
            "Departments",
            "Cities",
            "States",
            "Average Salary",
            "Average Attendance",
            "Average Performance",
            "Quality Score"
        ],
        "Value": [
            st.session_state.dataset_name,
            st.session_state.dataset_type,
            len(df),
            df["Department"].nunique(),
            df["City"].nunique(),
            df["State"].nunique(),
            f"₹ {int(df['Salary'].mean()):,}",
            f"{round(df['Attendance_Percentage'].mean(),2)}%",
            round(df["Performance_Rating"].mean(),2),
            f"{st.session_state.quality['score']}%"
        ]
    })

    st.dataframe(
        summary,
        use_container_width=True,
        hide_index=True
    )

else:

    st.warning("No dataset available in current session.")

st.divider()


section(
    "Reset Streamlit Workspace",
    "Clear only the current Streamlit session without deleting PostgreSQL warehouse data."
)

st.warning(
    """
    This action clears the dataset loaded inside Streamlit dashboards.

    PostgreSQL Warehouse data remains unchanged unless you use
    **Remove Dataset from PostgreSQL**.
    """
)

if st.button(
    "Reset Current Workspace",
    use_container_width=True
):

    session_keys = [
        "dataset",
        "dataset_name",
        "dataset_type",
        "quality",
        "ai_report"
    ]

    for key in session_keys:
        if key in st.session_state:
            del st.session_state[key]

    write_log(
        "Workspace Reset",
        "Current Session",
        0
    )

    st.success("Current Streamlit workspace cleared successfully.")
    st.rerun()

st.divider()


section(
    "InsightForge AI Platform Capabilities",
    "Enterprise features included inside the Workforce Intelligence Platform."
)

feature_col1, feature_col2 = st.columns(2)

with feature_col1:

    st.markdown(
        """
        #### Data Engineering

        - CSV & Excel Workforce Upload
        - Automatic Data Cleaning
        - Missing Value Validation
        - Dataset Quality Scoring
        - PostgreSQL Data Warehouse
        - Audit Logging
        """
    )

with feature_col2:

    st.markdown(
        """
        #### Business Intelligence

        - Workforce Analytics
        - Salary Intelligence
        - Attrition Intelligence
        - Performance Analytics
        - AI Workforce Insights
        - Live Power BI Integration
        """
