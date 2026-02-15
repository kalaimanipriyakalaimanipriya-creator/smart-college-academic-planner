import sqlite3

def populate_departments():

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    
     # 1️⃣ Create table if it does not exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS departments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE
    )
    """)
    
    # 2️⃣ Sample department data
    departments = [
        ("BSc IT",),
        ("BCA",),
        ("BSc CS",)
    ]
    
    
    # todo a Clean insert (safe to re-run)
    # cursor.execute("DELETE FROM departments")
    
    # 3️⃣ Insert only if department does not exist
    cursor.executemany(
        "INSERT OR IGNORE INTO departments (name) VALUES (?)",
        departments
    )
    

    conn.commit()
    conn.close()

    print("Departments inserted successfully.")

if __name__ == "__main__":
    populate_departments()
