import sqlite3
from pathlib import Path

from populate_departments import populate_departments
from populate_staff import populate_staff
from populate_subjects import populate_subjects
from populate_timetable import populate_timetable

DB_PATH = Path(__file__).parent / "academic_planner.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

populate_departments(cursor)
populate_staff(cursor)
populate_subjects(cursor)
populate_timetable(cursor)

conn.commit()
conn.close()

print("All data populated successfully.")
