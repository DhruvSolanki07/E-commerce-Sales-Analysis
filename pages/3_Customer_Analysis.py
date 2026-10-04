"""
Customer & Regional Analysis Dashboard Page
=============================================
Top customers, customer profitability, regional performance,
segment analysis, shipping metrics, and transaction details.
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import sqlite3
import os

# ── Page config ─────────────────────────────────────────────────
st.set_page_config(page_title="Customer & Regional Analysis", page_icon="👥", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
div[data-testid="stMetric"] {
    background: linear-gradient(135deg, #667eea11, #764ba211);
    border: 1px solid #e2e8f0; border-radius: 12px;
    padding: 16px 18px; box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}
.insight-box { background:#f0f9ff; border-left:4px solid #3b82f6;
    border-radius:8px; padding:14px 18px; margin:6px 0; }
.insight-box-warn { background:#fefce8; border-left:4px solid #eab308;
    border-radius:8px; padding:14px 18px; margin:6px 0; }
.insight-box-good { background:#f0fdf4; border-left:4px solid #22c55e;
    border-radius:8px; padding:14px 18px; margin:6px 0; }
.insight-box-bad { background:#fef2f2; border-left:4px solid #ef4444;
    border-radius:8px; padding:14px 18px; margin:6px 0; }
#MainMenu {visibility:hidden;} footer {visibility:hidden;}
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    db = os.path.join("data", "ecommerce.db")
    csv_path = os.path.join("data", "clean_superstore.csv")
    try:
        if os.path.exists(db):
            conn = sqlite3.connect(db)
            df = pd.read_sql_query("SELECT * FROM sales", conn)
            conn.close()
        elif os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
        else:
            return None
    except Exception:
        return None
    df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
    df["Ship Date"] = pd.to_datetime(df["Ship Date"], errors="coerce")
    for c in ("Sales", "Profit", "Quantity", "Discount", "Shipping_Days"):
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    return df


# ── Load ────────────────────────────────────────────────────────
st.title("👥 Customer & Regional Analysis")
st.caption("Customer insights, regional performance & shipping analytics")
st.markdown("---")

df = load_data()
if df is None:
    st.error("⚠️ Data not found! Run the data pipeline first.")
    st.stop()

ccol = "Customer Name" if "Customer Name" in df.columns else "Customer ID"

# ── Sidebar filters ─────────────────────────────────────────────
st.sidebar.header("🔍 Filters")

regions = (["All"] + sorted(df["Region"].dropna().unique().tolist())) if "Region" in df.columns else ["All"]
sel_reg = st.sidebar.selectbox("Region", regions)

segments = (["All"] + sorted(df["Segment"].dropna().unique().tolist())) if "Segment" in df.columns else ["All"]
sel_seg = st.sidebar.selectbox("Segment", segments)

years = ["All"] + sorted(df["Year"].dropna().unique().tolist())
sel_year = st.sidebar.selectbox("Year", years)

fdf = df.copy()
if sel_reg != "All" and "Region" in fdf.columns:
    fdf = fdf[fdf["Region"] == sel_reg]
if sel_seg != "All" and "Segment" in fdf.columns:
    fdf = fdf[fdf["Segment"] == sel_seg]
if sel_year != "All":
    fdf = fdf[fdf["Year"] == sel_year]

if len(fdf) == 0:
    st.warning("⚠️ No data matches the selected filters.")
    st.stop()

# ── Customer Overview KPIs ──────────────────────────────────────
st.header("📊 Customer Overview")

total_cust = fdf[ccol].nunique()
total_sales = fdf["Sales"].sum()
total_profit = fdf["Profit"].sum()
total_orders = fdf["Order ID"].nunique()
avg_sales_cust = total_sales / total_cust if total_cust > 0 else 0
avg_orders_cust = total_orders / total_cust if total_cust > 0 else 0

c1, c2, c3 = st.columns(3)
c1.metric("Total Customers", f"{total_cust:,}")
c1.metric("Total Orders", f"{total_orders:,}")
c2.metric("Total Sales", f"${total_sales:,.2f}")
c2.metric("Total Profit", f"${total_profit:,.2f}")
c3.metric("Avg Sales/Customer", f"${avg_sales_cust:,.2f}")
c3.metric("Avg Orders/Customer", f"{avg_orders_cust:.1f}")

st.markdown("---")

# ── Customer aggregation ────────────────────────────────────────
cust = (
    fdf.groupby(ccol)
    .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"),
         Orders=("Order ID", "nunique"), Quantity=("Quantity", "sum"))
    .reset_index()
)
cust["Avg_Order_Value"] = np.where(cust["Orders"] > 0, cust["Sales"] / cust["Orders"], 0)

# ── Top 20 Customers by Sales ───────────────────────────────────
st.header("🏆 Top 20 Customers by Sales")

top20 = cust.nlargest(20, "Sales")
fig = px.bar(top20, y=ccol, x="Sales", orientation="h",
             title="Top 20 Customers by Sales Revenue",
             color="Sales", color_continuous_scale="Blues", text_auto="$,.0f")
fig.update_layout(yaxis=dict(categoryorder="total ascending"), height=600,
                  showlegend=False, xaxis_tickprefix="$", xaxis_tickformat=",")
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ── Customer Profitability ──────────────────────────────────────
st.header("💰 Customer Profitability Analysis")

c1, c2 = st.columns(2)

with c1:
    top15p = cust.nlargest(15, "Profit")
    fig = px.bar(top15p, y=ccol, x="Profit", orientation="h",
                 title="Top 15 Customers by Profit",
                 color="Profit", color_continuous_scale="Greens")
    fig.update_layout(yaxis=dict(categoryorder="total ascending"), height=500,
                      showlegend=False, xaxis_tickprefix="$", xaxis_tickformat=",")
    st.plotly_chart(fig, use_container_width=True)

with c2:
    top15o = cust.nlargest(15, "Orders")
    fig = px.bar(top15o, y=ccol, x="Orders", orientation="h",
                 title="Top 15 Customers by Order Count",
                 color="Orders", color_continuous_scale="Oranges")
    fig.update_layout(yaxis=dict(categoryorder="total ascending"), height=500,
                      showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ── Regional Performance ────────────────────────────────────────
if "Region" in fdf.columns:
    st.header("🌍 Regional Performance")

    reg = (
        fdf.groupby("Region")
        .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"),
             Orders=("Order ID", "nunique"), Customers=(ccol, "nunique"))
        .reset_index()
    )
    reg["Profit_Margin"] = np.where(reg["Sales"] > 0, reg["Profit"] / reg["Sales"] * 100, 0)
    reg = reg.sort_values("Sales", ascending=False)

    c1, c2 = st.columns(2)
    with c1:
        fig = px.bar(reg, x="Region", y="Sales", title="Sales by Region",
                     color="Region", color_discrete_sequence=px.colors.qualitative.Vivid, text_auto="$,.0f")
        fig.update_layout(height=400, showlegend=False, yaxis_tickprefix="$", yaxis_tickformat=",")
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        fig = px.pie(reg, values="Profit", names="Region", title="Profit Distribution by Region", hole=0.4)
        fig.update_traces(textinfo="percent+label", hovertemplate="%{label}: $%{value:,.0f}<extra></extra>")
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 📊 Regional Metrics")
    st.dataframe(
        reg.style.format({
            "Sales": "${:,.2f}", "Profit": "${:,.2f}",
            "Orders": "{:,}", "Customers": "{:,}", "Profit_Margin": "{:.2f}%",
        }),
        use_container_width=True,
    )
    st.markdown("---")

# ── Segment Analysis ────────────────────────────────────────────
if "Segment" in fdf.columns:
    st.header("👔 Customer Segment Analysis")

    seg = (
        fdf.groupby("Segment")
        .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"),
             Orders=("Order ID", "nunique"), Customers=(ccol, "nunique"))
        .reset_index()
    )
    seg["Avg_Sale_per_Customer"] = np.where(seg["Customers"] > 0, seg["Sales"] / seg["Customers"], 0)
    seg["Profit_Margin"] = np.where(seg["Sales"] > 0, seg["Profit"] / seg["Sales"] * 100, 0)

    c1, c2 = st.columns(2)
    with c1:
        fig = px.bar(seg, x="Segment", y=["Sales", "Profit"],
                     title="Sales & Profit by Customer Segment", barmode="group",
                     text_auto=".2s")
        fig.update_layout(height=400, yaxis_tickprefix="$", yaxis_tickformat=",")
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        fig = px.pie(seg, values="Customers", names="Segment",
                     title="Customer Distribution by Segment")
        fig.update_traces(textinfo="percent+label")
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 📊 Segment Metrics")
    st.dataframe(
        seg.style.format({
            "Sales": "${:,.2f}", "Profit": "${:,.2f}", "Orders": "{:,}",
            "Customers": "{:,}", "Avg_Sale_per_Customer": "${:,.2f}",
            "Profit_Margin": "{:.2f}%",
        }),
        use_container_width=True,
    )
    st.markdown("---")

# ── Shipping Performance ────────────────────────────────────────
if "Ship Mode" in fdf.columns:
    st.header("🚚 Shipping Performance Analysis")

    ship = (
        fdf.groupby("Ship Mode")
        .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"),
             Count=("Order ID", "count"), Avg_Days=("Shipping_Days", "mean"))
        .reset_index()
    )
    ship = ship.sort_values("Count", ascending=False)

    c1, c2 = st.columns(2)
    with c1:
        fig = px.bar(ship, x="Ship Mode", y="Count", title="Orders by Shipping Mode",
                     color="Count", color_continuous_scale="Blues", text_auto=",")
        fig.update_layout(height=400, showlegend=False, xaxis_tickangle=-20)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        fig = px.bar(ship, x="Ship Mode", y="Avg_Days", title="Avg Shipping Days by Mode",
                     color="Avg_Days", color_continuous_scale="Oranges", text="Avg_Days")
        fig.update_traces(texttemplate="%{text:.1f} days", textposition="outside")
        fig.update_layout(height=400, showlegend=False, xaxis_tickangle=-20)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 📦 Shipping Metrics")
    st.dataframe(
        ship.style.format({
            "Sales": "${:,.2f}", "Profit": "${:,.2f}",
            "Count": "{:,}", "Avg_Days": "{:.2f}",
        }),
        use_container_width=True,
    )
    st.markdown("---")

# ── Customer Performance Table ──────────────────────────────────
st.header("🔍 Customer Performance Table")
st.caption("Search and sort customers to explore detailed performance")

search = st.text_input("🔍 Search for a customer", "")
if search:
    results = cust[cust[ccol].str.contains(search, case=False, na=False)]
else:
    results = cust

sort_col = st.selectbox("Sort by", ["Sales", "Profit", "Orders", "Quantity"], index=0)
results = results.sort_values(sort_col, ascending=False).copy()
results["Profit_Margin"] = np.where(results["Sales"] > 0, results["Profit"] / results["Sales"] * 100, 0)

st.dataframe(
    results.style.format({
        "Sales": "${:,.2f}", "Profit": "${:,.2f}", "Orders": "{:,}",
        "Quantity": "{:,.0f}", "Avg_Order_Value": "${:,.2f}",
        "Profit_Margin": "{:.2f}%",
    }),
    use_container_width=True,
    height=400,
)
st.markdown(f"**Showing {len(results):,} customers**")

csv = results.to_csv(index=False).encode("utf-8")
st.download_button("📥 Download Customer Data as CSV", csv, "customer_analysis_data.csv", "text/csv")

st.markdown("---")

# ── Detailed Transaction Table ──────────────────────────────────
st.header("📋 Transaction Details")

with st.expander("Click to view / download transaction data"):
    pcol = "Product Name" if "Product Name" in fdf.columns else "Product ID"
    disp = ["Order ID", "Order Date", ccol, "Category", pcol,
            "Sales", "Quantity", "Discount", "Profit"]
    extras = ["Region", "Segment", "Ship Mode"]
    for e in extras:
        if e in fdf.columns:
            disp.append(e)
    disp = [c for c in disp if c in fdf.columns]

    st.dataframe(
        fdf[disp].sort_values("Order Date", ascending=False),
        use_container_width=True, height=400,
    )

    csv_tx = fdf[disp].to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download All Transactions CSV", csv_tx,
                       "customer_regional_transactions.csv", "text/csv")

# Footer
st.markdown("---")
st.markdown(
    '<div style="text-align:center;color:#94a3b8;padding:16px;">'
    '👥 Customer & Regional Analysis | E-Commerce Analytics Dashboard</div>',
    unsafe_allow_html=True,
)
