from .db import get_db_connection, get_db_connection_dict
from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, username, email, role='user'):
        self.id = id
        self.username = username
        self.email = email
        self.role = role

    @staticmethod
    def get_by_id(user_id):
        conn = get_db_connection_dict()
        cur = conn.cursor()
        cur.execute("SELECT id, username, email, role FROM users WHERE id = %s", (user_id,))
        user = cur.fetchone()
        cur.close()
        conn.close()
        if user:
            return User(user['id'], user['username'], user['email'], user['role'])
        return None

    @staticmethod
    def get_by_username(username):
        conn = get_db_connection_dict()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cur.fetchone()
        cur.close()
        conn.close()
        return user

    @staticmethod
    def create(username, email, password_hash):
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute(
                "INSERT INTO users (username, email, password, role) VALUES (%s, %s, %s, 'user')",
                (username, email, password_hash)
            )
            conn.commit()
            return True
        except:
            return False
        finally:
            cur.close()
            conn.close()
