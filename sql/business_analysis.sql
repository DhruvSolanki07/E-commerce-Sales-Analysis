-- E-COMMERCE SALES ANALYSIS - BUSINESS QUERIES
-- This file contains 25+ SQL queries for comprehensive business analysis

-- ========================================
-- BASIC AGGREGATIONS
-- ========================================

-- 1. Total Sales
SELECT
    ROUND(SUM(Sales), 2) as total_sales
FROM sales;

-- 2. Total Profit
SELECT
    ROUND(SUM(Profit), 2) as total_profit
FROM sales;

-- 3. Total Orders
SELECT
    COUNT(DISTINCT "Order ID") as total_orders
FROM sales;

-- 4. Total Customers
SELECT
    COUNT(DISTINCT "Customer ID") as total_customers
FROM sales;

-- 5. Overall Profit Margin
SELECT
    ROUND(SUM(Profit) * 100.0 / SUM(Sales), 2) as profit_margin_percentage
FROM sales;

-- ========================================
-- CATEGORY ANALYSIS
-- ========================================

-- 6. Sales by Category
SELECT
    Category,
    ROUND(SUM(Sales), 2) as total_sales,
    COUNT(*) as order_count
FROM sales
GROUP BY Category
ORDER BY total_sales DESC;

-- 7. Profit by Category
SELECT
    Category,
    ROUND(SUM(Profit), 2) as total_profit,
    ROUND(SUM(Profit) * 100.0 / SUM(Sales), 2) as profit_margin_pct
FROM sales
GROUP BY Category
ORDER BY total_profit DESC;

-- 8. Profit Margin by Category
SELECT
    Category,
    ROUND(SUM(Sales), 2) as total_sales,
    ROUND(SUM(Profit), 2) as total_profit,
    ROUND(SUM(Profit) * 100.0 / SUM(Sales), 2) as profit_margin_pct
FROM sales
GROUP BY Category
ORDER BY profit_margin_pct DESC;

-- ========================================
-- REGIONAL ANALYSIS
-- ========================================

-- 9. Sales by Region
SELECT
    Region,
    ROUND(SUM(Sales), 2) as total_sales,
    COUNT(DISTINCT "Order ID") as total_orders
FROM sales
GROUP BY Region
ORDER BY total_sales DESC;

-- 10. Profit by Region
SELECT
    Region,
    ROUND(SUM(Profit), 2) as total_profit,
    ROUND(SUM(Profit) * 100.0 / SUM(Sales), 2) as profit_margin_pct
FROM sales
GROUP BY Region
ORDER BY total_profit DESC;

-- ========================================
-- PRODUCT ANALYSIS
-- ========================================

-- 11. Top 10 Products by Sales
SELECT
    "Product Name",
    Category,
    "Sub-Category",
    ROUND(SUM(Sales), 2) as total_sales,
    SUM(Quantity) as total_quantity
FROM sales
GROUP BY "Product Name", Category, "Sub-Category"
ORDER BY total_sales DESC
LIMIT 10;

-- 12. Top 10 Products by Profit
SELECT
    "Product Name",
    Category,
    ROUND(SUM(Profit), 2) as total_profit,
    ROUND(SUM(Sales), 2) as total_sales
FROM sales
GROUP BY "Product Name", Category
ORDER BY total_profit DESC
LIMIT 10;

-- 13. Bottom 10 Products by Profit (Loss-makers)
SELECT
    "Product Name",
    Category,
    ROUND(SUM(Profit), 2) as total_profit,
    ROUND(SUM(Sales), 2) as total_sales,
    COUNT(*) as order_count
FROM sales
GROUP BY "Product Name", Category
ORDER BY total_profit ASC
LIMIT 10;

-- ========================================
-- CUSTOMER ANALYSIS
-- ========================================

-- 14. Top 10 Customers by Sales
SELECT
    "Customer Name",
    Segment,
    Region,
    ROUND(SUM(Sales), 2) as total_sales,
    ROUND(SUM(Profit), 2) as total_profit,
    COUNT(DISTINCT "Order ID") as total_orders
FROM sales
GROUP BY "Customer Name", Segment, Region
ORDER BY total_sales DESC
LIMIT 10;

