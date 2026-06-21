from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models.cart import get_user_cart, add_to_cart, update_cart_quantity, remove_from_cart

cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/cart')
@login_required
def cart():
    items = get_user_cart(current_user.id)
    products = []
    total = 0
    
    for item in items:
        product_id = item[2]
        quantity = item[3]
        name = item[6]
        price = float(item[7])
        image_url = item[8]
        
        subtotal = price * quantity
        total += subtotal
        products.append({
            'id': product_id,
            'name': name,
            'price': price,
            'image_url': image_url,
            'quantity': quantity,
            'subtotal': subtotal
        })
    
    return render_template('cart.html', products=products, total=total)

@cart_bp.route('/add_to_cart/<int:product_id>')
@login_required
def add_to_cart_route(product_id):
    quantity = request.args.get('quantity', 1, type=int)
    success, message = add_to_cart(current_user.id, product_id, quantity)
    flash(message, 'success' if success else 'danger')
    return redirect(url_for('products.index'))

@cart_bp.route('/update_cart/<int:product_id>', methods=['POST'])
@login_required
def update_cart_route(product_id):
    quantity = int(request.form['quantity'])
    update_cart_quantity(current_user.id, product_id, quantity)
    flash('Panier mis à jour', 'info')
    return redirect(url_for('cart.cart'))

@cart_bp.route('/remove_from_cart/<int:product_id>')
@login_required
def remove_from_cart_route(product_id):
    remove_from_cart(current_user.id, product_id)
    flash('Produit retiré du panier', 'info')
    return redirect(url_for('cart.cart'))
