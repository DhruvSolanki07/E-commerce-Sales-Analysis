"""Clean and preprocess Superstore sales data."""
import pandas as pd
import numpy as np
import os
import sys


def clean_superstore_data():
    """
    Clean the raw superstore dataset.
    Returns cleaned dataframe and prints a comprehensive quality report.
    """
    input_file = os.path.join("data", "superstore.csv")
    output_file = os.path.join("data", "clean_superstore.csv")

    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"[ERROR] {input_file} not found!")
        print("Please run 'python src/download_data.py' first.")
        return None

    print("Loading dataset...")
    # Try different encodings for robustness
    for enc in ("utf-8", "latin-1", "ISO-8859-1"):
        try:
            df = pd.read_csv(input_file, encoding=enc)
            break
        except UnicodeDecodeError:
            continue
    else:
        print("[ERROR] Unable to read file with any known encoding.")
        return None

    print(f"[OK] Dataset loaded: {len(df)} rows")

    # Store original count
    original_count = len(df)

    print("\n" + "=" * 60)
    print("DATA QUALITY REPORT - BEFORE CLEANING")
    print("=" * 60)
    print(f"\nOriginal row count: {original_count:,}")
    print(f"Column count: {len(df.columns)}")
    print(f"Columns: {list(df.columns)}")

    # Duplicates
    duplicate_count = df.duplicated().sum()
    print(f"\nDuplicate rows: {duplicate_count}")

    # Missing values
    print("\nMissing values per column:")
    missing = df.isnull().sum()
    if missing.sum() > 0:
        for col in missing[missing > 0].index:
            pct = missing[col] / len(df) * 100
            print(f"  - {col}: {missing[col]} ({pct:.2f}%)")
    else:
        print("  No missing values found")

    # Data types
    print("\nOriginal data types:")
    for col, dtype in df.dtypes.items():
        print(f"  - {col}: {dtype}")

    print("\n" + "=" * 60)
    print("CLEANING DATA...")
    print("=" * 60)

    # 1. Remove duplicates
    if duplicate_count > 0:
        df = df.drop_duplicates()
        print(f"[OK] Removed {duplicate_count} duplicate rows")

    # 2. Drop rows missing essential columns
    essential_columns = ["Order ID", "Order Date", "Sales", "Profit"]
    before_drop = len(df)
    df = df.dropna(subset=essential_columns)
    removed = before_drop - len(df)
    if removed > 0:
        print(f"[OK] Removed {removed} rows with missing essential data")

    # 3. Convert date columns
    try:
        df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
        df["Ship Date"] = pd.to_datetime(df["Ship Date"], errors="coerce")
        print("[OK] Converted date columns to datetime")
    except Exception as e:
        print(f"[ERROR] Converting dates: {e}")

    # 4. Convert numeric columns
    for col in ("Sales", "Quantity", "Discount", "Profit"):
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    print("[OK] Converted numeric columns")

    # 5. Remove rows with invalid dates or numeric values
    before_invalid = len(df)
    df = df.dropna(subset=["Order Date", "Ship Date", "Sales", "Profit"])
    removed_invalid = before_invalid - len(df)
    if removed_invalid > 0:
        print(f"[OK] Removed {removed_invalid} rows with invalid data")

    # 6. Create derived columns
    print("\nCreating derived columns...")

    df["Year"] = df["Order Date"].dt.year
    df["Month"] = df["Order Date"].dt.month
    df["Month_Name"] = df["Order Date"].dt.strftime("%B")
    df["Year_Month"] = df["Order Date"].dt.to_period("M").astype(str)
    print("[OK] Created Year, Month, Month_Name, Year_Month")

    df["Shipping_Days"] = (df["Ship Date"] - df["Order Date"]).dt.days
    print("[OK] Created Shipping_Days")

    # Profit Margin (division-by-zero safe)
    df["Profit_Margin"] = np.where(
        df["Sales"] > 0,
        (df["Profit"] / df["Sales"]) * 100,
        0,
    )
    print("[OK] Created Profit_Margin")

    df["Profit_Status"] = df["Profit"].apply(
        lambda x: "Profit" if x > 0 else ("Loss" if x < 0 else "Break-even")
    )
    print("[OK] Created Profit_Status")

    # Clean column names (strip whitespace)
    df.columns = df.columns.str.strip()

    # Save cleaned data
    df.to_csv(output_file, index=False, encoding="utf-8")
    cleaned_count = len(df)

    print("\n" + "=" * 60)
    print("DATA QUALITY REPORT - AFTER CLEANING")
    print("=" * 60)
    print(f"\nCleaned row count: {cleaned_count:,}")
    print(f"Rows removed: {original_count - cleaned_count:,}")
    print(f"Data retention: {cleaned_count / original_count * 100:.2f}%")

    print("\nFinal data types:")
    for col, dtype in df.dtypes.items():
        print(f"  - {col}: {dtype}")

    print(f"\n[OK] Cleaned data saved to: {output_file}")

    # Sample statistics
    print("\n" + "=" * 60)
    print("SAMPLE STATISTICS")
    print("=" * 60)
    print(f"\nTotal Sales: ${df['Sales'].sum():,.2f}")
    print(f"Total Profit: ${df['Profit'].sum():,.2f}")
    print(f"Total Orders: {df['Order ID'].nunique():,}")
    cust_col = "Customer Name" if "Customer Name" in df.columns else "Customer ID"
    print(f"Total Customers: {df[cust_col].nunique():,}")
    print(
        f"Date Range: {df['Order Date'].min().strftime('%Y-%m-%d')} "
        f"to {df['Order Date'].max().strftime('%Y-%m-%d')}"
    )

    print("\n" + "=" * 60)
    print("[OK] DATA CLEANING COMPLETE")
    print("=" * 60)

    return df


if __name__ == "__main__":
    print("=" * 60)
    print("E-COMMERCE SALES ANALYSIS - DATA CLEANING")
    print("=" * 60)
    print()

    df = clean_superstore_data()

    if df is not None:
        print("\n" + "=" * 60)
        print("NEXT STEP: Run 'python src/eda.py'")
        print("=" * 60)
        sys.exit(0)
    else:
        sys.exit(1)
