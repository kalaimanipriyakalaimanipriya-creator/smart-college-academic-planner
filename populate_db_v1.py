import sqlite3

def populate_subjects_strict():
    subjects = [

        # ================= BSc IT =================
        # Sem 1
        ('BSc IT', 1, 'Elective Paper I', 'theory', 5),
        ('BSc IT', 1, 'Programming in C', 'theory', 5),
        ('BSc IT', 1, 'Digital Logic', 'theory', 5),
        ('BSc IT', 1, 'Mathematics I', 'theory', 5),
        ('BSc IT', 1, 'English I', 'theory', 5),
        ('BSc IT', 1, 'Programming Lab', 'lab', 4),

        # Sem 2
        ('BSc IT', 2, 'Elective Paper II', 'theory', 5),
        ('BSc IT', 2, 'Data Structures', 'theory', 5),
        ('BSc IT', 2, 'Object Oriented Concepts', 'theory', 5),
        ('BSc IT', 2, 'Mathematics II', 'theory', 5),
        ('BSc IT', 2, 'English II', 'theory', 5),
        ('BSc IT', 2, 'DS & OOPS Lab', 'lab', 4),

        # Sem 3
        ('BSc IT', 3, 'Elective Paper III', 'theory', 5),
        ('BSc IT', 3, 'Java Programming', 'theory', 5),
        ('BSc IT', 3, 'Operating Systems', 'theory', 5),
        ('BSc IT', 3, 'Database Management Systems', 'theory', 5),
        ('BSc IT', 3, 'Software Engineering', 'theory', 5),
        ('BSc IT', 3, 'Java & DBMS Lab', 'lab', 4),

        # Sem 4
        ('BSc IT', 4, 'Elective Paper IV', 'theory', 5),
        ('BSc IT', 4, 'Web Technologies', 'theory', 5),
        ('BSc IT', 4, 'Computer Networks', 'theory', 5),
        ('BSc IT', 4, 'Mobile Computing', 'theory', 5),
        ('BSc IT', 4, 'Design & Analysis of Algorithms', 'theory', 5),
        ('BSc IT', 4, 'Web & Networks Lab', 'lab', 4),

        # Sem 5
        ('BSc IT', 5, 'Elective Paper V', 'theory', 5),
        ('BSc IT', 5, 'Python Programming', 'theory', 5),
        ('BSc IT', 5, 'Cloud Computing', 'theory', 5),
        ('BSc IT', 5, 'Data Mining', 'theory', 5),
        ('BSc IT', 5, 'Information Security', 'theory', 5),
        ('BSc IT', 5, 'Python & Cloud Lab', 'lab', 4),

        # Sem 6
        ('BSc IT', 6, 'Elective Paper VI', 'theory', 5),
        ('BSc IT', 6, 'Artificial Intelligence', 'theory', 5),
        ('BSc IT', 6, 'Machine Learning', 'theory', 5),
        ('BSc IT', 6, 'Internet of Things', 'theory', 5),
        ('BSc IT', 6, 'Big Data Analytics', 'theory', 5),
        ('BSc IT', 6, 'Major Project', 'lab', 10),

        # ================= BCA =================
        # Sem 1
        ('BCA', 1, 'Elective Paper I', 'theory', 5),
        ('BCA', 1, 'Programming in C', 'theory', 5),
        ('BCA', 1, 'Foundation Mathematics', 'theory', 5),
        ('BCA', 1, 'Computer Fundamentals', 'theory', 5),
        ('BCA', 1, 'English I', 'theory', 5),
        ('BCA', 1, 'C Programming Lab', 'lab', 4),

        # Sem 2
        ('BCA', 2, 'Elective Paper II', 'theory', 5),
        ('BCA', 2, 'C++ Programming', 'theory', 5),
        ('BCA', 2, 'Financial Accounting', 'theory', 5),
        ('BCA', 2, 'Discrete Mathematics', 'theory', 5),
        ('BCA', 2, 'English II', 'theory', 5),
        ('BCA', 2, 'C++ Programming Lab', 'lab', 4),

        # Sem 3
        ('BCA', 3, 'Elective Paper III', 'theory', 5),
        ('BCA', 3, 'Java Programming', 'theory', 5),
        ('BCA', 3, 'Data Structures', 'theory', 5),
        ('BCA', 3, 'Computer Organization', 'theory', 5),
        ('BCA', 3, 'Statistics', 'theory', 5),
        ('BCA', 3, 'Java & DS Lab', 'lab', 4),

        # Sem 4
        ('BCA', 4, 'Elective Paper IV', 'theory', 5),
        ('BCA', 4, 'RDBMS', 'theory', 5),
        ('BCA', 4, 'Software Testing', 'theory', 5),
        ('BCA', 4, 'Visual Programming', 'theory', 5),
        ('BCA', 4, 'Web Design', 'theory', 5),
        ('BCA', 4, 'RDBMS & Web Lab', 'lab', 4),

        # Sem 5
        ('BCA', 5, 'Elective Paper V', 'theory', 5),
        ('BCA', 5, 'PHP & MySQL', 'theory', 5),
        ('BCA', 5, 'Android Programming', 'theory', 5),
        ('BCA', 5, 'Multimedia Systems', 'theory', 5),
        ('BCA', 5, 'Animation Techniques', 'theory', 5),
        ('BCA', 5, 'PHP & Android Lab', 'lab', 4),

        # Sem 6
        ('BCA', 6, 'Elective Paper VI', 'theory', 5),
        ('BCA', 6, 'Cyber Law', 'theory', 5),
        ('BCA', 6, 'E-Commerce', 'theory', 5),
        ('BCA', 6, 'Management Information Systems', 'theory', 5),
        ('BCA', 6, 'Entrepreneurship', 'theory', 5),
        ('BCA', 6, 'Final Project', 'lab', 10),

        # ================= BSc CS =================
        # Sem 1
        ('BSc CS', 1, 'Elective Paper I', 'theory', 5),
        ('BSc CS', 1, 'Digital Logic', 'theory', 5),
        ('BSc CS', 1, 'Programming in C', 'theory', 5),
        ('BSc CS', 1, 'Statistics I', 'theory', 5),
        ('BSc CS', 1, 'English I', 'theory', 5),
        ('BSc CS', 1, 'C Programming Lab', 'lab', 4),

        # Sem 2
        ('BSc CS', 2, 'Elective Paper II', 'theory', 5),
        ('BSc CS', 2, 'Data Structures', 'theory', 5),
        ('BSc CS', 2, 'Discrete Mathematics', 'theory', 5),
        ('BSc CS', 2, 'Computer Architecture', 'theory', 5),
        ('BSc CS', 2, 'English II', 'theory', 5),
        ('BSc CS', 2, 'DS Lab', 'lab', 4),

        # Sem 3
        ('BSc CS', 3, 'Elective Paper III', 'theory', 5),
        ('BSc CS', 3, 'Java Programming', 'theory', 5),
        ('BSc CS', 3, 'Microprocessor', 'theory', 5),
        ('BSc CS', 3, 'Operating Systems', 'theory', 5),
        ('BSc CS', 3, 'Numerical Methods', 'theory', 5),
        ('BSc CS', 3, 'Java Lab', 'lab', 4),

        # Sem 4
        ('BSc CS', 4, 'Elective Paper IV', 'theory', 5),
        ('BSc CS', 4, 'Relational Databases', 'theory', 5),
        ('BSc CS', 4, 'Algorithms', 'theory', 5),
        ('BSc CS', 4, 'Computer Graphics', 'theory', 5),
        ('BSc CS', 4, 'Linux Administration', 'theory', 5),
        ('BSc CS', 4, 'RDBMS Lab', 'lab', 4),

        # Sem 5
        ('BSc CS', 5, 'Elective Paper V', 'theory', 5),
        ('BSc CS', 5, 'Compiler Design', 'theory', 5),
        ('BSc CS', 5, 'Software Engineering', 'theory', 5),
        ('BSc CS', 5, 'Computer Networks', 'theory', 5),
        ('BSc CS', 5, 'Data Science', 'theory', 5),
        ('BSc CS', 5, 'Networks Lab', 'lab', 4),

        # Sem 6
        ('BSc CS', 6, 'Elective Paper VI', 'theory', 5),
        ('BSc CS', 6, 'Network Security', 'theory', 5),
        ('BSc CS', 6, 'Theory of Computation', 'theory', 5),
        ('BSc CS', 6, 'Mobile Application Development', 'theory', 5),
        ('BSc CS', 6, 'Open Source Technologies', 'theory', 5),
        ('BSc CS', 6, 'Major Project', 'lab', 10),
    ]

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM subjects")

    cursor.executemany("""
        INSERT INTO subjects
        (department, semester, subject_name, subject_type, hours_per_week)
        VALUES (?, ?, ?, ?, ?)
    """, subjects)

    conn.commit()
    conn.close()

    print(f"Inserted {len(subjects)} subjects under STRICT rule.")

if __name__ == "__main__":
    populate_subjects_strict()
