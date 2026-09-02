import os
import pandas as pd

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

# ==========================================================
# LOAD ENVIRONMENT VARIABLES
# ==========================================================

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Local Development Database
if DATABASE_URL is None:

    DATABASE_URL = (
        f"postgresql+psycopg2://"
        f"{os.getenv('DB_USER','postgres')}:"
        f"{os.getenv('DB_PASSWORD','postgres')}@"
        f"{os.getenv('DB_HOST','localhost')}:"
        f"{os.getenv('DB_PORT','5432')}/"
        f"{os.getenv('DB_NAME','workforce360')}"
    )

# PostgreSQL Engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300
)

# ==========================================================
# DATABASE INITIALIZATION
# ==========================================================

def initialize_database():
    """
    Creates Workforce360 warehouse tables if they do not exist.
    Works for both Local PostgreSQL and Render PostgreSQL.
    """

    with engine.begin() as conn:

        # ===============================================
        # DATASET REGISTRY TABLE
        # ===============================================

        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS dataset_registry(

            dataset_id SERIAL PRIMARY KEY,

            dataset_name TEXT NOT NULL,

            dataset_type TEXT,

            quality_score FLOAT,

            total_records INTEGER,

            upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        );
        """))

        # ===============================================
        # FACT WORKFORCE TABLE
        # ===============================================

        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS fact_workforce(

            employee_id TEXT,

            employee_name TEXT,

            gender TEXT,

            age INTEGER,

            email TEXT,

            phone TEXT,

            department TEXT,

            job_role TEXT,

            city TEXT,

            state TEXT,

            joining_date DATE,

            employment_type TEXT,

            salary FLOAT,

            experience_years FLOAT,

            tenure_years FLOAT,

            attendance_percentage FLOAT,

            performance_rating FLOAT,

            training_hours FLOAT,

            overtime_hours FLOAT,

            promotion_status TEXT,

            attrition_status TEXT,

            salary_band TEXT,

            experience_group TEXT,

            joining_year INTEGER,

            joining_month TEXT,

            joining_quarter TEXT,

            dataset_id INTEGER REFERENCES dataset_registry(dataset_id)

        );
        """))

        # ===============================================
        # AUDIT LOG TABLE
        # ===============================================

        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS audit_log(

            log_id SERIAL PRIMARY KEY,

            dataset_id INTEGER,

            activity TEXT,

            records_processed INTEGER,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        );
        """))

        # ===============================================
        # DIMENSION TABLES
        # ===============================================

        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS dim_department(

            department_id SERIAL PRIMARY KEY,

            department_name TEXT UNIQUE

        );
        """))

        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS dim_location(

            location_id SERIAL PRIMARY KEY,

            city TEXT,

            state TEXT

        );
        """))

        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS dim_date(

            date_id SERIAL PRIMARY KEY,

            joining_date DATE,

            joining_year INTEGER,

            joining_month TEXT,

            joining_quarter TEXT

        );
        """))

    return True

def register_dataset(dataset_name, dataset_type, quality_score, rows):

    initialize_database()

    with engine.begin() as conn:

        dataset_id = conn.execute(
            text("""
                INSERT INTO dataset_registry(
                    dataset_name,
                    dataset_type,
                    quality_score,
                    total_records
                )
                VALUES(
                    :dataset_name,
                    :dataset_type,
                    :quality_score,
                    :total_records
                )
                RETURNING dataset_id;
            """),
            {
                "dataset_name": dataset_name,
                "dataset_type": dataset_type,
                "quality_score": quality_score,
                "total_records": rows
            }
        ).scalar()

    return dataset_id


def log_ingestion(dataset_id, activity, rows):

    initialize_database()

    with engine.begin() as conn:

        conn.execute(
            text("""
                INSERT INTO audit_log(
                    dataset_id,
                    activity,
                    records_processed
                )
                VALUES(
                    :dataset_id,
                    :activity,
                    :records_processed
                );
            """),
            {
                "dataset_id": dataset_id,
                "activity": activity,
                "records_processed": rows
            }
        )


