import re
import os
from flask import Flask, render_template, request, flash, redirect, url_for, session
from models import db, Product, Company
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'secret_key'

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(BASE_DIR, 'db.sqlite')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
with app.app_context():
    db.create_all()


# Временные функции-заглушки, чтобы проект запускался без actions_db
def product_exists(title):
    return Product.query.filter_by(name=title).first() is not None


def add_product(title, price, category):
    new_prod = Product(name=title, price=price, category=category)
    db.session.add(new_prod)
    db.session.commit()


def get_products():
    return Product.query.all()


def get_products_by_category(category):
    return Product.query.filter_by(category=category).all()


def get_categories():
    products = Product.query.all()
    return list(set([p.category for p in products if p.category]))


def is_logged():
    return 'company' in session


@app.route('/', methods=['GET', 'POST'])
@app.route('/products', methods=['GET', 'POST'])
def products():
    session.permanent = True

    if not is_logged():
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form.get('title')
        price = request.form.get('price')
        category = request.form.get('category')

        if not title or not price:
            flash('Title and Price cannot be empty!')
            return redirect(url_for('products'))

        price = float(price)

        if product_exists(title):
            flash(f'Product {title} already exists!')
        else:
            add_product(title, price, category)
            flash(f'Product {title} was added!')

        return redirect(url_for('products'))

    all_categories = get_categories()
    choose_category = request.args.get('category', 'all')

    if choose_category == 'all':
        filter_products = get_products()
    else:
        filter_products = get_products_by_category(choose_category)

    return render_template('product.html',
                           products=filter_products,
                           categories=all_categories,
                           choose_category=choose_category)


@app.route('/delete/<name_product>')
def delete(name_product):
    prod = Product.query.filter_by(name=name_product).first()
    if prod:
        db.session.delete(prod)
        db.session.commit()
    flash(f'Product {name_product} was deleted!')
    return redirect(url_for('products'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        password = request.form.get('password', '')

        if not name:
            flash('Логін не може бути порожнім')
            return redirect(url_for('register'))

        if len(password) < 6:
            flash('Пароль має бути не коротшим за 6 символів')
            return redirect(url_for('register'))

        if not re.search(r'[A-Za-z]', password):
            flash('Пароль має містити хоча б одну літеру')
            return redirect(url_for('register'))

        if not re.search(r'\d', password):
            flash('Пароль має містити хоча б одну цифру')
            return redirect(url_for('register'))

        if not re.search(r'[^A-Za-z0-9]', password):
            flash('Пароль має містити хоча б один спеціальний знак')
            return redirect(url_for('register'))

        existing_company = Company.query.filter_by(name=name).first()
        if existing_company:
            flash(f'Company {name} already exists!')
            return redirect(url_for('register'))
        else:
            hash_pass = generate_password_hash(password)
            new_company = Company(name=name, password=hash_pass)
            db.session.add(new_company)
            db.session.commit()

            flash(f'Company {name} was created!')
            return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')

        company = Company.query.filter_by(name=name).first()

        if not company:
            flash(f'Company {name} does not exist!')
            return redirect(url_for('login'))

        if not check_password_hash(company.password, password):
            flash(f'Password incorrect!')
            return redirect(url_for('login'))

        session['company'] = company.name
        flash(f'Welcome {name}!')
        return redirect(url_for('products'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('company', None)
    flash('Ви вийшли з системи')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)











