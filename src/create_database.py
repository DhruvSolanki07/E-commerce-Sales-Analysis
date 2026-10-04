"""Create SQLite database from cleaned data."""
import pandas as pd
import sqlite3
import os
import sys


def create_database():
    """
    Create SQLite database and load cleaned data into 'sales' table.
    Also creates indexes for common query patterns.
    """
    input_file = os.path.join("data", "clean_superstore.csv")
    db_path = os.path.join("data", "ecommerce.db")

    if not os.path.exists(input_file):
        print(f"[ERROR] {input_file} not found!")
        print("Please run 'python src/clean_data.py' first.")
        return False

    print("Loading cleaned data...")
    df = pd.read_csv(input_file)
    print(f"[OK] Loaded {len(df):,} records")

    # Convert date columns
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    df["Ship Date"] = pd.to_datetime(df["Ship Date"])

    # Create / replace database
    print(f"\nCreating database: {db_path}")
    conn = sqlite3.connect(db_path)

    print("Writing data to 'sales' table...")
    df.to_sql("sales", conn, if_exists="replace", index=False)

    # Verify
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM sales")
    count = cursor.fetchone()[0]
    print(f"[OK] Inserted {count:,} records into 'sales' table")

    # Schema
    cursor.execute("PRAGMA table_info(sales)")
    columns = cursor.fetchall()

    print("\n" + "=" * 60)
    print("DATABASE SCHEMA")
    print("=" * 60)
    print("\nTable: sales\n")
    print(f"  {'Column':<25s} {'Type'}")
    print(f"  {'-'*25} {'-'*15}")
    for col in columns:
        print(f"  {col[1]:<25s} {col[2]}")

    # Indexes
    print("\nCreating indexes...")
    try:
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_order_date ON sales("Order Date")')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_category ON sales(Category)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_region ON sales(Region)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_segment ON sales(Segment)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_customer ON sales("Customer ID")')
        conn.commit()
        print("[OK] Indexes created successfully")
    except Exception as e:
        print(f"Note: {e}")

    # Test query
    print("\n" + "=" * 60)
    print("DATABASE TEST QUERY")
    print("=" * 60)
    test_q = """
    SELECT
        COUNT(*) as total_rows,
        COUNT(DISTINCT "Order ID") as total_orders,
        ROUND(SUM(Sales), 2) as total_sales,
        ROUND(SUM(Profit), 2) as total_profit,
        ROUND(SUM(Profit) * 100.0 / SUM(Sales), 2) as profit_margin_pct
    FROM sales
    """
    result = pd.read_sql_query(test_q, conn)
    print("\nTest Query Results:")
    print(result.to_string(index=False))

    conn.close()

    print("\n" + "=" * 60)
    print("[OK] DATABASE CREATED SUCCESSFULLY")
    print("=" * 60)
    print(f"\nDatabase: {db_path}")
    print(f"Table:    sales")
    print(f"Records:  {count:,}")

    return True


if __name__ == "__main__":
    print("=" * 60)
    print("E-COMMERCE SALES ANALYSIS - DATABASE CREATION")
    print("=" * 60)
    print()

    success = create_database()

    if success:
        print("\n" + "=" * 60)
        print("NEXT STEP: Run 'streamlit run app.py'")
        print("=" * 60)
        sys.exit(0)
    else:
        sys.exit(1)
