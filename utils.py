import re
from datetime import datetime 

#Print title
def print_header(title: str):
    border="="+len(title)
    print(f"\n{border}")
    print(title.upper)
    print(f"{border}")

#Print message
def print_success(message: str):
    print(f"Success: {message}")

#Print errror
def print_error(message: str):
    print(f"Error: {message}")

#Print warning
def print_warning(message: str):
    print(f"Warning: {message}")

#Validate non empty string 
def validate_non_empty_string(promt: str)->str:
    while True:
        value=input(promt).strip()
        if not value:
            print_error("Input can't be empty, please enter a valid value")
            continue
        return value

#Validate amount
def validate_amount(promt: str, allow_zero: bool = False)-> float:
    while True:
        raw_input=input(promt).strip()
        if not raw_input:
            print_error("Amount cant be empty")
            continue
        try:
            amount=float(raw_input)
            if amount<0:
                print_error("Amount cant be negative")
                continue
            elif amount==0 and not allow_zero:
                print_error("Amount cant be zero")
                continue
            return amount
        except ValueError:
            print_error("Invalid amount. Please enter a valid amount")

#validate date
def validate_date(prompt: str)->str:
    while True:
        raw_input=input(prompt).strip()
        if not raw_input:
            print_error("Date cant be empty")
            continue
        if raw_input.lower()=="today":
            return datetime.now().strftime("%d/%m/%Y")
        try:
            parsed_date=datetime.strptime(raw_input,"%d/%m/%Y")
            return parsed_date.strftime("%d/%m/%Y")
        except ValueError:
            print_error("Invalid format of date. Use DD/MM/YYYY")
        
#validate email
def validate_email(prompt: str)->str:
    email_regex=r"^[\w\.-]+@[\w\.-]+\.\w+$"
    while True:
        email=input(prompt).strip()
        if not email:
            print_error("Enter your mail")
            continue
        if re.match(email_regex, email):
            return email
        else:
            print_error("Enter proper format of email")

#validate age
def validate_age(prompt: str)->int:
    while True:
        raw_input=input(prompt).strip()
        if not raw_input:
            print_error("Enter your age")
            continue
        try:
            age=int(raw_input)
            if age<0 or age>120:
                print_error("Enter a realistic age")
                continue
            return age
        except ValueError:
            print_error("Invalide age. Please enter a whole number")