"""SQLite storage layer for SpendWise."""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "spendwise.db"


def connect():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    with connect() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount_cents INTEGER NOT NULL CHECK (amount_cents > 0),
                category TEXT NOT NULL,
                description TEXT NOT NULL,
                spent_on TEXT NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS budgets (
                category TEXT PRIMARY KEY COLLATE NOCASE,
                amount_cents INTEGER NOT NULL CHECK (amount_cents > 0)
            )
        """)


def to_cents(amount) -> int:
    """Store money as integer paise/cents to avoid floating-point errors."""
    return int(amount * 100)


def add_expense(amount, category: str, description: str, spent_on: str) -> int:
    category = category.strip().title()
    description = description.strip()
    if not category or not description:
        raise ValueError("Category and description cannot be empty.")
    with connect() as conn:
        cursor = conn.execute(
            "INSERT INTO expenses (amount_cents, category, description, spent_on) VALUES (?, ?, ?, ?)",
            (to_cents(amount), category, description, spent_on),
        )
        return cursor.lastrowid


def fetch_expenses(month: str | None = None):
    with connect() as conn:
        if month:
            return conn.execute(
                """SELECT id, amount_cents, category, description, spent_on
                   FROM expenses WHERE substr(spent_on, 1, 7) = ?
                   ORDER BY spent_on DESC, id DESC""", (month,)
            ).fetchall()
        return conn.execute(
            """SELECT id, amount_cents, category, description, spent_on
               FROM expenses ORDER BY spent_on DESC, id DESC"""
        ).fetchall()


def list_expenses():
    expenses = fetch_expenses()
    if not expenses:
        print("No expenses yet. Add one with: python3 main.py add 120 Food \"Lunch\"")
        return
    print(f"{'ID':<5} {'DATE':<12} {'CATEGORY':<16} {'AMOUNT':>12}  DESCRIPTION")
    print("-" * 72)
    for item in expenses:
        print(f"{item['id']:<5} {item['spent_on']:<12} {item['category']:<16} "
              f"₹{item['amount_cents'] / 100:>10.2f}  {item['description']}")


def delete_expense(expense_id: int) -> bool:
    with connect() as conn:
        cursor = conn.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
        return cursor.rowcount > 0
