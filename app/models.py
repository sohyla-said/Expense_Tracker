from .database import db
from datetime import datetime

class Category(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), unique = True, nullable = False)

class Expenses(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    description = db.Column(db.String(200))
    amount = db.Column(db.Float, nullable = False)
    date = db.Column(db.DateTime, default = datetime.utcnow)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category')

class Budget(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    month = db.Column(db.Integer)
    year = db.Column(db.Integer)
    amount = db.Column(db.Float)