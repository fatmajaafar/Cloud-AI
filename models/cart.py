from .db import get_db_connection

def get_user_cart(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        SELECT c.*, p.name, p.price, p.image_url
        FROM cart c
        JOIN products p ON c.product_id = p.id
        WHERE c.user_id = %s
    ''', (user_id,))
    items = cur.fetchall()
    cur.close()
    conn.close()
    return items

def add_to_cart(user_id, product_id, quantity=1):
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT stock FROM products WHERE id = %s", (product_id,))
    stock = cur.fetchone()
    if not stock or stock[0] < quantity:
        cur.close()
        conn.close()
        return False, "Stock insuffisant"
    
    cur.execute('''
        INSERT INTO cart (user_id, product_id, quantity)
        VALUES (%s, %s, %s)
        ON CONFLICT (user_id, product_id)
        DO UPDATE SET quantity = cart.quantity + %s, updated_at = CURRENT_TIMESTAMP
    ''', (user_id, product_id, quantity, quantity))
    
    conn.commit()
    cur.close()
    conn.close()
    return True, "Produit ajouté"

def update_cart_quantity(user_id, product_id, quantity):
    conn = get_db_connection()
    cur = conn.cursor()
    
    if quantity <= 0:
        cur.execute("DELETE FROM cart WHERE user_id = %s AND product_id = %s", (user_id, product_id))
    else:
        cur.execute('''
            UPDATE cart SET quantity = %s, updated_at = CURRENT_TIMESTAMP
            WHERE user_id = %s AND product_id = %s
        ''', (quantity, user_id, product_id))
    
    conn.commit()
    cur.close()
    conn.close()

def remove_from_cart(user_id, product_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM cart WHERE user_id = %s AND product_id = %s", (user_id, product_id))
    conn.commit()
    cur.close()
    conn.close()

def clear_cart(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM cart WHERE user_id = %s", (user_id,))
    conn.commit()
    cur.close()
    conn.close()