def load_workforce(df, dataset_name, dataset_type, quality_score):

    initialize_database()

    dataset_id = register_dataset(
        dataset_name,
        dataset_type,
        quality_score,
        len(df)
    )

    upload = df.copy()

    upload.columns = (
        upload.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    upload.rename(columns={
        "salary_band": "salary_band",
        "experience_group": "experience_group",
        "joining_year": "joining_year",
        "joining_month": "joining_month",
        "joining_quarter": "joining_quarter"
    }, inplace=True)

    upload["dataset_id"] = dataset_id

    with engine.begin() as conn:

        upload.to_sql(
            "fact_workforce",
            conn,
            if_exists="append",
            index=False,
            method="multi",
            chunksize=5000
        )

        departments = (
            upload[["department"]]
            .drop_duplicates()
            .rename(columns={"department": "department_name"})
        )

        departments.to_sql(
            "dim_department",
            conn,
            if_exists="append",
            index=False,
            method="multi"
        )

        locations = (
            upload[["city", "state"]]
            .drop_duplicates()
        )

        locations.to_sql(
            "dim_location",
            conn,
            if_exists="append",
            index=False,
            method="multi"
        )

        dates = (
            upload[
                [
                    "joining_date",
                    "joining_year",
                    "joining_month",
                    "joining_quarter"
                ]
            ]
            .drop_duplicates()
        )

        dates.to_sql(
            "dim_date",
            conn,
            if_exists="append",
            index=False,
            method="multi"
        )

    log_ingestion(
        dataset_id,
        f"Dataset Loaded : {dataset_name}",
        len(upload)
    )

    return dataset_id

def fetch_workforce():

    initialize_database()

    try:
        return pd.read_sql(
            """
            SELECT *
            FROM fact_workforce
            ORDER BY joining_date DESC
            """,
            engine
        )

    except SQLAlchemyError:
        return pd.DataFrame()


def fetch_datasets():

    initialize_database()

    try:
        return pd.read_sql(
            """
            SELECT
                dataset_id,
                dataset_name,
                dataset_type,
                quality_score,
                total_records,
                upload_time
            FROM dataset_registry
            ORDER BY upload_time DESC
            """,
            engine
        )

    except SQLAlchemyError:
        return pd.DataFrame()


def fetch_audit_logs():

    initialize_database()

    try:
        return pd.read_sql(
            """
            SELECT
                log_id,
                dataset_id,
                activity,
                records_processed,
                created_at
            FROM audit_log
            ORDER BY created_at DESC
            """,
            engine
        )

    except SQLAlchemyError:
        return pd.DataFrame()


def warehouse_record_count():

    initialize_database()

    try:
        with engine.begin() as conn:

            count = conn.execute(
                text("""
                    SELECT COUNT(*)
                    FROM fact_workforce
                """)
            ).scalar()

        return count if count else 0

    except SQLAlchemyError:
        return 0


def dataset_record_count(dataset_id):

    initialize_database()

    try:
        with engine.begin() as conn:

            count = conn.execute(
                text("""
                    SELECT COUNT(*)
                    FROM fact_workforce
                    WHERE dataset_id = :dataset_id
                """),
                {"dataset_id": dataset_id}
            ).scalar()

        return count if count else 0

    except SQLAlchemyError:
        return 0


def latest_dataset():

    initialize_database()

    try:
        df = pd.read_sql(
            """
            SELECT *
            FROM dataset_registry
            ORDER BY upload_time DESC
            LIMIT 1
            """,
            engine
        )

        return df

    except SQLAlchemyError:
        return pd.DataFrame()


def department_summary():

    initialize_database()

    try:
        return pd.read_sql(
            """
            SELECT
                department,
                COUNT(*) AS employees,
                ROUND(AVG(salary),2) AS avg_salary,
                ROUND(AVG(performance_rating),2) AS avg_performance,
                ROUND(AVG(attendance_percentage),2) AS avg_attendance
            FROM fact_workforce
            GROUP BY department
            ORDER BY employees DESC
            """,
            engine
        )

    except SQLAlchemyError:
        return pd.DataFrame()


def city_summary():

    initialize_database()

    try:
        return pd.read_sql(
            """
            SELECT
                city,
                state,
                COUNT(*) AS employees
            FROM fact_workforce
            GROUP BY city, state
            ORDER BY employees DESC
            """,
            engine
        )

    except SQLAlchemyError:
        return pd.DataFrame()

def clear_workforce_data():

    initialize_database()

    with engine.begin() as conn:

        conn.execute(text("""
            TRUNCATE TABLE fact_workforce
            RESTART IDENTITY CASCADE
        """))

        conn.execute(text("""
            TRUNCATE TABLE dataset_registry
            RESTART IDENTITY CASCADE
        """))

        conn.execute(text("""
            TRUNCATE TABLE audit_log
            RESTART IDENTITY CASCADE
        """))

        conn.execute(text("""
            TRUNCATE TABLE dim_department
            RESTART IDENTITY CASCADE
        """))

        conn.execute(text("""
            TRUNCATE TABLE dim_location
            RESTART IDENTITY CASCADE
        """))

        conn.execute(text("""
            TRUNCATE TABLE dim_date
            RESTART IDENTITY CASCADE
        """))

    return True


def delete_dataset(dataset_id):

    initialize_database()

    with engine.begin() as conn:

        conn.execute(
            text("""
                DELETE FROM fact_workforce
                WHERE dataset_id = :dataset_id
            """),
            {"dataset_id": dataset_id}
        )

        conn.execute(
            text("""
                DELETE FROM audit_log
                WHERE dataset_id = :dataset_id
            """),
            {"dataset_id": dataset_id}
        )

        conn.execute(
            text("""
                DELETE FROM dataset_registry
                WHERE dataset_id = :dataset_id
            """),
            {"dataset_id": dataset_id}
        )

    return True


def database_status():

    try:

        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))

        return {
            "status": "Connected",
            "message": "PostgreSQL Warehouse Connected"
        }

    except Exception as e:

        return {
            "status": "Disconnected",
            "message": str(e)
        }


