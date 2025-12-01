import datetime
import json
import csv

class Expenses():
    # create an expense object with description, amount, category and date
    def __init__(self, description, amount, category):
        self.description = description
        if amount <= 0:
            print( "invalid amount, can't create this expense.")
            return
        else:
            self.amount = amount
        self.date = datetime.datetime.now()
        self.category = category

    # method to add a new expense
    def addExpense(self):
        # convert the object into dict
        expense_data = {
            "description": self.description,
            "amount": self.amount,
            "date": self.date.isoformat(),
            "category": self.category
        }
        try:
            # open and read the file and convert json to dict
            file = open('./Data/expenses.txt', 'r+')
            jsonText = file.read()
            expenses = json.loads(jsonText) if jsonText else {}
            # make a new item with a new id
            if expenses:
                max_id = max([int(k) for k in expenses.keys()])
                new_id = str(max_id + 1)
            else:
                new_id = "1"
            expenses[new_id] = expense_data
            jsonResult = json.dumps(expenses, indent=2)
            file.seek(0)
            file.write(jsonResult)
            file.truncate() # ensure old data is erased
            file.close()
            return new_id
        except FileNotFoundError:
            with open("./Data/expenses.txt", 'w') as file:
                expenses = {"1": expense_data}
                file.write(json.dumps(expenses, indent=2))
            return "1"


# function to update an expense
def updateExpense(id, updateValue):
    try:
        # open and read the file and convert json to dict
        file = open('./Data/expenses.txt', 'r+')
        jsonText = file.read()
        expenses = json.loads(jsonText) if jsonText else {}
        foundId = False
        for key in expenses.keys():
            if key == str(id):
                foundId = True
        if foundId:
            updatedExpense = expenses[str(id)]

            if updatedExpense:
                # if the updateed value is int then we are updating the amount of the expense
                if isinstance(updateValue, int):
                    if updateValue > 0:
                        updatedExpense['amount'] = updateValue
                    else:
                        print("The value should be greater than 0, please enter a valid value.")
                        return
                    # if it is a string then the updated value is the description
                else:
                    if updateValue != "":
                        updatedExpense['description'] = updateValue
                    else:
                        print("The new value can't be an empty string, please enter a valid value.")
                        return
                
                expenses[str(id)] = updatedExpense
                jsonResult = json.dumps(expenses, indent=2)
                file.seek(0)
                file.write(jsonResult)
                file.truncate()
                file.close()
                return "Expense Updated Successfully!"
        else:
            return "No expense with this id is found, try again with another id."
    except FileNotFoundError:
        print("No Expenses found, please add expenses first")


# function to delete an expense
def deleteExpense(id):
    try:
        # open and read the file and convert json to dict
        file = open('./Data/expenses.txt', 'r+')
        jsonText = file.read()
        expenses = json.loads(jsonText) if jsonText else {}
        foundId = False
        for key in expenses.keys():
            if key == str(id):
                foundId = True
        if foundId:
            deletedExpense = expenses[str(id)]

            if deletedExpense:
                
                expenses.pop(str(id))
                jsonResult = json.dumps(expenses, indent=2)
                file.seek(0)
                file.write(jsonResult)
                file.truncate()
                file.close()
                return "Expense Deleted Successfully!"
        else:
            return "No expense with this id is found, try again with another id."
    except FileNotFoundError:
        print("No Expenses found, please add expenses first")


# function to view all expense
def viewAllExpenses():
    try:
        # open and read the file and convert json to dict
        file = open('./Data/expenses.txt', 'r')
        jsonText = file.read()
        expenses = json.loads(jsonText) if jsonText else {}
        return expenses
        

    except FileNotFoundError:
        print("No Expenses found, please add expenses first")

# function to view a summary of all expense
def allExpensesSummary():
    try:
        # open and read the file and convert json to dict
        file = open('./Data/expenses.txt', 'r')
        jsonText = file.read()
        expenses = json.loads(jsonText) if jsonText else {}
        totalAmount = 0
        for value in expenses.values():
            totalAmount = totalAmount + value['amount']
        return totalAmount

    except FileNotFoundError:
        print("No Expenses found, please add expenses first")

