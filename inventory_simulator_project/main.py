from inventory_simulator import InventorySimulator
import matplotlib.pyplot as plt


def main():
    sim = InventorySimulator(
        initial_inventory=100,
        reorder_point=40,
        reorder_quantity=80
    )

    results = sim.run_simulation(days=60)

    print("\n--- Simulation Summary ---")
    print(f"Total Profit: {sim.total_profit}")
    print(f"Total Lost Sales: {sim.total_lost_sales}")
    print(f"Final Inventory: {sim.inventory}")

    # 4️⃣ Строим графики
    plt.figure()
    plt.plot(results["day"], results["inventory"])
    plt.title("Inventory Over Time")
    plt.xlabel("Day")
    plt.ylabel("Inventory Level")
    plt.show()

    plt.figure()
    plt.plot(results["day"], results["cumulative_profit"])
    plt.title("Cumulative Profit")
    plt.xlabel("Day")
    plt.ylabel("Profit")
    plt.show()


if __name__ == "__main__":
    main()