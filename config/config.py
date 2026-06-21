import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'ma_cle_secrete_123')
    DATABASE_URL = os.environ.get(
        'DATABASE_URL',
        'postgresql://postgres:password@postgres-service:5432/ecommerce'
    )
    DEBUG = os.environ.get('DEBUG', 'False') == 'True'
