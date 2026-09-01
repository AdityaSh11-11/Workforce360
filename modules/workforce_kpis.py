def workforce_kpis(df):

    kpi = {}

    kpi["Total Employees"] = len(df)

    if "Attrition_Status" in df.columns:

        left = (df["Attrition_Status"] == "Left").sum()

        kpi["Active Employees"] = len(df) - left
        kpi["Attrition Rate"] = round((left / len(df)) * 100, 2)

    if "Salary" in df.columns:
        kpi["Average Salary"] = round(df["Salary"].mean(), 2)
        kpi["Salary Expense"] = round(df["Salary"].sum(), 2)

    if "Attendance_Percentage" in df.columns:
        kpi["Average Attendance"] = round(
            df["Attendance_Percentage"].mean(), 2
        )

    if "Performance_Rating" in df.columns:
        kpi["Average Rating"] = round(
            df["Performance_Rating"].mean(), 2
        )

    if "Tenure_Years" in df.columns:
        kpi["Average Tenure"] = round(
            df["Tenure_Years"].mean(), 2
        )

    if "Department" in df.columns:
        kpi["Departments"] = df["Department"].nunique()

    if "Job_Role" in df.columns:
        kpi["Job Roles"] = df["Job_Role"].nunique()

    return kpi