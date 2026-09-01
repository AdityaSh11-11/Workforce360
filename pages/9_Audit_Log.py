import streamlit as st
import pandas as pd
import plotly.express as px

from styles.theme import load_theme, hero, footer
from styles.cards import section, empty_state, insight
from modules.warehouse import fetch_audit_logs, fetch_datasets
from components.sidebar import enterprise_sidebar

enterprise_sidebar()
# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Audit Log",
    layout="wide"
)

load_theme()

hero(
    "Audit & Dataset Registry",
    "Track dataset uploads, PostgreSQL warehouse activity and ingestion history."
)

# ==========================================================
# LOAD DATA
# ==========================================================

audit_df = fetch_audit_logs()
dataset_df = fetch_datasets()

if audit_df.empty and dataset_df.empty:
    empty_state("No audit records found in PostgreSQL Warehouse.")
    footer()
    st.stop()

# ==========================================================
# CLEAN DATA
# ==========================================================

if not audit_df.empty:
    audit_df["log_time"] = pd.to_datetime(
        audit_df["log_time"],
        errors="coerce"
    )

if not dataset_df.empty:
    dataset_df["uploaded_at"] = pd.to_datetime(
        dataset_df["uploaded_at"],
        errors="coerce"
    )

# ==========================================================
# KPI OVERVIEW
# ==========================================================

section(
    "Warehouse Activity Overview",
    "Monitor PostgreSQL ingestion history and dataset registry."
)

c1, c2, c3, c4 = st.columns(4)

c1.metric("Datasets Uploaded", len(dataset_df))
c2.metric("Audit Events", len(audit_df))

if not dataset_df.empty:
    c3.metric(
        "Records Stored",
        int(dataset_df["total_records"].sum())
    )

    c4.metric(
        "Average Quality Score",
        f"{dataset_df['quality_score'].mean():.1f}%"
    )

st.divider()

# ==========================================================
# DATASET REGISTRY
# ==========================================================

section(
    "Dataset Registry",
    "Every dataset uploaded into PostgreSQL Warehouse."
)

if not dataset_df.empty:

    registry = dataset_df.copy()

    registry["uploaded_at"] = registry["uploaded_at"].dt.strftime(
        "%d %b %Y %I:%M %p"
    )

    st.dataframe(
        registry,
        use_container_width=True,
        hide_index=True
    )

st.divider()

# ==========================================================
# QUALITY SCORE TREND
# ==========================================================

section(
    "Dataset Quality Trend",
    "Quality score comparison across uploaded datasets."
)

if not dataset_df.empty:

    fig = px.bar(
        dataset_df.sort_values("uploaded_at"),
        x="dataset_name",
        y="quality_score",
        color="quality_score",
        title="Quality Score by Dataset"
    )

    fig.update_layout(
        template="plotly_dark",
        height=450
    )

    st.plotly_chart(fig, use_container_width=True)

    insight(
        "Dataset Quality Insight",
        "Quality score measures completeness and duplicate checks performed during ingestion.",
        "Maintain quality scores above 90% before publishing analytics dashboards."
    )

st.divider()

# ==========================================================
# RECORD COUNT TREND
# ==========================================================

section(
    "Dataset Size Comparison",
    "Compare total employee records stored in each dataset."
)

if not dataset_df.empty:

    fig = px.bar(
        dataset_df.sort_values("total_records", ascending=False),
        x="dataset_name",
        y="total_records",
        color="dataset_type",
        title="Dataset Size Comparison"
    )

    fig.update_layout(
        template="plotly_dark",
        height=450
    )

    st.plotly_chart(fig, use_container_width=True)

st.divider()

# ==========================================================
# INGESTION TIMELINE
# ==========================================================

section(
    "Dataset Upload Timeline",
    "Timeline of PostgreSQL warehouse uploads."
)

if not dataset_df.empty:

    timeline = (
        dataset_df.groupby(dataset_df["uploaded_at"].dt.date)
        .size()
        .reset_index(name="uploads")
        .rename(columns={"uploaded_at": "date"})
    )

    fig = px.line(
        timeline,
        x="date",
        y="uploads",
        markers=True,
        title="Dataset Upload Timeline"
    )

    fig.update_layout(
        template="plotly_dark",
        height=450
    )

    st.plotly_chart(fig, use_container_width=True)

st.divider()

# ==========================================================
# AUDIT EVENT DISTRIBUTION
# ==========================================================

section(
    "Audit Event Distribution",
    "Frequency of warehouse activities."
)

if not audit_df.empty:

    activity = (
        audit_df.groupby("activity")
        .size()
        .reset_index(name="events")
        .sort_values("events", ascending=False)
    )

    fig = px.bar(
        activity,
        x="activity",
        y="events",
        color="events",
        title="Audit Event Distribution"
    )

    fig.update_layout(
        template="plotly_dark",
        height=450
    )

    st.plotly_chart(fig, use_container_width=True)

    insight(
        "Audit Insight",
        "Tracks ingestion events and warehouse operations performed by users.",
        "Use audit history for governance, compliance and data lineage."
    )

st.divider()

# ==========================================================
# AUDIT TIMELINE TABLE
# ==========================================================

section(
    "Audit Timeline",
    "Chronological PostgreSQL warehouse activity log."
)

if not audit_df.empty:

    logs = audit_df.sort_values("log_time", ascending=False).copy()

    logs["log_time"] = logs["log_time"].dt.strftime(
        "%d %b %Y %I:%M %p"
    )

    st.dataframe(
        logs,
        use_container_width=True,
        hide_index=True
    )

st.divider()

# ==========================================================
# DATASET DETAILS
# ==========================================================

section(
    "Dataset Details",
    "Inspect upload metadata for each dataset."
)

if not dataset_df.empty:

    selected = st.selectbox(
        "Select Dataset",
        dataset_df["dataset_name"]
    )

    info = dataset_df[
        dataset_df["dataset_name"] == selected
    ].iloc[0]

    c1, c2 = st.columns(2)

    with c1:
        st.metric("Dataset ID", info["dataset_id"])
        st.metric("Dataset Type", info["dataset_type"])
        st.metric("Quality Score", f"{info['quality_score']}%")

    with c2:
        st.metric("Total Records", int(info["total_records"]))
        st.metric(
            "Upload Time",
            info["uploaded_at"].strftime("%d %b %Y")
        )

st.divider()

# ==========================================================
# EXECUTIVE SUMMARY
# ==========================================================

section(
    "Audit Executive Summary",
    "Business summary of warehouse ingestion activity."
)

if not dataset_df.empty:

    summary = f"""
### Warehouse Summary

- Total datasets stored in PostgreSQL: **{len(dataset_df)}**
- Total employee records processed: **{int(dataset_df['total_records'].sum()):,}**
- Average dataset quality score: **{dataset_df['quality_score'].mean():.1f}%**
- Audit events recorded: **{len(audit_df)}**

### Business Value

The Audit Center provides complete visibility into workforce data ingestion,
warehouse history and data governance for enterprise HR analytics.
"""

    st.markdown(summary)

footer()