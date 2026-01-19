def health_score(df):
    if df.empty:
        return 0

    total = df["amount"].sum()

    food = df[df["category"].str.lower() == "food"]["amount"].sum()

    score = 100

    if total > 50000:
        score -= 30

    if total > 0 and food / total > 0.4:
        score -= 20

    return max(score, 0)
