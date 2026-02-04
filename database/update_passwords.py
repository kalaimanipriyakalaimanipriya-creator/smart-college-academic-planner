import sqlite3
from utils.security import hash_password

conn = sqlite3.connect("database.db")
cur = conn.cursor()

# Fetch all users
cur.execute("SELECT id, password FROM users")
users = cur.fetchall()

for user_id, plain_password in users:
    # already hashed ah irundha skip panna venum
    if len(plain_password) == 64:   # SHA-256 hash length
        continue

    hashed = hash_password(plain_password)

    cur.execute(
        "UPDATE users SET password=? WHERE id=?",
        (hashed, user_id)
    )

conn.commit()
conn.close()

print("✅ Existing passwords updated to hashed format")
