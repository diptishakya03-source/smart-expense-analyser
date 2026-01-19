def suggestions(df):
    if df.empty:
        return ["No suggestions yet"]

    category_sum = df.groupby("category")["amount"].sum()
    top_category = category_sum.idxmax()

    return [
        f"If you reduce {top_category} expenses by ₹500/week, you save ₹24,000/year"
    ]
