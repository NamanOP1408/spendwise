# SpendWise 💸

A command-line personal expense tracker built with Python and SQLite. Record expenses, review spending, set monthly budgets, and generate category reports — with no third-party dependencies.

## Features

- Add expenses with amount, category, description, and date
- Store data persistently in a local SQLite database
- List and delete transactions
- View overall spending summaries
- Break spending down by category
- Generate reports for a chosen month
- Set category budgets and check current-month budget status
- Validate user input and store money as integer paise to avoid floating-point rounding errors
- Automated unit tests for core database behavior

## Requirements

- Python 3.10 or newer
- No external packages required (SQLite is included with Python)

## Quick start

Clone the repository, then run:

```bash
git clone https://github.com/YOUR-USERNAME/spendwise.git
cd spendwise
python3 main.py --help
```

The database is created automatically the first time you run a command.

## Usage

Add an expense:

```bash
python3 main.py add 149.50 Food "Lunch with friends"
python3 main.py add 60 Travel "Metro card" --date 2026-10-20
```

List expenses and review totals:

```bash
python3 main.py list
python3 main.py summary
python3 main.py categories
```

Monthly report:

```bash
python3 main.py monthly 2026-10
```

Set and check a monthly budget:

```bash
python3 main.py budget Food 3000
python3 main.py budget Travel 1500
python3 main.py budgets
```

Delete a transaction by its ID:

```bash
python3 main.py delete 1
```

Run tests:

```bash
python3 -m unittest discover -s tests -v
```

## Project structure

```text
spendwise/
├── main.py              # CLI commands and input validation
├── database.py          # SQLite database operations
├── reports.py           # Summaries, category reports, and budgets
├── tests/
│   └── test_database.py # Unit tests
├── .gitignore
└── README.md
```

## Example workflow

```text
$ python3 main.py add 250 Food "Groceries"
Expense saved (ID 1): ₹250.00 for Food.

$ python3 main.py summary

SPENDING SUMMARY
Total expenses:   1
Total spent:      ₹250.00
Average expense:  ₹250.00
```

## Learning outcomes

This project practices functions, modules, command-line arguments, validation, exceptions, SQL, SQLite, data aggregation, unit testing, and Git-based project documentation.

## Roadmap

- [ ] Export transactions to CSV
- [ ] Add income tracking and net cash flow
- [ ] Add date-range filters
- [ ] Build a web dashboard with Flask or Streamlit
- [ ] Add charts and recurring expense reminders

## Privacy

Transactions are stored locally in `spendwise.db`. The database is intentionally ignored by Git so personal financial records are not committed to the repository.

## License

MIT — see `LICENSE`.
