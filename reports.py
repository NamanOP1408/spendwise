"""Reporting and budgeting features for SpendWise."""

from datetime import date
from database import connect, fetch_expenses, to_cents


def show_summary():
    with connect() as conn:
        row = conn.execute(
            "SELECT COUNT(*) AS count, COALESCE(SUM(amount_cents), 0) AS total FROM expenses"
        ).fetchone()
    count, total = row["count"], row["total"]
    average = total / count / 100 if count else 0
    print("\nSPENDING SUMMARY")
    print(f"Total expenses:   {count}")
    print(f"Total spent:      ₹{total / 100:.2f}")
    print(f"Average expense:  ₹{average:.2f}")


def show_categories(month: str | None = None):
    query = """
        SELECT category, SUM(amount_cents) AS total, COUNT(*) AS count
        FROM expenses
    """
    params = ()
    if month:
        query += " WHERE substr(spent_on, 1, 7) = ?"
        params = (month,)
    query += " GROUP BY category ORDER BY total DESC"
    with connect() as conn:
        rows = conn.execute(query, params).fetchall()
    if not rows:
        print("No expenses found for this period.")
        return
    print("\nSPENDING BY CATEGORY")
    for row in rows:
        print(f"{row['category']:<18} ₹{row['total'] / 100:>10.2f}  ({row['count']} transactions)")


def show_monthly_report(month: str):
    expenses = fetch_expenses(month)
    total = sum(item["amount_cents"] for item in expenses)
    print(f"\nMONTHLY REPORT — {month}")
    print(f"Transactions: {len(expenses)}")
    print(f"Total spent:  ₹{total / 100:.2f}")
    show_categories(month)


def set_budget(category: str, amount):
    category = category.strip().title()
    if not category:
        print("Category cannot be empty.")
        return
    with connect() as conn:
        conn.execute(
            """INSERT INTO budgets (category, amount_cents) VALUES (?, ?)
               ON CONFLICT(category) DO UPDATE SET amount_cents = excluded.amount_cents""",
            (category, to_cents(amount)),
        )
    print(f"Monthly budget for {category} set to ₹{amount:.2f}.")


def show_budgets():
    month = date.today().strftime("%Y-%m")
    with connect() as conn:
        budgets = conn.execute(
            "SELECT category, amount_cents FROM budgets ORDER BY category"
        ).fetchall()
        spent_rows = conn.execute(
            """SELECT category, SUM(amount_cents) AS total FROM expenses
               WHERE substr(spent_on, 1, 7) = ? GROUP BY category""", (month,)
        ).fetchall()
    spent = {row["category"].casefold(): row["total"] for row in spent_rows}
    if not budgets:
        print("No budgets set. Try: python3 main.py budget Food 3000")
        return
    print(f"\nBUDGET STATUS — {month}")
    for budget in budgets:
        used = spent.get(budget["category"].casefold(), 0)
        limit = budget["amount_cents"]
        remaining = limit - used
        status = "OVER BUDGET" if remaining < 0 else "within budget"
        print(f"{budget['category']:<18} spent ₹{used/100:>9.2f} / ₹{limit/100:<9.2f} "
              f"| {status} (₹{remaining/100:.2f} remaining)")
