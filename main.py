"""SpendWise: a simple command-line expense tracker."""

import argparse
from datetime import date
from decimal import Decimal, InvalidOperation
from database import initialize_database, add_expense, list_expenses, delete_expense
from reports import show_summary, show_categories, show_monthly_report, set_budget, show_budgets


def parse_amount(value: str) -> Decimal:
    try:
        amount = Decimal(value)
    except InvalidOperation as exc:
        raise argparse.ArgumentTypeError("Amount must be a number, e.g. 149.50") from exc
    if amount <= 0:
        raise argparse.ArgumentTypeError("Amount must be greater than zero.")
    if amount.as_tuple().exponent < -2:
        raise argparse.ArgumentTypeError("Use at most two decimal places.")
    return amount


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="spendwise",
        description="Track expenses and understand where your money goes.",
    )
    commands = parser.add_subparsers(dest="command", required=True)

    add = commands.add_parser("add", help="Record a new expense")
    add.add_argument("amount", type=parse_amount, help="Amount, e.g. 249.50")
    add.add_argument("category", help="Category, e.g. Food, Travel, Bills")
    add.add_argument("description", help="Short description (use quotes for multiple words)")
    add.add_argument("--date", dest="spent_on", default=date.today().isoformat(),
                     help="Date in YYYY-MM-DD format (defaults to today)")

    commands.add_parser("list", help="List recent expenses")
    commands.add_parser("summary", help="Show total spending and average expense")
    commands.add_parser("categories", help="Show spending grouped by category")

    monthly = commands.add_parser("monthly", help="Show a monthly spending report")
    monthly.add_argument("month", help="Month in YYYY-MM format")

    budget = commands.add_parser("budget", help="Set a monthly category budget")
    budget.add_argument("category", help="Category name")
    budget.add_argument("amount", type=parse_amount, help="Monthly budget amount")

    commands.add_parser("budgets", help="Compare this month's spending with budgets")

    delete = commands.add_parser("delete", help="Delete an expense by ID")
    delete.add_argument("expense_id", type=int, help="ID shown by the list command")
    return parser


def main() -> None:
    initialize_database()
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "add":
        try:
            date.fromisoformat(args.spent_on)
        except ValueError:
            parser.error("Date must be a valid date in YYYY-MM-DD format.")
        expense_id = add_expense(args.amount, args.category, args.description, args.spent_on)
        print(f"Expense saved (ID {expense_id}): ₹{args.amount:.2f} for {args.category}.")
    elif args.command == "list":
        list_expenses()
    elif args.command == "summary":
        show_summary()
    elif args.command == "categories":
        show_categories()
    elif args.command == "monthly":
        if len(args.month) != 7 or args.month[4] != "-":
            parser.error("Month must use YYYY-MM format, e.g. 2026-10.")
        try:
            date.fromisoformat(args.month + "-01")
        except ValueError:
            parser.error("Enter a valid month, e.g. 2026-10.")
        show_monthly_report(args.month)
    elif args.command == "budget":
        set_budget(args.category, args.amount)
    elif args.command == "budgets":
        show_budgets()
    elif args.command == "delete":
        if delete_expense(args.expense_id):
            print(f"Deleted expense {args.expense_id}.")
        else:
            print(f"No expense found with ID {args.expense_id}.")


if __name__ == "__main__":
    main()
