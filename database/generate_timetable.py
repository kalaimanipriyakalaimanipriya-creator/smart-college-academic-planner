import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "academic_planner.db"

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
PERIODS_PER_DAY = 5


def is_staff_free(cursor, staff_id, day, period):
    cursor.execute("""
        SELECT 1 FROM timetable
        WHERE staff_id = ? AND day = ? AND period = ?
    """, (staff_id, day, period))
    return cursor.fetchone() is None


def generate_timetable(department_name, semester):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Get department id
    cursor.execute(
        "SELECT id FROM departments WHERE name = ?",
        (department_name,)
    )
    dept = cursor.fetchone()
    if not dept:
        raise ValueError("Department not found")

    department_id = dept[0]

    # Fetch subjects with staff mapping
    cursor.execute("""
        SELECT id, subject_type, hours_per_week, staff_id
        FROM subjects
        WHERE department_id = ? AND semester = ?
        ORDER BY subject_type
    """, (department_id, semester))

    subjects = cursor.fetchall()
    if not subjects:
        raise ValueError("No subjects found")

    theory = []
    labs = []

    for sid, stype, hours, staff_id in subjects:
        if stype == "lab":
            labs.append((sid, hours, staff_id))
        else:
            theory.extend([(sid, staff_id)] * hours)

    # Clear existing timetable
    cursor.execute("""
        DELETE FROM timetable
        WHERE department_id = ? AND semester = ?
    """, (department_id, semester))

    timetable = {}

    # 1️⃣ Place LABS with staff check
    for subject_id, lab_hours, staff_id in labs:
        placed = False

        for day in DAYS:
            for start in range(1, PERIODS_PER_DAY - lab_hours + 2):
                block_ok = True

                for p in range(start, start + lab_hours):
                    if (day, p) in timetable:
                        block_ok = False
                        break
                    if not is_staff_free(cursor, staff_id, day, p):
                        block_ok = False
                        break

                if block_ok:
                    for p in range(start, start + lab_hours):
                        timetable[(day, p)] = (subject_id, staff_id)
                    placed = True
                    break

            if placed:
                break

        if not placed:
            raise Exception("Unable to place lab due to staff clash")

    # 2️⃣ Place THEORY with staff check
    theory_index = 0

    for day in DAYS:
        for period in range(1, PERIODS_PER_DAY + 1):
            if theory_index >= len(theory):
                break

            if (day, period) in timetable:
                continue

            subject_id, staff_id = theory[theory_index]

            if is_staff_free(cursor, staff_id, day, period):
                timetable[(day, period)] = (subject_id, staff_id)
                theory_index += 1

        if theory_index >= len(theory):
            break

    # Insert timetable
    for (day, period), (subject_id, staff_id) in timetable.items():
        cursor.execute("""
            INSERT OR IGNORE INTO timetable
            (department_id, semester, day, period, subject_id, staff_id)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (department_id, semester, day, period, subject_id, staff_id))

    conn.commit()
    conn.close()

    print(f"Timetable generated with staff clash prevention for {department_name} - Sem {semester}")


if __name__ == "__main__":
    generate_timetable("BSc IT", 1)
