import psycopg2
from psycopg2.extras import RealDictCursor
from config.config import Config

def get_db_connection():
    return psycopg2.connect(Config.DATABASE_URL)

def get_db_connection_dict():
    return psycopg2.connect(Config.DATABASE_URL, cursor_factory=RealDictCursor)
# Deux types de connexions :

# get_db_connection() → retourne des tuples (valeur1, valeur2, ...) → on accède par index row[0]
# get_db_connection_dict() → retourne des dictionnaires {'id': 1, 'name': '...'} → on accède par nom row['id']