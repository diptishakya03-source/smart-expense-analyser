import pandas as pd

def month_comparison(df):
    if df.empty:
        return []

    df["date"] = pd.to_datetime(df["date"])
    df["month"] = df["date"].dt.to_period("M")

    current_month = df["month"].max()
    previous_month = current_month - 1

    current = df[df["month"] == current_month]
    previous = df[df["month"] == previous_month]

    insights = []

    if previous.empty:
        insights.append("Not enough data for month comparison")
        return insights

    curr_sum = current.groupby("category")["amount"].sum()
    prev_sum = previous.groupby("category")["amount"].sum()

    for cat in curr_sum.index:
        if cat in prev_sum:
            change = ((curr_sum[cat] - prev_sum[cat]) / prev_sum[cat]) * 100
            insights.append(
                f"{cat} changed by {change:.1f}% compared to last month"
            )

    return insights
