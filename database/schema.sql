CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    role TEXT
);

CREATE TABLE IF NOT EXISTS subjects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    department TEXT,
    semester INTEGER,
    subject_name TEXT,
    subject_type TEXT, -- theory / lab
    hours_per_week INTEGER,
    semester_id INTEGER
);

-- CREATE TABLE IF NOT EXISTS timetable (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     department TEXT,
--     semester INTEGER,
--     day TEXT,
--     period INTEGER,
--     subject_name TEXT
-- );
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
CREATE UNIQUE INDEX idx_unique_slot
ON timetable(department, semester, day, period);


CREATE TABLE IF NOT EXISTS staff (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    department TEXT,
    designation TEXT
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


