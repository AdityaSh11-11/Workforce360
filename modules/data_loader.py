import streamlit as st
import pandas as pd

# ==========================================================
# STANDARD WORKFORCE SCHEMA
# Compatible with CSV, Excel, Manual Entry and PostgreSQL
# ==========================================================

STANDARD_COLUMNS = {
    "employee id": "Employee_ID",
    "employeeid": "Employee_ID",
    "emp_id": "Employee_ID",
    "emp id": "Employee_ID",

    "employee name": "Employee_Name",
    "name": "Employee_Name",
    "full name": "Employee_Name",

    "gender": "Gender",
    "sex": "Gender",

    "age": "Age",

    "email": "Email",
    "mail": "Email",

    "phone": "Phone",
    "mobile": "Phone",

    "department": "Department",

    "job role": "Job_Role",
    "jobrole": "Job_Role",
    "role": "Job_Role",
    "designation": "Job_Role",

    "city": "City",
    "location": "City",

    "state": "State",

    "joining date": "Joining_Date",
    "joining_date": "Joining_Date",
    "joiningdate": "Joining_Date",
    "date of joining": "Joining_Date",

    "employment type": "Employment_Type",
    "employment_type": "Employment_Type",

    "salary": "Salary",

    "experience": "Experience_Years",
    "experience years": "Experience_Years",
    "experience_years": "Experience_Years",

    "tenure": "Tenure_Years",
    "tenure years": "Tenure_Years",
    "tenure_years": "Tenure_Years",

    "attendance": "Attendance_Percentage",
    "attendance percentage": "Attendance_Percentage",
    "attendance_percentage": "Attendance_Percentage",

    "performance": "Performance_Rating",
    "performance rating": "Performance_Rating",
    "performance_rating": "Performance_Rating",

    "training hours": "Training_Hours",
    "training_hours": "Training_Hours",

    "overtime hours": "Overtime_Hours",
    "overtime_hours": "Overtime_Hours",

    "promotion status": "Promotion_Status",
    "promotion_status": "Promotion_Status",

    "attrition": "Attrition_Status",
    "attrition status": "Attrition_Status",
    "attrition_status": "Attrition_Status",
}

REQUIRED_COLUMNS = [
    "Employee_ID",
    "Employee_Name",
    "Gender",
    "Age",
    "Email",
    "Phone",
    "Department",
    "Job_Role",
    "City",
    "State",
    "Joining_Date",
    "Employment_Type",
    "Salary",
    "Experience_Years",
    "Tenure_Years",
    "Attendance_Percentage",
    "Performance_Rating",
    "Training_Hours",
    "Overtime_Hours",
    "Promotion_Status",
    "Attrition_Status",
]

# ==========================================================
# COLUMN NORMALIZATION
# ==========================================================

def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:

    df = df.copy()

    df.columns = [
        str(col).strip().replace("_", " ").replace("-", " ").lower()
        for col in df.columns
    ]

    df.rename(columns=STANDARD_COLUMNS, inplace=True)

    return df


# ==========================================================
# CREATE MISSING COLUMNS
# ==========================================================

