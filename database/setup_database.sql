DROP TABLE IF EXISTS fact_workforce CASCADE;
DROP TABLE IF EXISTS workforce_dataset CASCADE;
DROP TABLE IF EXISTS audit_log CASCADE;

CREATE TABLE workforce_dataset(
    dataset_id SERIAL PRIMARY KEY,
    dataset_name VARCHAR(255),
    dataset_type VARCHAR(50),
    quality_score FLOAT,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE fact_workforce(
    employee_id VARCHAR(50),
    employee_name VARCHAR(255),
    gender VARCHAR(20),
    age INT,
    email VARCHAR(255),
    phone VARCHAR(50),
    department VARCHAR(100),
    job_role VARCHAR(150),
    city VARCHAR(100),
    state VARCHAR(100),
    joining_date DATE,
    employment_type VARCHAR(50),
    salary FLOAT,
    experience_years FLOAT,
    tenure_years FLOAT,
    attendance_percentage FLOAT,
    performance_rating FLOAT,
    training_hours FLOAT,
    overtime_hours FLOAT,
    promotion_status VARCHAR(50),
    attrition_status VARCHAR(50),
    salary_band VARCHAR(50),
    experience_group VARCHAR(50),
    joining_year INT,
    joining_month VARCHAR(20),
    joining_quarter VARCHAR(10),
    dataset_id INT
);

CREATE TABLE audit_log(
    log_id SERIAL PRIMARY KEY,
    dataset_id INT,
    activity TEXT,
    records_processed INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);