-- 15. Customer Ranking by Profit
SELECT
    "Customer Name",
    ROUND(SUM(Profit), 2) as total_profit,
    ROUND(SUM(Sales), 2) as total_sales,
    COUNT(DISTINCT "Order ID") as order_count,
    RANK() OVER (ORDER BY SUM(Profit) DESC) as profit_rank
FROM sales
GROUP BY "Customer Name"
ORDER BY profit_rank
LIMIT 20;

-- ========================================
-- TIME-BASED ANALYSIS
-- ========================================

-- 16. Monthly Sales Trend
SELECT
    Year_Month,
    ROUND(SUM(Sales), 2) as monthly_sales,
    ROUND(SUM(Profit), 2) as monthly_profit,
    COUNT(DISTINCT "Order ID") as order_count
FROM sales
GROUP BY Year_Month
ORDER BY Year_Month;

-- 17. Yearly Sales and Profit
SELECT
    Year,
    ROUND(SUM(Sales), 2) as yearly_sales,
    ROUND(SUM(Profit), 2) as yearly_profit,
    COUNT(DISTINCT "Order ID") as total_orders,
    COUNT(DISTINCT "Customer ID") as unique_customers
FROM sales
GROUP BY Year
ORDER BY Year;

-- 18. Year-over-Year Sales Growth
WITH yearly_sales AS (
    SELECT
        Year,
        SUM(Sales) as total_sales
    FROM sales
    GROUP BY Year
)
SELECT
    Year,
    ROUND(total_sales, 2) as sales,
    LAG(total_sales) OVER (ORDER BY Year) as previous_year_sales,
    ROUND(
        (total_sales - LAG(total_sales) OVER (ORDER BY Year)) * 100.0 /
        NULLIF(LAG(total_sales) OVER (ORDER BY Year), 0),
        2
    ) as yoy_growth_pct
FROM yearly_sales
ORDER BY Year;

-- ========================================
-- SEGMENT ANALYSIS
-- ========================================

-- 19. Performance by Customer Segment
SELECT
    Segment,
    ROUND(SUM(Sales), 2) as total_sales,
    ROUND(SUM(Profit), 2) as total_profit,
    COUNT(DISTINCT "Customer ID") as customer_count,
    COUNT(DISTINCT "Order ID") as order_count,
    ROUND(AVG(Sales), 2) as avg_order_value
FROM sales
GROUP BY Segment
ORDER BY total_sales DESC;

-- ========================================
-- DISCOUNT ANALYSIS
-- ========================================

-- 20. Impact of Discount on Profit
SELECT
    CASE
        WHEN Discount = 0 THEN 'No Discount'
        WHEN Discount <= 0.1 THEN '1-10%'
        WHEN Discount <= 0.2 THEN '11-20%'
        WHEN Discount <= 0.3 THEN '21-30%'
        ELSE '30%+'
    END as discount_range,
    COUNT(*) as order_count,
    ROUND(SUM(Sales), 2) as total_sales,
    ROUND(SUM(Profit), 2) as total_profit,
    ROUND(AVG(Profit_Margin), 2) as avg_profit_margin_pct
FROM sales
GROUP BY discount_range
ORDER BY
    CASE discount_range
        WHEN 'No Discount' THEN 1
        WHEN '1-10%' THEN 2
        WHEN '11-20%' THEN 3
        WHEN '21-30%' THEN 4
        ELSE 5
    END;

-- ========================================
-- SHIPPING ANALYSIS
-- ========================================

-- 21. Shipping Mode Performance
SELECT
    "Ship Mode",
    COUNT(*) as order_count,
    ROUND(SUM(Sales), 2) as total_sales,
    ROUND(AVG(Shipping_Days), 2) as avg_shipping_days,
    ROUND(SUM(Profit), 2) as total_profit
FROM sales
GROUP BY "Ship Mode"
ORDER BY order_count DESC;

-- ========================================
-- SUB-CATEGORY ANALYSIS
-- ========================================

