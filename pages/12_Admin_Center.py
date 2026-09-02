import streamlit as st
import pandas as pd
from datetime import datetime
from sqlalchemy import text

from styles.theme import load_theme, hero, footer
from styles.cards import section, insight, empty_state
from modules.data_loader import get_active_dataset
from modules.warehouse import engine
from components.sidebar import enterprise_sidebar

enterprise_sidebar()


st.set_page_config(
    page_title="Admin Center",
    layout="wide"
)

load_theme()

hero(
    "Admin Center",
    "Monitor PostgreSQL Warehouse, Session Status, Dataset Registry and Platform Health."
)

section(
    "Platform Health Overview",
    "Current health status of the InsightForge AI platform."
)

db_status = "Connected"
db_message = "PostgreSQL Warehouse is available."

try:
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
except Exception:
    db_status = "Disconnected"
    db_message = "Unable to connect to PostgreSQL."

dataset = get_active_dataset()
dataset_loaded = dataset is not None and not dataset.empty

ai_report = st.session_state.get("ai_report", None)

c1, c2, c3, c4 = st.columns(4)

c1.metric("PostgreSQL", db_status)
c2.metric("Dataset Status", "Loaded" if dataset_loaded else "Not Loaded")
c3.metric("AI Report", "Generated" if ai_report else "Pending")
c4.metric("System Date", datetime.now().strftime("%d %b %Y"))

st.info(db_message)

st.divider()


section(
    "Current Dataset Information",
    "Details of the dataset currently active across dashboards."
)

if dataset_loaded and dataset is not None:

    avg_salary = pd.to_numeric(
        dataset["Salary"],
        errors="coerce"
    ).fillna(0).mean() if "Salary" in dataset.columns else 0

    info = pd.DataFrame({
        "Property": [
            "Dataset Name",
            "Dataset Type",
            "Employees",
            "Departments",
            "Cities",
            "Average Salary",
            "Quality Score"
        ],
        "Value": [
            st.session_state.get("dataset_name", "Unknown"),
            st.session_state.get("dataset_type", "Unknown"),
            len(dataset),
            dataset["Department"].nunique(),
            dataset["City"].nunique(),
            f"₹ {avg_salary:,.0f}",
            f"{st.session_state.get('quality', {}).get('score', 0)}%"
        ]
    })

    st.dataframe(
        info,
        use_container_width=True,
        hide_index=True
    )

else:
    empty_state("No active dataset available in this session.")

st.divider()


section(
    "Warehouse Table Status",
    "Check PostgreSQL warehouse tables and record counts."
)

tables = [
    "dataset_registry",
    "fact_workforce",
    "audit_log"
]

table_status = []

try:
    with engine.connect() as conn:

        for table in tables:

            try:
                count = conn.execute(
                    text(f"SELECT COUNT(*) FROM {table}")
                ).scalar()

                table_status.append({
                    "Table": table,
                    "Rows": int(count) if count is not None else 0,
                    "Status": "Available"
                })

            except Exception:
                table_status.append({
                    "Table": table,
                    "Rows": 0,
                    "Status": "Missing"
                })

    st.dataframe(
        pd.DataFrame(table_status),
        use_container_width=True,
        hide_index=True
    )

except Exception:
    st.warning("Warehouse connection unavailable.")

st.divider()


section(
    "Session State Monitor",
    "Current Streamlit session variables used by the application."
)

session_items = []

for key, value in st.session_state.items():

    value_type = type(value).__name__

    if isinstance(value, pd.DataFrame):
        value_preview = f"DataFrame ({len(value)} rows)"
    elif isinstance(value, dict):
        value_preview = f"Dictionary ({len(value)} keys)"
    elif isinstance(value, list):
        value_preview = f"List ({len(value)} items)"
    else:
        value_preview = str(value)[:60]

    session_items.append({
        "Session Variable": key,
        "Type": value_type,
        "Value": value_preview
    })

if session_items:
    st.dataframe(
        pd.DataFrame(session_items),
        use_container_width=True,
        hide_index=True
    )
else:
    st.info("No session variables available.")

st.divider()


section(
    "Active Dataset Preview",
    "Preview the first records currently stored in session."
)

if dataset_loaded and dataset is not None:

    st.dataframe(
        dataset.head(15),
        use_container_width=True,
        hide_index=True
    )

else:
    st.info("Dataset preview unavailable.")

st.divider()


section(
    "Platform Configuration",
    "Technology stack powering InsightForge AI."
)

platform = pd.DataFrame({
    "Component": [
        "Frontend",
        "Backend",
        "Database",
        "Analytics Library",
        "Visualization",
        "Warehouse",
        "Export",
        "AI Module"
    ],
    "Technology": [
        "Streamlit",
        "Python",
        "PostgreSQL",
        "Pandas",
        "Plotly",
        "SQLAlchemy",
        "CSV / Excel / Power BI",
        "AI Workforce Studio"
    ]
})

st.dataframe(
    platform,
    use_container_width=True,
    hide_index=True
)

st.divider()


section(
    "Platform Statistics",
    "Overall application statistics from the active dataset."
)

if dataset_loaded:

    c1, c2 = st.columns(2)

    with c1:

        st.metric("Columns in Dataset", len(dataset.columns) if dataset is not None else 0)
        st.metric("Missing Values", int(dataset.isna().sum().sum()) if dataset is not None else 0)
        st.metric("Duplicate Rows", int(dataset.duplicated().sum()) if dataset is not None else 0)

    with c2:

        st.metric("Departments", dataset["Department"].nunique() if dataset is not None else 0)
        st.metric("Cities", dataset["City"].nunique() if dataset is not None else 0)
        st.metric("Employment Types", dataset["Employment_Type"].nunique() if dataset is not None else 0)

st.divider()


section(
    "Workspace Management",
    "Reset the current Streamlit workspace without affecting PostgreSQL warehouse data."
)

st.warning(
    "This clears only the current Streamlit session dataset, filters and AI report. PostgreSQL warehouse records remain unchanged."
)

if st.button("Clear Current Session Workspace", use_container_width=True):

    reset_keys = [
        "dataset",
        "dataset_name",
        "dataset_type",
        "quality",
        "ai_report",
        "chat_history"
    ]

    for key in reset_keys:
        if key in st.session_state:
            del st.session_state[key]

    st.success("Workspace cleared successfully.")
    st.rerun()

st.divider()


section(
    "Executive Admin Summary",
    "Operational overview of the InsightForge AI platform."
)

summary = f"""
**Platform Health**

- PostgreSQL Status: **{db_status}**
- Active Dataset: **{"Loaded" if dataset_loaded else "Not Loaded"}**
- AI Report Status: **{"Generated" if ai_report else "Pending"}**

**Administrative Capabilities**

1. PostgreSQL Warehouse Monitoring
2. Dataset Registry Validation
3. Session State Monitoring
4. Workspace Reset
5. Platform Configuration Review

The Admin Center provides operational visibility into the Workforce Intelligence Platform and helps administrators monitor data availability, warehouse connectivity and application state.
"""

st.markdown(summary)

footer()
