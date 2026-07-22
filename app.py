import os
import re
from flask import Flask, render_template, request, flash, redirect, url_for, session
from models import db, Product, Company
from werkzeug.security import check_password_hash
import actions_db

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

app.secret_key = 'secret_key'

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# Підключаємо правильну базу даних проєкту
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(BASE_DIR, 'products.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
with app.app_context():
    db.create_all()

    # --- БЕЗПЕЧНИЙ АВТОПАТЧ БАЗИ ДАНИХ (ОНОВЛЕНИЙ) ---
    # Цей код автоматично додає відсутні колонки category та description, зберігаючи всі товари
    try:
        import sqlite3

        with sqlite3.connect(os.path.join(BASE_DIR, 'products.db')) as conn:
            # Спроба додати колонку category, якщо її немає
            try:
                conn.execute("ALTER TABLE product ADD COLUMN category TEXT;")
            except Exception:
                pass

            # Спроба додати колонку description, якщо її немає
            try:
                conn.execute("ALTER TABLE product ADD COLUMN description TEXT;")
            except Exception:
                pass
    except Exception:
        pass


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

        if actions_db.product_exists(title):
            flash(f'Product {title} already exists!')
        else:
            actions_db.add_product(title, price, category)
            flash(f'Product {title} was added!')

        return redirect(url_for('products'))

    all_categories = actions_db.get_categories()
    choose_category = request.args.get('category', 'all')

    if choose_category == 'all':
        filter_products = actions_db.get_products()
    else:
        filter_products = actions_db.get_products_by_category(choose_category)

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

        error = actions_db.validate_registration(name, password)
        if error:
            flash(error)
            return redirect(url_for('register'))

        existing_company = actions_db.get_company_by_name(name)
        if existing_company:
            flash(f'Company {name} already exists!')
            return redirect(url_for('register'))

        actions_db.create_company(name, password)
        flash(f'Company {name} was created!')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')

        company = actions_db.get_company_by_name(name)

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


@app.route('/edit/<name_product>', methods=['GET', 'POST'])
def edit(name_product):
    if not is_logged():
        return redirect(url_for('login'))

    prod = Product.query.filter_by(name=name_product).first_or_404()

    if request.method == 'POST':
        title = request.form.get('title')
        price = request.form.get('price')
        category = request.form.get('category')

        if not title or not price:
            flash('Title and Price cannot be empty!')
            return redirect(url_for('edit', name_product=name_product))

        prod.name = title
        prod.price = float(price)
        prod.category = category

        db.session.commit()
        flash(f'Product {name_product} was updated!')
        return redirect(url_for('products'))

    return render_template('edit.html', product=prod)


if __name__ == '__main__':
    app.run(debug=True)
