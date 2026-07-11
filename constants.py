import os
from pathlib import Path

Base_dir=Path(__file__).resolve().parent

Data_dir=Base_dir/"data"
Log_dir=Base_dir/"logs"

Data_dir.mkdir(parents=True, exist_ok=True)
Log_dir.mkdir(parents=True, exist_ok=True)

Json_path=Data_dir/"expenses.json"
Csv_path=Data_dir/"expenses.csv"

logs_path=Log_dir/"app.log"

Expense_categories=(
    "Food",
    "Travel",
    "Shopping",
    "Bills",
    "Education",
    "Medical",
    "Entertainment",
    "Investment",
    "Others"
)

Income_resources=(
    "Salary",
    "Freelancing",
    "Bonus",
    "Other"
)