def warehouse_metrics():

    initialize_database()

    try:

        with engine.begin() as conn:

            employees = conn.execute(text("""
                SELECT COUNT(*)
                FROM fact_workforce
            """)).scalar()

            datasets = conn.execute(text("""
                SELECT COUNT(*)
                FROM dataset_registry
            """)).scalar()

            departments = conn.execute(text("""
                SELECT COUNT(DISTINCT department)
                FROM fact_workforce
            """)).scalar()

            payroll = conn.execute(text("""
                SELECT COALESCE(SUM(salary),0)
                FROM fact_workforce
            """)).scalar()

        return {
            "employees": employees or 0,
            "datasets": datasets or 0,
            "departments": departments or 0,
            "payroll": payroll or 0
        }

    except Exception:

        return {
            "employees": 0,
            "datasets": 0,
            "departments": 0,
            "payroll": 0
        }


def refresh_dimensions():

    initialize_database()

    with engine.begin() as conn:

        conn.execute(text("DELETE FROM dim_department"))
        conn.execute(text("DELETE FROM dim_location"))
        conn.execute(text("DELETE FROM dim_date"))

        conn.execute(text("""
            INSERT INTO dim_department(department_name)
            SELECT DISTINCT department
            FROM fact_workforce
            WHERE department IS NOT NULL
        """))

        conn.execute(text("""
            INSERT INTO dim_location(city, state)
            SELECT DISTINCT city, state
            FROM fact_workforce
            WHERE city IS NOT NULL
        """))

        conn.execute(text("""
            INSERT INTO dim_date(
                joining_date,
                joining_year,
                joining_month,
                joining_quarter
            )
            SELECT DISTINCT
                joining_date,
                joining_year,
                joining_month,
                joining_quarter
            FROM fact_workforce
            WHERE joining_date IS NOT NULL
        """))

    return True


def refresh_powerbi():

    initialize_database()

    refresh_dimensions()

    return {
        "status": "success",
        "message": "Warehouse refreshed successfully. Refresh Power BI to view latest data."
    }
