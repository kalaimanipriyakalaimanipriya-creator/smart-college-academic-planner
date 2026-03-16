-- CREATE TABLE IF NOT EXISTS users (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     username TEXT UNIQUE,
--     password TEXT,
--     role TEXT
-- );

CREATE TABLE IF NOT EXISTS student (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    regNo TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    department TEXT,
    image TEXT
);

CREATE TABLE IF NOT EXISTS subjects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    department TEXT,
    semester INTEGER,
    subject_name TEXT,
    subject_type TEXT, -- theory / lab
    hours_per_week INTEGER,
    semester_id INTEGER,
    UNIQUE (department, semester, subject_name)
);

CREATE TABLE IF NOT EXISTS timetable (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    department TEXT,
    semester INTEGER,
    day TEXT,
    period INTEGER,
    subject_id INTEGER,
    staff_id INTEGER,
    FOREIGN KEY (subject_id) REFERENCES subjects(id),
    FOREIGN KEY (staff_id) REFERENCES staff(id)
);
CREATE UNIQUE INDEX IF NOT EXISTS idx_unique_slot
ON timetable(department, semester, day, period);


CREATE TABLE IF NOT EXISTS staff (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    department TEXT,
    designation TEXT,
    image TEXT
);


CREATE TABLE IF NOT EXISTS semester (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    semester_no INTEGER NOT NULL, -- 1,2,3,4,5,6
    academic_year TEXT NOT NULL -- 2024-25
);

CREATE TABLE IF NOT EXISTS staff_subject_map (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    staff_id INTEGER NOT NULL,
    subject_id INTEGER NOT NULL,
    UNIQUE(staff_id, subject_id),
    FOREIGN KEY (staff_id) REFERENCES staff(id),
    FOREIGN KEY (subject_id) REFERENCES subjects(id)
);

CREATE TABLE IF NOT EXISTS college_overview (
    id INTEGER PRIMARY KEY,
    total_student INTEGER DEFAULT 0,
    total_staff INTEGER DEFAULT 0,
    total_department INTEGER DEFAULT 0,
    total_course INTEGER DEFAULT 0,
    total_placement INTEGER DEFAULT 0
);

INSERT OR IGNORE INTO college_overview
(id, total_student, total_staff, total_department, total_course, total_placement)
VALUES (1, 0, 0, 0, 0, 0);

CREATE TABLE IF NOT EXISTS admin (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
);

INSERT OR IGNORE INTO admin (id, name, username, password)
VALUES (1, 'Administrator', 'admin', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9');