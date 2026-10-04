"""Exploratory Data Analysis for E-commerce Sales Data.

Generates key business metrics, trend charts, and saves
PNG visualizations into the outputs/ directory.
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")  # non-interactive backend for headless environments
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys
import warnings

warnings.filterwarnings("ignore")

# Visual style
sns.set_style("whitegrid")
plt.rcParams["figure.figsize"] = (12, 6)
plt.rcParams["font.size"] = 10


def load_clean_data():
    """Load the cleaned CSV dataset."""
    file_path = os.path.join("data", "clean_superstore.csv")

    if not os.path.exists(file_path):
        print(f"[ERROR] {file_path} not found!")
        print("Please run 'python src/clean_data.py' first.")
        return None

    df = pd.read_csv(file_path)
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    df["Ship Date"] = pd.to_datetime(df["Ship Date"])
    return df


def create_output_dir():
    """Create outputs directory if missing."""
    if not os.path.exists("outputs"):
        os.makedirs("outputs")
        print("[OK] Created 'outputs' directory")


# ── Metric calculations ─────────────────────────────────────────
def calculate_key_metrics(df):
    """Calculate and print key business metrics."""
    print("\n" + "=" * 60)
    print("KEY BUSINESS METRICS")
    print("=" * 60)

    customer_col = "Customer Name" if "Customer Name" in df.columns else "Customer ID"
    product_col = "Product Name" if "Product Name" in df.columns else "Product ID"

    m = {
        "total_sales": df["Sales"].sum(),
        "total_profit": df["Profit"].sum(),
        "total_quantity": df["Quantity"].sum(),
        "total_orders": df["Order ID"].nunique(),
        "total_customers": df[customer_col].nunique(),
        "total_products": df[product_col].nunique(),
    }
    m["profit_margin"] = (m["total_profit"] / m["total_sales"]) * 100
    m["avg_order_value"] = m["total_sales"] / m["total_orders"]

    print(f"\nTotal Sales:          ${m['total_sales']:,.2f}")
    print(f"Total Profit:         ${m['total_profit']:,.2f}")
    print(f"Total Orders:         {m['total_orders']:,}")
    print(f"Total Customers:      {m['total_customers']:,}")
    print(f"Total Products:       {m['total_products']:,}")
    print(f"Total Quantity Sold:  {int(m['total_quantity']):,}")
    print(f"Profit Margin:        {m['profit_margin']:.2f}%")
    print(f"Avg Order Value:      ${m['avg_order_value']:,.2f}")
    return m


# ── Time trend analysis ─────────────────────────────────────────
def analyze_time_trends(df):
    """Monthly sales and profit trend charts."""
    print("\n" + "=" * 60)
    print("TIME TREND ANALYSIS")
    print("=" * 60)

    monthly = (
        df.groupby("Year_Month")
        .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"), Orders=("Order ID", "nunique"))
        .reset_index()
        .sort_values("Year_Month")
    )
    print(f"\n[OK] Analyzed {len(monthly)} months of data")

    fig, axes = plt.subplots(2, 1, figsize=(14, 10))

    axes[0].plot(monthly["Year_Month"], monthly["Sales"], marker="o", lw=2, color="#2E86AB", ms=5)
    axes[0].set_title("Monthly Sales Trend", fontsize=14, fontweight="bold", pad=20)
    axes[0].set_ylabel("Sales ($)", fontsize=11)
    axes[0].grid(True, alpha=0.3)
    axes[0].tick_params(axis="x", rotation=45)
    # show only every N-th label to avoid clutter
    n = max(1, len(monthly) // 12)
    for idx, label in enumerate(axes[0].xaxis.get_ticklabels()):
        if idx % n != 0:
            label.set_visible(False)

    axes[1].plot(monthly["Year_Month"], monthly["Profit"], marker="o", lw=2, color="#06A77D", ms=5)
    axes[1].set_title("Monthly Profit Trend", fontsize=14, fontweight="bold", pad=20)
    axes[1].set_ylabel("Profit ($)", fontsize=11)
    axes[1].grid(True, alpha=0.3)
    axes[1].tick_params(axis="x", rotation=45)
    for idx, label in enumerate(axes[1].xaxis.get_ticklabels()):
        if idx % n != 0:
            label.set_visible(False)

    plt.tight_layout()
    plt.savefig("outputs/monthly_trends.png", dpi=300, bbox_inches="tight")
    plt.close()
    print("[OK] Saved: outputs/monthly_trends.png")
    return monthly


# ── Category analysis ────────────────────────────────────────────
def analyze_categories(df):
    """Category and sub-category performance charts."""
    print("\n" + "=" * 60)
    print("CATEGORY ANALYSIS")
    print("=" * 60)

    cat = (
        df.groupby("Category")
        .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"),
             Quantity=("Quantity", "sum"), Orders=("Order ID", "nunique"))
        .reset_index()
        .sort_values("Sales", ascending=False)
    )
    print("\nCategory Performance:")
    print(cat.to_string(index=False))

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    colors_s = ["#2E86AB", "#A23B72", "#F18F01"]
    colors_p = ["#06A77D", "#D81159", "#FFBC42"]

    axes[0].bar(cat["Category"], cat["Sales"], color=colors_s[: len(cat)])
    axes[0].set_title("Sales by Category", fontsize=14, fontweight="bold", pad=20)
    axes[0].set_ylabel("Sales ($)")
    axes[0].tick_params(axis="x", rotation=0)

    axes[1].bar(cat["Category"], cat["Profit"], color=colors_p[: len(cat)])
    axes[1].set_title("Profit by Category", fontsize=14, fontweight="bold", pad=20)
    axes[1].set_ylabel("Profit ($)")
    axes[1].tick_params(axis="x", rotation=0)

    plt.tight_layout()
    plt.savefig("outputs/category_performance.png", dpi=300, bbox_inches="tight")
    plt.close()
    print("[OK] Saved: outputs/category_performance.png")

    # Sub-category
    if "Sub-Category" in df.columns:
        subcat = (
            df.groupby("Sub-Category")
            .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
            .reset_index()
            .sort_values("Sales", ascending=False)
        )
        print("\nTop Sub-Categories by Sales:")
        print(subcat.to_string(index=False))

        fig, ax = plt.subplots(figsize=(12, 8))
        ax.barh(subcat["Sub-Category"], subcat["Sales"], color="#2E86AB")
        ax.invert_yaxis()
        ax.set_xlabel("Sales ($)")
        ax.set_title("Sub-Categories by Sales", fontsize=14, fontweight="bold", pad=20)
        plt.tight_layout()
        plt.savefig("outputs/subcategory_performance.png", dpi=300, bbox_inches="tight")
        plt.close()
        print("[OK] Saved: outputs/subcategory_performance.png")

    return cat


# ── Regional analysis ────────────────────────────────────────────
def analyze_regions(df):
    """Regional sales and profit charts."""
    print("\n" + "=" * 60)
    print("REGIONAL ANALYSIS")
    print("=" * 60)

    if "Region" not in df.columns:
        print("Region column not found, skipping.")
        return None

    reg = (
        df.groupby("Region")
        .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"), Orders=("Order ID", "nunique"))
        .reset_index()
        .sort_values("Sales", ascending=False)
    )
    print("\nRegional Performance:")
    print(reg.to_string(index=False))

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    axes[0].bar(reg["Region"], reg["Sales"], color="#2E86AB")
    axes[0].set_title("Sales by Region", fontsize=14, fontweight="bold", pad=20)
    axes[0].set_ylabel("Sales ($)")

    axes[1].bar(reg["Region"], reg["Profit"], color="#06A77D")
    axes[1].set_title("Profit by Region", fontsize=14, fontweight="bold", pad=20)
    axes[1].set_ylabel("Profit ($)")

    plt.tight_layout()
    plt.savefig("outputs/regional_performance.png", dpi=300, bbox_inches="tight")
    plt.close()
    print("[OK] Saved: outputs/regional_performance.png")
    return reg


# ── Product analysis ─────────────────────────────────────────────
def analyze_products(df):
    """Top/bottom product charts."""
    print("\n" + "=" * 60)
    print("PRODUCT ANALYSIS")
    print("=" * 60)

    pcol = "Product Name" if "Product Name" in df.columns else "Product ID"
    prod = (
        df.groupby(pcol)
        .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"), Quantity=("Quantity", "sum"))
        .reset_index()
    )

    top10 = prod.nlargest(10, "Sales")
    bot10 = prod.nsmallest(10, "Profit")

    print("\nTop 10 Products by Sales:")
    for _, r in top10.iterrows():
        print(f"  {r[pcol][:50]}: ${r['Sales']:,.2f}")

    print("\nBottom 10 Products by Profit (Loss-making):")
    for _, r in bot10.iterrows():
        print(f"  {r[pcol][:50]}: ${r['Profit']:,.2f}")

    # Top 10 chart
    fig, ax = plt.subplots(figsize=(12, 8))
    names = [n[:40] + "..." if len(n) > 40 else n for n in top10[pcol]]
    ax.barh(range(len(names)), top10["Sales"].values, color="#2E86AB")
    ax.set_yticks(range(len(names)))
    ax.set_yticklabels(names, fontsize=9)
    ax.invert_yaxis()
    ax.set_xlabel("Sales ($)")
    ax.set_title("Top 10 Products by Sales", fontsize=14, fontweight="bold", pad=20)
    plt.tight_layout()
    plt.savefig("outputs/top_products.png", dpi=300, bbox_inches="tight")
    plt.close()
    print("[OK] Saved: outputs/top_products.png")

    # Bottom 10 chart
    fig, ax = plt.subplots(figsize=(12, 8))
    names_b = [n[:40] + "..." if len(n) > 40 else n for n in bot10[pcol]]
    ax.barh(range(len(names_b)), bot10["Profit"].values, color="#D81159")
    ax.set_yticks(range(len(names_b)))
    ax.set_yticklabels(names_b, fontsize=9)
    ax.invert_yaxis()
    ax.set_xlabel("Profit ($)")
    ax.set_title("Bottom 10 Products by Profit", fontsize=14, fontweight="bold", pad=20)
    plt.tight_layout()
    plt.savefig("outputs/bottom_products.png", dpi=300, bbox_inches="tight")
    plt.close()
    print("[OK] Saved: outputs/bottom_products.png")

    return top10, bot10


# ── Customer analysis ────────────────────────────────────────────
def analyze_customers(df):
    """Top customers by sales."""
    print("\n" + "=" * 60)
    print("CUSTOMER ANALYSIS")
    print("=" * 60)

    ccol = "Customer Name" if "Customer Name" in df.columns else "Customer ID"
    cust = (
        df.groupby(ccol)
        .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"), Orders=("Order ID", "nunique"))
        .reset_index()
    )
    top10 = cust.nlargest(10, "Sales")

    print("\nTop 10 Customers by Sales:")
    for _, r in top10.iterrows():
        print(f"  {r[ccol]}: ${r['Sales']:,.2f} ({r['Orders']} orders)")

    fig, ax = plt.subplots(figsize=(12, 8))
    ax.barh(range(len(top10)), top10["Sales"].values, color="#2E86AB")
    ax.set_yticks(range(len(top10)))
    ax.set_yticklabels(top10[ccol].values, fontsize=9)
    ax.invert_yaxis()
    ax.set_xlabel("Sales ($)")
    ax.set_title("Top 10 Customers by Sales", fontsize=14, fontweight="bold", pad=20)
    plt.tight_layout()
    plt.savefig("outputs/top_customers.png", dpi=300, bbox_inches="tight")
    plt.close()
    print("[OK] Saved: outputs/top_customers.png")
    return top10


# ── Segment analysis ─────────────────────────────────────────────
def analyze_segments(df):
    """Segment performance chart."""
    print("\n" + "=" * 60)
    print("SEGMENT ANALYSIS")
    print("=" * 60)

    if "Segment" not in df.columns:
        print("Segment column not found, skipping.")
        return None

    seg = (
        df.groupby("Segment")
        .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"), Orders=("Order ID", "nunique"))
        .reset_index()
        .sort_values("Sales", ascending=False)
    )
    print("\nSegment Performance:")
    print(seg.to_string(index=False))

    fig, ax = plt.subplots(figsize=(10, 6))
    x = np.arange(len(seg))
    w = 0.35
    ax.bar(x - w / 2, seg["Sales"], w, label="Sales", color="#2E86AB")
    ax.bar(x + w / 2, seg["Profit"], w, label="Profit", color="#06A77D")
    ax.set_xticks(x)
    ax.set_xticklabels(seg["Segment"])
    ax.set_title("Sales & Profit by Segment", fontsize=14, fontweight="bold", pad=20)
    ax.set_ylabel("Amount ($)")
    ax.legend()
    plt.tight_layout()
    plt.savefig("outputs/segment_performance.png", dpi=300, bbox_inches="tight")
    plt.close()
    print("[OK] Saved: outputs/segment_performance.png")
    return seg


# ── Discount impact analysis ────────────────────────────────────
def analyze_discount_impact(df):
    """Discount vs. profit analysis."""
    print("\n" + "=" * 60)
    print("DISCOUNT IMPACT ANALYSIS")
    print("=" * 60)

    df = df.copy()
    df["Discount_Range"] = pd.cut(
        df["Discount"],
        bins=[-0.01, 0, 0.1, 0.2, 0.3, 1.0],
        labels=["No Discount", "1-10%", "11-20%", "21-30%", "30%+"],
    )

    disc = (
        df.groupby("Discount_Range", observed=False)
        .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"), Count=("Order ID", "count"))
        .reset_index()
    )
    disc["Profit_Margin"] = np.where(disc["Sales"] > 0, disc["Profit"] / disc["Sales"] * 100, 0)

    print("\nDiscount Impact on Profit:")
    print(disc.to_string(index=False))

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    axes[0].bar(disc["Discount_Range"].astype(str), disc["Sales"], color="#2E86AB")
    axes[0].set_title("Sales by Discount Range", fontsize=14, fontweight="bold", pad=20)
    axes[0].set_ylabel("Sales ($)")
    axes[0].tick_params(axis="x", rotation=45)

    axes[1].bar(disc["Discount_Range"].astype(str), disc["Profit_Margin"], color="#06A77D")
    axes[1].set_title("Profit Margin by Discount Range", fontsize=14, fontweight="bold", pad=20)
    axes[1].set_ylabel("Profit Margin (%)")
    axes[1].axhline(y=0, color="red", ls="--", alpha=0.5)
    axes[1].tick_params(axis="x", rotation=45)

    plt.tight_layout()
    plt.savefig("outputs/discount_impact.png", dpi=300, bbox_inches="tight")
    plt.close()
    print("[OK] Saved: outputs/discount_impact.png")
    return disc


# ── Shipping analysis ────────────────────────────────────────────
def analyze_shipping(df):
    """Shipping mode performance chart."""
    print("\n" + "=" * 60)
    print("SHIPPING ANALYSIS")
    print("=" * 60)

    if "Ship Mode" not in df.columns:
        print("Ship Mode column not found, skipping.")
        return None

    ship = (
        df.groupby("Ship Mode")
        .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"),
             Avg_Days=("Shipping_Days", "mean"), Count=("Order ID", "count"))
        .reset_index()
        .sort_values("Count", ascending=False)
    )
    print("\nShipping Mode Performance:")
    print(ship.to_string(index=False))

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(ship["Ship Mode"], ship["Count"], color="#2E86AB")
    ax.set_title("Orders by Shipping Mode", fontsize=14, fontweight="bold", pad=20)
    ax.set_ylabel("Number of Orders")
    plt.tight_layout()
    plt.savefig("outputs/shipping_performance.png", dpi=300, bbox_inches="tight")
    plt.close()
    print("[OK] Saved: outputs/shipping_performance.png")
    return ship


# ── Loss-making products analysis ─────────────────────────────────
def analyze_loss_products(df):
    """Identify and chart loss-making products."""
    print("\n" + "=" * 60)
    print("LOSS-MAKING PRODUCTS ANALYSIS")
    print("=" * 60)

    pcol = "Product Name" if "Product Name" in df.columns else "Product ID"
    prod = (
        df.groupby(pcol)
        .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"), Quantity=("Quantity", "sum"))
        .reset_index()
    )
    loss = prod[prod["Profit"] < 0].sort_values("Profit")

    print(f"\nTotal loss-making products: {len(loss)}")
    print(f"Total loss amount: ${loss['Profit'].sum():,.2f}")

    if len(loss) > 0:
        fig, ax = plt.subplots(figsize=(12, 8))
        top_loss = loss.head(15)
        names = [n[:40] + "..." if len(n) > 40 else n for n in top_loss[pcol]]
        ax.barh(range(len(names)), top_loss["Profit"].values, color="#D81159")
        ax.set_yticks(range(len(names)))
        ax.set_yticklabels(names, fontsize=9)
        ax.invert_yaxis()
        ax.set_xlabel("Profit ($)")
        ax.set_title("Top 15 Loss-Making Products", fontsize=14, fontweight="bold", pad=20)
        plt.tight_layout()
        plt.savefig("outputs/loss_making_products.png", dpi=300, bbox_inches="tight")
        plt.close()
        print("[OK] Saved: outputs/loss_making_products.png")

    return loss


# ── Entry point ──────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print("E-COMMERCE SALES ANALYSIS - EXPLORATORY DATA ANALYSIS")
    print("=" * 60)

    df = load_clean_data()
    if df is None:
        sys.exit(1)

    print(f"\n[OK] Loaded {len(df):,} records")
    create_output_dir()

    try:
        metrics = calculate_key_metrics(df)
        monthly = analyze_time_trends(df)
        cat = analyze_categories(df)
        reg = analyze_regions(df)
        top_prod, bot_prod = analyze_products(df)
        top_cust = analyze_customers(df)
        seg = analyze_segments(df)
        disc = analyze_discount_impact(df)
        ship = analyze_shipping(df)
        loss = analyze_loss_products(df)

        print("\n" + "=" * 60)
        print("[OK] EDA COMPLETE - ALL CHARTS GENERATED")
        print("=" * 60)
        print("\nGenerated files in 'outputs/':")
        for f in sorted(os.listdir("outputs")):
            print(f"  - {f}")

        print("\n" + "=" * 60)
        print("NEXT STEP: Run 'python src/create_database.py'")
        print("=" * 60)

    except Exception as e:
        print(f"\n[ERROR] During EDA: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
