import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

DB_NAME = "database.db"
CSV_FILE = "data/transactions.csv"

def extract():
    print("Extracting data...")
    df = pd.read_csv(CSV_FILE)
    return df


def transform(df):
    print("Transforming data...")

    df.dropna(inplace=True)

    df["date"] = pd.to_datetime(df["date"])

    df["amount_signed"] = df.apply(
        lambda row: row["amount"] if row["type"] == "income" else -row["amount"],
        axis=1
    )

    # 👇 ВАЖНО
    df["month"] = df["date"].dt.to_period("M").astype(str)

    return df



def load(df):
    print("Loading into database...")

    conn = sqlite3.connect(DB_NAME)

    df.to_sql("raw_transactions", conn, if_exists="replace", index=False)
    df.to_sql("clean_transactions", conn, if_exists="replace", index=False)

    conn.close()


def create_analytics():
    print("Creating analytics tables...")

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Monthly summary
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS monthly_summary AS
        SELECT
            month,
            SUM(CASE WHEN type = 'income' THEN amount ELSE 0 END) AS total_income,
            SUM(CASE WHEN type = 'expense' THEN amount ELSE 0 END) AS total_expense,
            SUM(amount_signed) AS net_profit
        FROM clean_transactions
        GROUP BY month
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS category_summary AS
        SELECT
            category,
            SUM(amount_signed) AS total_amount
        FROM clean_transactions
        GROUP BY category
    """)

    conn.commit()
    conn.close()


def show_kpis():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM clean_transactions", conn)
    conn.close()

    print("\n📊 KPI Metrics")
    print("-------------------")

    total_income = df[df["type"] == "income"]["amount"].sum()
    total_expense = df[df["type"] == "expense"]["amount"].sum()
    net_profit = df["amount_signed"].sum()
    avg_transaction = df["amount"].mean()
    max_expense = df[df["type"] == "expense"]["amount"].max()

    print(f"Total Income: {total_income}")
    print(f"Total Expense: {total_expense}")
    print(f"Net Profit: {net_profit}")
    print(f"Average Transaction: {avg_transaction:.2f}")
    print(f"Largest Expense: {max_expense}")


def visualize():
    conn = sqlite3.connect(DB_NAME)
    monthly = pd.read_sql_query("SELECT * FROM monthly_summary", conn)
    category = pd.read_sql_query("SELECT * FROM category_summary", conn)
    conn.close()

    # Balance over time
    plt.figure()
    plt.plot(monthly["month"], monthly["net_profit"])
    plt.title("Net Profit by Month")
    plt.xlabel("Month")
    plt.ylabel("Net Profit")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # Category spending
    plt.figure()
    plt.bar(category["category"], category["total_amount"])
    plt.title("Category Summary")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    df_raw = extract()
    df_clean = transform(df_raw)
    load(df_clean)
    create_analytics()
    show_kpis()
    visualize()

    print("\nFinance Analytics Pipeline Completed 🚀")

