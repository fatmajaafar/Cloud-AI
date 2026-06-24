from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models.db import get_db_connection
from models.product import (
    get_all_products, get_product_by_id,
    create_product, update_product, delete_product
)

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required():
    if current_user.role != 'admin':
        flash('Accès réservé aux administrateurs.', 'danger')
        return False
    return True

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    if not admin_required():
        return redirect(url_for('products.index'))
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT COUNT(*) FROM users")
    users_count = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM products")
    products_count = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM orders")
    orders_count = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM orders WHERE status = 'En attente'")
    pending_orders = cur.fetchone()[0]
    
    cur.close()
    conn.close()
    
    return render_template('admin/dashboard.html',
                         users_count=users_count,
                         products_count=products_count,
                         orders_count=orders_count,
                         pending_orders=pending_orders)

@admin_bp.route('/products')
@login_required
def products():
    if not admin_required():
        return redirect(url_for('products.index'))
    
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM products ORDER BY id")
    products = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('admin/products.html', products=products)

@admin_bp.route('/orders')
@login_required
def orders():
    if not admin_required():
        return redirect(url_for('products.index'))
    
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        SELECT o.*, u.username
        FROM orders o
        JOIN users u ON o.user_id = u.id
        ORDER BY o.created_at DESC
    ''')
    orders = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('admin/orders.html', orders=orders)

@admin_bp.route('/update_order_status/<int:order_id>', methods=['POST'])
@login_required
def update_order_status(order_id):
    if not admin_required():
        return redirect(url_for('products.index'))
    
    status = request.form['status']
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("UPDATE orders SET status = %s, updated_at = CURRENT_TIMESTAMP WHERE id = %s", (status, order_id))
    conn.commit()
    cur.close()
    conn.close()
    
    flash('Statut de la commande mis à jour.', 'success')
    return redirect(url_for('admin.orders'))
# ── AJOUTER ──────────────────────────────────────────────────────────────────

@admin_bp.route('/products/add', methods=['GET', 'POST'])
@login_required
def add_product():
    if not admin_required():
        return redirect(url_for('products.index'))

    if request.method == 'POST':
        name        = request.form['name'].strip()
        description = request.form['description'].strip()
        price       = float(request.form['price'])
        stock       = int(request.form['stock'])
        image_url   = request.form.get('image_url', '').strip()

        if not name or price < 0 or stock < 0:
            flash('Données invalides.', 'danger')
        else:
            create_product(name, description, price, stock, image_url)
            flash('✅ Produit ajouté avec succès.', 'success')
            return redirect(url_for('admin.products'))

    return render_template('admin/product_form.html', product=None, action='add')

# ── MODIFIER ──────────────────────────────────────────────────────────────────

@admin_bp.route('/products/edit/<int:product_id>', methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
    if not admin_required():
        return redirect(url_for('products.index'))

    product = get_product_by_id(product_id)
    if not product:
        flash('Produit introuvable.', 'danger')
        return redirect(url_for('admin.products'))

    if request.method == 'POST':
        name        = request.form['name'].strip()
        description = request.form['description'].strip()
        price       = float(request.form['price'])
        stock       = int(request.form['stock'])
        image_url   = request.form.get('image_url', '').strip()

        update_product(product_id, name, description, price, stock, image_url)
        flash('✅ Produit mis à jour.', 'success')
        return redirect(url_for('admin.products'))

    return render_template('admin/product_form.html', product=product, action='edit')

# ── SUPPRIMER ─────────────────────────────────────────────────────────────────

@admin_bp.route('/products/delete/<int:product_id>', methods=['POST'])
@login_required
def delete_product_route(product_id):
    if not admin_required():
        return redirect(url_for('products.index'))
    delete_product(product_id)
    flash('🗑️ Produit supprimé.', 'info')
    return redirect(url_for('admin.products'))    
