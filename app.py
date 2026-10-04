"""
E-Commerce Sales & Profit Analytics Dashboard — Main Application
================================================================
Entry point for the Streamlit multipage dashboard.
Provides global styling, sidebar navigation, overview KPIs,
and auto-generated business insights computed from the dataset.
"""
import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
import os

# ── Page configuration ──────────────────────────────────────────
st.set_page_config(
    page_title="E-Commerce Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Global CSS for professional styling ─────────────────────────
st.markdown("""
<style>
/* Google font import */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* ---- Main page ---- */
.main { padding: 0.5rem 1rem; }

/* ---- KPI metric cards ---- */
div[data-testid="stMetric"] {
    background: linear-gradient(135deg, #667eea11, #764ba211);
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 18px 20px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    transition: transform 0.2s ease;
}
div[data-testid="stMetric"]:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 14px rgba(0,0,0,0.08);
}

/* ---- Section headers ---- */
h1 {
    color: #1e293b;
    padding-bottom: 8px;
    border-bottom: 3px solid #667eea;
}
h2 { color: #334155; margin-top: 24px; }
h3 { color: #475569; }

/* ---- Sidebar ---- */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #f8fafc 0%, #eef2ff 100%);
}

/* ---- Insight cards ---- */
.insight-card {
    background: linear-gradient(135deg, #f0f9ff, #eff6ff);
    border-left: 4px solid #3b82f6;
    border-radius: 8px;
    padding: 16px 20px;
    margin: 8px 0;
}
.insight-card-warn {
    background: linear-gradient(135deg, #fefce8, #fef9c3);
    border-left: 4px solid #eab308;
    border-radius: 8px;
    padding: 16px 20px;
    margin: 8px 0;
}
.insight-card-success {
    background: linear-gradient(135deg, #f0fdf4, #dcfce7);
    border-left: 4px solid #22c55e;
    border-radius: 8px;
    padding: 16px 20px;
    margin: 8px 0;
}
.insight-card-danger {
    background: linear-gradient(135deg, #fef2f2, #fee2e2);
    border-left: 4px solid #ef4444;
    border-radius: 8px;
    padding: 16px 20px;
    margin: 8px 0;
}

/* ---- Footer ---- */
.footer {
    text-align: center;
    color: #94a3b8;
    padding: 32px 0 16px;
    font-size: 0.85rem;
}

/* Hide default Streamlit elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# ── Data loading (cached) ───────────────────────────────────────
@st.cache_data
def load_data():
    """Load cleaned data from SQLite database or CSV fallback."""
    db_path = os.path.join("data", "ecommerce.db")
    csv_path = os.path.join("data", "clean_superstore.csv")

    try:
        if os.path.exists(db_path):
            conn = sqlite3.connect(db_path)
            df = pd.read_sql_query("SELECT * FROM sales", conn)
            conn.close()
        elif os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
        else:
            return None
    except Exception:
        return None

    # Ensure date types
    df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
    df["Ship Date"] = pd.to_datetime(df["Ship Date"], errors="coerce")

    # Ensure numeric types
    for col in ["Sales", "Profit", "Quantity", "Discount"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


# ── Load data ───────────────────────────────────────────────────
df = load_data()

if df is None:
    st.error("⚠️ **Data not found!** Please run the data pipeline first:")
    st.code(
        "python src/download_data.py\n"
        "python src/clean_data.py\n"
        "python src/create_database.py",
        language="bash",
    )
    st.stop()


# ── Sidebar ─────────────────────────────────────────────────────
st.sidebar.title("🔍 Navigation")
st.sidebar.markdown("""
### Dashboard Pages

Use the sidebar navigation to explore:

1. **📊 Executive Overview** — Key metrics & trends
2. **🏆 Product Analysis** — Product performance
3. **👥 Customer Analysis** — Customer & regional analytics

---
""")

st.sidebar.markdown("### 📈 Data Summary")
st.sidebar.metric("Total Records", f"{len(df):,}")
st.sidebar.metric(
    "Date Range",
    f"{df['Order Date'].min().strftime('%b %Y')} – {df['Order Date'].max().strftime('%b %Y')}",
)

# ── Hero Section ────────────────────────────────────────────────
st.title("📊 E-Commerce Sales & Profit Analytics")
st.markdown(
    "_A production-quality data analytics dashboard powered by Python, SQL & Streamlit_"
)
st.markdown("---")

# ── Quick KPIs ──────────────────────────────────────────────────
total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()
total_orders = df["Order ID"].nunique()
customer_col = "Customer Name" if "Customer Name" in df.columns else "Customer ID"
total_customers = df[customer_col].nunique()
profit_margin = (total_profit / total_sales * 100) if total_sales > 0 else 0
avg_order_value = (total_sales / total_orders) if total_orders > 0 else 0
total_quantity = int(df["Quantity"].sum())

product_col = "Product Name" if "Product Name" in df.columns else "Product ID"
total_products = df[product_col].nunique()

c1, c2, c3, c4 = st.columns(4)
c1.metric("💰 Total Sales", f"${total_sales:,.0f}")
c2.metric("💵 Total Profit", f"${total_profit:,.0f}")
c3.metric("📦 Total Orders", f"{total_orders:,}")
c4.metric("👥 Total Customers", f"{total_customers:,}")

c5, c6, c7, c8 = st.columns(4)
c5.metric("📊 Profit Margin", f"{profit_margin:.2f}%")
c6.metric("💳 Avg Order Value", f"${avg_order_value:,.2f}")
c7.metric("📋 Total Products", f"{total_products:,}")
c8.metric("🛒 Units Sold", f"{total_quantity:,}")

st.markdown("---")

# ── Auto-Generated Business Insights ────────────────────────────
st.header("💡 Key Business Insights")
st.caption("Automatically calculated from the dataset — no hard-coded values")

# --- Category insights ---
cat_data = df.groupby("Category").agg({"Sales": "sum", "Profit": "sum"}).reset_index()
cat_data["Margin"] = cat_data["Profit"] / cat_data["Sales"] * 100

best_cat_sales = cat_data.loc[cat_data["Sales"].idxmax()]
best_cat_profit = cat_data.loc[cat_data["Profit"].idxmax()]
worst_cat_margin = cat_data.loc[cat_data["Margin"].idxmin()]

# --- Regional insights ---
if "Region" in df.columns:
    reg_data = df.groupby("Region").agg({"Sales": "sum", "Profit": "sum"}).reset_index()
    best_region = reg_data.loc[reg_data["Sales"].idxmax()]
    worst_region = reg_data.loc[reg_data["Profit"].idxmin()]

# --- Product insights ---
prod_data = df.groupby(product_col).agg({"Sales": "sum", "Profit": "sum"}).reset_index()
top_product = prod_data.loc[prod_data["Sales"].idxmax()]
loss_product = prod_data.loc[prod_data["Profit"].idxmin()]
num_loss_products = len(prod_data[prod_data["Profit"] < 0])

# --- Customer insights ---
cust_data = (
    df.groupby(customer_col)
    .agg({"Sales": "sum", "Profit": "sum"})
    .reset_index()
)
top_customer = cust_data.loc[cust_data["Sales"].idxmax()]

# --- Discount insights ---
discount_profit_corr = df["Discount"].corr(df["Profit"])
high_discount = df[df["Discount"] > 0.3]
avg_profit_high_disc = high_discount["Profit"].mean() if len(high_discount) > 0 else 0

# Display insights in cards
col_l, col_r = st.columns(2)

with col_l:
    st.markdown(f"""
    <div class="insight-card-success">
        <strong>🏆 Highest Revenue Category:</strong> {best_cat_sales['Category']}<br>
        Sales: ${best_cat_sales['Sales']:,.0f}
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="insight-card-success">
        <strong>💰 Most Profitable Category:</strong> {best_cat_profit['Category']}<br>
        Profit: ${best_cat_profit['Profit']:,.0f}
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="insight-card-danger">
        <strong>⚠️ Lowest Margin Category:</strong> {worst_cat_margin['Category']}<br>
        Margin: {worst_cat_margin['Margin']:.2f}%
    </div>
    """, unsafe_allow_html=True)

    if "Region" in df.columns:
        st.markdown(f"""
        <div class="insight-card">
            <strong>🌍 Best Region:</strong> {best_region['Region']}<br>
            Sales: ${best_region['Sales']:,.0f}
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="insight-card-danger">
            <strong>📉 Worst Region (by Profit):</strong> {worst_region['Region']}<br>
            Profit: ${worst_region['Profit']:,.0f}
        </div>
        """, unsafe_allow_html=True)

with col_r:
    st.markdown(f"""
    <div class="insight-card">
        <strong>🥇 Top Product:</strong><br>
        {top_product[product_col][:70]}<br>
        Sales: ${top_product['Sales']:,.0f}
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="insight-card-danger">
        <strong>❌ Most Loss-Making Product:</strong><br>
        {loss_product[product_col][:70]}<br>
        Loss: ${loss_product['Profit']:,.0f}
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="insight-card-warn">
        <strong>📊 Unprofitable Products:</strong> {num_loss_products} out of {total_products}
        ({num_loss_products / total_products * 100:.1f}%)
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="insight-card-success">
        <strong>👤 Highest-Value Customer:</strong> {top_customer[customer_col]}<br>
        Sales: ${top_customer['Sales']:,.0f}
    </div>
    """, unsafe_allow_html=True)

    disc_direction = "negatively" if discount_profit_corr < 0 else "positively"
    st.markdown(f"""
    <div class="insight-card-warn">
        <strong>💸 Discount–Profit Correlation:</strong> {discount_profit_corr:.3f}<br>
        Discounts are <strong>{disc_direction}</strong> correlated with profitability.
        {"Orders >30% discount average $" + f"{avg_profit_high_disc:,.2f} profit per item." if len(high_discount) > 0 else ""}
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ── Project Overview & Getting Started ──────────────────────────
col_about, col_tech = st.columns([3, 2])

with col_about:
    st.header("🎯 Project Overview")
    st.markdown("""
    This is a **production-quality data analytics portfolio project** demonstrating:

    - **Data Engineering** — Automated data download, cleaning & validation
    - **Database Design** — SQLite database with optimized schema & indexes
    - **SQL Analysis** — 30 business intelligence queries (CTEs, window functions, subqueries)
    - **Python EDA** — Comprehensive exploratory analysis with Matplotlib/Seaborn
    - **Interactive Dashboard** — Multi-page Streamlit app with Plotly visualizations
    - **Business Insights** — Actionable findings calculated from real data
    """)

with col_tech:
    st.header("🛠️ Tech Stack")
    st.markdown("""
    | Layer | Technology |
    |---|---|
    | Language | Python 3 |
    | Data | Pandas, NumPy |
    | Visualization | Matplotlib, Seaborn, Plotly |
    | Database | SQLite + SQL |
    | Dashboard | Streamlit |
    | Version Control | Git & GitHub |
    """)

st.markdown("---")

# ── Getting Started ─────────────────────────────────────────────
st.header("🚀 Getting Started")

st.markdown("""
1. **Navigate** → Use the sidebar to explore the three analysis pages
2. **Filter** → Use interactive controls on each page to drill down
3. **Hover** → Charts are interactive — hover for details, zoom, pan
4. **Download** → Export filtered data as CSV on any page

| Page | Description |
|------|-------------|
| 📊 **Executive Overview** | High-level KPIs, monthly trends, category & regional breakdowns |
| 🏆 **Product Analysis** | Top/bottom products, sub-category performance, discount impact |
| 👥 **Customer & Regional** | Customer rankings, segment analysis, shipping performance |
""")

st.markdown("---")

# ── Footer ──────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    📊 E-Commerce Sales & Profit Analytics Dashboard<br>
    Built with Python · Pandas · SQLite · Plotly · Streamlit<br>
    © 2024 — Data Analytics Portfolio Project
</div>
""", unsafe_allow_html=True)
