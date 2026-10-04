"""
Executive Overview Dashboard Page
==================================
KPI cards, monthly trends, category/regional/segment performance,
interactive filters, business insights, and detailed data table.
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import sqlite3
import os

# ── Page config ─────────────────────────────────────────────────
st.set_page_config(page_title="Executive Overview", page_icon="📊", layout="wide")

# ── Shared CSS ──────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
div[data-testid="stMetric"] {
    background: linear-gradient(135deg, #667eea11, #764ba211);
    border: 1px solid #e2e8f0; border-radius: 12px;
    padding: 16px 18px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
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


# ── Data loader ─────────────────────────────────────────────────
@st.cache_data
def load_data():
    db = os.path.join("data", "ecommerce.db")
    csv = os.path.join("data", "clean_superstore.csv")
    try:
        if os.path.exists(db):
            conn = sqlite3.connect(db)
            df = pd.read_sql_query("SELECT * FROM sales", conn)
            conn.close()
        elif os.path.exists(csv):
            df = pd.read_csv(csv)
        else:
            return None
    except Exception:
        return None
    df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
    df["Ship Date"] = pd.to_datetime(df["Ship Date"], errors="coerce")
    for c in ("Sales", "Profit", "Quantity", "Discount"):
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    return df


# ── Load ────────────────────────────────────────────────────────
st.title("📊 Executive Overview")
st.caption("Key performance indicators and business trends")
st.markdown("---")

df = load_data()
if df is None:
    st.error("⚠️ Data not found! Run the data pipeline first.")
    st.stop()

# ── Sidebar filters ─────────────────────────────────────────────
st.sidebar.header("🔍 Filters")

years = ["All"] + sorted(df["Year"].dropna().unique().tolist())
selected_year = st.sidebar.selectbox("Year", years)

categories = ["All"] + sorted(df["Category"].dropna().unique().tolist())
selected_cat = st.sidebar.selectbox("Category", categories)

regions = (["All"] + sorted(df["Region"].dropna().unique().tolist())) if "Region" in df.columns else ["All"]
selected_reg = st.sidebar.selectbox("Region", regions)

segments = (["All"] + sorted(df["Segment"].dropna().unique().tolist())) if "Segment" in df.columns else ["All"]
selected_seg = st.sidebar.selectbox("Segment", segments)

ship_modes = (["All"] + sorted(df["Ship Mode"].dropna().unique().tolist())) if "Ship Mode" in df.columns else ["All"]
selected_ship = st.sidebar.selectbox("Ship Mode", ship_modes)

# Apply filters
fdf = df.copy()
if selected_year != "All":
    fdf = fdf[fdf["Year"] == selected_year]
if selected_cat != "All":
    fdf = fdf[fdf["Category"] == selected_cat]
if selected_reg != "All" and "Region" in fdf.columns:
    fdf = fdf[fdf["Region"] == selected_reg]
if selected_seg != "All" and "Segment" in fdf.columns:
    fdf = fdf[fdf["Segment"] == selected_seg]
if selected_ship != "All" and "Ship Mode" in fdf.columns:
    fdf = fdf[fdf["Ship Mode"] == selected_ship]

if len(fdf) == 0:
    st.warning("⚠️ No data matches the selected filters. Please adjust your selection.")
    st.stop()

# ── KPIs ────────────────────────────────────────────────────────
st.header("💼 Key Performance Indicators")

total_sales = fdf["Sales"].sum()
total_profit = fdf["Profit"].sum()
total_orders = fdf["Order ID"].nunique()
cust_col = "Customer Name" if "Customer Name" in fdf.columns else "Customer ID"
total_cust = fdf[cust_col].nunique()
margin = (total_profit / total_sales * 100) if total_sales > 0 else 0
aov = (total_sales / total_orders) if total_orders > 0 else 0

c1, c2, c3 = st.columns(3)
c1.metric("💰 Total Sales", f"${total_sales:,.2f}")
c1.metric("📦 Total Orders", f"{total_orders:,}")
c2.metric("💵 Total Profit", f"${total_profit:,.2f}")
c2.metric("👥 Total Customers", f"{total_cust:,}")
c3.metric("📊 Profit Margin", f"{margin:.2f}%")
c3.metric("💳 Avg Order Value", f"${aov:,.2f}")

st.markdown("---")

# ── Monthly trends ──────────────────────────────────────────────
st.header("📈 Sales & Profit Trends")

monthly = (
    fdf.groupby("Year_Month")
    .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"), Orders=("Order ID", "nunique"))
    .reset_index()
    .sort_values("Year_Month")
)

c1, c2 = st.columns(2)

with c1:
    fig = px.line(monthly, x="Year_Month", y="Sales", title="Monthly Sales Trend", markers=True)
    fig.update_traces(line_color="#2E86AB", line_width=3)
    fig.update_layout(xaxis_title="Month", yaxis_title="Sales ($)", hovermode="x unified",
                      height=400, yaxis_tickprefix="$", yaxis_tickformat=",")
    st.plotly_chart(fig, use_container_width=True)

with c2:
    fig = px.line(monthly, x="Year_Month", y="Profit", title="Monthly Profit Trend", markers=True)
    fig.update_traces(line_color="#06A77D", line_width=3)
    fig.update_layout(xaxis_title="Month", yaxis_title="Profit ($)", hovermode="x unified",
                      height=400, yaxis_tickprefix="$", yaxis_tickformat=",")
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ── Category performance ────────────────────────────────────────
st.header("📊 Performance by Category")

cat = (
    fdf.groupby("Category")
    .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"), Orders=("Order ID", "nunique"))
    .reset_index()
    .sort_values("Sales", ascending=False)
)

c1, c2 = st.columns(2)
with c1:
    fig = px.bar(cat, x="Category", y="Sales", title="Sales by Category",
                 color="Category", color_discrete_sequence=px.colors.qualitative.Set2, text_auto="$,.0f")
    fig.update_layout(showlegend=False, height=400, yaxis_tickprefix="$", yaxis_tickformat=",")
    st.plotly_chart(fig, use_container_width=True)

with c2:
    fig = px.bar(cat, x="Category", y="Profit", title="Profit by Category",
                 color="Category", color_discrete_sequence=px.colors.qualitative.Pastel, text_auto="$,.0f")
    fig.update_layout(showlegend=False, height=400, yaxis_tickprefix="$", yaxis_tickformat=",")
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ── Regional performance ────────────────────────────────────────
if "Region" in fdf.columns:
    st.header("🌍 Performance by Region")

    reg = (
        fdf.groupby("Region")
        .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"), Orders=("Order ID", "nunique"))
        .reset_index()
        .sort_values("Sales", ascending=False)
    )

    c1, c2 = st.columns(2)
    with c1:
        fig = px.bar(reg, x="Region", y="Sales", title="Sales by Region",
                     color="Region", color_discrete_sequence=px.colors.qualitative.Vivid, text_auto="$,.0f")
        fig.update_layout(showlegend=False, height=400, yaxis_tickprefix="$", yaxis_tickformat=",")
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        fig = px.pie(reg, values="Profit", names="Region", title="Profit Distribution by Region", hole=0.35)
        fig.update_layout(height=400)
        fig.update_traces(textinfo="percent+label", hovertemplate="%{label}: $%{value:,.0f}<extra></extra>")
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

# ── Segment performance ─────────────────────────────────────────
if "Segment" in fdf.columns:
    st.header("👔 Performance by Customer Segment")

    seg = (
        fdf.groupby("Segment")
        .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"), Orders=("Order ID", "nunique"))
        .reset_index()
    )

    c1, c2 = st.columns(2)
    with c1:
        fig = px.bar(seg, x="Segment", y=["Sales", "Profit"], title="Sales & Profit by Segment",
                     barmode="group")
        fig.update_layout(height=400, yaxis_tickprefix="$", yaxis_tickformat=",")
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.markdown("### Segment Metrics")
        for _, row in seg.iterrows():
            with st.expander(f"📌 {row['Segment']}"):
                ca, cb = st.columns(2)
                ca.metric("Sales", f"${row['Sales']:,.2f}")
                ca.metric("Orders", f"{row['Orders']:,}")
                m = (row["Profit"] / row["Sales"] * 100) if row["Sales"] > 0 else 0
                cb.metric("Profit", f"${row['Profit']:,.2f}")
                cb.metric("Margin", f"{m:.2f}%")

    st.markdown("---")

# ── Business Insights (auto-calculated) ─────────────────────────
st.header("💡 Business Insights")
st.caption("Automatically calculated from the filtered dataset")

# Best/worst category
if len(cat) > 0:
    best_cat = cat.iloc[0]
    worst_cat = cat.iloc[-1] if len(cat) > 1 else cat.iloc[0]
    cat_margin = cat.copy()
    cat_margin["Margin"] = np.where(cat_margin["Sales"] > 0, cat_margin["Profit"] / cat_margin["Sales"] * 100, 0)
    best_margin_cat = cat_margin.loc[cat_margin["Margin"].idxmax()]
    worst_margin_cat = cat_margin.loc[cat_margin["Margin"].idxmin()]

    il, ir = st.columns(2)
    with il:
        st.markdown(f'<div class="insight-box-good"><strong>Highest Revenue Category:</strong> '
                     f'{best_cat["Category"]} — ${best_cat["Sales"]:,.0f}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="insight-box-good"><strong>Best Margin Category:</strong> '
                     f'{best_margin_cat["Category"]} — {best_margin_cat["Margin"]:.1f}%</div>', unsafe_allow_html=True)
    with ir:
        st.markdown(f'<div class="insight-box-bad"><strong>Lowest Revenue Category:</strong> '
                     f'{worst_cat["Category"]} — ${worst_cat["Sales"]:,.0f}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="insight-box-warn"><strong>Lowest Margin Category:</strong> '
                     f'{worst_margin_cat["Category"]} — {worst_margin_cat["Margin"]:.1f}%</div>', unsafe_allow_html=True)

if "Region" in fdf.columns and len(reg) > 0:
    best_reg = reg.iloc[0]
    worst_reg = reg.iloc[-1]
    il2, ir2 = st.columns(2)
    with il2:
        st.markdown(f'<div class="insight-box"><strong>Best Region:</strong> '
                     f'{best_reg["Region"]} — ${best_reg["Sales"]:,.0f}</div>', unsafe_allow_html=True)
    with ir2:
        st.markdown(f'<div class="insight-box-bad"><strong>Weakest Region:</strong> '
                     f'{worst_reg["Region"]} — ${worst_reg["Sales"]:,.0f}</div>', unsafe_allow_html=True)

st.markdown("---")

# ── Data Table ──────────────────────────────────────────────────
st.header("📋 Detailed Data Table")

with st.expander("Click to view / download transaction data", expanded=False):
    # Columns requested in spec
    display_cols = ["Order ID", "Order Date", cust_col, "Category",
                    "Product Name" if "Product Name" in fdf.columns else "Product ID",
                    "Sales", "Quantity", "Discount", "Profit"]
    display_cols = [c for c in display_cols if c in fdf.columns]

    st.dataframe(
        fdf[display_cols].sort_values("Order Date", ascending=False),
        use_container_width=True,
        height=400,
    )

    csv_data = fdf[display_cols].to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Filtered Data as CSV",
        data=csv_data,
        file_name="executive_overview_data.csv",
        mime="text/csv",
    )

# ── Footer ──────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    '<div style="text-align:center;color:#94a3b8;padding:16px;">'
    '📊 Executive Overview | E-Commerce Analytics Dashboard</div>',
    unsafe_allow_html=True,
)
