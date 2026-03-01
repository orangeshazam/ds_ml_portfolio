import requests
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
def fetch_crypto_data(coin_id="bitcoin", days=30):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
    params = {"vs_currency": "usd", "days": days}

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Ошибка запроса к API: {e}")
        return []

    data = response.json()
    if "prices" not in data:
        print("Нет данных 'prices' в ответе API:", data)
        return []

    formatted_data = [(datetime.fromtimestamp(p[0] / 1000), p[1]) for p in data["prices"]]
    return formatted_data
def create_table():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS crypto_prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT UNIQUE,
            price REAL
        )
    """)
    conn.commit()
    conn.close()

def insert_data(data):
    if not data:
        print("Нет данных для вставки в базу")
        return

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    for d in data:
        try:
            cursor.execute(
                "INSERT OR IGNORE INTO crypto_prices (timestamp, price) VALUES (?, ?)",
                (str(d[0]), d[1])
            )
        except sqlite3.Error as e:
            print(f"Ошибка вставки данных: {e}")

    conn.commit()
    conn.close()

def analyze_data():
    conn = sqlite3.connect("database.db")
    df = pd.read_sql_query("SELECT * FROM crypto_prices", conn)
    conn.close()

    if df.empty:
        print("Нет данных для анализа")
        return

    df["price"] = df["price"].astype(float)
    print("\nАналитика:")
    print(f"Средняя цена: {df['price'].mean():.2f} USD")
    print(f"Максимальная цена: {df['price'].max():.2f} USD")
    print(f"Минимальная цена: {df['price'].min():.2f} USD")
    print(f"Волатильность (std): {df['price'].std():.2f}")

def plot_data():
    conn = sqlite3.connect("database.db")
    df = pd.read_sql_query("SELECT * FROM crypto_prices", conn)
    conn.close()

    if df.empty:
        print("Нет данных для построения графика")
        return

    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df = df.dropna(subset=["timestamp"])

    plt.figure(figsize=(10,5))
    plt.plot(df["timestamp"], df["price"], marker='o', linestyle='-')
    plt.title("Crypto Price Over Time")
    plt.xlabel("Date")
    plt.ylabel("Price (USD)")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    create_table()

    print("Загружаем данные с CoinGecko...")
    data = fetch_crypto_data("bitcoin", 30)

    insert_data(data)
    analyze_data()
    plot_data()
