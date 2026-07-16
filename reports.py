from collections import defaultdict
from models import User, Income, Expense
from utils import print_header, print_warning

def get_month_year_from_date(date_str:str)->str:
    parts=date_str.split('/')
    if len(parts)==3:
        return f"{parts[1]}/{parts[2]}"
    return ""

def generate_monthly_report(incomes:list[Income], expenses:list[Expense], target_month:str):
    monthly_incomes=[inc for inc in incomes if get_month_year_from_date(inc.date)==target_month]
    monthly_expenses=[exp for exp in expenses if get_month_year_from_date(exp.date)==target_month]
    
    print_header(f"Monthly Report for {target_month}")

    total_income=sum(inc.amount for inc in monthly_incomes)
    total_expense=sum(exp.amount for exp in monthly_expenses)
    savings=total_income-total_expense

    savings_pct=(savings/total_income*100) if total_income>0 else 0.0

    print(f"Total Income:           ₹{total_income:,.2f}")
    print(f"Total Expense:          ₹{total_expense:,.2f}")
    print(f"Net Savings:            ₹{savings:,.2f} ({savings_pct:.1f}%)")

    if not monthly_expenses:
        print("\nNo expenses recorded for this month")
        return
    
    expense_amounts=[exp.amount for exp in monthly_expenses]
    highest_expense=max(expense_amounts)
    lowest_expense=min(expense_amounts)

    avg_expense=sum(expense_amounts)/len(expense_amounts)

    highest_exp_obj=max(monthly_expenses, key=lambda x:x.amount)

    print(f"Average Expense:        ₹{avg_expense:,.2f}")
    print(f"Highest Expense:        ₹{highest_expense:,.2f} ({highest_exp_obj.category} - '{highest_exp_obj.description}')")
    print(f"Lowest Expense:         ₹{lowest_expense:,.2f}")

    category_totals=defaultdict(float)
    for exp in monthly_expenses:
        category_totals[exp.category]+=exp.amount

    top_category=max(category_totals, key=category_totals.get)
    print(f"Top Spending Category:  {top_category} (₹{category_totals[top_category]:,.2f})")

def generate_category_report(expenses:list[Expense]):
    print_header("All-Time Category Report")
    if not expenses:
        print_warning("No expenses recorded yet. Cannot generate category report")
        return
    
    category_totals=defaultdict(float)
    total_spent=0.0
    for exp in expenses:
        category_totals[exp.category]+=exp.amount
        total_spent+=exp.amount
    
    sorted_categories=sorted(category_totals.items(), key=lambda x:x[1], reverse=True)
    print(f"{'Category':<15} | {'Total Spent':<12} | {'Percentage':<10}")
    print("-" * 43)
    for cat, amount in sorted_categories:
        percentage = (amount / total_spent * 100) if total_spent > 0 else 0.0
        print(f"{cat:<15} | ₹{amount:<10,.2f} | {percentage:>8.1f}%")
    print("-" * 43)
    print(f"{'TOTAL':<15} | ₹{total_spent:<10,.2f} | 100.0%")
    
def print_statistics(user:User| None, incomes:list[Income], expenses:list[Expense]):
    print_header("Overall Financial Statistics")
    total_income=sum(inc.amount for inc in incomes)
    total_expense=sum(exp.amount for exp in expenses)
    if user:
        print(f"User Profile: {user.name} | Age: {user.age} | Monthly Salary: ₹{user.monthly_salary:,.2f}")
        print("-" * 50)

    savings=total_income-total_expense
    savings_pct=(savings/total_income*100) if total_income>0 else 0.0

    print(f"Total Income:     ₹{total_income:,.2f}")
    print(f"Total Expenses:   ₹{total_expense:,.2f}")
    print(f"Total Savings:    ₹{savings:,.2f}")
    print(f"Savings Ratio:    {savings_pct:.1f}%")
    print("-" * 50)
