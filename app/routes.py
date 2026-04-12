from flask import Blueprint, request, jsonify
from . import expenses_services as expense_services
from . import budget_services 
from . import category_services

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return 'Welcome to our Expense Tracker System'

############################# Expenses apis #############################
@main.route('/api/expenses/add', methods=['POST'])
def add_expense_route():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'JSON body required'}), 400
    
    description = data.get('description')
    amount = data.get('amount')
    category = data.get('category')

    if description is None or amount is None or category is None:
        return jsonify({"error": "description, amount, and category are required"}), 400
    try:
        amount = float(amount)
    except ValueError:
        return jsonify({"error": "amount must be a number"}), 400
    
    expense_id = expense_services.add_expense(description, amount, category)

    return jsonify({
        "message": "Expense added successfully",
        "id": expense_id
    }), 201


@main.route('/api/expenses/update/<int:id>', methods=['PUT'])
def update_expense_route(id):

    data = request.get_json()
    if not data:
        return jsonify({'error': 'JSON body required'}), 400
    
    result, status_code = expense_services.update_expense(id, data)
    
    return jsonify(result), status_code


@main.route('/api/expenses/delete/<int:id>', methods=['DELETE'])
def delete_expense_route(id):

    result, status_code = expense_services.delete_expense(id)
    return jsonify(result), status_code


@main.route('/api/expenses')
def get_current_month_expenses_route():
    result, status_code = expense_services.get_current_month_expenses()
    return jsonify(result), status_code

@main.route('/api/expenses/month')
def get_expenses_by_month_route():
    month = request.args.get("month")

    if not month:
        return jsonify({'error': "Month number must be present in Query parameter"}), 400
    
    try:
        month = int(month)
    except ValueError:
        return jsonify({"error": "month must be an integer between 1-12"}), 400
    
    result, status_code = expense_services.get_expenses_by_month(month)
    return jsonify(result), status_code

@main.route('/api/expenses/summary')
def get_current_month_summary_route():
    result, status_code = expense_services.get_current_month_summary()
    return jsonify(result), status_code

@main.route('/api/expenses/month/summary')
def get_month_summary_route():
    month = request.args.get("month")

    if not month:
        return jsonify({'error': "Month number must be present in Query parameter"}), 400
    try:
        month = int(month)
    except ValueError:
        return jsonify({"error": "month must be an integer between 1-12"}), 400
    
    result, status_code = expense_services.get_month_summary(month)
    return jsonify(result), status_code

@main.route('/api/expenses/category')
def filter_expenses_by_category_route():
    category = request.args.get("category")
    if not category:
        return jsonify({'error': "Category must be present in Query parameter"}), 400
    result, status_code = expense_services.filter_by_category(category)

    return jsonify(result), status_code

@main.route('/api/expenses/export')
def export_all_expenses_csv_route():
    result, status_code = expense_services.export_to_csv()
    return jsonify(result), status_code

@main.route('/api/expenses/month/export')
def export_month_expenses_route():
    month = request.args.get("month")
    if not month:
        return jsonify({'error': "Month must be present in Query parameter"}), 400

    try:
        month = int(month)
    except ValueError:
        return jsonify({"error": "month must be an integer between 1-12"}), 400

    result, status_code = expense_services.export_to_csv(month)
    return jsonify(result), status_code


############################# Budget apis #############################

@main.route('/api/budget/set', methods=['POST'])
def set_budget_route():
    month = request.args.get("month")
    budget = request.args.get("budget")

    if not month or not budget:
        return jsonify({'error': "Month and budget must be present in Query parameter"}), 400
    try:
        month = int(month)
        budget = int(budget)
    except ValueError:
        return jsonify({"error": "month and budget must be integers"}), 400
    
    result, status_code = budget_services.set_budget(month, budget)

    return jsonify(result), status_code

@main.route('/api/budget/check')
def check_budget_route():
    month = request.args.get("month")

    if not month:
        return jsonify({'error': "Month must be present in Query parameter"}), 400
    try:
        month = int(month)
    except ValueError:
        return jsonify({"error": "month must be integer"}), 400
    
    result, status_code = budget_services.check_budget(month)

    return jsonify(result), status_code

@main.route("/api/budget/month")
def get_month_budget_route():
    month = request.args.get("month")

    if not month:
        return jsonify({'error': "Month must be present in Query parameter"}), 400
    try:
        month = int(month)
    except ValueError:
        return jsonify({"error": "month must be integer"}), 400
    result, status_code = budget_services.get_month_budget(month)
    return jsonify(result), status_code


############################# Categories apis #############################
@main.route("/api/categories")
def get_categories_route():
    result, status_code = category_services.get_categories()
    return jsonify(result), status_code

@main.route("/api/categories/add", methods = ["POST"])
def add_category_route():
    payload = request.get_json(silent=True) or {}
    name = payload.get("name")
    if not name:
        return jsonify({"error": "Category name must be specified"}), 400
    result, status_code = category_services.add_category(name)

    return jsonify(result), status_code
