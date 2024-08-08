# utils/database.py

import sqlite3
from contextlib import closing
from src.config import DB_NAME


def create_table():
    with closing(sqlite3.connect(DB_NAME)) as connection:
        with connection as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,                     
                    name TEXT NOT NULL,
                    age INTEGER NOT NULL
                )
            ''')

def add_user(name, age):
    with closing(sqlite3.connect(DB_NAME)) as connection:
        with connection as conn:
            conn.execute('''
                INSERT INTO users (name, age) VALUES (?, ?)
            ''', (name, age))

def get_users():
    with closing(sqlite3.connect(DB_NAME)) as connection:
        with connection as conn:
            return conn.execute('SELECT id, name, age FROM users').fetchall()

# Ensure the table is created when this module is imported
create_table()
