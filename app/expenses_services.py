import csv
import os

from .models import Budget, Expenses, Category
from .database import db
from datetime import datetime
from sqlalchemy import extract, func


def add_expense(description: str, amount: float, category_name: str):
    category = Category.query.filter_by(name = category_name).first()

    if not category:
        category = Category(name=category_name)
        db.session.add(category)

    expense = Expenses(
        description = description,
        amount = amount,
        category = category
    )

    db.session.add(expense)
    db.session.commit()

    return expense.id


def update_expense(id, updated_data):
    expense = Expenses.query.get(id)

    if not expense:
        return {"error": f"Expense with id {id} not found"}, 404
    
    if "description" in updated_data:
        if not updated_data['description']:
            return {"error": "description can't be empty"}, 400
        expense.description = updated_data['description']

    if 'amount' in updated_data:
        try:
            amount = float(updated_data['amount'])
            if amount <= 0:
                return {"error": "Amount must be greater than 0"}, 400
            expense.amount = amount

        except ValueError:
            return {"error": "Invalid amount"}, 400
        
    if 'category' in updated_data:
        category_name = updated_data['category']
        
        if not category_name:
            return {"error": "catgory name can't be empty"}, 400
            
        category = Category.query.filter_by(name = category_name).first()

        if not category:
            category = Category(name=category_name)
            db.session.add(category)

        expense.category = category
    
    db.session.commit()
    return {
        "message": "Expense updated successfully",
        "expense": {
            "id": expense.id,
            "description": expense.description,
            "amount": expense.amount,
            "category": expense.category.name
        }
    }, 200


def delete_expense(id):
    expense = Expenses.query.get(id)

    if not expense:
        return {"error": f"Expense with id {id} not found"}, 404
    
    db.session.delete(expense)
    db.session.commit()

    return {"message": f"Expense with id {id} deleted successfully"}, 200


def get_expenses_by_month(month):

    if month < 1 or month > 12:
        return {"error": "Month must be between 1 and 12"}, 400
    
    current_year = datetime.now().year

    expenses = Expenses.query.filter(
        extract('month', Expenses.date) == month,
        extract('year', Expenses.date) == current_year
    ).all()

    result = []
    total = 0
    for exp in expenses:
        result.append({
            "id": exp.id,
            "description": exp.description,
            "amount": exp.amount,
            "date": exp.date,
            "category": exp.category.name if exp.category else None
        })
        total += exp.amount
    
    return{
        "month": month,
        "year": current_year,
        "total": total,
        "count": len(result),
        "expenses": result
    }, 200


def get_current_month_expenses():
    current_month = datetime.now().month
    return get_expenses_by_month(current_month)


def get_month_summary(month):
    current_year = datetime.now().year

    total = db.session.query(func.sum(Expenses.amount)).filter(
        extract('month', Expenses.date) == month,
        extract('year', Expenses.date) == current_year
    ).scalar()

    return {
        "month": month,
        "total": total or 0
    }, 200


def get_current_month_summary():
    current_month = datetime.now().month
    return get_month_summary(current_month) 


def filter_by_category(cat_name):
    category = Category.query.filter_by(name=cat_name).first()
    if not category:
        return {"error": f"Category with name {cat_name} not found"}, 404
    
    expenses = Expenses.query.filter_by(category=category).all()

    result = []
    total = 0
    for exp in expenses:
        result.append({
            "id": exp.id,
            "description": exp.description,
            "amount": exp.amount,
            "date": exp.date,
            "category": exp.category.name if exp.category else None
        })
        total += exp.amount

    return {"total": total,
            "expenses": result
            }, 200



def export_to_csv(month = None):
    try:
        query = Expenses.query

        current_year = datetime.now().year

        if month:
            if month < 1 or month > 12:
                return {"error": "Month must be between 1 and 12"}, 400

            query = query.filter(
                extract('month', Expenses.date) == month,
                extract('year', Expenses.date) == current_year
            )

        expenses = query.all()

        if not expenses:
            return {"error": "No expenses found"}, 404

        os.makedirs("Data", exist_ok=True)

        if month:
            filename = f"Data/expenses_month_{month}_{current_year}.csv"
        else:
            month = datetime.now().month
            filename = f"Data/expenses_month_{month}_{current_year}.csv"

        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            fieldnames = ["id", "description", "amount", "date", "category"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            writer.writeheader()

            for exp in expenses:
                writer.writerow({
                    "id": exp.id,
                    "description": exp.description,
                    "amount": exp.amount,
                    "date": exp.date.strftime("%Y-%m-%d"),
                    "category": exp.category.name if exp.category else None
                })

        # 6️⃣ Return success response
        return {
            "message": "CSV exported successfully",
            "file": filename,
            "count": len(expenses)
        }, 200

    except Exception as e:
        return {
            "error": str(e)
        }, 500
    


