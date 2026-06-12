import pandas as pd
from pathlib import Path

def load_sessions (file_path):
    file_path = Path(file_path)
    df = pd.read_csv(file_path)
    required_columns= {"student_id","date","subject","duration_minutes","focus_score","difficulty"}

    if not required_columns.issubset(df.columns):
        missing_columns = required_columns - set(df.columns)
        raise ValueError(f"Missing: {missing_columns}")

    df[["student_id", "duration_minutes","focus_score","difficulty"]] = df[["student_id", "duration_minutes","focus_score","difficulty"]].astype(int)

    if (df["duration_minutes"] <= 0).any():
        raise ValueError("Duration should be more than 0")
    if not df["focus_score"].between(0, 10).all():
        raise ValueError("Focus score should be between 0 and 10")
    if not df["difficulty"].between(0, 10).all():
        raise ValueError("Difficulty score should be between 0 and 10")

    return df
