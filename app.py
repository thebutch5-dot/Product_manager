from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'some_secret_key'

products = [
    {"name": "iPhone 15", "price": 40000, "category": "Смартфони"},
    {"name": "MacBook Air", "price": 55000, "category": "Ноутбуки"}
]


@app.route('/', methods=['GET', 'POST'])
def products_list():
    if request.method == 'POST':
        name = request.form.get('name')
        price = request.form.get('price')
        category = request.form.get('category')

        products.append({"name": name, "price": price, "category": category})
        flash('Товар додано!')
        return redirect(url_for('products_list'))

    return render_template('product.html', products=products)


@app.route('/edit/<name>', methods=['GET', 'POST'])
def edit_product(name):
    product = next((p for p in products if p['name'] == name), None)

    if not product:
        return "Товар не знайдено", 404

    if request.method == 'POST':
        product['price'] = request.form.get('price')
        product['category'] = request.form.get('category')

        flash('Товар оновлено!')
        return redirect(url_for('products_list'))

    return render_template('edit.html', product=product)


if __name__ == '__main__':
    app.run(debug=True)
