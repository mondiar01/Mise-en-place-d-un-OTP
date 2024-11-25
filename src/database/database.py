# src/database/database.py
import sqlite3
from datetime import datetime

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('users.db')
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            birth_date TEXT NOT NULL,
            address TEXT NOT NULL,
            postal_code TEXT NOT NULL,
            otp_secret TEXT,
            failed_attempts INTEGER DEFAULT 0,
            last_attempt_time TEXT,
            created_at TEXT NOT NULL
        )
        ''')
        self.conn.commit()