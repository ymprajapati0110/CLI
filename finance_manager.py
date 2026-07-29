import logging

from datetime import datetime

from constants import Expense_categories, Income_resources, CSV_PATH

from models import User, Income, Expense

import file_handler
import utils

logger = logging.getLogger("finance_manager")

class FinanceManager:
    """
    Coordinates application state (User, Incomes, Expenses).
    Handles operations (Add, View, Search, Update, Delete) and auto-saves to JSON.
    """
    
    def __init__(self):
        self.user, self.incomes, self.expenses = file_handler.load_data()
        
    def _get_next_transaction_id(self) -> int:
        """
        Helper method to generate a unique ID.
        Checks all existing incomes and expenses, finding the maximum ID and adding 1.
        """
        existing_ids = [inc.transaction_id for inc in self.incomes] + [exp.transaction_id for exp in self.expenses]
        
        return max(existing_ids, default=0) + 1

    def is_user_registered(self) -> bool:
        """
        Checks if a user profile is registered.
        """
        return self.user is not None

    def register_user(self):
        """
        Prompts user for details and registers them in the system.
        """
        utils.print_header("User Registration")
        
        name = utils.validate_non_empty_string("Enter Name: ")
        age = utils.validate_age("Enter Age: ")
        email = utils.validate_email("Enter Email: ")
        salary = utils.validate_amount("Enter Monthly Salary: ")
        
        self.user = User(name, age, email, salary)
        
        file_handler.save_data(self.user, self.incomes, self.expenses)
        
        logger.info(f"User Registered: Name: {name}, Age: {age}, Salary: {salary}")
        utils.print_success(f"Welcome {name}! Your profile has been registered successfully.")

    def add_income(self):
        """
        Guides user through adding a new income transaction.
        """
        utils.print_header("Add Income")
        
        print("Available Income Sources:")
        for idx, src in enumerate(Income_resources, 1):
            print(f"  {idx}. {src}")
            
        while True:
            choice_raw = input(f"Select source (1-{len(Income_resources)}): ").strip()
            try:
                choice_idx = int(choice_raw)
                if 1 <= choice_idx <= len(Income_resources):
                    source = Income_resources[choice_idx - 1]
                    break 
                else:
                    utils.print_error(f"Please select a number between 1 and {len(Income_resources)}.")
            except ValueError:
                utils.print_error("Invalid input. Please enter a number.")
                
        amount = utils.validate_amount("Enter Income Amount: ")
        date = utils.validate_date("Enter Date (DD/MM/YYYY) or type 'today': ")
        description = utils.validate_non_empty_string("Enter Description: ")
        
        transaction_id = self._get_next_transaction_id()
        
        new_income = Income(transaction_id, amount, date, description, source)
        
        self.incomes.append(new_income)
        
        file_handler.save_data(self.user, self.incomes, self.expenses)
        
        current_time = datetime.now().strftime("%H:%M")
        logger.info(f"Income Added | ID: {transaction_id} | Amount: {amount} | Source: {source} | Time: {current_time}")
        utils.print_success(f"Income of ₹{amount:,.2f} added from source '{source}'!")

    def add_expense(self):
        """
        Guides user through adding a new expense transaction.
        """
        utils.print_header("Add Expense")
        
        print("Available Categories:")
        for idx, cat in enumerate(Expense_categories, 1):
            print(f"  {idx}. {cat}")
            
        while True:
            choice_raw = input(f"Select category (1-{len(Expense_categories)}): ").strip()
            try:
                choice_idx = int(choice_raw)
                if 1 <= choice_idx <= len(Expense_categories):
                    category = Expense_categories[choice_idx - 1]
                    break
                else:
                    utils.print_error(f"Please select a number between 1 and {len(Expense_categories)}.")
            except ValueError:
                utils.print_error("Invalid input. Please enter a number.")
                
        amount = utils.validate_amount("Enter Expense Amount: ")
        date = utils.validate_date("Enter Date (DD/MM/YYYY) or type 'today': ")
        description = utils.validate_non_empty_string("Enter Description: ")
        
        transaction_id = self._get_next_transaction_id()
        new_expense = Expense(transaction_id, amount, date, description, category)
        
        self.expenses.append(new_expense)
        file_handler.save_data(self.user, self.incomes, self.expenses)
        
        current_time = datetime.now().strftime("%H:%M")
        logger.info(f"Expense Added | ID: {transaction_id} | Amount: {amount} | Category: {category} | Time: {current_time}")
        utils.print_success(f"Expense of ₹{amount:,.2f} added to category '{category}'!")

    def view_expenses(self, sort_by_date: bool = True):
        """
        Displays all recorded expenses in a formatted table.
        Optionally sorts expenses by date (default oldest to newest).
        """
        utils.print_header("View Expenses")
        
        if not self.expenses:
            print("No expenses recorded yet.")
            return

        if sort_by_date:
            display_list = sorted(
                self.expenses,
                key=lambda x: datetime.strptime(x.date, "%d/%m/%Y")
            )
        else:
            display_list = self.expenses

        print(f"{'ID':<6} | {'Category':<15} | {'Amount':<12} | {'Date':<12} | {'Description'}")
        print("-" * 65)
        for exp in display_list:
            print(f"{exp.transaction_id:<6} | {exp.category:<15} | ₹{exp.amount:<10,.2f} | {exp.date:<12} | {exp.description}")
        print("-" * 65)

    def search_expense(self):
        """
        Allows searching expenses by Category, Amount, Date, or Description.
        Case-insensitive matches are supported.
        """
        utils.print_header("Search Expenses")
        
        if not self.expenses:
            print("No expenses recorded yet. Nothing to search.")
            return
            
        print("Search by:")
        print("  1. Category")
        print("  2. Amount")
        print("  3. Date (DD/MM/YYYY)")
        print("  4. Description")
        
        choice = input("Enter choice (1-4): ").strip()
        query = input("Enter search query: ").strip().lower()
        
        if not query:
            utils.print_error("Search query cannot be empty.")
            return
            
        results = []
        for exp in self.expenses:
            if choice == "1" and query in exp.category.lower():
                results.append(exp)
            elif choice == "2":
                try:
                    val = float(query)
                    if abs(exp.amount - val) < 0.01:
                        results.append(exp)
                except ValueError:
                    if query in str(exp.amount):
                        results.append(exp)
            elif choice == "3" and query in exp.date.lower():
                results.append(exp)
            elif choice == "4" and query in exp.description.lower():
                results.append(exp)
                
        if results:
            utils.print_success(f"Found {len(results)} matching expense(s):")
            print(f"\n{'ID':<6} | {'Category':<15} | {'Amount':<12} | {'Date':<12} | {'Description'}")
            print("-" * 65)
            for exp in results:
                print(f"{exp.transaction_id:<6} | {exp.category:<15} | ₹{exp.amount:<10,.2f} | {exp.date:<12} | {exp.description}")
            print("-" * 65)
        else:
            print("\nNo matching expenses found.")

    def delete_expense(self):
        """
        Deletes an expense matching a user-provided Expense ID.
        Requires confirmation.
        """
        utils.print_header("Delete Expense")
        
        if not self.expenses:
            print("No expenses recorded yet.")
            return
            
        try:
            exp_id = int(input("Enter Expense ID to delete: ").strip())
        except ValueError:
            utils.print_error("Invalid ID format. Must be an integer.")
            return
            
        target_exp = None
        for exp in self.expenses:
            if exp.transaction_id == exp_id:
                target_exp = exp
                break
                
        if not target_exp:
            utils.print_error(f"Expense with ID {exp_id} not found.")
            return
            
        print(f"\nFound Expense: ID: {target_exp.transaction_id} | {target_exp.category} | ₹{target_exp.amount:,.2f} | Date: {target_exp.date} | Description: {target_exp.description}")
        confirm = input("Are you sure you want to delete this expense? (Y/N): ").strip().upper()
        
        if confirm == 'Y':
            self.expenses.remove(target_exp)
            file_handler.save_data(self.user, self.incomes, self.expenses)
            logger.info(f"Expense Deleted | ID: {exp_id} | Category: {target_exp.category} | Amount: {target_exp.amount}")
            utils.print_success(f"Expense ID {exp_id} deleted successfully.")
        else:
            print("Deletion cancelled.")

    def update_expense(self):
        """
        Updates fields of an existing expense matching a user-provided Expense ID.
        """
        utils.print_header("Update Expense")
        
        if not self.expenses:
            print("No expenses recorded yet.")
            return
            
        try:
            exp_id = int(input("Enter Expense ID to update: ").strip())
        except ValueError:
            utils.print_error("Invalid ID format. Must be an integer.")
            return
            
        target_exp = None
        for exp in self.expenses:
            if exp.transaction_id == exp_id:
                target_exp = exp
                break
                
        if not target_exp:
            utils.print_error(f"Expense with ID {exp_id} not found.")
            return
            
        print(f"\nEditing: ID: {target_exp.transaction_id} | Category: {target_exp.category} | Amount: ₹{target_exp.amount:,.2f} | Date: {target_exp.date} | Description: {target_exp.description}")
        
        print("\nWhat do you want to update?")
        print("  1. Category")
        print("  2. Amount")
        print("  3. Date")
        print("  4. Description")
        
        choice = input("Enter option (1-4): ").strip()
        
        old_val = ""
        new_val = ""
        
        if choice == "1":
            print("Available Categories:")
            for idx, cat in enumerate(Expense_categories, 1):
                print(f"  {idx}. {cat}")
            while True:
                choice_raw = input(f"Select new category (1-{len(Expense_categories)}): ").strip()
                try:
                    choice_idx = int(choice_raw)
                    if 1 <= choice_idx <= len(Expense_categories):
                        old_val = target_exp.category
                        target_exp.category = Expense_categories[choice_idx - 1]
                        new_val = target_exp.category
                        break
                    else:
                        utils.print_error(f"Select between 1 and {len(Expense_categories)}.")
                except ValueError:
                    utils.print_error("Invalid number selection.")
        elif choice == "2":
            old_val = str(target_exp.amount)
            target_exp.amount = utils.validate_amount("Enter new Amount: ")
            new_val = str(target_exp.amount)
        elif choice == "3":
            old_val = target_exp.date
            target_exp.date = utils.validate_date("Enter new Date (DD/MM/YYYY) or 'today': ")
            new_val = target_exp.date
        elif choice == "4":
            old_val = target_exp.description
            target_exp.description = utils.validate_non_empty_string("Enter new Description: ")
            new_val = target_exp.description
        else:
            utils.print_error("Invalid choice. Update aborted.")
            return
            
        file_handler.save_data(self.user, self.incomes, self.expenses)
        logger.info(f"Expense Updated | ID: {exp_id} | Choice: {choice} | Old: {old_val} | New: {new_val}")
        utils.print_success(f"Expense ID {exp_id} updated successfully!")

    def export_csv(self):
        """
        Exports all expenses to CSV format at the path specified in constants.
        """
        utils.print_header("Export CSV")
        if not self.expenses:
            utils.print_warning("No expenses recorded. Exporting an empty list.")
            
        success = file_handler.export_expenses_to_csv(self.expenses, CSV_PATH)
        if success:
            utils.print_success(f"Expenses exported to CSV file successfully!\nLocation: {CSV_PATH}")
            logger.info("CSV Export Executed successfully.")
        else:
            utils.print_error("Export failed. See logs/app.log for details.")

    def import_csv(self):
        """
        Imports expenses from a CSV file.
        Assigns a new unique transaction ID to each imported item.
        """
        utils.print_header("Import CSV")
        print(f"Reading from CSV file at: {CSV_PATH}")
        print("Make sure files exist there with headers: Category, Amount, Date, Description")
        
        confirm = input("Do you want to import this data? (Y/N): ").strip().upper()
        if confirm != 'Y':
            print("Import cancelled.")
            return
            
        imported_raw_records = file_handler.import_expenses_from_csv(CSV_PATH)
        if not imported_raw_records:
            utils.print_warning("No valid expenses imported.")
            return
            
        added_count = 0
        for record in imported_raw_records:
            tx_id = self._get_next_transaction_id()
            
            expense_obj = Expense(
                transaction_id=tx_id,
                amount=record["amount"],
                date=record["date"],
                description=record["description"],
                category=record["category"]
            )
            self.expenses.append(expense_obj)
            added_count += 1
            
        if added_count > 0:
            file_handler.save_data(self.user, self.incomes, self.expenses)
            logger.info(f"Imported {added_count} expenses from CSV file.")
            utils.print_success(f"Successfully imported {added_count} expenses from CSV.")
        else:
            utils.print_warning("No new transactions were loaded from CSV.")

