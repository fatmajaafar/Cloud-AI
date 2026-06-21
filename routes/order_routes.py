from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models.cart import get_user_cart
from models.order import get_user_orders
from services.order_service import process_checkout

order_bp = Blueprint('orders', __name__)

@order_bp.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    cart_items = get_user_cart(current_user.id)
    
    if not cart_items:
        flash('Votre panier est vide.', 'warning')
        return redirect(url_for('products.index'))
    
    if request.method == 'POST':
        shipping_address = request.form.get('shipping_address', 'Adresse non spécifiée')
        order_id, error = process_checkout(current_user.id, shipping_address)
        
        if error:
            flash(error, 'danger')
            return redirect(url_for('cart.cart'))
        
        flash('✅ Commande validée avec succès !', 'success')
        return redirect(url_for('orders.list'))
    
    products = []
    total = 0
    for item in cart_items:
        subtotal = float(item[6]) * item[3]
        total += subtotal
        products.append({
            'id': item[2],
            'name': item[5],
            'price': float(item[6]),
            'stock': item[7],
            'quantity': item[3],
            'subtotal': subtotal
        })
    
    return render_template('checkout.html', products=products, total=total)

@order_bp.route('/orders')
@login_required
def list():
    orders = get_user_orders(current_user.id)
    return render_template('orders.html', orders=orders)
