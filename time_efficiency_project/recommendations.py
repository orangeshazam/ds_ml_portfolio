import pandas as pd

def generate_recommendations (summary_df):
    recommendations = []

    for _, row in summary_df.iterrows():
        message = []

        if row["overloaded"]:
            message.append("Reduce study time tomorrow.")

        if row["avg_focus"] < 5:
            message.append("Work on improving concentration (try Pomodoro).")

        if row["total_minutes"] < 120:
            message.append("Increase study duration for better progress.")

        if row["avg_efficiency"] < 0.5:
            message.append("Review difficult topics more carefully.")

        if not message:
            message.append("Great balance. Keep it up!")

        recommendations.append({
            "date": row["date"],
            "recommendations": " ".join(message)
        })

    return pd.DataFrame(recommendations)