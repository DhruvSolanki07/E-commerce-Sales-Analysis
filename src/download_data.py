"""Download Superstore dataset from GitHub."""
import os
import urllib.request
import sys


def download_superstore_data():
    """
    Download the Superstore sales dataset from GitHub.
    Saves to data/superstore.csv
    """
    # Create data directory if it doesn't exist
    if not os.path.exists("data"):
        os.makedirs("data")
        print("[OK] Created 'data' directory")

    # Dataset URL
    url = "https://raw.githubusercontent.com/leonism/sample-superstore/master/data/superstore.csv"
    output_path = os.path.join("data", "superstore.csv")

    try:
        print(f"Downloading dataset from:\n{url}")
        print("\nPlease wait...")

        # Download the file
        urllib.request.urlretrieve(url, output_path)

        # Check file size
        file_size = os.path.getsize(output_path)
        file_size_mb = file_size / (1024 * 1024)

        print(f"\n[OK] Dataset downloaded successfully!")
        print(f"[OK] Saved to: {output_path}")
        print(f"[OK] File size: {file_size_mb:.2f} MB")
        print(f"[OK] File size: {file_size:,} bytes")

        return True

    except Exception as e:
        print(f"\n[ERROR] Error downloading dataset: {str(e)}")
        print("\nPlease check your internet connection and try again.")
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("E-COMMERCE SALES ANALYSIS - DATA DOWNLOAD")
    print("=" * 60)
    print()

    success = download_superstore_data()

    if success:
        print("\n" + "=" * 60)
        print("NEXT STEP: Run 'python src/clean_data.py'")
        print("=" * 60)
        sys.exit(0)
    else:
        sys.exit(1)
