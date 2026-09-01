import pandas as pd

# ==========================================================
# SAFE DATASET
# ==========================================================

def _clean(df):
    df = df.copy()

    numeric = [
        "Salary","Attendance_Percentage","Performance_Rating",
        "Training_Hours","Experience_Years"
    ]

    for col in numeric:
        if col not in df.columns:
            df[col] = 0
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    for col in ["Department","Attrition_Status","City","Job_Role"]:
        if col not in df.columns:
            df[col] = "Unknown"
        df[col] = df[col].fillna("Unknown")

    return df

# ==========================================================
# EXECUTIVE SUMMARY
# ==========================================================

def generate_executive_summary(df):
    df = _clean(df)

    employees = len(df)
    departments = df["Department"].nunique()
    payroll = int(df["Salary"].sum())
    avg_salary = int(df["Salary"].mean())
    attendance = round(df["Attendance_Percentage"].mean(),2)
    performance = round(df["Performance_Rating"].mean(),2)
    attrition = round((df["Attrition_Status"]=="Left").mean()*100,2)

    top_salary = df.groupby("Department")["Salary"].mean().idxmax()
    top_perf = df.groupby("Department")["Performance_Rating"].mean().idxmax()

    return f"""
INSIGHTFORGE AI EXECUTIVE REPORT

Employees              : {employees}
Departments            : {departments}
Payroll                : ₹ {payroll:,}
Average Salary         : ₹ {avg_salary:,}
Attendance             : {attendance}%
Performance Rating     : {performance}/5
Attrition Rate         : {attrition}%

Highest Salary Department : {top_salary}
Best Performance Department: {top_perf}

Recommendation:
• Improve retention in high attrition departments.
• Continue investing in employee training.
• Track attendance below company average.
"""

# ==========================================================
# HR RECOMMENDATIONS
# ==========================================================

def generate_hr_recommendations(df):
    df = _clean(df)

    rec = []

    if df["Attendance_Percentage"].mean() < 90:
        rec.append("Increase attendance improvement initiatives.")

    if (df["Attrition_Status"]=="Left").mean()*100 > 15:
        rec.append("Attrition is above healthy range. Launch retention program.")

    if df["Training_Hours"].mean() < 15:
        rec.append("Increase employee learning & development hours.")

    if df["Performance_Rating"].mean() < 3.5:
        rec.append("Introduce quarterly performance coaching.")

    if not rec:
        rec.append("Overall workforce health looks good.")

    return "\n".join(f"• {i}" for i in rec)

# ==========================================================
# SQL GENERATOR
# ==========================================================

def generate_sql_query(prompt):

    p = prompt.lower()

    if "average salary" in p:
        return """
SELECT department,
AVG(salary) AS average_salary
FROM fact_workforce
GROUP BY department
ORDER BY average_salary DESC;
"""

    if "attrition" in p:
        return """
SELECT department,
COUNT(*) FILTER (WHERE attrition_status='Left') AS attrition_count
FROM fact_workforce
GROUP BY department;
"""

    if "attendance" in p:
        return """
SELECT employee_name,
attendance_percentage
FROM fact_workforce
ORDER BY attendance_percentage DESC;
"""

    return f"-- SQL suggestion for: {prompt}"

# ==========================================================
# POWER BI DAX
# ==========================================================

def generate_powerbi_dax(prompt):

    p = prompt.lower()

    if "attrition" in p:
        return """
Attrition Rate =
DIVIDE(
    CALCULATE(COUNTROWS(fact_workforce),
        fact_workforce[attrition_status]="Left"),
    COUNTROWS(fact_workforce)
)
"""

    if "salary" in p:
        return """
Average Salary =
AVERAGE(fact_workforce[salary])
"""

    if "attendance" in p:
        return """
Average Attendance =
AVERAGE(fact_workforce[attendance_percentage])
"""

    return f"-- DAX Measure for: {prompt}"

# ==========================================================
# AI CHAT
# ==========================================================

def workforce_chat(question, df):

    df = _clean(df)
    q = question.lower()

    if "employee" in q and "how many" in q:
        return f"There are **{len(df)} employees** in the dataset."

    if "average salary" in q:
        return f"Average salary is **₹ {int(df['Salary'].mean()):,}**."

    if "attendance" in q:
        return f"Average attendance is **{round(df['Attendance_Percentage'].mean(),2)}%**."

    if "performance" in q:
        return f"Average performance rating is **{round(df['Performance_Rating'].mean(),2)}/5**."

    if "department" in q:
        return "Departments:\n\n" + "\n".join(
            f"• {d}" for d in sorted(df["Department"].unique())
        )

    if "attrition" in q:
        rate = round((df["Attrition_Status"]=="Left").mean()*100,2)
        return f"Overall attrition rate is **{rate}%**."

    return (
        "I can answer workforce questions about employees, salary, "
        "attendance, performance, departments, cities and attrition."
    )