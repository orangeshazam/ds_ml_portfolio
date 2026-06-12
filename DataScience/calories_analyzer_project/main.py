from etl import transform_products, read_products, read_users, validate_products, generate_meal_plan, analyze_meal_plan, load_to_sql

from pathlib import Path

def main ():
    product_path = Path("data/products.csv")
    users_path = Path("data/users.csv")
    products_df = transform_products(validate_products(read_products(product_path)))
    user_df = read_users(users_path)
    meal_plan_df = generate_meal_plan(user_df, products_df)
    analyze_meal_plan(meal_plan_df)
    load_to_sql(meal_plan_df, "meal plan")


if __name__ == "__main__":
    main()