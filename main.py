from expenses import (
    Expenses,
    updateExpense,
    deleteExpense,
    viewAllExpenses,
    allExpensesSummary,
    monthExpensesSummary,
    filterByCategory,
    summaryByCategory,
    checkMonthlyBudget,
    exportToCSV
)

def main():
    while True:
        print("\n===== Expense Tracker Menu =====")
        print("1. Add Expense")
        print("2. Update Expense")
        print("3. Delete Expense")
        print("4. View All Expenses")
        print("5. View Summary of All Expenses")
        print("6. View Summary for a Specific Month")
        print("7. Filter Expenses by Category")
        print("8. Summary of Expenses by Category")
        print("9. Check Monthly Budget")
        print("10. Export Expenses to CSV")
        print("0. Exit")
        
        choice = input("Enter your choice: ")

        if choice == "1":
            description = input("Enter description: ")
            try:
                amount = int(input("Enter amount: "))
            except ValueError:
                print("Invalid amount. Please enter a number.")
                continue
            category = input("Enter category: ")
            expense = Expenses(description, amount, category)
            new_id = expense.addExpense() 
            print(f"Expense added successfully! (ID: {new_id})")


        elif choice == "2":
            try:
                exp_id = int(input("Enter expense ID to update: "))
            except ValueError:
                print("Invalid ID.")
                continue
            update_type = input("Update 'am' for 'amount' or 'desc' for 'description'? ").strip().lower()
            if update_type == "am":
                try:
                    new_amount = int(input("Enter new amount: "))
                    resMsg = updateExpense(exp_id, new_amount)
                    print(resMsg)
                except ValueError:
                    print("Invalid amount.")
            elif update_type == "desc":
                new_desc = input("Enter new description: ")
                resMsg = updateExpense(exp_id, new_desc)
                print(resMsg)
            else:
                print("Invalid update type.")

        elif choice == "3":
            try:
                exp_id = int(input("Enter expense ID to delete: "))
                resMsg = deleteExpense(exp_id)
                print(resMsg)
            except ValueError:
                print("Invalid ID.")

        elif choice == "4":
            expenses = viewAllExpenses()
            for key, value in expenses.items():
                print(f"Expense {key}, description: {value['description']}, amount: {value['amount']}, created at: {value['date']}, category: {value['category']}")

        elif choice == "5":
            totalAmount = allExpensesSummary()
            print(f"Total Expenses: ${totalAmount}")

        elif choice == "6":
            try:
                month = int(input("Enter month number (1-12): "))
                totalAmount, month = monthExpensesSummary(month)
                print(f"Total Expenses for {month}: ${totalAmount}")
            except ValueError:
                print("Invalid month.")

        elif choice == "7":
            category = input("Enter category to filter: ")
            filtered_expenses = filterByCategory(category)
            for key, value in filtered_expenses.items():
                print(f"Expense {key}, description: {value['description']}, amount: {value['amount']}, created at: {value['date']}, category: {value['category']}")

        elif choice == "8":
            category = input("Enter category: ")
            totalAmount = summaryByCategory(category)
            print(f"Total Expenses for {category}: ${totalAmount}")  

        elif choice == "9":
            try:
                month = int(input("Enter month number (1-12): "))
                budget = int(input("Enter monthly budget: "))
                result = checkMonthlyBudget(budget, month)
                print(result)
            except ValueError:
                print("Invalid input.")

        elif choice == "10":
            exportToCSV()
            print("Expenses exported to expenses.csv successfully.")

        elif choice == "0":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
