import os
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    DATABASE_URL = (
        f"postgresql+psycopg2://"
        f"{os.getenv('DB_USER','postgres')}:"
        f"{os.getenv('DB_PASSWORD','postgres')}@"
        f"{os.getenv('DB_HOST','localhost')}:"
        f"{os.getenv('DB_PORT','5432')}/"
        f"{os.getenv('DB_NAME','insightforge_ai')}"
    )

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

def initialize_database():

    with engine.begin() as conn:

        # ================================
        # DATASET REGISTRY
        # ================================
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

        # ================================
        # FACT WORKFORCE
        # ================================
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

        # ================================
        # AUDIT LOG
        # ================================
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS audit_log(
            log_id SERIAL PRIMARY KEY,
            action TEXT,
            dataset_name TEXT,
            records INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """))

        # ================================
        # DEPARTMENT DIMENSION
        # ================================
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS dim_department(
            department_id SERIAL PRIMARY KEY,
            department_name TEXT UNIQUE
        );
        """))

        # ================================
        # LOCATION DIMENSION
        # ================================
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS dim_location(
            location_id SERIAL PRIMARY KEY,
            city TEXT,
            state TEXT
        );
        """))

        # ================================
        # DATE DIMENSION
        # ================================
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS dim_date(
            date_id SERIAL PRIMARY KEY,
            joining_date DATE,
            joining_year INTEGER,
            joining_month TEXT,
            joining_quarter TEXT
        );
        """))

def register_dataset(dataset_name, dataset_type, quality_score, rows):

    initialize_database()

    with engine.begin() as conn:

        dataset_id = conn.execute(text("""
            INSERT INTO dataset_registry(
                dataset_name,
                dataset_type,
                quality_score,
                total_records
            )
            VALUES(
                :name,
                :dtype,
                :quality,
                :rows
            )
            RETURNING dataset_id;
        """),{
            "name": dataset_name,
            "dtype": dataset_type,
            "quality": quality_score,
            "rows": rows
        }).scalar()

    return dataset_id

def load_workforce(df, dataset_name, dataset_type, quality_score):

    initialize_database()

    dataset_id = register_dataset(
        dataset_name,
        dataset_type,
        quality_score,
        len(df)
    )

    upload = df.copy()

    upload.columns = [
        c.lower()
         .replace(" ","_")
        for c in upload.columns
    ]

    upload["dataset_id"] = dataset_id

    upload.to_sql(
        "fact_workforce",
        engine,
        if_exists="append",
        index=False
    )

    log_ingestion(
        dataset_id,
        f"Loaded {dataset_name}",
        len(upload)
    )

    return dataset_id

def log_ingestion(dataset_id, activity, rows):

    initialize_database()

    with engine.begin() as conn:

        conn.execute(text("""
        INSERT INTO audit_log
        (
            dataset_id,
            activity,
            records_processed
        )
        VALUES
        (
            :dataset_id,
            :activity,
            :rows
        );
        """),{
            "dataset_id":dataset_id,
            "activity":activity,
            "rows":rows
        })

# ==========================================================
# READ FACT TABLE
# ==========================================================

def fetch_workforce():

    initialize_database()

    try:
        return pd.read_sql(
            "SELECT * FROM fact_workforce",
            engine
        )

    except SQLAlchemyError:
        return pd.DataFrame()

def fetch_datasets():

    initialize_database()

    return pd.read_sql("""
    SELECT *
    FROM dataset_registry
    ORDER BY uploaded_at DESC
    """,engine)


def fetch_audit_logs():
    initialize_database()

    try:
        return pd.read_sql("""
        SELECT *
        FROM audit_log
        ORDER BY log_time DESC
        """, engine)

    except Exception:
        # Old schema compatibility
        return pd.read_sql("""
        SELECT *,
               CURRENT_TIMESTAMP AS log_time
        FROM audit_log
        ORDER BY log_id DESC
        """, engine)


def clear_database():

    initialize_database()

    with engine.begin() as conn:

        conn.execute(text("DELETE FROM fact_workforce"))
        conn.execute(text("DELETE FROM dataset_registry"))
        conn.execute(text("DELETE FROM audit_log"))

from sqlalchemy import text

def clear_workforce_data():
    initialize_database()

    with engine.begin() as conn:
        conn.execute(text("TRUNCATE TABLE fact_workforce RESTART IDENTITY CASCADE;"))
        conn.execute(text("TRUNCATE TABLE dataset_registry RESTART IDENTITY CASCADE;"))

    return True


def warehouse_record_count():
    initialize_database()

    with engine.begin() as conn:
        count = conn.execute(
            text("SELECT COUNT(*) FROM fact_workforce")
        ).scalar()

    return count
