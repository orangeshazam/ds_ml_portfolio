import pandas as pd
from pathlib import Path
from core import load_data, calculate_productivity_score, daily_summary, generate_recommendations, detect_entertainment_overload
def main():
    file_path = Path("list.csv")
    df = load_data(file_path)
    df = calculate_productivity_score(df)
    summary_df = daily_summary(df)
    summary_df = detect_entertainment_overload(summary_df)
    recommendation = generate_recommendations(summary_df)
    print("\n=== DAILY SUMMARY ===")
    print(summary_df)

    print("\n=== RECOMMENDATIONS ===")
    print(recommendation)


if __name__ == "__main__":
    main()
