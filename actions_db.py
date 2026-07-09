from peewee import SqliteDatabase, Model, CharField, DecimalField, IntegerField

db = SqliteDatabase('products.db')

class BaseModel(Model):
    class Meta:
        database = db

class Product(BaseModel):
    name = CharField(unique=True, max_length=100)
    price = DecimalField(max_digits=10, decimal_places=2)
    quantity = IntegerField(default=0)

def init_db():
    with db:
        db.create_tables([Product])

def add_product(name, price, quantity):
    try:
        return Product.create(name=name, price=price, quantity=quantity)
    except Exception:
        return None

def get_all_products():
    return list(Product.select())

def get_product_by_id(product_id):
    try:
        return Product.get_by_id(product_id)
    except Product.DoesNotExist:
        return None

def update_product(product_id, name=None, price=None, quantity=None):
    try:
        product = Product.get_by_id(product_id)
        if name is not None:
            product.name = name
        if price is not None:
            product.price = price
        if quantity is not None:
            product.quantity = quantity
        product.save()
        return product
    except Product.DoesNotExist:
        return None

# ЗМІНЕНО ТУТ: Видалення за НАЗВОЮ
def delete_product(product_name):
    try:
        query = Product.delete().where(Product.name == product_name)
        rows_deleted = query.execute()
        return rows_deleted > 0
    except Exception:
        return False

if __name__ == '__main__':
    init_db()


