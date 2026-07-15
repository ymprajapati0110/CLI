import json
import csv
import logging
from pathlib import Path
from constants import Json_path, Csv_path
from models import User, Income, Expense

logger=logging.getLogger("finance_manager")

def save_data(user:User|None, incomes:list[Income], expenses:list[Expense])->bool:
    data={
        "user":user.to_dict() if user else None,
        "incomes":[income.to_dict() for income in incomes],
        "expenses":[expense.to_dict() for expense in expenses]
    }
    try:
        with open(Json_path,'w',encoding='utf-8') as f:
            json.dump(data,f,indent=4)
        logger.info(f"Successfully saved application data to {Json_path}")
        return True

    except IOError as e:
        logger.error(f"Falied to save data to JSON file: {e}",exc_info=True)
        print(f"Error saving data to file: {e}")
        return False
    
def load_data()->tuple[User|None, list[Income, list[Expense]]]:
    if not Json_path.exists():
        logger.info("JSON data not found. Starting with empty data")
        return None,[],[]
    
    try:
        with open(Json_path,'r',encoding='utf-8') as f:
            data=json.load(f)
        user_data=data.get("user")
        user=User.from_dict(user_data) if user_data else None

        incomes=[]
        for inc_dict in data.get("incomes",[]):
            incomes.append(Income.from_dict(inc_dict))

        expenses=[]
        for exp_dict in data.get("expenses",[]):
            expenses.append(Expense.from_dict(exp_dict))

        logger.info(f"Successfullly loaded data from {Json_path}. User: {user.name if user else 'None'}, Incomes: {len(incomes)}, Expenses: {len(expenses)}")
        return user, incomes, expenses

    except (json.JSONDecodeError, KeyError, TypeError) as e:
        logger.warning(f"Data file is corrupted or formatted incorrectly. Starting with empty data. Details: {e}")
        print("Warning: Data file could not be parsed. Starting with a fresh profile")
        return None, [], []

    except IOError as e:
        logger.error(f"Failed to read data file: {e}", exc_info=True)
        print(f"Error reading data from file: {e}")
        return None, [], []

def export_expenses_to_csv(expenses: list[Expense], target_path: Path=Csv_path) -> bool:
    try:
        fieldnames=["ID","Category","Amount","Date","Description"]
        with open(target_path, "w", newline="", encoding="utf-8") as f:
            writer=csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for exp in expenses:
                writer.writerow({
                    "ID":exp.transaction_id,
                    "Category":exp.category,
                    "Amount":exp.amount,
                    "Date":exp.date,
                    "Description":exp.description
                })
        logger.info(f"Successfully exported {len(expenses)} expenses to CSV at {target_path}")
        return True
    except IOError as e:
        logger.error(f"Failed to export expenses to CSV: {e}", exc_info=True)
        print(f"Error exporting to csv: {e}")
        return False
    
def import_expenses_from_csv(target_path: Path=Csv_path)->list[dict]:
    if not target_path.exists():
        logger.warning(f"Attempted CSV import, but file does not exist at {target_path}")
        print(f"Import file not found at {target_path}")
        return []

    imported_raw=[]
    try:
        with open(target_path, "r", encoding='utf-8') as f:
            reader=csv.DictReader(f)
            required_cols={"Category", "Amount", "Date", "Description"}
            if not reader.fieldnames or not required_cols.issubset(set(reader.fieldnames)):
                logger.error("CSV import failed: Missing required columns in CSV header")
                print("Invalid csv format. Headers must include: Category, Amount, Date, Description")
                return []
                
            for row in reader:
                try:
                    amount=float(row["Amount"])
                    category=row["Category"].strip()
                    date=row["Date"].strip()
                    description=row["Description"].strip()

                    if not category or not date or not description or amount<0:
                        continue
                
                    imported_raw.append({
                        "category":category,
                        "amount":amount,
                        "date":date,
                        "description":description
                    })
                except(ValueError, KeyError):
                    continue
        
        logger.info(f"Successfully imported {len(imported_raw)} records from CSV.")
        return imported_raw
    except IOError as e:
        logger.error(f"Failed to read CSV file: {e}", exc_info=True)
        print(f"Error reading CSV file: {e}")
        return []
