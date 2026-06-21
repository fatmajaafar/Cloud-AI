from .db import get_db_connection

def create_order(user_id, total, shipping_address):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO orders (user_id, total, status, shipping_address)
        VALUES (%s, %s, 'En attente', %s) RETURNING id
    ''', (user_id, total, shipping_address))
    order_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return order_id

def add_order_item(order_id, product_id, quantity, price):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO order_items (order_id, product_id, quantity, price)
        VALUES (%s, %s, %s, %s)
    ''', (order_id, product_id, quantity, price))
    conn.commit()
    cur.close()
    conn.close()

def get_user_orders(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM orders WHERE user_id = %s ORDER BY created_at DESC', (user_id,))
    orders = cur.fetchall()
    cur.close()
    conn.close()
    
    orders_list = []
    for order in orders:
        items = get_order_items(order[0])
        orders_list.append({
            'id': order[0],
            'total': float(order[2]),
            'status': order[3],
            'shipping_address': order[4],
            'created_at': order[6],
            'items': items
        })
    
    return orders_list

def get_order_items(order_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        SELECT oi.*, p.name
        FROM order_items oi
        JOIN products p ON oi.product_id = p.id
        WHERE oi.order_id = %s
    ''', (order_id,))
    items = cur.fetchall()
    cur.close()
    conn.close()
    
    items_list = []
    for item in items:
        items_list.append({
            'name': item[5],
            'quantity': item[3],
            'price': float(item[4])
        })
    
    return items_list

def update_product_stock(product_id, quantity):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("UPDATE products SET stock = stock - %s WHERE id = %s", (quantity, product_id))
    conn.commit()
    cur.close()
    conn.close()
