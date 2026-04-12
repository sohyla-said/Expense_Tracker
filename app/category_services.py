from .models import Category
from .database import db
from sqlalchemy.exc import IntegrityError

def get_categories():
    categories = Category.query.all()

    return {
        "categories": [
            {
                "id": category.id,
                "name": category.name
            }
            for category in categories
        ]
    }, 200

def add_category(cat_name: str):
    if not cat_name or not cat_name.strip():
        return {"error": "Category name must not be empty"}, 400

    normalized_name = cat_name.strip()

    existing = Category.query.filter(db.func.lower(Category.name) == normalized_name.lower()).first()
    if existing:
        return {
            "message": "Category already exists",
            "category_id": existing.id,
            "category_name": existing.name
        }, 200

    category = Category(name=normalized_name)
    db.session.add(category)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return {"error": "Category already exists"}, 409

    return {
        "category_id": category.id,
        "category_name": category.name
    }, 201

def delete_category(id):
    category = Category.query.get(id)

    if not category:
        return {"error": f"Category with id {id} doesn't exist"}, 404
    db.session.delete(category)
    db.session.commit()

    return {"message": f"Category with id {id} deleted successfully"}, 200