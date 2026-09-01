DROP TABLE IF EXISTS fact_workforce CASCADE;
DROP TABLE IF EXISTS dataset_master CASCADE;
DROP TABLE IF EXISTS dim_department CASCADE;
DROP TABLE IF EXISTS dim_role CASCADE;
DROP TABLE IF EXISTS dim_location CASCADE;
DROP TABLE IF EXISTS dim_date CASCADE;

CREATE TABLE dim_department (
    department_id SERIAL PRIMARY KEY,
    department_name VARCHAR(100) UNIQUE
);

CREATE TABLE dim_role (
    role_id SERIAL PRIMARY KEY,
    role_name VARCHAR(100) UNIQUE
);

CREATE TABLE dim_location (
    location_id SERIAL PRIMARY KEY,
    city VARCHAR(100),
    state VARCHAR(100),
    UNIQUE(city, state)
);

CREATE TABLE dim_date (
    date_id SERIAL PRIMARY KEY,
    joining_date DATE UNIQUE,
    joining_year INT,
    joining_month VARCHAR(20),
    joining_quarter VARCHAR(10)
);

CREATE TABLE dataset_master (
    dataset_id SERIAL PRIMARY KEY,
    dataset_name VARCHAR(200),
    upload_source VARCHAR(100),
    total_rows INT,
    total_columns INT,
    quality_score FLOAT,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE fact_workforce (
    employee_id VARCHAR(30) PRIMARY KEY,
    dataset_id INT REFERENCES dataset_master(dataset_id),

    department_id INT REFERENCES dim_department(department_id),
    role_id INT REFERENCES dim_role(role_id),
    location_id INT REFERENCES dim_location(location_id),
    date_id INT REFERENCES dim_date(date_id),

    employee_name VARCHAR(150),
    gender VARCHAR(20),
    age INT,

    salary NUMERIC,
    experience_years NUMERIC,
    tenure_years NUMERIC,

    attendance_percentage NUMERIC,
    performance_rating NUMERIC,
    training_hours NUMERIC,
    overtime_hours NUMERIC,

    promotion_status VARCHAR(30),
    attrition_status VARCHAR(30)
);