import os
from flask import Flask, render_template, request, redirect, url_for
from models import db
from actions_db import get_all_products, get_product_by_id, update_product, init_db

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates'))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


with app.app_context():
    init_db()


@app.route('/')
def index():
    products = get_all_products()
    return render_template('product.html', products=products)


@app.route('/edit/<int:product_id>', methods=['GET', 'POST'])
def edit_product_route(product_id):
    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        price = request.form['price']
        description = request.form['description']

        update_product(product_id, name, category, price, description)
        return redirect(url_for('index'))

    product = get_product_by_id(product_id)
    return render_template('edit.html', product=product)


@app.route('/test-bootstrap')
def test_bootstrap():
    return render_template('product.html', products=[])


if __name__ == '__main__':
    app.run(debug=True, port=5001)









