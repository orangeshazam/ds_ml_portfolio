from pathlib import Path
import pandas as pd


def load_data(file_path):
    file_path = Path(file_path)
    df = pd.read_csv(file_path)

    required_columns = {
        "user_id",
        "date",
        "content_type",
        "title",
        "category",
        "duration_minutes",
        "rating",
        "productive",
    }

    if not required_columns.issubset(df.columns):
        missing_cols = required_columns - set(df.columns)
        raise ValueError(f"Missing columns: {missing_cols}")

    df[["user_id", "duration_minutes", "rating", "productive"]] = (
        df[["user_id", "duration_minutes", "rating", "productive"]]
        .astype(int)
    )

    if (df["duration_minutes"] <= 0).any():
        raise ValueError("Duration should be more than 0")

    if not df["rating"].between(0, 10).all():
        raise ValueError("Rating should be between 0 and 10")

    if not df["productive"].isin([0, 1]).all():
        raise ValueError("Productive column must contain only 0 or 1")

    return df


def calculate_productivity_score(df):
    df["productivity_score"] = (
        df["duration_minutes"] * df["rating"] * df["productive"]
    ) / 10
    return df


def daily_summary(df):
    df["productive_minutes"] = df["duration_minutes"] * df["productive"]
    df["entertainment_minutes"] = (
        df["duration_minutes"] * (1 - df["productive"])
    )

    summary = (
        df.groupby("date")
        .agg(
            total_time=("duration_minutes", "sum"),
            productive_time=("productive_minutes", "sum"),
            entertainment_time=("entertainment_minutes", "sum"),
            avg_rating=("rating", "mean"),
            productivity_score_sum=("productivity_score", "sum"),
        )
    )

    summary["productivity_ratio"] = (
        summary["productive_time"] / summary["total_time"]
    )

    return summary


def detect_entertainment_overload(summary):
    overload_conditions = (
        (summary["entertainment_time"] > summary["productive_time"])
        | (summary["productivity_ratio"] < 0.4)
    )

    summary["overloaded"] = overload_conditions
    return summary


def generate_recommendations(summary):
    recommendations = []

    for date, row in summary.iterrows():
        message = []

        if row["overloaded"]:
            message.append("Reduce time tomorrow.")

        if row["productivity_ratio"] < 0.4:
            message.append(
                "Too much entertainment content. Increase educational content."
            )

        if 0.4 <= row["productivity_ratio"] <= 0.6:
            message.append(
                "Moderate balance. Try to slightly increase productive time."
            )

        if row["entertainment_time"] > 180:
            message.append(
                "Entertainment time is high. Consider setting limits."
            )

        if not message:
            message.append("Good balance. Keep your current routine.")

        recommendations.append({
            "date": date,
            "recommendations": " ".join(message)
        })

    return pd.DataFrame(recommendations)





