import pandas as pd
from pathlib import Path
import sqlite3


def read_products(file_path):
    file_path = Path(file_path)
    suffix = file_path.suffix.lower()

    if suffix == '.csv':
        df = pd.read_csv(file_path)
    elif suffix in ['.xls', '.xlsx']:
        df = pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported file format")

    return df


def read_users(file_path):
    file_path = Path(file_path)
    suffix = file_path.suffix.lower()

    if suffix == '.csv':
        df = pd.read_csv(file_path)
    elif suffix in ['.xls', '.xlsx']:
        df = pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported file format")

    required_columns = {"user_id", "target_calories", "preferences"}

    if not required_columns.issubset(df.columns):
        missing = required_columns - set(df.columns)
        raise ValueError(f"Missing these columns: {missing}")

    return df


def validate_products(df):
    required_columns = {"name", "calories", "protein", "fat", "carbs", "portion"}

    if not required_columns.issubset(df.columns):
        missing = required_columns - set(df.columns)
        raise ValueError(f"Missing these columns: {missing}")

    missing_names = df['name'].isna().sum()
    negative_calories = (df["calories"] < 0).sum()
    duplicate_names = df['name'].duplicated().sum()

    print("Validation Report:")
    print(f"Missing names: {missing_names}")
    print(f"Negative calories: {negative_calories}")
    print(f"Duplicate names: {duplicate_names}")

    return df


def transform_products(df):
    df = df.dropna(subset=["name"])
    df = df[df["calories"] >= 0]
    df = df[df["portion"] > 0]

    numeric_cols = ["calories", "protein", "fat", "carbs", "portion"]
    df[numeric_cols] = df[numeric_cols].astype(float)

    df["calories_per_100g"] = (df["calories"] / df["portion"]) * 100

    df.sort_values(by='calories', inplace=True)

    return df


def generate_meal_plan(user_df, products_df):
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    meals = ["Breakfast", "Lunch", "Dinner"]

    meal_plan_records = []

    for _, user in user_df.iterrows():
        user_id = user["user_id"]
        target_calories = user["target_calories"]
        calories_per_meal = target_calories / 3

        for day in days:
            for meal in meals:
                product = products_df.sample(n=1).iloc[0]
                product_calories = product["calories"]

                if product_calories == 0:
                    continue

                portion_needed = round(calories_per_meal / product_calories, 2)

                total_calories = round(portion_needed * product_calories, 2)
                total_protein = round(portion_needed * product["protein"], 2)
                total_fat = round(portion_needed * product["fat"], 2)
                total_carbs = round(portion_needed * product["carbs"], 2)

                meal_plan_records.append({
                    "user_id": user_id,
                    "day": day,
                    "meal": meal,
                    "product": product["name"],
                    "portion": portion_needed,
                    "calories": total_calories,
                    "protein": total_protein,
                    "fat": total_fat,
                    "carbs": total_carbs
                })

    meal_plan_df = pd.DataFrame(meal_plan_records)

    return meal_plan_df


def analyze_meal_plan(meal_plan_df):
    print("\n===== ANALYSIS REPORT =====\n")

    weekly_summary = meal_plan_df.groupby("user_id")[["calories", "protein", "fat", "carbs"]].sum()
    print("Weekly totals per user:")
    print(weekly_summary)

    daily_calories = meal_plan_df.groupby(["user_id", "day"])["calories"].sum()
    print("\nDaily calories per user:")
    print(daily_calories)

    avg_portion = meal_plan_df["portion"].mean()
    print(f"\nAverage portion size: {round(avg_portion, 2)}")

    print("\n===========================\n")


def load_to_sql(df, table_name):
    conn = sqlite3.connect("database.db")
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    conn.close()