# function to view a summary of expenses for a specific month (of current year).
def monthExpensesSummary(month):
    currentYear = datetime.datetime.now().year
    try:
        # open and read the file and convert json to dict
        file = open('./Data/expenses.txt', 'r')
        jsonText = file.read()
        expenses = json.loads(jsonText) if jsonText else {}
        totalAmount = 0
        for value in expenses.values():
            date = value['date']
            format_string = "%Y-%m-%dT%H:%M:%S.%f"
            datetime_object = datetime.datetime.strptime(date, format_string)
            dateMonth = datetime_object.month
            dateYear = datetime_object.year
            if month == dateMonth and dateYear == currentYear:
                totalAmount = totalAmount + value['amount']
            else:
                pass
        months = {
            "1" : "January",
            "2" : "February", 
            "3" : "March",
            "4" : "April",
            "5" : "May",
            "6" : "June",
            "7" : "July",
            "8" : "August",
            "9" : "September",
            "10" : "October",
            "11" : "November",
            "12" : "December"
        }
        return totalAmount, months[str(month)]

    except FileNotFoundError:
        print("No Expenses found, please add expenses first")

# function to filter expenses by category
def filterByCategory(categoryFilter):
    try:
        # open and read the file and convert json to dict
        file = open('./Data/expenses.txt', 'r')
        jsonText = file.read()
        expenses = json.loads(jsonText) if jsonText else {}
        filtered_expenses = {}
        for key, value in expenses.items():
            if value['category'].lower() == categoryFilter.lower():
                filtered_expenses[key] = value
            else:
                pass
        return filtered_expenses

    except FileNotFoundError:
        print("No Expenses found, please add expenses first")

# function to view summary of expenses by category
def summaryByCategory(categoryFilter):
    try:
        # open and read the file and convert json to dict
        file = open('./Data/expenses.txt', 'r')
        jsonText = file.read()
        expenses = json.loads(jsonText) if jsonText else {}
        totalAmount = 0
        for key, value in expenses.items():
            if value['category'].lower() == categoryFilter.lower():
                totalAmount = totalAmount + value['amount']
            else:
                pass
        return totalAmount
         
    except FileNotFoundError:
        print("No Expenses found, please add expenses first")

# function to check if the monthly budget is exceeded
def checkMonthlyBudget(budget, month):
    currentYear = datetime.datetime.now().year
    try:
        # open and read the file and convert json to dict
        file = open('./Data/expenses.txt', 'r')
        jsonText = file.read()
        expenses = json.loads(jsonText) if jsonText else {}
        totalAmount = 0
        for value in expenses.values():
            date = value['date']
            format_string = "%Y-%m-%dT%H:%M:%S.%f"
            datetime_object = datetime.datetime.strptime(date, format_string)
            dateMonth = datetime_object.month
            dateYear = datetime_object.year
            if month == dateMonth and dateYear == currentYear:
                totalAmount = totalAmount + value['amount']
            else:
                pass
        months = {
            "1" : "January",
            "2" : "February", 
            "3" : "March",
            "4" : "April",
            "5" : "May",
            "6" : "June",
            "7" : "July",
            "8" : "August",
            "9" : "September",
            "10" : "October",
            "11" : "November",
            "12" : "December"
        }
        if totalAmount > budget:
            result = f"Warning! Total Expenses for {months[str(month)]}: ${totalAmount} exceeds your budget."
        elif totalAmount == budget:
            result = f"No more spending! Total Expenses for {months[str(month)]}: ${totalAmount} is exactly equal to your budget."
        else:
            result = f"It's fine! Total Expenses for {months[str(month)]}: ${totalAmount} is lower than your budget."
        return result
    
    except FileNotFoundError:
        print("No Expenses found, please add expenses first")

# function to export expenses to a csv file
def exportToCSV():
    try:
        # open and read the file and convert json to dict
        file = open('./Data/expenses.txt', 'r')
        jsonText = file.read()
        expenses = json.loads(jsonText) if jsonText else {}
        
        csvFile = open("./Data/expenses.csv", 'w', newline='')
        fieldNames = ['id', 'description', 'amount', 'date', 'category']
        writer = csv.DictWriter(csvFile, fieldnames=fieldNames)
        writer.writeheader()
        for key, value in expenses.items():
            row = {'id': key, **value}
            writer.writerow(row)
    except FileNotFoundError:
        print("No Expenses found, please add expenses first")