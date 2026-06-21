from .db import get_db_connection

def get_all_products():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        SELECT p.id, p.name, p.description, p.price, p.stock, p.image_url,
               COALESCE(AVG(r.rating), 0) as avg_rating
        FROM products p
        LEFT JOIN reviews r ON p.id = r.product_id
        GROUP BY p.id
        ORDER BY p.id
    ''')
    products = cur.fetchall()
    cur.close()
    conn.close()
    return products

def get_product_by_id(product_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, name, description, price, stock, image_url, created_at FROM products WHERE id = %s', (product_id,))
    product = cur.fetchone()
    cur.close()
    conn.close()
    return product

def get_reviews_by_product(product_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        SELECT r.*, u.username
        FROM reviews r
        JOIN users u ON r.user_id = u.id
        WHERE r.product_id = %s
        ORDER BY r.created_at DESC
    ''', (product_id,))
    reviews = cur.fetchall()
    cur.close()
    conn.close()
    return reviews

def search_products(query, category_id=None):
    conn = get_db_connection()
    cur = conn.cursor()
    
    if query and category_id:
        cur.execute('''
            SELECT DISTINCT p.id, p.name, p.description, p.price, p.stock, p.image_url
            FROM products p
            LEFT JOIN product_categories pc ON p.id = pc.product_id
            WHERE p.name ILIKE %s AND pc.category_id = %s
        ''', (f'%{query}%', category_id))
    elif query:
        cur.execute('SELECT id, name, description, price, stock, image_url FROM products WHERE name ILIKE %s', (f'%{query}%',))
    elif category_id:
        cur.execute('''
            SELECT p.id, p.name, p.description, p.price, p.stock, p.image_url
            FROM products p
            JOIN product_categories pc ON p.id = pc.product_id
            WHERE pc.category_id = %s
        ''', (category_id,))
    else:
        cur.execute('SELECT id, name, description, price, stock, image_url FROM products')
    
    products = cur.fetchall()
    cur.close()
    conn.close()
    return products

def get_categories():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, name FROM categories')
    categories = cur.fetchall()
    cur.close()
    conn.close()
    return categories
