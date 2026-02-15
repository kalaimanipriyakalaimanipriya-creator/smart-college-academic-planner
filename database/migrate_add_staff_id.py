import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "academic_planner.db"


def column_exists(cursor, table, column):
    cursor.execute(f"PRAGMA table_info({table})")
    return column in [row[1] for row in cursor.fetchall()]


def migrate():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Add staff_id to subjects
    if not column_exists(cursor, "subjects", "staff_id"):
        cursor.execute("""
            ALTER TABLE subjects
            ADD COLUMN staff_id INTEGER
        """)
        print("Added staff_id to subjects table")
    else:
        print("staff_id already exists in subjects table")

    # Add staff_id to timetable if missing (safety check)
    if not column_exists(cursor, "timetable", "staff_id"):
        cursor.execute("""
            ALTER TABLE timetable
            ADD COLUMN staff_id INTEGER
        """)
        print("Added staff_id to timetable table")
    else:
        print("staff_id already exists in timetable table")

    conn.commit()
    conn.close()


if __name__ == "__main__":
    migrate()
