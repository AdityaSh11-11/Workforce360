import streamlit as st
import pandas as pd

from styles.theme import load_theme, hero, footer
from styles.cards import section, empty_state
from modules.data_loader import get_active_dataset
from components.sidebar import enterprise_sidebar

enterprise_sidebar()
# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="AI Workforce Chat",
    layout="wide"
)

load_theme()

hero(
    "AI Workforce Chat Assistant",
    "Ask questions about your workforce dataset using natural language."
)

# ==========================================================
# LOAD DATASET
# ==========================================================

df = get_active_dataset()

if df is None or df.empty:
    empty_state("No workforce dataset available.")
    footer()
    st.stop()

# ==========================================================
# CLEAN DATA
# ==========================================================

numeric_cols = [
    "Salary",
    "Attendance_Percentage",
    "Performance_Rating",
    "Experience_Years",
    "Training_Hours",
    "Overtime_Hours",
    "Age"
]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

# ==========================================================
# CHAT HISTORY
# ==========================================================

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

section(
    "Workforce AI Assistant",
    "Ask HR analytics questions based on the active dataset."
)

question = st.text_input(
    "Ask a workforce question",
    placeholder="Example: Which department has the highest average salary?"
)

# ==========================================================
# AI RESPONSE ENGINE
# ==========================================================

def workforce_answer(query: str):
    
    if df is None or df.empty:
        return "No workforce dataset available."

    q = query.lower()

    # Employees
    if "total employee" in q or "employees" in q:
        return f"The organization currently has **{len(df):,} employees**."

    # Salary
    if "average salary" in q:
        avg = df["Salary"].mean()
        return f"The average employee salary is **₹ {avg:,.0f}**."

    if "highest salary" in q:
        emp = df.loc[df["Salary"].idxmax()]
        return (
            f"**{emp['Employee_Name']}** has the highest salary of "
            f"**₹ {emp['Salary']:,.0f}** in the **{emp['Department']}** department."
        )

    # Attendance
    if "attendance" in q:
        avg = df["Attendance_Percentage"].mean()
        return f"The average attendance across the workforce is **{avg:.1f}%**."

    # Performance
    if "performance" in q:
        avg = df["Performance_Rating"].mean()
        return f"The average performance rating is **{avg:.2f}/5**."

    # Attrition
    if "attrition" in q:
        left = df["Attrition_Status"].astype(str).str.lower().eq("left").sum()
        rate = round((left / len(df)) * 100, 2)
        return (
            f"**{left} employees** have left the organization. "
            f"The attrition rate is **{rate}%**."
        )

    # Department
    if "largest department" in q:
        dept = (
            df.groupby("Department")
            .size()
            .sort_values(ascending=False)
        )
        return f"The largest department is **{dept.index[0]}** with **{dept.iloc[0]} employees**."

    # City
    if "city" in q or "location" in q:
        city = (
            df.groupby("City")
            .size()
            .sort_values(ascending=False)
        )
        return f"The city with the largest workforce is **{city.index[0]}** with **{city.iloc[0]} employees**."

    # Training
    if "training" in q:
        avg = df["Training_Hours"].mean()
        return f"The average employee training hours are **{avg:.1f} hours**."

    # Overtime
    if "overtime" in q:
        avg = df["Overtime_Hours"].mean()
        return f"The average overtime is **{avg:.1f} hours**."

    # Promotion
    if "promotion" in q:
        promoted = (
            df["Promotion_Status"]
            .astype(str)
            .str.lower()
            .eq("promoted")
            .sum()
        )
        return f"**{promoted} employees** have been promoted."

    return (
        "I can answer questions related to salary, attendance, performance, "
        "attrition, departments, cities, overtime, promotions and workforce KPIs."
    )

# ==========================================================
# ASK BUTTON
# ==========================================================

if st.button("Generate Answer", use_container_width=True):

    if question.strip():

        answer = workforce_answer(question)

        st.session_state.chat_history.append(
            {
                "question": question,
                "answer": answer
            }
        )

# ==========================================================
# CHAT DISPLAY
# ==========================================================

section(
    "Conversation History",
    "AI responses generated from the active workforce dataset."
)

if not st.session_state.chat_history:

    st.info("Ask your first workforce analytics question.")

else:

    for item in reversed(st.session_state.chat_history):

        with st.container(border=True):

            st.markdown("**Question**")
            st.write(item["question"])

            st.markdown("---")

            st.markdown("**AI Response**")
            st.write(item["answer"])

# ==========================================================
# QUICK QUESTIONS
# ==========================================================

section(
    "Quick Business Questions",
    "Click a question to instantly generate workforce insights."
)

quick_questions = [
    "How many employees are there?",
    "What is the average salary?",
    "Which department has the highest salary?",
    "What is the average attendance?",
    "What is the attrition rate?",
    "Which city has the highest workforce?",
    "How many employees were promoted?",
    "What are the average training hours?"
]

cols = st.columns(2)

for i, q in enumerate(quick_questions):

    if cols[i % 2].button(q, key=f"quick_{i}"):

        answer = workforce_answer(q)

        st.session_state.chat_history.append(
            {
                "question": q,
                "answer": answer
            }
        )

st.divider()

# ==========================================================
# SQL HELPER
# ==========================================================

section(
    "AI SQL Helper",
    "Generate PostgreSQL queries for common HR business questions."
)

sql_type = st.selectbox(
    "Business SQL Query",
    [
        "Average Salary by Department",
        "Employees Who Left",
        "Top 10 Salaries",
        "Low Attendance Employees",
        "Performance Leaders"
    ]
)

sql_map = {
    "Average Salary by Department":
"""SELECT department,
AVG(salary) AS average_salary
FROM fact_workforce
GROUP BY department
ORDER BY average_salary DESC;""",

    "Employees Who Left":
"""SELECT employee_name,
department,
city
FROM fact_workforce
WHERE LOWER(attrition_status)='left';""",

    "Top 10 Salaries":
"""SELECT employee_name,
department,
salary
FROM fact_workforce
ORDER BY salary DESC
LIMIT 10;""",

    "Low Attendance Employees":
"""SELECT employee_name,
attendance_percentage
FROM fact_workforce
WHERE attendance_percentage<75;""",

    "Performance Leaders":
"""SELECT employee_name,
department,
performance_rating
FROM fact_workforce
ORDER BY performance_rating DESC
LIMIT 20;"""
}

st.code(sql_map[sql_type], language="sql")

st.download_button(
    "Download SQL Query",
    sql_map[sql_type],
    file_name="workforce_query.sql",
    use_container_width=True
)

st.divider()

# ==========================================================
# DATASET SUMMARY
# ==========================================================

section(
    "Dataset Summary",
    "AI-readable summary of the currently active workforce dataset."
)

summary = pd.DataFrame({
    "Metric": [
        "Employees",
        "Departments",
        "Cities",
        "Average Salary",
        "Average Attendance",
        "Average Performance",
        "Average Training Hours",
        "Average Overtime"
    ],
    "Value": [
        len(df),
        df["Department"].nunique(),
        df["City"].nunique(),
        f"₹ {df['Salary'].mean():,.0f}",
        f"{df['Attendance_Percentage'].mean():.1f}%",
        f"{df['Performance_Rating'].mean():.2f}/5",
        f"{df['Training_Hours'].mean():.1f}",
        f"{df['Overtime_Hours'].mean():.1f}"
    ]
})

st.dataframe(summary, use_container_width=True, hide_index=True)

footer()