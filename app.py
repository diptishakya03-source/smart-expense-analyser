from analysis.behavior import spending_behavior
from flask import Flask, render_template, request, redirect
import sqlite3
import pandas as pd
from analysis.health_score import health_score
from analysis.suggestions import suggestions
from analysis.monthly_compare import month_comparison
from analysis.alerts import smart_alerts
import json

app = Flask(__name__)

# ---------- DATABASE ----------
def get_db():
    return sqlite3.connect("database.db")

def create_table():
    conn = get_db()
    conn.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY,
        date TEXT,
        category TEXT,
        amount REAL,
        note TEXT
    )
    """)
    conn.commit()
    conn.close()

create_table()

# ---------- ROUTES ----------
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        date = request.form.get("date")
        category = request.form.get("category")
        amount = request.form.get("amount")
        note = request.form.get("note", "")

        conn = get_db()
        conn.execute(
            "INSERT INTO expenses (date, category, amount, note) VALUES (?, ?, ?, ?)",
            (date, category, amount, note)
        )
        conn.commit()
        conn.close()
        return redirect("/")

    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    conn = get_db()
    df = pd.read_sql("SELECT * FROM expenses", conn)
    conn.close()

    if df.empty:
        return render_template(
            "dashboard.html",
            expenses=[],
            summary={},
            total=0,
            insights=["No expenses yet"],
            score=0,
            tips=[],
            monthly_insights=[],
            alerts=[]
        )

    summary = df.groupby("category")["amount"].sum().to_dict()
    total = df["amount"].sum()

    expenses = df.to_dict(orient="records")

    insights = spending_behavior(df)
    score = health_score(df)
    tips = suggestions(df)
    monthly_insights = month_comparison(df)
    alerts = smart_alerts(df)

    return render_template(
        "dashboard.html",
        expenses=expenses,
        summary=summary,
        total=total,
        insights=insights,
        score=score,
        tips=tips,
        monthly_insights=monthly_insights,
        alerts=alerts,
        chart_data=json.dumps(summary)
    )
@app.route("/edit/<int:id>", methods=["GET"])
def edit_expense(id):
    conn = get_db()
    expense = conn.execute("SELECT * FROM expenses WHERE id = ?", (id,)).fetchone()
    conn.close()

    return render_template("edit.html", expense=expense)
@app.route("/update/<int:id>", methods=["POST"])
def update_expense(id):
    date = request.form.get("date")
    category = request.form.get("category")
    amount = request.form.get("amount")
    note = request.form.get("note")

    conn = get_db()
    conn.execute("""
        UPDATE expenses
        SET date = ?, category = ?, amount = ?, note = ?
        WHERE id = ?
    """, (date, category, amount, note, id))
    conn.commit()
    conn.close()

    return redirect("/dashboard")
@app.route("/delete/<int:id>", methods=["POST"])
def delete_expense(id):
    conn = get_db()
    conn.execute("DELETE FROM expenses WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect("/dashboard")

@app.route("/clear", methods=["POST"])
def clear_expenses():
    conn = get_db()
    conn.execute("DELETE FROM expenses")
    conn.commit()
    conn.close()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
