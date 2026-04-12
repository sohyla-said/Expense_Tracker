from .models import Budget, Expenses
from .database import db
from datetime import datetime
from sqlalchemy import extract, func


def set_budget(month, budget):
    year = datetime.now().year

    existing = Budget.query.filter_by(month=month, year=year).first()

    if existing:
        existing.amount = budget

    else:
        new_budget = Budget(
            month = month,
            year = year,
            amount = budget
        )
        db.session.add(new_budget)
    
    db.session.commit()
    return {"message": "Budget Saved sucessfully"}, 200


def check_budget(month):
    year = datetime.now().year

    budget = Budget.query.filter_by(month=month, year=year).first()

    if not budget:
        return {"error": "No budget set for this month"}, 404
    
    total = db.session.query(func.sum(Expenses.amount)).filter(
        extract('month', Expenses.date) == month,
        extract('year', Expenses.date) == year
    ).scalar() or 0

    if total > budget.amount:
        status = "exceeded"
    elif total == budget.amount:
        status = "exact"
    else:
        status = "within"

    return {
        "month": month,
        "budget": budget.amount,
        "spent": total,
        "status": status
    }, 200

def get_month_budget(month):
    current_year = datetime.now().year

    if month < 1 or month > 12:
        return {"error": "Month must be between 1 and 12"}, 400
    
    budget = Budget.query.filter_by(month = month, year = current_year).first()
    
    if not budget:
        return {"error": "No budget set for this month"}, 404
    return {
        "month": budget.month,
        "year": budget.year,
        "amount": budget.amount
    }, 200