from analytics import (
    load_data,
    calculate_productivity,
    analyze_patterns,
    visualize_energy,
)


def main():
    df = load_data("energy_log.csv")

    df = calculate_productivity(df)

    results = analyze_patterns(df)

    visualize_energy(results)


if __name__ == "__main__":
    main()