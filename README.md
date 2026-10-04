# 📊 E-Commerce Sales & Profit Analytics

## 🎯 Project Overview

This is a **comprehensive data analytics portfolio project** that demonstrates end-to-end data analysis skills using Python, SQL, and interactive dashboards. The project analyzes e-commerce sales data to uncover business insights, track KPIs, and identify opportunities for growth and optimization.

## 🚀 Live Dashboard

*Add screenshot here after running the application*

## 📌 Business Problem

E-commerce businesses need to:
- Track sales and profitability across products, regions, and customer segments
- Identify top-performing and underperforming products
- Understand customer behavior and preferences
- Optimize discount strategies
- Improve regional and segment-specific performance
- Monitor shipping efficiency

## 🎯 Objectives

1. **Data Engineering**: Build an automated data pipeline for downloading, cleaning, and validating sales data
2. **Database Design**: Create a SQLite database with optimized schema and queries
3. **Exploratory Analysis**: Perform comprehensive EDA to uncover patterns and trends
4. **SQL Analytics**: Write complex business intelligence queries
5. **Interactive Dashboard**: Build a production-quality Streamlit dashboard with filtering and visualization
6. **Business Insights**: Generate actionable recommendations based on data analysis

## 📊 Dataset

**Source**: [Sample Superstore Dataset](https://raw.githubusercontent.com/leonism/sample-superstore/master/data/superstore.csv)

**Description**: The dataset contains retail sales transactions with the following information:
- Order details (dates, shipping, customer info)
- Product information (category, sub-category, product name)
- Sales metrics (sales amount, quantity, discount, profit)
- Geographic data (region, state, city)
- Customer segments

### Data Dictionary

| Column | Description | Type |
|--------|-------------|------|
| Order ID | Unique order identifier | String |
| Order Date | Date when order was placed | Date |
| Ship Date | Date when order was shipped | Date |
| Ship Mode | Shipping method | Categorical |
| Customer ID | Unique customer identifier | String |
| Customer Name | Customer full name | String |
| Segment | Customer segment (Consumer/Corporate/Home Office) | Categorical |
| Country | Country name | String |
| City | City name | String |
| State | State name | String |
| Region | Geographic region | Categorical |
| Product ID | Unique product identifier | String |
| Category | Product category | Categorical |
| Sub-Category | Product sub-category | Categorical |
| Product Name | Full product name | String |
| Sales | Sales amount in USD | Float |
| Quantity | Number of units sold | Integer |
| Discount | Discount percentage | Float |
| Profit | Profit amount in USD | Float |

### Derived Columns (Created During Cleaning)

| Column | Description |
|--------|-------------|
| Year | Year extracted from Order Date |
| Month | Month number (1-12) |
| Month_Name | Month name (January-December) |
| Year_Month | Year-Month combination for time series |
| Shipping_Days | Days between order and ship date |
| Profit_Margin | (Profit / Sales) * 100 |
| Profit_Status | Profit/Loss/Break-even classification |

## 🛠️ Technologies & Tools

### Programming & Analysis
- **Python 3.8+**: Core programming language
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computations
- **Matplotlib**: Static visualizations
- **Seaborn**: Statistical visualizations

### Database
- **SQLite**: Relational database for data storage
- **SQL**: Business intelligence queries

### Dashboard & Visualization
- **Streamlit**: Interactive web dashboard framework
- **Plotly**: Interactive charts and graphs

### Version Control
- **Git**: Version control system
- **GitHub**: Code repository hosting

## 📁 Project Structure

```
ecommerce-sales-analysis/
│
├── data/                          # Data files
│   ├── superstore.csv            # Raw downloaded data
│   ├── clean_superstore.csv      # Cleaned data
│   └── ecommerce.db              # SQLite database
│
├── src/                          # Python source code
│   ├── download_data.py          # Download dataset from GitHub
│   ├── clean_data.py             # Data cleaning and preprocessing
│   ├── eda.py                    # Exploratory data analysis
│   └── create_database.py        # SQLite database creation
│
├── sql/                          # SQL queries
│   └── business_analysis.sql     # 30+ business intelligence queries
│
├── outputs/                      # Generated visualizations
│   ├── monthly_trends.png
│   ├── category_performance.png
│   ├── regional_performance.png
│   └── ... (other charts)
│
├── pages/                        # Streamlit dashboard pages
│   ├── 1_Executive_Overview.py   # KPIs and high-level trends
│   ├── 2_Product_Analysis.py     # Product performance analysis
│   └── 3_Customer_Analysis.py    # Customer and regional insights
│
├── app.py                        # Main Streamlit application
├── requirements.txt              # Python dependencies
├── README.md                     # Project documentation
├── .gitignore                    # Git ignore rules
└── LICENSE                       # Project license
```

## 🔄 Data Pipeline

### 1. Data Download (`download_data.py`)
- Automatically downloads dataset from GitHub
- Validates file size and integrity
- Saves to `data/superstore.csv`

### 2. Data Cleaning (`clean_data.py`)
- Removes duplicate records
- Handles missing values
- Converts data types (dates, numerics)
- Creates derived columns
- Validates data quality
- Saves to `data/clean_superstore.csv`
- Generates data quality report

### 3. Exploratory Data Analysis (`eda.py`)
- Calculates key business metrics
- Analyzes time trends
- Examines category and regional performance
- Identifies top/bottom products
- Analyzes customer behavior
- Studies discount impact
- Generates static visualizations
- Saves charts to `outputs/`

### 4. Database Creation (`create_database.py`)
- Creates SQLite database
- Loads cleaned data into `sales` table
- Creates indexes for query optimization
- Validates data integrity

## 📊 SQL Analysis

The `sql/business_analysis.sql` file contains **30+ business intelligence queries** including:

### Basic Metrics
1. Total sales, profit, orders, customers
2. Overall profit margin

### Category Analysis
3. Sales and profit by category
4. Profit margin by category
5. Sub-category performance

### Regional Analysis
6. Sales and profit by region
7. Regional rankings

### Product Analysis
8. Top 10 products by sales
9. Top 10 products by profit
10. Bottom 10 products (loss-makers)
11. Top 3 products per category (window functions)

### Customer Analysis
12. Top customers by sales
13. Customer lifetime value (CLV)
14. Customer ranking with RANK()

### Time-Based Analysis
15. Monthly sales and profit trends
16. Yearly aggregations
17. Year-over-year growth with LAG()

### Segment Analysis
18. Performance by customer segment

### Discount Analysis
19. Impact of discounts on profitability

### Shipping Analysis
20. Shipping mode performance
21. Average processing time

### Advanced Queries
22. Loss-making products with filters
23. High sales, low profit products
24. Profit status distribution
25. CTEs and subqueries

## 📈 Dashboard Features

### Page 1: Executive Overview
- **KPI Cards**: Sales, Profit, Orders, Customers, Profit Margin, Avg Order Value
- **Time Trends**: Monthly sales and profit line charts
- **Category Performance**: Sales and profit by category
- **Regional Performance**: Regional sales and profit distribution
- **Segment Analysis**: Performance by customer segment
- **Interactive Filters**: Year, Category, Region, Segment, Ship Mode
- **Data Export**: Download filtered data as CSV

### Page 2: Product Analysis
- **Top 10 Products**: By sales and profit
- **Bottom 10 Products**: Loss-making products
- **Sub-Category Analysis**: Performance breakdown
- **Discount Impact**: Profitability by discount range
- **Quantity Analysis**: Units sold by product and category
- **Searchable Table**: Filter and sort products
- **Product Filters**: Category, Sub-Category, Year

### Page 3: Customer & Regional Analysis
- **Top 20 Customers**: By sales revenue
- **Customer Profitability**: Top customers by profit
- **Order Frequency**: Customers by order count
- **Regional Performance**: Sales and profit by region
- **Segment Breakdown**: Analysis by customer segment
- **Shipping Performance**: Efficiency by shipping mode
- **Customer Search**: Find and analyze specific customers
- **Transaction Details**: Downloadable detailed data

## 💡 Key Insights

*These insights will be populated after running the analysis on actual data. Example format:*

### Sales Performance
- **Total Sales**: $X.XX million
- **Total Profit**: $X.XX million
- **Overall Profit Margin**: X.XX%
- **Total Orders**: X,XXX
- **Total Customers**: X,XXX

### Category Insights
- **Highest Revenue Category**: [Category Name]
- **Most Profitable Category**: [Category Name]
- **Lowest Margin Category**: [Category Name]

### Regional Performance
- **Best Performing Region**: [Region Name]
- **Region Needing Attention**: [Region Name]

### Product Insights
- **Top Product**: [Product Name]
- **Most Loss-Making Product**: [Product Name]
- **Number of Unprofitable Products**: X

### Customer Behavior
- **Top Customer**: [Customer Name]
- **Average Order Value**: $XXX.XX
- **Most Valuable Segment**: [Segment Name]

### Discount Strategy
- **Discount Impact**: Higher discounts correlate with lower/higher profit margins
- **Optimal Discount Range**: X-X%

## 📋 Business Recommendations

*Example recommendations based on typical e-commerce patterns:*

1. **Optimize Discount Strategy**
   - Review products with high discounts but negative profitability
   - Test discount caps to maintain healthy margins

2. **Focus on High-Margin Categories**
   - Increase marketing spend on profitable categories
   - Bundle low-margin with high-margin products

3. **Regional Expansion**
   - Invest in underperforming regions with growth potential
   - Replicate successful strategies from top regions

4. **Product Portfolio Management**
   - Discontinue or repricing consistently loss-making products
   - Increase inventory for top performers

5. **Customer Retention**
   - Develop loyalty programs for top customers
   - Re-engage dormant high-value customers

6. **Shipping Optimization**
   - Negotiate better rates for most-used shipping modes
   - Optimize shipping speed vs. cost trade-off

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git (for cloning repository)

### Step 1: Clone Repository
```bash
git clone https://github.com/yourusername/ecommerce-sales-analysis.git
cd ecommerce-sales-analysis
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

## ▶️ How to Run

### Complete Pipeline (Recommended for First Run)

Run all steps in sequence:

```bash
# Step 1: Download data
python src/download_data.py

# Step 2: Clean data
python src/clean_data.py

# Step 3: Run EDA and generate charts
python src/eda.py

# Step 4: Create SQLite database
python src/create_database.py

# Step 5: Launch Streamlit dashboard
streamlit run app.py
```

The dashboard will open automatically in your default web browser at `http://localhost:8501`

### Quick Start (If Data Already Exists)

If you've already run the pipeline:

```bash
streamlit run app.py
```

## 📸 Project Screenshots

*Add screenshots after running the application:*

1. **Executive Overview Dashboard**
   - *Screenshot of main dashboard with KPIs*

2. **Product Analysis Page**
   - *Screenshot of product performance charts*

3. **Customer Analysis Page**
   - *Screenshot of customer insights*

4. **EDA Visualizations**
   - *Screenshots of generated charts from outputs/*

## 🔍 SQL Query Examples

You can run SQL queries directly against the database:

```bash
# Open SQLite CLI
sqlite3 data/ecommerce.db

# Run a query
SELECT Category, SUM(Sales) as Total_Sales 
FROM sales 
GROUP BY Category 
ORDER BY Total_Sales DESC;

# Exit
.exit
```

Or execute queries from the SQL file:

```bash
sqlite3 data/ecommerce.db < sql/business_analysis.sql
```

## 🧪 Testing

The project includes built-in validation:

1. **Data Quality Checks**: Automatic validation during cleaning
2. **Database Integrity**: Test queries after database creation
3. **Dashboard Testing**: Error handling for empty filters

## 🔮 Future Improvements

- [ ] Add predictive analytics (sales forecasting)
- [ ] Implement customer segmentation using clustering
- [ ] Add more advanced SQL analytics (cohort analysis, RFM analysis)
- [ ] Create automated email reports
- [ ] Add real-time data refresh capability
- [ ] Implement A/B testing framework for discount strategies
- [ ] Add geospatial visualization for regional analysis
- [ ] Create executive PDF reports
- [ ] Add user authentication for dashboard
- [ ] Deploy to cloud (Streamlit Cloud, Heroku, AWS)

## 🎓 Skills Demonstrated

### Technical Skills
- Python programming (Pandas, NumPy, Matplotlib, Seaborn)
- SQL (SQLite, complex queries, window functions, CTEs)
- Data cleaning and preprocessing
- Exploratory data analysis (EDA)
- Statistical analysis
- Data visualization
- Dashboard development (Streamlit, Plotly)
- Version control (Git/GitHub)

### Business Skills
- Business intelligence
- KPI tracking and monitoring
- Data-driven decision making
- Insight generation
- Stakeholder reporting
- Business recommendations

### Software Engineering
- Modular code organization
- Error handling
- Documentation
- Project structure
- Code reusability

## 🎤 Interview Talking Points

### Project Introduction (30 seconds)
*"I built an end-to-end e-commerce analytics platform that processes sales data, stores it in a SQLite database, and presents insights through an interactive Streamlit dashboard. The project demonstrates my skills in Python, SQL, data visualization, and translating data into business recommendations."*

### Technical Deep-Dive
- **Data Pipeline**: Explain the ETL process
- **SQL Complexity**: Discuss window functions, CTEs, and optimization
- **Dashboard Design**: Explain UX decisions and interactivity
- **Insights Generation**: Walk through key findings

### Challenges & Solutions
- **Challenge**: Handling missing data and ensuring data quality
- **Solution**: Implemented comprehensive validation and quality checks

### Business Impact
- Identified loss-making products worth $XXX
- Discovered discount optimization opportunity
- Highlighted top 20% customers driving 80% of profit

## 📄 License

MIT License - Feel free to use this project for learning and portfolio purposes.

## 👤 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- LinkedIn: [Your LinkedIn](https://linkedin.com/in/yourprofile)
- Email: your.email@example.com

## 🙏 Acknowledgments

- Dataset source: [Sample Superstore Dataset](https://github.com/leonism/sample-superstore)
- Inspired by real-world business intelligence projects
- Built as a portfolio project to demonstrate data analytics skills

---

⭐ **If you find this project helpful, please give it a star!** ⭐
