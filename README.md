# Workforce360 — Enterprise Workforce Intelligence Platform

<p align="center">
  <img src="https://img.shields.io/badge/Streamlit-Enterprise%20Dashboard-red?style=for-the-badge&logo=streamlit"/>
  <img src="https://img.shields.io/badge/PostgreSQL-Data%20Warehouse-blue?style=for-the-badge&logo=postgresql"/>
  <img src="https://img.shields.io/badge/Power%20BI-Executive%20Dashboard-yellow?style=for-the-badge&logo=powerbi"/>
  <img src="https://img.shields.io/badge/Python-Data%20Analytics-green?style=for-the-badge&logo=python"/>
</p>

<p align="center">
  <b>AI-Powered Workforce Analytics | PostgreSQL Data Warehouse | Power BI Executive Dashboard | Enterprise HR Decision Intelligence</b>
</p>

---
## Project Overview

**Workforce360** is an enterprise-grade Workforce Intelligence Platform that transforms raw HR data into actionable business intelligence using **Streamlit, PostgreSQL, AI, Plotly, and Power BI**.

The platform provides a complete end-to-end workforce analytics ecosystem, including automated data ingestion, data quality validation, PostgreSQL warehousing, executive dashboards, AI-powered workforce insights, forecasting, reporting, and live Power BI integration for HR decision-making.
Unlike traditional dashboards, Workforce360 provides an end-to-end analytics workflow—from data ingestion and warehousing to interactive dashboards and business intelligence.

---

# ✨ Enterprise Features

| Module | Description |
|--------|-------------|
| Data Ingestion | Upload CSV, Excel, or manually create employee records. |
| Data Quality Engine | Automatic validation, missing value detection, quality scoring, preprocessing. |
| PostgreSQL Warehouse | Centralized workforce warehouse with Star Schema architecture. |
| Workforce Dashboard | HR KPIs, demographics, attendance, salary, promotions, attrition. |
| Salary Intelligence | Payroll insights, salary bands, compensation analytics. |
| Performance Intelligence | Performance vs Attendance, Training Impact, Department Ratings. |
| Attrition Intelligence | Employee churn analysis, retention metrics, high-risk departments. |
| AI Insights | Executive recommendations generated from workforce metrics. |
| Workforce Forecasting | Hiring, payroll, salary growth, promotion, and attrition forecasting. |
| Audit Center | Tracks uploads, warehouse operations, AI reports, and system events. |
| Power BI Integration | Live executive dashboard connected directly to PostgreSQL. |

---

# 🖥️ Complete Platform Architecture

<p align="center">
  <img src="https://raw.githubusercontent.com/ashishps1/awesome-low-level-design/main/diagrams/data-pipeline.png" width="90%">
</p>

```text
              CSV / Excel / Manual Entry
                       │
                       ▼
            Streamlit ETL & Validation Engine
                       │
      Data Cleaning • Quality Score • Audit Log
                       │
                       ▼
           PostgreSQL Workforce Warehouse
                       │
       Star Schema | Fact & Dimension Tables
                       │
         ┌─────────────┴─────────────┐
         ▼                           ▼
 Streamlit Analytics          Power BI Executive Dashboard
         │                           │
         └─────────────┬─────────────┘
                       ▼
              AI Workforce Intelligence
```

---

# 🏗️ Tech Stack

| Category | Technology |
|----------|------------|
| Frontend | Streamlit |
| Language | Python |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Data Processing | Pandas, NumPy |
| Visualizations | Plotly |
| AI Layer | OpenRouter API |
| Business Intelligence | Microsoft Power BI |
| Data Warehouse | Star Schema |
| Version Control | Git + GitHub |

---

# 📂 Project Structure

