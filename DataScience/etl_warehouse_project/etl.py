import pandas as pd
import sqlite3
from pathlib import Path

DB_NAME = "database.db"
RAW_FILE = "data/raw_sales.csv"


def extract():
    print("Extracting data...")
    df = pd.read_csv(RAW_FILE)
    return df

def transform(df):
    print("Transforming data...")
    df.dropna(inplace=True)
    df["order_date"] = pd.to_datetime(df["order_date"])
    df["total_amount"] = df["quantity"] * df["price"]
    return df

def load(df):
    print("Loading into database...")

    conn = sqlite3.connect(DB_NAME)
    df.to_sql("raw_sales", conn, if_exists="replace", index=False)
    df.to_sql("clean_sales", conn, if_exists="replace", index=False)

    conn.close()

def create_analytics():
    print("Creating analytics tables...")

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sales_by_category AS
        SELECT 
            category,
            SUM(total_amount) AS total_revenue,
            SUM(quantity) AS total_quantity
        FROM clean_sales
        GROUP BY category
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sales_by_date AS
        SELECT 
            order_date,
            SUM(total_amount) AS daily_revenue
        FROM clean_sales
        GROUP BY order_date
    """)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    df_raw = extract()
    df_clean = transform(df_raw)
    load(df_clean)
    create_analytics()

    print("ETL Pipeline Completed Successfully 🚀")
