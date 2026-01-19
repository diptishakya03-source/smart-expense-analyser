import pandas as pd

def spending_behavior(df):
    insights = []

    if df.empty:
        return ["No data to analyze yet"]

    category_sum = df.groupby("category")["amount"].sum()
    top_category = category_sum.idxmax()
    insights.append(f"Highest spending category: {top_category}")

    df["date"] = pd.to_datetime(df["date"])
    df["day"] = df["date"].dt.day_name()

    weekend_spend = df[df["day"].isin(["Saturday", "Sunday"])]["amount"].sum()
    insights.append(f"Weekend spending: ₹{int(weekend_spend)}")

    return insights