```text
Workforce360/
│
├── app.py                         # Streamlit Entry Point
├── config/
│   ├── database.py                # PostgreSQL Connection
│   ├── settings.py
│
├── pages/
│   ├── 0_Data_Ingestion.py
│   ├── 1_Workforce_Overview.py
│   ├── 2_Salary_Intelligence.py
│   ├── 3_Performance_Intelligence.py
│   ├── 4_Attrition_Intelligence.py
│   ├── 5_AI_Insights.py
│   ├── 6_Workforce_Forecasting.py
│   ├── 7_Reports.py
│   ├── 8_Admin_Center.py
│   ├── 9_Audit_Log.py
│
├── modules/
│   ├── warehouse.py
│   ├── upload_engine.py
│   ├── audit_engine.py
│   ├── ai_engine.py
│   ├── report_engine.py
│
├── styles/
│   ├── theme.py
│   ├── cards.py
│
├── assets/
│   ├── logo.png
│   ├── background.png
│
├── powerbi/
│   ├── InsightForge_AI.pbix
│
├── requirements.txt
└── README.md
```

---

# 📊 Workforce Analytics Modules

## 1️⃣ Workforce Overview

- Executive KPI Dashboard
- Employee Demographics
- Department Distribution
- Gender Diversity
- Age Distribution
- Experience Distribution
- Attendance Analytics
- Salary Distribution

---

## 2️⃣ Salary Intelligence

- Total Payroll
- Average Salary
- Salary Band Analysis
- Department Salary Ranking
- Highest Paid Employees
- Compensation Distribution
- Salary vs Experience
- Payroll Planning

---

## 3️⃣ Performance Intelligence

- Average Performance Score
- Attendance vs Performance
- Training Impact Analysis
- Overtime Analysis
- Department Performance Ranking
- Top Performing Employees
- Promotion Eligibility
- Employee Performance Heatmap

---

## 4️⃣ Attrition Intelligence

- Attrition Rate
- Active vs Left Employees
- Attrition by Department
- Attrition by City
- Attrition by Salary Band
- Attrition by Experience Group
- High Risk Workforce Analysis

---

## 5️⃣ AI Workforce Intelligence

- AI Workforce Score
- Executive HR Recommendations
- Workforce Health Summary
- Department Risk Detection
- Promotion Suggestions
- Payroll Optimization Insights

---

## 6️⃣ Workforce Forecasting

- Hiring Forecast
- Payroll Forecast
- Salary Growth Forecast
- Promotion Forecast
- Attrition Forecast
- Future Workforce Planning
- AI Hiring Recommendations

---

## 7️⃣ Admin Center

- PostgreSQL Health
- Warehouse Monitoring
- Session Monitoring
- Dataset Management
- AI Report Status
- Workspace Reset

---

## 8️⃣ Audit Center

- Upload History
- PostgreSQL Events
- AI Report Logs
- Warehouse Activity Logs
- Timestamped System Events

---

# 🗄️ PostgreSQL Workforce Warehouse

### Star Schema Design

```text
                 dim_date
                    │
dim_department ─ fact_workforce ─ dim_location
                    │
               dataset_registry
                    │
                 audit_log
```

### Core Tables

| Table | Purpose |
|-------|----------|
| fact_workforce | Employee workforce facts |
| dataset_registry | Dataset metadata |
| dim_department | Department dimension |
| dim_location | City & State dimension |
| dim_date | Joining Date dimension |
| audit_log | System activity logs |

---

# 📥 Data Ingestion Pipeline

### Supported Upload Methods

- CSV Upload
- Excel Upload
- Manual Employee Entry

### Upload Modes

#### Direct Upload Mode

- Stores dataset in Streamlit Session.
- Instantly updates all dashboards.
- Does **not** write into PostgreSQL.

#### PostgreSQL Warehouse Mode

- Loads dataset into PostgreSQL.
- Updates warehouse tables.
- Synchronizes with Power BI dashboard.

### Built-in Data Quality Checks

- Missing Values
- Duplicate Detection
- Invalid Data Handling
- Column Standardization
- Quality Score Generation

---

# 📈 Power BI Executive Dashboard

## Live Enterprise Dashboard

Power BI is connected directly with PostgreSQL Warehouse.

### Dashboard Includes

- Executive KPI Cards
- Workforce Overview
- Salary Intelligence
- Performance Intelligence
- Attrition Intelligence
- Forecasting Dashboard
- AI Insights Panel

