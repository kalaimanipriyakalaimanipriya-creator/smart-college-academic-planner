import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "academic_planner.db"

def map_staff():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    mappings = [
        # subject_name, department_name, staff_name
        ("Programming in C", "BSc IT", "Dr. Kumar"),
        ("C Lab", "BSc IT", "Dr. Kumar"),
        ("Data Structures", "BSc IT", "Ms. Priya"),
        ("Digital Computer Fundamentals", "BSc IT", "Ms. Priya"),
        ("English I", "BSc IT", "Ms. Priya"),
        ("Environmental Studies", "BSc IT", "Ms. Priya"),
    ]

    for subject, dept, staff in mappings:
        cursor.execute("""
            UPDATE subjects
            SET staff_id = (
                SELECT s.id
                FROM staff s
                JOIN departments d ON d.id = subjects.department_id
                WHERE s.name = ? AND d.name = ?
            )
            WHERE subject_name = ?
        """, (staff, dept, subject))

    conn.commit()
    conn.close()
    print("Staff mapped to subjects.")

if __name__ == "__main__":
    map_staff()
