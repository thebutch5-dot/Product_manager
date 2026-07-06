from flask import Flask, render_template, request, redirect, url_for, flash
from actions_db import create_table, get_all_products, add_product, get_product_by_name, update_product_by_name, \
    delete_product_by_name

app = Flask(__name__)
app.secret_key = 'some_secret_key'

create_table()


@app.route('/', methods=['GET', 'POST'])
def products_list():
    if request.method == 'POST':
        name = request.form.get('name')
        price = request.form.get('price')
        category = request.form.get('category')
        add_product(name, price, category)
        flash('Товар додано!')
        return redirect(url_for('products_list'))

    products = get_all_products()
    return render_template('product.html', products=products)


@app.route('/edit/<name>', methods=['GET', 'POST'])
def edit_product(name):
    product = get_product_by_name(name)
    if not product:
        return "Товар не знайдено", 404

    if request.method == 'POST':
        new_name = request.form.get('name')
        new_price = request.form.get('price')
        new_category = request.form.get('category')
        update_product_by_name(name, new_name, new_price, new_category)
        flash('Товар оновлено!')
        return redirect(url_for('products_list'))

    return render_template('edit.html', product=product)


@app.route('/delete/<name>', methods=['POST'])
def delete_product(name):
    delete_product_by_name(name)
    flash('Товар видалено!')
    return redirect(url_for('products_list'))


if __name__ == '__main__':
    app.run(debug=True)


