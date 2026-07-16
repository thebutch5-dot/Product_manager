from models import Product

def init_db():
    from app import db
    db.create_all()

def get_all_products():
    return Product.query.all()

def get_product_by_id(product_id):
    return Product.query.get_or_404(product_id)

def update_product(product_id, name, category, price, description):
    from app import db
    product = Product.query.get_or_404(product_id)
    product.name = name
    product.category = category
    product.price = price
    product.description = description
    db.session.commit()






