from models.cart import get_user_cart, clear_cart
from models.order import create_order, add_order_item, update_product_stock

def process_checkout(user_id, shipping_address):
    cart_items = get_user_cart(user_id)
    
    if not cart_items:
        return None, "Votre panier est vide"
    
    total = 0
    items = []
    
    for item in cart_items:
        product_id = item[2]
        quantity = item[3]
        price = float(item[6])
        stock = item[7]
        
        if stock < quantity:
            return None, f"Stock insuffisant pour {item[5]}"
        
        subtotal = price * quantity
        total += subtotal
        items.append((product_id, quantity, price))
    
    order_id = create_order(user_id, total, shipping_address)
    
    for product_id, quantity, price in items:
        add_order_item(order_id, product_id, quantity, price)
        update_product_stock(product_id, quantity)
    
    clear_cart(user_id)
    
    return order_id, None
