from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


def load_data(file_path):
    file_path = Path(file_path)
    df = pd.read_csv(file_path)

    required_columns = {
        "date",
        "hour",
        "task_type",
        "duration_minutes",
        "focus_score",
        "energy_level",
    }

    if not required_columns.issubset(df.columns):
        missing = required_columns - set(df.columns)
        raise ValueError(f"Missing columns: {missing}")

    df[["hour", "duration_minutes", "focus_score", "energy_level"]] = \
        df[["hour", "duration_minutes", "focus_score", "energy_level"]].astype(int)

    if not df["hour"].between(0, 23).all():
        raise ValueError("Hour must be between 0 and 23")

    if (df["duration_minutes"] <= 0).any():
        raise ValueError("Duration must be greater than 0")

    if not df["focus_score"].between(0, 10).all():
        raise ValueError("Focus score must be between 0 and 10")

    if not df["energy_level"].between(0, 10).all():
        raise ValueError("Energy level must be between 0 and 10")

    return df


def calculate_productivity(df):
    df["productivity_score"] = (
        df["duration_minutes"]
        * df["focus_score"]
        * df["energy_level"]
    ) / 100

    return df


def analyze_patterns(df):
    print("\n===== ANALYSIS REPORT =====\n")

    hourly_energy = df.groupby("hour")["energy_level"].mean()
    hourly_focus = df.groupby("hour")["focus_score"].mean()
    hourly_productivity = df.groupby("hour")["productivity_score"].mean()

    peak_hour = hourly_productivity.idxmax()

    daily_summary = (
        df.groupby("date")
        .agg(
            total_time=("duration_minutes", "sum"),
            avg_energy=("energy_level", "mean"),
            avg_focus=("focus_score", "mean"),
        )
    )

    daily_summary["burnout_risk"] = (
        (daily_summary["total_time"] > 480) &
        (daily_summary["avg_energy"] < 4)
    )

    print("Peak productivity hour:", peak_hour)
    print("\nDaily summary:")
    print(daily_summary)

    print("\n===========================\n")

    return {
        "hourly_energy": hourly_energy,
        "hourly_focus": hourly_focus,
        "daily_summary": daily_summary,
    }


def visualize_energy(analysis_results):
    hourly_energy = analysis_results["hourly_energy"]
    hourly_focus = analysis_results["hourly_focus"]

    plt.figure()
    plt.plot(hourly_energy.index, hourly_energy.values)
    plt.xlabel("Hour of Day")
    plt.ylabel("Average Energy")
    plt.title("Average Energy by Hour")
    plt.show()

    plt.figure()
    plt.plot(hourly_focus.index, hourly_focus.values)
    plt.xlabel("Hour of Day")
    plt.ylabel("Average Focus")
    plt.title("Average Focus by Hour")
    plt.show()