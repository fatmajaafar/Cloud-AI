import psycopg2
from psycopg2.extras import RealDictCursor
from config.config import Config

def get_db_connection():
    return psycopg2.connect(Config.DATABASE_URL)

def get_db_connection_dict():
    return psycopg2.connect(Config.DATABASE_URL, cursor_factory=RealDictCursor)