### Live Sync Workflow

```text
Streamlit Upload
       │
       ▼
PostgreSQL Warehouse
       │
       ▼
Power BI Refresh
       │
       ▼
Updated Executive Dashboard
```

---

# 🤖 AI Decision Intelligence

The AI engine generates executive workforce insights using workforce metrics.

### AI Recommendations Include

- High Attrition Departments
- Promotion Eligible Employees
- Salary Optimization
- Workforce Risk Analysis
- Hiring Priorities
- Payroll Planning Suggestions

---

# Business KPIs Generated

| Category | KPIs |
|----------|------|
| Workforce | Total Employees, Departments, Cities |
| Salary | Payroll, Avg Salary, Highest Salary |
| Performance | Avg Rating, Top Performers |
| Attendance | Avg Attendance, Attendance Rate |
| Promotion | Promotion Rate |
| Attrition | Attrition %, Retention % |
| AI | Workforce Health Score |

---

# Business Problems Solved

- Workforce Health Monitoring
- Payroll Planning
- Employee Performance Tracking
- Promotion Readiness
- Employee Retention Strategy
- Hiring Forecasting
- Executive HR Reporting
- Workforce Decision Intelligence

---

# Platform Preview

---

# Installation

## Clone Repository

```bash
git clone https://github.com/yourusername/Workforce360.git

cd Workforce360
```

## Create Virtual Environment

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### Mac / Linux

```bash
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure PostgreSQL

Create `.env`

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=insightforge
DB_USER=postgres
DB_PASSWORD=your_password

OPENROUTER_API_KEY=your_api_key
```

---

## Run Application

```bash
streamlit run app.py
```

Application starts at

```text
http://localhost:8501
```

---

# 📦 Power BI Setup

1. Publish `Workforce360.pbix` to Power BI Service.
2. Connect Power BI to PostgreSQL database.
3. Copy the Embed URL.
4. Paste Embed URL inside Streamlit.
5. Refresh Power BI after loading data into PostgreSQL.

---

# 📁 Dataset Information

| Attribute | Details |
|-----------|---------|
| Records | 60,000 Employees |
| Columns | 20+ Workforce Attributes |
| Industries | Enterprise Workforce Dataset |
| Locations | Multiple Indian Cities |
| Departments | 10 Business Departments |
| Salary Bands | Low • Medium • High • Executive |

---

# 🚀 Enterprise Highlights

- Enterprise Workforce Intelligence Platform
- PostgreSQL Star Schema Warehouse
- Interactive Streamlit Analytics
- AI Workforce Decision Engine
- Live Power BI Executive Dashboard
- Audit Logging System
- Forecasting & Workforce Planning
- Business-Ready HR Analytics Platform

---

# 📚 Skills Demonstrated

### Data Analytics

- Data Cleaning
- Exploratory Data Analysis
- KPI Design
- Workforce Analytics
- HR Metrics

### Data Engineering

- ETL Pipeline
- PostgreSQL Warehouse
- SQLAlchemy
- Audit Logging
- Session Management

### Business Intelligence

- Power BI Dashboard
- DAX Measures
- Star Schema Modeling
- Executive Reporting
- Dashboard Design

### Python

- Pandas
- NumPy
- Plotly
- Streamlit
- PostgreSQL Integration

---

# 💼 Resume Project Description

**Workforce360 — Enterprise Workforce Intelligence Platform**

Designed and developed a full-stack workforce analytics platform integrating **Streamlit, PostgreSQL, AI, and Power BI** to automate HR data ingestion, warehouse management, executive analytics, forecasting, and AI-driven workforce decision intelligence across **60,000+ employee records**.

---

# 👨‍💻 Author

**Aditya Sharma**

**Aspiring Data Analyst | Business Intelligence Developer | Power BI & Python Analytics**

- Python
- SQL
- PostgreSQL
- Streamlit
- Power BI
- Plotly
- Pandas

---

<p align="center">
  ⭐ If you found this project useful, consider giving it a star on GitHub.
</p>
