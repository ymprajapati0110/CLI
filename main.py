import os
import sys
import logging

if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

from constants import logs_path
import utils
import reports
from finance_manager import FinanceManager

logging.basicConfig(
    filename=logs_path,
    filemode="a", 
    level=logging.INFO,
    format="%(levelname)s | %(asctime)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

logger = logging.getLogger("main")

def main():
    """
    Main entry point for the Personal Finance Manager application.
    Executes the interactive terminal loop, handling routing and validation.
    """
    logger.info("Application starting up...")
    
    manager = FinanceManager()
    
    if not manager.is_user_registered():
        print("Welcome to Personal Finance Manager!")
        print("It looks like you are running this application for the first time.")
        print("Please take a moment to register your profile.")
        try:
            manager.register_user()
        except KeyboardInterrupt:
            print("\nRegistration cancelled. Exiting application...")
            sys.exit(0)

    while True:
        try:
            utils.print_header("Personal Finance Manager")
            
            user_name = manager.user.name if manager.user else "User"
            total_inc = sum(inc.amount for inc in manager.incomes)
            total_exp = sum(exp.amount for exp in manager.expenses)
            savings = total_inc - total_exp
            savings_pct = (savings / total_inc * 100) if total_inc > 0 else 0.0
            
            print(f"Profile: {user_name} | Monthly Salary: ₹{manager.user.monthly_salary if manager.user else 0:,.2f}")
            print("-" * 50)
            print(f"Dashboard Stats (All-Time):")
            print(f"  Total Incomes:  ₹{total_inc:,.2f}")
            print(f"  Total Expenses: ₹{total_exp:,.2f}")
            print(f"  Net Savings:    ₹{savings:,.2f} ({savings_pct:.1f}%)")
            print("=" * 50)
            
            print("1. Add Income")
            print("2. Add Expense")
            print("3. View Expenses")
            print("4. Search Expense")
            print("5. Delete Expense")
            print("6. Update Expense")
            print("7. Monthly Report")
            print("8. Category Report")
            print("9. Export CSV")
            print("10. Import CSV")
            print("11. Exit")
            print("=" * 50)
            
            choice = input("Select an option (1-11): ").strip()
            
            match choice:
                case "1":
                    manager.add_income()
                case "2":
                    manager.add_expense()
                case "3":
                    manager.view_expenses(sort_by_date=True)
                case "4":
                    manager.search_expense()
                case "5":
                    manager.delete_expense()
                case "6":
                    manager.update_expense()
                case "7":
                    target_month = utils.validate_date("Enter target month (DD/MM/YYYY or 'today') to filter month: ")
                    month_year = reports.get_month_year_from_date(target_month)
                    reports.generate_monthly_report(manager.incomes, manager.expenses, month_year)
                case "8":
                    reports.generate_category_report(manager.expenses)
                case "9":
                    manager.export_csv()
                case "10":
                    manager.import_csv()
                case "11":
                    print("\nThank you for using Personal Finance Manager! Goodbye.")
                    logger.info("Application shutting down normally.")
                    sys.exit(0)
                case _:
                    utils.print_error("Invalid option. Please choose a number between 1 and 11.")
            
            input("\nPress Enter to return to the Main Menu...")
            
        except KeyboardInterrupt:
            print("\n\nSession interrupted (Ctrl+C). Saving and exiting...")
            logger.info("Application interrupted via KeyboardInterrupt.")
            sys.exit(0)
        except Exception as e:
            logger.critical("An unhandled exception occurred in the main loop.", exc_info=True)
            utils.print_error(f"An unexpected error occurred: {e}")
            print("The application has recovered. Please check logs/app.log for details.")
            input("\nPress Enter to return to the Main Menu...")

if __name__ == "__main__":
    main()