-- 22. Top Sub-Categories by Sales
SELECT
    Category,
    "Sub-Category",
    ROUND(SUM(Sales), 2) as total_sales,
    ROUND(SUM(Profit), 2) as total_profit,
    ROUND(SUM(Profit) * 100.0 / SUM(Sales), 2) as profit_margin_pct
FROM sales
GROUP BY Category, "Sub-Category"
ORDER BY total_sales DESC
LIMIT 15;

-- ========================================
-- ADVANCED QUERIES
-- ========================================

-- 23. Loss-Making Products Analysis
SELECT
    "Product Name",
    Category,
    "Sub-Category",
    ROUND(SUM(Sales), 2) as total_sales,
    ROUND(SUM(Profit), 2) as total_profit,
    COUNT(*) as order_count,
    ROUND(AVG(Discount), 2) as avg_discount
FROM sales
GROUP BY "Product Name", Category, "Sub-Category"
HAVING SUM(Profit) < 0
ORDER BY total_profit ASC
LIMIT 20;

-- 24. High Sales, Low Profit Products
SELECT
    "Product Name",
    Category,
    ROUND(SUM(Sales), 2) as total_sales,
    ROUND(SUM(Profit), 2) as total_profit,
    ROUND(SUM(Profit) * 100.0 / SUM(Sales), 2) as profit_margin_pct
FROM sales
GROUP BY "Product Name", Category
HAVING SUM(Sales) > 10000 AND SUM(Profit) * 100.0 / SUM(Sales) < 5
ORDER BY total_sales DESC;

-- 25. Top 3 Products per Category (Window Function)
WITH ranked_products AS (
    SELECT
        Category,
        "Product Name",
        ROUND(SUM(Sales), 2) as total_sales,
        RANK() OVER (PARTITION BY Category ORDER BY SUM(Sales) DESC) as rank
    FROM sales
    GROUP BY Category, "Product Name"
)
SELECT
    Category,
    "Product Name",
    total_sales,
    rank
FROM ranked_products
WHERE rank <= 3
ORDER BY Category, rank;

-- 26. Customer Lifetime Value (CLV)
SELECT
    "Customer Name",
    Segment,
    Region,
    COUNT(DISTINCT "Order ID") as total_orders,
    ROUND(SUM(Sales), 2) as lifetime_value,
    ROUND(SUM(Profit), 2) as lifetime_profit,
    ROUND(AVG(Sales), 2) as avg_order_value,
    MIN("Order Date") as first_order_date,
    MAX("Order Date") as last_order_date
FROM sales
GROUP BY "Customer Name", Segment, Region
ORDER BY lifetime_value DESC
LIMIT 20;

-- 27. Profit Status Distribution
SELECT
    Profit_Status,
    COUNT(*) as transaction_count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM sales), 2) as percentage,
    ROUND(SUM(Sales), 2) as total_sales,
    ROUND(SUM(Profit), 2) as total_profit
FROM sales
GROUP BY Profit_Status
ORDER BY transaction_count DESC;

-- 28. Regional Performance with Rankings
SELECT
    Region,
    ROUND(SUM(Sales), 2) as total_sales,
    ROUND(SUM(Profit), 2) as total_profit,
    RANK() OVER (ORDER BY SUM(Sales) DESC) as sales_rank,
    RANK() OVER (ORDER BY SUM(Profit) DESC) as profit_rank,
    DENSE_RANK() OVER (ORDER BY SUM(Profit) * 100.0 / SUM(Sales) DESC) as margin_rank
FROM sales
GROUP BY Region;

-- 29. Category Performance by Year
SELECT
    Year,
    Category,
    ROUND(SUM(Sales), 2) as yearly_sales,
    ROUND(SUM(Profit), 2) as yearly_profit
FROM sales
GROUP BY Year, Category
ORDER BY Year, yearly_sales DESC;

-- 30. Average Order Processing Time by Ship Mode
SELECT
    "Ship Mode",
    ROUND(AVG(Shipping_Days), 2) as avg_processing_days,
    MIN(Shipping_Days) as min_days,
    MAX(Shipping_Days) as max_days,
    COUNT(*) as order_count
FROM sales
WHERE Shipping_Days >= 0
GROUP BY "Ship Mode"
ORDER BY avg_processing_days;
