from flask import Flask, redirect, url_for, request
from flask_login import LoginManager, current_user
from flask_bcrypt import Bcrypt
from config.config import Config
from models.user import User

# ============================================
# Création de l'application
# ============================================
app = Flask(__name__)
app.config.from_object(Config)

# ============================================
# Initialisation des extensions
# ============================================
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)

# ============================================
# Protection des routes
# ============================================
@app.before_request
def require_login():
    public_routes = [
        'auth.login',
        'auth.register',
        'static'
    ]
    
    if request.endpoint in public_routes:
        return None
    
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    
    return None

# ============================================
# Enregistrement des Blueprints
# ============================================
from routes.auth_routes import auth_bp
from routes.product_routes import products_bp
from routes.cart_routes import cart_bp
from routes.order_routes import order_bp
from routes.admin_routes import admin_bp

app.register_blueprint(auth_bp)
app.register_blueprint(products_bp)
app.register_blueprint(cart_bp)
app.register_blueprint(order_bp)
app.register_blueprint(admin_bp)

# ============================================
# Lancement de l'application
# ============================================
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)