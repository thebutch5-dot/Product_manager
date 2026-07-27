import re
from models import db, Product, Company
from werkzeug.security import generate_password_hash


def validate_registration(name, password):
    if not name:
        return 'Логін не може бути порожнім'

    if len(password) < 6:
        return 'Пароль має бути не коротшим за 6 символів'

    if not re.search(r'[A-Za-z]', password):
        return 'Пароль має містити хоча б одну літеру'

    if not re.search(r'\d', password):
        return 'Пароль має містити хоча б одну цифру'

    if not re.search(r'[^A-Za-z0-9]', password):
        return 'Пароль має містити хоча б один спеціальний знак'

    return None


def product_exists(title):
    return Product.query.filter_by(name=title).first() is not None


def add_product(title, price, category, quantity=0):
    new_prod = Product(name=title, price=price, category=category, quantity=quantity)
    db.session.add(new_prod)
    db.session.commit()


def get_products():
    return Product.query.all()


def get_products_by_category(category):
    return Product.query.filter_by(category=category).all()


def get_categories():
    products = Product.query.all()
    return list(set([p.category for p in products if p.category]))


def get_company_by_name(name):
    return Company.query.filter_by(name=name).first()


def create_company(name, password):
    hash_pass = generate_password_hash(password)
    new_company = Company(name=name, password=hash_pass)
    db.session.add(new_company)
    db.session.commit()








