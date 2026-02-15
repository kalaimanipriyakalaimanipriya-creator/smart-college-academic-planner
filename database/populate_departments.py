def populate_departments(cursor):
    departments = [
        ("BSc IT",),
        ("BCA",),
        ("BSc CS",)
    ]

    cursor.executemany(
        "INSERT OR IGNORE INTO departments (name) VALUES (?)",
        departments
    )