def ensure_schema(df: pd.DataFrame) -> pd.DataFrame:

    df = normalize_columns(df)

    defaults = {
        "Employee_ID": "",
        "Employee_Name": "Unknown",
        "Gender": "Unknown",
        "Age": 0,
        "Email": "Unknown",
        "Phone": "Unknown",
        "Department": "Unknown",
        "Job_Role": "Unknown",
        "City": "Unknown",
        "State": "Unknown",
        "Joining_Date": pd.Timestamp.today().date(),
        "Employment_Type": "Full-Time",
        "Salary": 0,
        "Experience_Years": 0,
        "Tenure_Years": 0,
        "Attendance_Percentage": 0,
        "Performance_Rating": 3,
        "Training_Hours": 0,
        "Overtime_Hours": 0,
        "Promotion_Status": "Not Promoted",
        "Attrition_Status": "Active",
    }

    for col in REQUIRED_COLUMNS:
        if col not in df.columns:
            df[col] = defaults[col]

    # ---------- Numeric ----------

    numeric_cols = [
        "Age",
        "Salary",
        "Experience_Years",
        "Tenure_Years",
        "Attendance_Percentage",
        "Performance_Rating",
        "Training_Hours",
        "Overtime_Hours",
    ]

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(defaults[col])

    # ---------- Date ----------

    df["Joining_Date"] = pd.to_datetime(
        df["Joining_Date"],
        errors="coerce"
    )

    df["Joining_Date"] = df["Joining_Date"].fillna(
        pd.Timestamp.today()
    )

    # ---------- Strings ----------

    string_cols = [
        "Employee_ID",
        "Employee_Name",
        "Gender",
        "Email",
        "Phone",
        "Department",
        "Job_Role",
        "City",
        "State",
        "Employment_Type",
        "Promotion_Status",
        "Attrition_Status",
    ]

    for col in string_cols:
        df[col] = (
            df[col]
            .astype(str)
            .replace("nan", defaults[col])
            .replace("None", defaults[col])
            .fillna(defaults[col])
            .str.strip()
        )

    # ---------- Auto Employee IDs ----------

    if (df["Employee_ID"] == "").any():

        missing = df["Employee_ID"] == ""

        df.loc[missing, "Employee_ID"] = [
            f"EMP{1000+i}"
            for i in range(missing.sum())
        ]

    # ---------- Derived Columns ----------

    df["Joining_Year"] = df["Joining_Date"].dt.year

    df["Joining_Month"] = df["Joining_Date"].dt.strftime("%b")

    df["Joining_Quarter"] = "Q" + (
        ((df["Joining_Date"].dt.month - 1) // 3 + 1)
        .astype(int)
        .astype(str)
    )

    df["Salary_Band"] = pd.cut(
        df["Salary"],
        bins=[-1,40000,70000,100000,999999999],
        labels=["Low","Medium","High","Executive"]
    ).astype(str)

    df["Experience_Group"] = pd.cut(
        df["Experience_Years"],
        bins=[-1,2,5,10,20,100],
        labels=[
            "0-2 Years",
            "3-5 Years",
            "6-10 Years",
            "11-20 Years",
            "20+ Years"
        ]
    ).astype(str)

    return df[REQUIRED_COLUMNS + [
        "Salary_Band",
        "Experience_Group",
        "Joining_Year",
        "Joining_Month",
        "Joining_Quarter"
    ]]


# ==========================================================
# QUALITY REPORT
# ==========================================================

def dataset_quality(df: pd.DataFrame):

    quality = {
        "rows": len(df),
        "columns": len(df.columns),
        "missing_values": int(df.isna().sum().sum()),
        "duplicate_rows": int(df.duplicated().sum()),
    }

    score = 100

    score -= quality["missing_values"] * 0.05
    score -= quality["duplicate_rows"] * 2

    quality["score"] = int(round(max(score, 0), 1))

    return quality


# ==========================================================
# FILE LOADER
# ==========================================================

def load_dataset(uploaded_file):

    try:

        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)

        else:
            df = pd.read_excel(uploaded_file)

        df = ensure_schema(df)

        quality = dataset_quality(df)

        return {
            "status": True,
            "data": df,
            "quality": quality,
            "message": "Dataset loaded successfully."
        }

    except Exception as e:

        return {
            "status": False,
            "data": None,
            "quality": {},
            "message": str(e)
        }


# ==========================================================
# SESSION DATASET HELPERS
# ==========================================================

def save_session_dataset(df, dataset_name="Manual Dataset", dataset_type="Direct Upload"):

    st.session_state.dataset = ensure_schema(df)
    st.session_state.dataset_name = dataset_name
    st.session_state.dataset_type = dataset_type
    st.session_state.quality = dataset_quality(st.session_state.dataset)


def get_active_dataset():

    if "dataset" not in st.session_state:
        return None

    df = st.session_state.dataset

    if df is None or len(df) == 0:
        return None

    return ensure_schema(df)