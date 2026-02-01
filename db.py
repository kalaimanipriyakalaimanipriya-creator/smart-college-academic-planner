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

import sqlite3
from flask import g

DATABASE = "database.db"

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

def query_db(query, args=(), one=False):
    db = get_db()
    cur = db.execute(query, args)
    db.commit()
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def init_db():
    db = get_db()
    with open("database/schema.sql") as f:
        db.executescript(f.read())
    db.close()