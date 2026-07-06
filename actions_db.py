import sqlite3

def get_db_connection():
    conn = sqlite3.connect('db.sqlite')
    conn.row_factory = sqlite3.Row
    return conn

def create_table():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            price REAL,
            category TEXT
        )
    ''')
    conn.commit()
    conn.close()

def get_all_products():
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM products').fetchall()
    conn.close()
    return products

def add_product(name, price, category):
    conn = get_db_connection()
    conn.execute('INSERT INTO products (name, price, category) VALUES (?, ?, ?)', (name, price, category))
    conn.commit()
    conn.close()

def get_product_by_name(name):
    conn = get_db_connection()
    product = conn.execute('SELECT * FROM products WHERE name = ?', (name,)).fetchone()
    conn.close()
    return product

def update_product_by_name(old_name, new_name, new_price, new_category):
    conn = get_db_connection()
    conn.execute('''
        UPDATE products 
        SET name = ?, price = ?, category = ? 
        WHERE name = ?
    ''', (new_name, new_price, new_category, old_name))
    conn.commit()
    conn.close()

def delete_product_by_name(name):
    conn = get_db_connection()
    conn.execute('DELETE FROM products WHERE name = ?', (name,))
    conn.commit()
    conn.close()

