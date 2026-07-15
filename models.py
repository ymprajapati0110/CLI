class User:
    def __init__(self, name:str, age:int, email:str, monthly_salary:float):
        self._name=name
        self._age=age
        self._email=email
        self._monthly_salary=monthly_salary

    @property
    def name(self)->str:
        return self._name

    @name.setter
    def name(self, value:str):
        if not value.strip:
            raise ValueError("Name cannot be empty")
        self._name=value.strip()

    @property
    def age(self)->int:
        return self._age

    @age.setter
    def age(self, value:int):
        if value<=0 or value>120:
            raise ValueError("Age must be between 1 to 120")
        self._age=value

    @property
    def email(self)->str:
        return self._email

    @email.setter
    def email(self, value:str):
        if '@' not in value:
            raise ValueError('Invalid email syntax')
        self._email=value.strip()
    
    @property
    def monthly_salary(self)->float:
        return self._monthly_salary

    @monthly_salary.setter
    def monthly_salary(self, value:float):
        if value<0:
            raise ValueError("Salary cannot be negative")
        self._monthly_salary=value

    def to_dict(self)->dict:
        return{
            "name":self.name,
            "age":self.age,
            "email":self.email,
            "monthly_salary":self.monthly_salary
        }

    @classmethod
    def from_dict(cls, data:dict):
        return cls(
            name=data["name"],
            age=data["age"],
            email=data["email"],
            monthly_salary=data["monthly_salary"]
        )

class Transaction:
    def __init__(self, transaction_id:int, amount:float, date:str, description:str):
        self._transaction_id=transaction_id
        self._amount=amount
        self._date=date
        self._description=description

    @property
    def transaction_id(self)->int:
        return self._transaction_id
    
    @property
    def amount(self)->float:
        return self._amount

    @amount.setter
    def amount(self, value:float):
        if value<0:
            raise ValueError("Amount cannot be negative")
        self._amount=value

    @property
    def date(self)->str:
        return self._date

    @date.setter
    def date(self, value:str):
        self._date=value
    
    @property
    def description(self)->str:
        return self._description
    
    @description.setter
    def description(self, value:str):
        if not value.strip():
            raise ValueError("Description cannot be empty")
        self._description=value.strip()

    def to_dict(self)->dict:
        return{
            "id":self.transaction_id,
            "amount":self.amount,
            "date":self.date,
            "description":self.description
        }

class Income(Transaction):
    def __init__(self, transaction_id:int, amount:float, date:str, description:str, source:str):
        super().__init__(transaction_id, amount, date, description)
        self.source=source

    @property
    def source(self)->str:
        return self._source

    @source.setter
    def source(self, value:str):
        self._source=value
    
    def to_dict(self):
        data=super().to_dict()
        data["source"]=self.source
        return data

    @classmethod
    def from_dict(cls, data:dict):
        return cls(
            transaction_id=data["id"],
            amount=data["amount"],
            date=data["date"],
            description=data["description"],
            source=data["source"]
        )

class Expense(Transaction):
    def __init__(self, transaction_id:int, amount:float, date:str, description:str, category:str):
        super().__init__(transaction_id, amount, date, description)
        self._category=category

    @property
    def category(self)->str:
        return self._category

    @category.setter
    def category(self, value:str):
        self._category=value
    
    def to_dict(self)->dict:
        data=super().to_dict()
        data["category"]=self.category
        return data

    @classmethod
    def from_dict(cls, data:dict):
        return cls(
            transaction_id=data["id"],
            amount=data["amount"],
            date=data["date"],
            description=data["description"],
            category=data["category"]
        )