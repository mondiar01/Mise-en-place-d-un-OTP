# src/database/database.py
import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('users.db')
        self.cursor = self.conn.cursor()
        # Supprimer la base de données existante pour éviter les conflits
        self.cursor.execute('DROP TABLE IF EXISTS users')
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                email TEXT NOT NULL,
                birth_date TEXT NOT NULL,
                address TEXT NOT NULL,
                postal_code TEXT NOT NULL,
                login_attempts INTEGER DEFAULT 0
            )
        ''')
        self.conn.commit()

    def add_user(self, username, password_hash, email, birth_date, address, postal_code):
        try:
            self.cursor.execute('''
                INSERT INTO users (username, password_hash, email, birth_date, address, postal_code)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (username, password_hash, email, birth_date, address, postal_code))
            self.conn.commit()
            return True, "Inscription réussie!"
        except sqlite3.IntegrityError:
            return False, "Nom d'utilisateur déjà utilisé"

    def get_user(self, username):
        user = self.cursor.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        if user:
            return {
                'id': user[0],
                'username': user[1],
                'password_hash': user[2],
                'email': user[3],
                'birth_date': user[4],
                'address': user[5],
                'postal_code': user[6],
                'login_attempts': user[7]
            }
        return None

    def update_login_attempts(self, username, reset=False):
        if reset:
            self.cursor.execute('UPDATE users SET login_attempts = 0 WHERE username = ?', (username,))
        else:
            self.cursor.execute('UPDATE users SET login_attempts = login_attempts + 1 WHERE username = ?', (username,))
        self.conn.commit()