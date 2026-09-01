import pandas as pd


def clean_workforce_data(df):

    report = {}

    report["rows_before"] = len(df)

    df.columns = (
        df.columns.str.strip()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )

    duplicates = 0

    if "Employee_ID" in df.columns:
        duplicates = df["Employee_ID"].duplicated().sum()
        df = df.drop_duplicates(subset="Employee_ID")
    else:
        duplicates = df.duplicated().sum()
        df = df.drop_duplicates()

    report["duplicates_removed"] = int(duplicates)

    numeric_columns = [
        "Age",
        "Salary",
        "Experience_Years",
        "Attendance_Percentage",
        "Performance_Rating",
        "Training_Hours",
        "Overtime_Hours",
    ]

    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
            df[col] = df[col].fillna(df[col].median())

    categorical_columns = [
        "Department",
        "Job_Role",
        "Gender",
        "Promotion_Status",
        "Attrition_Status",
        "City",
        "State",
    ]

    for col in categorical_columns:
        if col in df.columns:
            df[col] = df[col].fillna("Unknown")

    if "Joining_Date" in df.columns:
        df["Joining_Date"] = pd.to_datetime(df["Joining_Date"], errors="coerce")

    report["missing_values_fixed"] = int(df.isna().sum().sum())

    df = df.fillna("Unknown")

    report["rows_after"] = len(df)

    return df.reset_index(drop=True), report