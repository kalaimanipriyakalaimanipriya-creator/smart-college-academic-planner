import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "academic_planner.db"
SCHEMA_PATH = Path(__file__).parent / "schema_v2.sql"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    with open(SCHEMA_PATH, "r") as f:
        cursor.executescript(f.read())

    conn.commit()
    conn.close()
    print("Database initialized successfully.")

if __name__ == "__main__":
    init_db()
