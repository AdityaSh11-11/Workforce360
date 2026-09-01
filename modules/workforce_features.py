import pandas as pd
from datetime import datetime

TODAY = pd.Timestamp.today().normalize()


def salary_band(salary):
    if salary < 30000:
        return "Low"
    elif salary < 70000:
        return "Medium"
    elif salary < 120000:
        return "High"
    return "Executive"


def age_group(age):
    if age <= 25:
        return "18-25"
    elif age <= 35:
        return "26-35"
    elif age <= 45:
        return "36-45"
    elif age <= 55:
        return "46-55"
    return "56+"


def experience_group(exp):
    if exp < 2:
        return "0-2 Years"
    elif exp < 5:
        return "2-5 Years"
    elif exp < 10:
        return "5-10 Years"
    return "10+ Years"


def attendance_status(value):
    if value >= 95:
        return "Excellent"
    elif value >= 85:
        return "Good"
    elif value >= 75:
        return "Average"
    return "Poor"


def performance_status(value):
    if value >= 4.5:
        return "Outstanding"
    elif value >= 4:
        return "Excellent"
    elif value >= 3:
        return "Good"
    elif value >= 2:
        return "Needs Improvement"
    return "Poor"


def create_workforce_features(df):

    if "Joining_Date" in df.columns:
        df["Joining_Date"] = pd.to_datetime(df["Joining_Date"], errors="coerce")

        df["Joining_Year"] = df["Joining_Date"].dt.year
        df["Joining_Month"] = df["Joining_Date"].dt.month_name()
        df["Joining_Quarter"] = "Q" + df["Joining_Date"].dt.quarter.astype(str)

        df["Tenure_Years"] = (
            (TODAY - df["Joining_Date"]).dt.days / 365
        ).round(1)

    if "Age" in df.columns:
        df["Age_Group"] = df["Age"].apply(age_group)

    if "Salary" in df.columns:
        df["Salary_Band"] = df["Salary"].apply(salary_band)

    if "Experience_Years" in df.columns:
        df["Experience_Group"] = df["Experience_Years"].apply(experience_group)

    if "Attendance_Percentage" in df.columns:
        df["Attendance_Status"] = df["Attendance_Percentage"].apply(
            attendance_status
        )

    if "Performance_Rating" in df.columns:
        df["Performance_Status"] = df["Performance_Rating"].apply(
            performance_status
        )

    return df