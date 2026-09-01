import pandas as pd
import numpy as np

# ==========================================================
# UNIVERSAL WORKFORCE SCHEMA
# ==========================================================

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
    "Attrition_Status"
]

# ==========================================================
# AUTO COLUMN MAPPING
# ==========================================================

COLUMN_MAPPING = {
    "employee id":"Employee_ID",
    "emp id":"Employee_ID",
    "employeeid":"Employee_ID",
    "id":"Employee_ID",

    "employee name":"Employee_Name",
    "name":"Employee_Name",
    "full name":"Employee_Name",

    "gender":"Gender",
    "sex":"Gender",

    "age":"Age",

    "email":"Email",
    "email address":"Email",

    "phone":"Phone",
    "mobile":"Phone",
    "contact":"Phone",

    "department":"Department",

    "job role":"Job_Role",
    "designation":"Job_Role",
    "role":"Job_Role",
    "position":"Job_Role",

    "city":"City",
    "location":"City",
    "office":"City",
    "branch":"City",

    "state":"State",
    "region":"State",

    "joining date":"Joining_Date",
    "hire date":"Joining_Date",
    "date of joining":"Joining_Date",

    "employment type":"Employment_Type",
    "employee type":"Employment_Type",

    "salary":"Salary",
    "monthly income":"Salary",
    "income":"Salary",

    "experience years":"Experience_Years",
    "experience":"Experience_Years",

    "tenure years":"Tenure_Years",
    "tenure":"Tenure_Years",

    "attendance percentage":"Attendance_Percentage",
    "attendance %":"Attendance_Percentage",

    "performance rating":"Performance_Rating",
    "rating":"Performance_Rating",
    "performance score":"Performance_Rating",

    "training hours":"Training_Hours",

    "overtime hours":"Overtime_Hours",
    "overtime":"Overtime_Hours",

    "promotion status":"Promotion_Status",

    "attrition status":"Attrition_Status",
    "attrition":"Attrition_Status",
    "left company":"Attrition_Status"
}

# ==========================================================
# LOAD CSV / EXCEL
# ==========================================================

def load_uploaded_file(file):

    if file.name.endswith(".csv"):
        df = pd.read_csv(file)

    elif file.name.endswith((".xlsx",".xls")):
        df = pd.read_excel(file)

    else:
        return {"status":False,"message":"Unsupported file format"}

    df = standardize_columns(df)
    df = clean_dataset(df)

    return {
        "status":True,
        "data":df,
        "quality":calculate_quality(df)
    }

# ==========================================================
# STANDARDIZE
# ==========================================================

def standardize_columns(df):

    rename = {}

    for col in df.columns:
        key = (
            str(col)
            .strip()
            .lower()
            .replace("_"," ")
        )
        rename[col] = COLUMN_MAPPING.get(key,col.strip())

    df.rename(columns=rename,inplace=True)

    for col in REQUIRED_COLUMNS:
        if col not in df.columns:
            df[col] = np.nan

    return df[REQUIRED_COLUMNS]

# ==========================================================
# CLEAN DATASET
# ==========================================================

def clean_dataset(df):

    text_cols = [
        "Employee_ID","Employee_Name","Gender","Email","Phone",
        "Department","Job_Role","City","State",
        "Employment_Type","Promotion_Status","Attrition_Status"
    ]

    num_cols = [
        "Age","Salary","Experience_Years","Tenure_Years",
        "Attendance_Percentage","Performance_Rating",
        "Training_Hours","Overtime_Hours"
    ]

    for col in text_cols:
        df[col] = (
            df[col]
            .fillna("Unknown")
            .astype(str)
            .replace("nan","Unknown")
            .str.strip()
        )

    for col in num_cols:
        df[col] = pd.to_numeric(df[col],errors="coerce")

        if df[col].isna().all():
            df[col] = 0
        else:
            df[col] = df[col].fillna(df[col].median())

    df["Joining_Date"] = pd.to_datetime(
        df["Joining_Date"],
        errors="coerce"
    )

    df["Joining_Date"] = df["Joining_Date"].fillna(pd.Timestamp.today())

    df.drop_duplicates(
        subset="Employee_ID",
        inplace=True
    )

    return create_derived_columns(df)

# ==========================================================
# DERIVED COLUMNS
# ==========================================================

def create_derived_columns(df):

    df["Salary_Band"] = pd.cut(
        df["Salary"],
        bins=[0,30000,60000,100000,200000,1000000],
        labels=["Low","Medium","High","Very High","Executive"]
    )

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
    )

    df["Joining_Year"] = df["Joining_Date"].dt.year
    df["Joining_Month"] = df["Joining_Date"].dt.strftime("%b")
    df["Joining_Quarter"] = (
        "Q"+(((df["Joining_Date"].dt.month-1)//3)+1).astype(int).astype(str)
    )

    return df.reset_index(drop=True)

# ==========================================================
# QUALITY SCORE
# ==========================================================

def calculate_quality(df):

    total = df.shape[0]*df.shape[1]
    missing = int(df.isna().sum().sum())
    duplicates = int(df.duplicated().sum())

    completeness = (
        ((total-missing)/total)*100 if total else 100
    )

    duplicate_health = (
        100-((duplicates/max(len(df),1))*100)
    )

    score = round(
        completeness*0.8 + duplicate_health*0.2,
        2
    )

    return {
        "score":score,
        "rows":len(df),
        "columns":len(df.columns),
        "missing_values":missing,
        "duplicate_rows":duplicates
    }

# ==========================================================
# MANUAL EMPLOYEE ENTRY
# ==========================================================

def create_manual_employee_dataframe(employee:dict):

    df = pd.DataFrame([employee])

    df = standardize_columns(df)
    df = clean_dataset(df)

    return df