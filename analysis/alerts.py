import pandas as pd

def smart_alerts(df):
    if df.empty:
        return []

    df["date"] = pd.to_datetime(df["date"])
    df["week"] = df["date"].dt.isocalendar().week

    current_week = df["week"].max()
    prev_weeks = df[df["week"] < current_week]

    alerts = []

    if prev_weeks.empty:
        return ["Not enough data for alerts"]

    avg_weekly = prev_weeks.groupby("category")["amount"].mean()
    current = df[df["week"] == current_week].groupby("category")["amount"].sum()

    for cat in current.index:
        if cat in avg_weekly and current[cat] > 2 * avg_weekly[cat]:
            alerts.append(
                f"Alert: {cat} spending is unusually high this week"
            )

    return alerts
