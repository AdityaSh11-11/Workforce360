CREATE OR REPLACE VIEW vw_department_summary AS
SELECT
d.department_name,
COUNT(*) employee_count,
ROUND(AVG(salary),2) average_salary,
ROUND(AVG(attendance_percentage),2) average_attendance,
ROUND(AVG(performance_rating),2) average_rating
FROM fact_workforce f
JOIN dim_department d
ON f.department_id=d.department_id
GROUP BY d.department_name;

CREATE OR REPLACE VIEW vw_attrition_summary AS
SELECT
d.department_name,
COUNT(*) attrition_count
FROM fact_workforce f
JOIN dim_department d
ON f.department_id=d.department_id
WHERE attrition_status='Left'
GROUP BY d.department_name;

CREATE OR REPLACE VIEW vw_salary_band_summary AS
SELECT
salary_band,
COUNT(*) employees,
ROUND(AVG(salary),2) average_salary
FROM(
SELECT salary,
CASE
WHEN salary<30000 THEN 'Low'
WHEN salary<70000 THEN 'Medium'
WHEN salary<120000 THEN 'High'
ELSE 'Executive'
END salary_band
FROM fact_workforce
)t
GROUP BY salary_band;