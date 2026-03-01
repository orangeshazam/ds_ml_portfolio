import numpy as np

class InventorySimulator:

    def __init__(self, initial_stock=500, reorder_point=200, reorder_quantity=400, lead_time=5, price=50, cost=20, days=60, avg_daily_demand=80):
        self.initial_stock = initial_stock
        self.inventory = initial_stock
        self.reorder_point = reorder_point
        self.reorder_quantity = reorder_quantity
        self.lead_time = lead_time
        self.price = price
        self.cost = cost
        self.days = days
        self.avg_daily_demand = avg_daily_demand
        self.pending_orders = []
        self.history = []
        self.total_profit = 0
        self.total_lost_sales = 0

    def generate_daily_demand(self):
        demand = np.random.poisson(lam=self.avg_daily_demand)
        return demand

    def process_day (self, day):
        arrived_orders = [order for order in self.pending_orders if order[0] == day]

        for arrival_day, quantity in arrived_orders:
            self.inventory += quantity

        self.pending_orders = [
            order for order in self.pending_orders if order[0] != day
        ]

        demand = self.generate_daily_demand()

        if demand <= self.inventory:
            sales = demand
            lost_sales = 0
        else:
            sales = self.inventory
            lost_sales = demand - self.inventory
            self.total_lost_sales += lost_sales

        self.inventory -= sales

        revenue = sales * self.price
        cost = sales * self.cost
        daily_profit = revenue - cost
        self.total_profit += daily_profit

        if self.inventory <= self.reorder_point:
            arrival_day = day + self.lead_time
            self.pending_orders.append((arrival_day, self.reorder_quantity))

        self.history.append({
            "day": day,
            "inventory": self.inventory,
            "demand": demand,
            "sales": sales,
            "lost_sales": lost_sales,
            "daily_profit": daily_profit
        })

    def run_simulation(self, days=30):
        for day in range(1, days + 1):
            self.process_day(day)

        import pandas as pd
        results_df = pd.DataFrame(self.history)

        results_df["cumulative_profit"] = results_df["daily_profit"].cumsum()

        print("Simulation finished.")
        print(f"Total profit: {self.total_profit}")
        print(f"Total lost sales: {self.total_lost_sales}")
        print(f"Final inventory: {self.inventory}")

        return results_df


