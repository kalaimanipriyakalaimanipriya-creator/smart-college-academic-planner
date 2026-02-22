# import sqlite3
# from utils.security import hash_password
# DB_NAME = "database.db"

# def get_db():
#     return sqlite3.connect(DB_NAME)

# def query_db(query, args=(), one=False):
#     db = get_db()
#     cur = db.cursor()
#     cur.execute(query, args)
#     result = cur.fetchone() if one else cur.fetchall()
#     db.commit()
#     db.close()
#     return result



# if not query_db("SELECT * FROM users", one=True):
#     query_db(
#         "INSERT INTO users VALUES (NULL,?,?,?)",
#         ("staff", hash_password("staff123"), "staff")
#     )
#     query_db(
#         "INSERT INTO users VALUES (NULL,?,?,?)",
#         ("student", hash_password("student123"), "student")
#     )

import os
import sqlite3
from flask import g

DATABASE = "database_test.db"

def get_db():
    print('get_db------------------------>>>')
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
        print (' debug statemnt ----->> ')
    print('prior to return get_db ----> ')
    return g.db

def query_db(query, args=(), one=False):
    print('query_db -------------------------->>> ')
    db = get_db()
    cur = db.execute(query, args)
    db.commit()
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def init_db():
    print('Checking/Initializing database...')
    db = get_db()
    
    # Check if a critical table (like 'users') exists
    # If it doesn't, run the schema script
    cursor = db.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
    if not cursor.fetchone():
        print("Table 'users' not found. Running schema.sql...")
        with open("database/schema.sql") as f:
            db.executescript(f.read())
        db.commit()
    else:
        print("Tables already exist. Skipping initialization.")

def init_db_initial():
    print('init db--------->>> ')
    db = get_db()
    with open("database/schema.sql") as f:
        db.executescript(f.read())
    db.close()