 import pandas as pd

def calculate_efficiency (df):
    df["efficiency_score"] = (df["focus_score"] / df["difficulty"]) * df["duration_minutes"]

    return df

def daily_summary (df):
    summary = (
        df.groupby("date")
        .agg(
            total_minutes=("duration_minutes", "sum"),
            avg_focus=("focus_score", "mean"),
            avg_efficiency=("efficiency_score", "mean")
        )
        .reset_index()
    )

    summary["study_intensity"] = (
            summary["total_minutes"] * summary["avg_focus"]
    )

    return summary

def detect_overload (summary_df):
    overload_conditions = (
        (summary_df["total_minutes"] > 300) |
        (summary_df["avg_focus"] > 4) |
        (summary_df["avg_efficiency"] > 0.4)
    )

    summary_df["overloaded"] = overload_conditions
    return summary_df





