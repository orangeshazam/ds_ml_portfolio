import matplotlib.pyplot as plt
from simulator import run_strategy_simulation


def visualize_results(results):
    strategies = list(results.keys())
    profits = [results[s]["profit"] for s in strategies]

    plt.figure()
    plt.bar(strategies, profits)
    plt.title("Pricing Strategy Profit Comparison")
    plt.xlabel("Strategy")
    plt.ylabel("Total Profit (30 Days)")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.show()


def main():
    results = run_strategy_simulation()

    print("\n===== STRATEGY RESULTS =====\n")
    for strategy, data in results.items():
        print(f"{strategy}")
        print(f"  Price: {data['price']}")
        print(f"  Revenue: {data['revenue']}")
        print(f"  Profit: {data['profit']}")
        print()

    visualize_results(results)

if __name__ == "__main__":
    main()