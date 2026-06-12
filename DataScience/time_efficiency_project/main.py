from data_loader import load_sessions
from analytics import calculate_efficiency, daily_summary, detect_overload
from recommendations import generate_recommendations
from pathlib import Path

def main():
    file_path = Path("study_sessions.csv")
    df = load_sessions(file_path)
    df = calculate_efficiency(df)
    summary_df = daily_summary(df)
    summary_df = detect_overload(summary_df)
    recommendation = generate_recommendations(summary_df)

    print("\n=== DAILY SUMMARY ===")
    print(summary_df)

    print("\n=== RECOMMENDATIONS ===")
    print(recommendation)


if __name__ == "__main__":
    main()
