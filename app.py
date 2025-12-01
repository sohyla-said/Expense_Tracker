from flask import Flask, request, jsonify
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

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to our Expenses Tracking system!"

@app.route('/api/expenses/add', methods = ['POST'])
def add_expenses():
    # create a new expense, expected JSON object as input: {"description": "", "amount": , "category": ""}
    data = request.get_json()
    if not data:
        return jsonify({'error': 'JSON body required'}), 400
    description = data['description']
    amount = data['amount']
    category = data['category']

    if description is None or amount is None or category is None:
        return jsonify({"error": "description, amount, and category are required"}), 400
    try:
        amount = int(amount)
    except ValueError:
        return jsonify({"error": "amount must be integer"}), 400
    new_expense = Expenses(description, amount, category)
    new_expense_id = new_expense.addExpense()

    if not new_expense_id:
        return jsonify({"error": "Failed to create expense "}), 400

    return jsonify({
        "message": "Expense added successfully",
        "id": new_expense_id
    }), 201


@app.route("/api/expenses/update/<int:id>", methods = ['PUT'])
def update_expenses(id):
    # update an expense amout: {"amount": } or description: {"description": ""}
    data = request.get_json()
    if not data:
        return jsonify({'error': 'JSON body required'}), 400
    
    if 'amount' in data:
        try:
            new_value = int(data['amount'])
        except ValueError:
            return jsonify({"error": "amount must be integer"}), 400
        
    elif'description' in data:
        new_value = data['description']
    
    else:
        return jsonify({"error": "Provide either 'amount' or 'description'"}), 400
    
    result = updateExpense(id, new_value)

    if not result:
        return jsonify({'error': 'No result is returned'}), 400
    if result == "No expense with this id is found, try again with another id.":
        return jsonify({"error": result}), 400
    
    return jsonify({'message': result}), 200
    

@app.route('/api/expenses/delete/<int:id>', methods = ['DELETE'])
def delete_expenses(id):
    # deletes an expense with specific id
    result = deleteExpense(id)

    if not result:
        return jsonify({"'error": "No result is returned"}), 400
    
    if result == "No expense with this id is found, try again with another id.":
        return jsonify({"error": result}), 400
    
    return jsonify({'message': result}), 200


@app.route('/api/expenses')
def get_all_expenses():
    # list all expenses
    result = viewAllExpenses()

    if not result:
        return jsonify({"'error": "No result is returned"}), 400
    
    return jsonify({'expenses': result}), 200


@app.route('/api/expenses/summary')
def all_expenses_summary():
    # get all expenses summary
    result = allExpensesSummary()

    if not result:
        return jsonify({"'error": "No result is returned"}), 400
    
    return jsonify({'expenses': result}), 200

@app.route('/api/expenses/summary/month')
def get_month_summary():
    # Summary of a specific month. Query param: ?month=
    month = request.args.get("month")
    if not month:
        return jsonify({'error': "Month number must be present in Query parameter"}), 400
    try:
        month = int(month)
    except ValueError:
        return jsonify({"error": "month must be an integer between 1-12"}), 400

    result, month_str = monthExpensesSummary(month)
    return jsonify({'result': f"Expenses for month {month_str} -> {result}"}), 200

@app.route('/api/expenses/filter')
def filter_by_category():
    # filter by a specific category. Query param: ?category=
    category = request.args.get("category")
    if not category:
        return jsonify({'error': "Category must be present in Query parameter"}), 400

    expenses = filterByCategory(category)
    return jsonify({'result': expenses}), 200

@app.route('/api/expenses/summary/filter')
def get_summary_category():
    # summary of expenses filtered by a specific category. Query param: ?category=
    category = request.args.get("category")
    if not category:
        return jsonify({'error': "Category must be present in Query parameter"}), 400

    result = summaryByCategory(category)
    return jsonify({'result': result}), 200

@app.route('/api/expenses/check')
def check_monthly_budget():
    # check Summary of a specific month against a given budget. Query param: ?month=3&budget=3
    month = request.args.get("month")
    budget = request.args.get("budget")

    if not month or not budget:
        return jsonify({'error': "Month and budget must be present in Query parameter"}), 400
    
    try:
        month = int(month)
        budget = int(budget)
    except ValueError:
        return jsonify({"error": "month and budget must be integers"}), 400
    
    result = checkMonthlyBudget(budget, month)
    return jsonify({'result': result}), 200

@app.route('/api/expenses/export')
def export_to_csv():
    # export expenses to a csv file
    exportToCSV()
    return jsonify({"message": "Expenses exported to ./Data/expenses.csv"}), 200


if __name__ == '__main__':
    app.run()