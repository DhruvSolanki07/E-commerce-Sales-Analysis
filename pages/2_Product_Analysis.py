"""
Product Analysis Dashboard Page
================================
Top/bottom products, sub-category performance, discount impact,
quantity analysis, searchable product table with CSV export.
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import sqlite3
import os

# ── Page config ─────────────────────────────────────────────────
st.set_page_config(page_title="Product Analysis", page_icon="🏆", layout="wide")

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
    for c in ("Sales", "Profit", "Quantity", "Discount"):
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    return df


# ── Load & guard ────────────────────────────────────────────────
st.title("🏆 Product Analysis")
st.caption("Product performance, profitability insights & discount impact")
st.markdown("---")

df = load_data()
if df is None:
    st.error("⚠️ Data not found! Run the data pipeline first.")
    st.stop()

pcol = "Product Name" if "Product Name" in df.columns else "Product ID"

# ── Sidebar filters ─────────────────────────────────────────────
st.sidebar.header("🔍 Filters")

cats = ["All"] + sorted(df["Category"].dropna().unique().tolist())
sel_cat = st.sidebar.selectbox("Category", cats)

# Dynamic sub-category list
if "Sub-Category" in df.columns:
    src = df[df["Category"] == sel_cat] if sel_cat != "All" else df
    subs = ["All"] + sorted(src["Sub-Category"].dropna().unique().tolist())
    sel_sub = st.sidebar.selectbox("Sub-Category", subs)
else:
    sel_sub = "All"

years = ["All"] + sorted(df["Year"].dropna().unique().tolist())
sel_year = st.sidebar.selectbox("Year", years)

# Apply
fdf = df.copy()
if sel_cat != "All":
    fdf = fdf[fdf["Category"] == sel_cat]
if sel_sub != "All" and "Sub-Category" in fdf.columns:
    fdf = fdf[fdf["Sub-Category"] == sel_sub]
if sel_year != "All":
    fdf = fdf[fdf["Year"] == sel_year]

if len(fdf) == 0:
    st.warning("⚠️ No data for selected filters.")
    st.stop()

# ── Summary KPIs ────────────────────────────────────────────────
st.header("📊 Product Performance Summary")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Products", f"{fdf[pcol].nunique():,}")
c2.metric("Units Sold", f"{int(fdf['Quantity'].sum()):,}")
c3.metric("Total Sales", f"${fdf['Sales'].sum():,.2f}")
c4.metric("Total Profit", f"${fdf['Profit'].sum():,.2f}")

st.markdown("---")

# ── Product aggregation ─────────────────────────────────────────
prod = (
    fdf.groupby(pcol)
    .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"),
         Quantity=("Quantity", "sum"), Orders=("Order ID", "count"))
    .reset_index()
)

# ── Top 10 by Sales ─────────────────────────────────────────────
st.header("🏅 Top 10 Products by Sales")

top10s = prod.nlargest(10, "Sales").copy()
top10s["Display"] = top10s[pcol].str[:55].where(top10s[pcol].str.len() <= 55, top10s[pcol].str[:52] + "...")

fig = px.bar(top10s, y="Display", x="Sales", orientation="h",
             title="Top 10 Products by Sales Revenue",
             color="Sales", color_continuous_scale="Blues", text_auto="$,.0f")
fig.update_layout(yaxis=dict(categoryorder="total ascending"), height=500,
                  showlegend=False, xaxis_tickprefix="$", xaxis_tickformat=",")
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ── Top 10 by Profit ────────────────────────────────────────────
st.header("💰 Top 10 Products by Profit")

top10p = prod.nlargest(10, "Profit").copy()
top10p["Display"] = top10p[pcol].str[:55].where(top10p[pcol].str.len() <= 55, top10p[pcol].str[:52] + "...")

fig = px.bar(top10p, y="Display", x="Profit", orientation="h",
             title="Top 10 Products by Profit",
             color="Profit", color_continuous_scale="Greens", text_auto="$,.0f")
fig.update_layout(yaxis=dict(categoryorder="total ascending"), height=500,
                  showlegend=False, xaxis_tickprefix="$", xaxis_tickformat=",")
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ── Bottom 10 by Profit ─────────────────────────────────────────
st.header("⚠️ Bottom 10 Products by Profit (Loss-Makers)")

bot10 = prod.nsmallest(10, "Profit").copy()
bot10["Display"] = bot10[pcol].str[:55].where(bot10[pcol].str.len() <= 55, bot10[pcol].str[:52] + "...")

fig = px.bar(bot10, y="Display", x="Profit", orientation="h",
             title="Bottom 10 Products — Negative Profitability",
             color="Profit", color_continuous_scale="Reds_r", text_auto="$,.0f")
fig.update_layout(yaxis=dict(categoryorder="total descending"), height=500,
                  showlegend=False, xaxis_tickprefix="$", xaxis_tickformat=",")
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ── Sub-Category Performance ────────────────────────────────────
if "Sub-Category" in fdf.columns:
    st.header("📦 Sub-Category Performance")

    subcat = (
        fdf.groupby("Sub-Category")
        .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"), Quantity=("Quantity", "sum"))
        .reset_index()
    )
    subcat["Profit_Margin"] = np.where(subcat["Sales"] > 0, subcat["Profit"] / subcat["Sales"] * 100, 0)
    subcat = subcat.sort_values("Sales", ascending=False)

    c1, c2 = st.columns(2)
    with c1:
        fig = px.bar(subcat, x="Sub-Category", y="Sales", title="Sales by Sub-Category",
                     color="Sales", color_continuous_scale="Viridis", text_auto="$,.0f")
        fig.update_layout(xaxis_tickangle=-45, height=420, showlegend=False,
                          yaxis_tickprefix="$", yaxis_tickformat=",")
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        fig = px.bar(subcat, x="Sub-Category", y="Profit", title="Profit by Sub-Category",
                     color="Profit", color_continuous_scale="RdYlGn", text_auto="$,.0f")
        fig.update_layout(xaxis_tickangle=-45, height=420, showlegend=False,
                          yaxis_tickprefix="$", yaxis_tickformat=",")
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

# ── Discount Impact ─────────────────────────────────────────────
st.header("💸 Discount Impact on Profitability")

fdf_disc = fdf.copy()
fdf_disc["Discount_Range"] = pd.cut(
    fdf_disc["Discount"],
    bins=[-0.01, 0, 0.1, 0.2, 0.3, 1.0],
    labels=["No Discount", "1-10%", "11-20%", "21-30%", "30%+"],
)

disc = (
    fdf_disc.groupby("Discount_Range", observed=False)
    .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"), Count=("Order ID", "count"))
    .reset_index()
)
disc["Profit_Margin"] = np.where(disc["Sales"] > 0, disc["Profit"] / disc["Sales"] * 100, 0)

c1, c2 = st.columns(2)
with c1:
    fig = px.bar(disc, x="Discount_Range", y="Sales", title="Sales by Discount Range",
                 color="Sales", color_continuous_scale="Blues", text_auto="$,.0f")
    fig.update_layout(height=400, showlegend=False, yaxis_tickprefix="$", yaxis_tickformat=",")
    st.plotly_chart(fig, use_container_width=True)

with c2:
    fig = px.line(disc, x="Discount_Range", y="Profit_Margin",
                  title="Profit Margin by Discount Range", markers=True, text="Profit_Margin")
    fig.update_traces(texttemplate="%{text:.1f}%", textposition="top center",
                      line_color="#06A77D", line_width=3)
    fig.add_hline(y=0, line_dash="dash", line_color="red", annotation_text="Break-even")
    fig.update_layout(height=400, yaxis_title="Profit Margin (%)")
    st.plotly_chart(fig, use_container_width=True)

with st.expander("📊 View Discount Analysis Table"):
    st.dataframe(
        disc.style.format({
            "Sales": "${:,.2f}", "Profit": "${:,.2f}",
            "Count": "{:,}", "Profit_Margin": "{:.2f}%",
        }),
        use_container_width=True,
    )

st.markdown("---")

# ── Quantity Analysis ────────────────────────────────────────────
st.header("📊 Quantity Analysis")

c1, c2 = st.columns(2)
with c1:
    topq = prod.nlargest(10, "Quantity").copy()
    topq["Display"] = topq[pcol].str[:40].where(topq[pcol].str.len() <= 40, topq[pcol].str[:37] + "...")
    fig = px.bar(topq, y="Display", x="Quantity", orientation="h",
                 title="Top 10 Products by Quantity Sold",
                 color="Quantity", color_continuous_scale="Oranges")
    fig.update_layout(yaxis=dict(categoryorder="total ascending"), height=400, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

with c2:
    if "Category" in fdf.columns:
        catq = fdf.groupby("Category")["Quantity"].sum().reset_index().sort_values("Quantity", ascending=False)
        fig = px.pie(catq, values="Quantity", names="Category", title="Quantity Distribution by Category")
        fig.update_traces(textinfo="percent+label")
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ── Searchable Product Table ─────────────────────────────────────
st.header("🔍 Product Performance Table")
st.caption("Search and sort products to explore detailed performance metrics")

search = st.text_input("🔍 Search for a product", "")
if search:
    results = prod[prod[pcol].str.contains(search, case=False, na=False)]
else:
    results = prod

sort_col = st.selectbox("Sort by", ["Sales", "Profit", "Quantity", "Orders"], index=0)
results = results.sort_values(sort_col, ascending=False).copy()
results["Profit_Margin"] = np.where(results["Sales"] > 0, results["Profit"] / results["Sales"] * 100, 0)

st.dataframe(
    results.style.format({
        "Sales": "${:,.2f}", "Profit": "${:,.2f}",
        "Quantity": "{:,.0f}", "Orders": "{:,}", "Profit_Margin": "{:.2f}%",
    }),
    use_container_width=True,
    height=400,
)
st.markdown(f"**Showing {len(results):,} products**")

csv = results.to_csv(index=False).encode("utf-8")
st.download_button("📥 Download Product Data as CSV", csv, "product_analysis_data.csv", "text/csv")

st.markdown("---")

# ── Detailed Transaction Table ───────────────────────────────────
st.header("📋 Detailed Data Table")

with st.expander("Click to view / download transaction data"):
    cust_col = "Customer Name" if "Customer Name" in fdf.columns else "Customer ID"
    disp = ["Order ID", "Order Date", cust_col, "Category", pcol,
            "Sales", "Quantity", "Discount", "Profit"]
    disp = [c for c in disp if c in fdf.columns]

    st.dataframe(
        fdf[disp].sort_values("Order Date", ascending=False),
        use_container_width=True, height=400,
    )

    csv2 = fdf[disp].to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download Filtered Transactions CSV", csv2,
                       "product_transactions.csv", "text/csv")

# Footer
st.markdown("---")
st.markdown(
    '<div style="text-align:center;color:#94a3b8;padding:16px;">'
    '🏆 Product Analysis | E-Commerce Analytics Dashboard</div>',
    unsafe_allow_html=True,
)
