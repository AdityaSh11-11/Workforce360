-- Total Sales by Category
SELECT category_name,
SUM(sales) total_sales
FROM vw_sales_summary
GROUP BY category_name
ORDER BY total_sales DESC;


-- Profit by Region
SELECT region_name,
SUM(total_profit) profit
FROM vw_sales_summary
GROUP BY region_name
ORDER BY profit DESC;


-- Top Customers
SELECT *
FROM vw_customer_sales
LIMIT 10;


-- Monthly Sales
SELECT
    d.month,
    SUM(fs.sales) total_sales
FROM fact_sales fs
JOIN dim_date d ON fs.date_id = d.date_id
GROUP BY d.month;