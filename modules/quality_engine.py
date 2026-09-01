import pandas as pd
import numpy as np
import re

# ==========================================================
# REGEX VALIDATORS
# ==========================================================

EMAIL_REGEX = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
PHONE_REGEX = r"^[0-9]{10}$"


# ==========================================================
# MAIN QUALITY ENGINE
# ==========================================================

def run_quality_checks(df: pd.DataFrame):

    report = {}

    report["rows"] = len(df)
    report["columns"] = len(df.columns)

    report["missing_values"] = int(df.isna().sum().sum())
    report["duplicate_rows"] = int(df.duplicated().sum())

    report["duplicate_employee_ids"] = duplicate_employee_ids(df)
    report["invalid_emails"] = invalid_emails(df)
    report["invalid_phones"] = invalid_phones(df)

    report["salary_outliers"] = salary_outliers(df)
    report["attendance_outliers"] = attendance_outliers(df)
    report["performance_outliers"] = performance_outliers(df)

    report["column_missing"] = column_missing(df)
    report["department_health"] = department_health(df)

    report["score"] = quality_score(report)
    report["recommendations"] = recommendations(report)

    return report


# ==========================================================
# DUPLICATE EMPLOYEE IDS
# ==========================================================

def duplicate_employee_ids(df):

    if "Employee_ID" not in df.columns:
        return 0

    return int(df["Employee_ID"].duplicated().sum())


# ==========================================================
# EMAIL VALIDATION
# ==========================================================

def invalid_emails(df):

    if "Email" not in df.columns:
        return 0

    invalid = df["Email"].astype(str).apply(
        lambda x: not bool(re.match(EMAIL_REGEX, x))
    )

    return int(invalid.sum())


# ==========================================================
# PHONE VALIDATION
# ==========================================================

def invalid_phones(df):

    if "Phone" not in df.columns:
        return 0

    invalid = df["Phone"].astype(str).apply(
        lambda x: not bool(re.match(PHONE_REGEX, x))
    )

    return int(invalid.sum())


# ==========================================================
# SALARY OUTLIERS
# ==========================================================

def salary_outliers(df):

    if "Salary" not in df.columns:
        return 0

    q1 = df["Salary"].quantile(.25)
    q3 = df["Salary"].quantile(.75)

    iqr = q3 - q1

    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr

    outliers = df[(df["Salary"] < lower) | (df["Salary"] > upper)]

    return int(len(outliers))


# ==========================================================
# ATTENDANCE OUTLIERS
# ==========================================================

def attendance_outliers(df):

    if "Attendance_Percentage" not in df.columns:
        return 0

    invalid = df[
        (df["Attendance_Percentage"] < 0)
        | (df["Attendance_Percentage"] > 100)
    ]

    return int(len(invalid))


# ==========================================================
# PERFORMANCE OUTLIERS
# ==========================================================

def performance_outliers(df):

    if "Performance_Rating" not in df.columns:
        return 0

    invalid = df[
        (df["Performance_Rating"] < 1)
        | (df["Performance_Rating"] > 5)
    ]

    return int(len(invalid))


# ==========================================================
# COLUMN MISSING SUMMARY
# ==========================================================

def column_missing(df):

    summary = (
        df.isna()
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    summary.columns = ["Column", "Missing"]

    summary["Missing_Percentage"] = (
        summary["Missing"] / len(df) * 100
    ).round(2)

    return summary


# ==========================================================
# DEPARTMENT HEALTH REPORT
# ==========================================================

def department_health(df):

    if "Department" not in df.columns:
        return pd.DataFrame()

    report = (
        df.groupby("Department")
        .agg(
            Employees=("Employee_ID", "count"),
            Missing=("Employee_ID", lambda x: x.isna().sum()),
            Avg_Attendance=("Attendance_Percentage", "mean"),
            Avg_Performance=("Performance_Rating", "mean"),
        )
        .round(2)
        .reset_index()
    )

    report["Health"] = np.where(
        report["Avg_Attendance"] >= 90,
        "Excellent",
        np.where(
            report["Avg_Attendance"] >= 80,
            "Good",
            "Needs Attention"
        )
    )

    return report


# ==========================================================
# QUALITY SCORE ENGINE
# ==========================================================

def quality_score(report):

    score = 100

    score -= report["missing_values"] * 0.20
    score -= report["duplicate_rows"] * 2
    score -= report["duplicate_employee_ids"] * 2
    score -= report["invalid_emails"] * 0.5
    score -= report["invalid_phones"] * 0.5
    score -= report["salary_outliers"] * 0.25
    score -= report["attendance_outliers"] * 0.50
    score -= report["performance_outliers"] * 0.50

    score = max(score, 0)

    return round(float(score), 2)


# ==========================================================
# BUSINESS RECOMMENDATIONS
# ==========================================================

def recommendations(report):

    tips = []

    if report["missing_values"] > 0:
        tips.append(
            f"Fill {report['missing_values']} missing values before reporting."
        )

    if report["duplicate_employee_ids"] > 0:
        tips.append("Remove duplicate Employee IDs.")

    if report["invalid_emails"] > 0:
        tips.append("Correct employee email addresses.")

    if report["invalid_phones"] > 0:
        tips.append("Validate phone numbers.")

    if report["salary_outliers"] > 0:
        tips.append("Review salary outliers for payroll accuracy.")

    if report["attendance_outliers"] > 0:
        tips.append("Attendance values should remain between 0–100.")

    if report["performance_outliers"] > 0:
        tips.append("Performance ratings should remain between 1–5.")

    if len(tips) == 0:
        tips.append("Dataset passed all enterprise quality checks.")

    return tips


# ==========================================================
# AI QUALITY SUMMARY
# ==========================================================

def quality_summary(report):

    return f"""
Enterprise Workforce Data Quality Report

Quality Score : {report['score']}/100

Rows : {report['rows']}
Columns : {report['columns']}

Missing Values : {report['missing_values']}
Duplicate Rows : {report['duplicate_rows']}
Duplicate Employee IDs : {report['duplicate_employee_ids']}

Invalid Emails : {report['invalid_emails']}
Invalid Phones : {report['invalid_phones']}

Salary Outliers : {report['salary_outliers']}
Attendance Outliers : {report['attendance_outliers']}
Performance Outliers : {report['performance_outliers']}
"""