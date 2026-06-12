import numpy as np


BASE_PRICE = 100
COST_PER_UNIT = 40
ELASTICITY = 0.8
DAYS = 30


def generate_market_conditions(days=DAYS):
    demand = np.random.normal(loc=200, scale=30, size=days)
    demand = np.clip(demand, 50, None)
    return demand


def simulate_sales(price, demand_array, elasticity=ELASTICITY):
    price_factor = (price - BASE_PRICE) / BASE_PRICE
    adjusted_demand = demand_array * (1 - elasticity * price_factor)
    adjusted_demand = np.clip(adjusted_demand, 0, None)

    units_sold = adjusted_demand
    revenue = units_sold * price
    cost = units_sold * COST_PER_UNIT
    profit = revenue - cost

    total_revenue = revenue.sum()
    total_profit = profit.sum()

    return total_revenue, total_profit


def run_strategy_simulation():
    demand = generate_market_conditions()

    strategies = {
        "Low Price": 80,
        "Medium Price": 100,
        "High Price": 130,
    }

    results = {}

    for strategy_name, price in strategies.items():
        revenue, profit = simulate_sales(price, demand)
        results[strategy_name] = {
            "price": price,
            "revenue": round(revenue, 2),
            "profit": round(profit, 2),
        }

    return results