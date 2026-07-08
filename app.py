from flask import Flask, render_template, request, redirect, url_for
from actions_db import init_db, get_all_products, add_product, update_product, get_product_by_id, delete_product

app = Flask(__name__)

init_db()

@app.route('/')
def index():
    products = get_all_products()
    return render_template('product.html', products=products)

@app.route('/add', methods=['POST'])
def create():
    name = request.form.get('name')
    price = request.form.get('price')
    quantity = request.form.get('quantity')
    add_product(name, price, quantity)
    return redirect(url_for('index'))

@app.route('/edit/<int:product_id>', methods=['GET', 'POST'])
def edit(product_id):
    product = get_product_by_id(product_id)
    if not product:
        return "Product not found", 404
    if request.method == 'POST':
        name = request.form.get('name')
        price = request.form.get('price')
        quantity = request.form.get('quantity')
        update_product(product_id, name, price, quantity)
        return redirect(url_for('index'))
    return render_template('edit.html', product=product)

@app.route('/delete/<int:product_id>', methods=['POST'])
def remove(product_id):
    delete_product(product_id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)



