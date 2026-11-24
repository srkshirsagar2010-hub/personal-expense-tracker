from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from pathlib import Path
from datetime import date

app = Flask(__name__)
app.secret_key = "expense-tracker-demo-key"

DB_PATH = Path(__file__).with_name("expenses.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_database():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            entry_type TEXT NOT NULL,
            expense_date TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        description = request.form.get("description", "").strip()
        category = request.form.get("category", "").strip()
        entry_type = request.form.get("entry_type", "")
        expense_date = request.form.get("expense_date", "")

        try:
            amount = float(request.form.get("amount", 0))
        except ValueError:
            amount = 0

        if (not description or not category or not expense_date
                or amount <= 0
                or entry_type not in ("Income", "Expense")):
            flash("Please enter valid transaction details.")
            return redirect(url_for("index"))

        conn = get_db()
        conn.execute("""
            INSERT INTO transactions
            (description, category, amount, entry_type, expense_date)
            VALUES (?, ?, ?, ?, ?)
        """, (description, category, amount, entry_type, expense_date))
        conn.commit()
        conn.close()

        flash("Transaction added successfully!")
        return redirect(url_for("index"))

    conn = get_db()
    transactions = conn.execute("""
        SELECT * FROM transactions
        ORDER BY expense_date DESC, id DESC
    """).fetchall()

    totals = conn.execute("""
        SELECT
            COALESCE(SUM(CASE WHEN entry_type='Income'
                THEN amount ELSE 0 END), 0) AS income,
            COALESCE(SUM(CASE WHEN entry_type='Expense'
                THEN amount ELSE 0 END), 0) AS expenses
        FROM transactions
    """).fetchone()

    conn.close()

    income = totals["income"]
    expenses = totals["expenses"]
    balance = income - expenses

    return render_template(
        "index.html",
        transactions=transactions,
        income=income,
        expenses=expenses,
        balance=balance,
        today=date.today().isoformat()
    )

@app.route("/delete/<int:transaction_id>", methods=["POST"])
def delete_transaction(transaction_id):
    conn = get_db()
    conn.execute(
        "DELETE FROM transactions WHERE id = ?",
        (transaction_id,)
    )
    conn.commit()
    conn.close()

    flash("Transaction deleted.")
    return redirect(url_for("index"))

initialize_database()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
