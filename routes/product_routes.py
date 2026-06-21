from flask import Blueprint, render_template, request, flash, redirect, url_for
from models.product import get_all_products, get_product_by_id, get_reviews_by_product, search_products, get_categories

products_bp = Blueprint('products', __name__)

@products_bp.route('/')
def index():
    products = get_all_products()
    return render_template('index.html', products=products)

@products_bp.route('/search')
def search():
    query = request.args.get('q', '')
    category_id = request.args.get('category', '')
    
    products = search_products(query, category_id if category_id else None)
    categories = get_categories()
    
    return render_template('index.html', products=products, categories=categories,
                          selected_category=category_id, search_query=query)

@products_bp.route('/product/<int:product_id>')
def detail(product_id):
    product = get_product_by_id(product_id)
    if not product:
        flash('Produit introuvable.', 'danger')
        return redirect(url_for('products.index'))
    
    reviews = get_reviews_by_product(product_id)
    return render_template('product_detail.html', product=product, reviews=reviews)
