CREATE TABLE IF NOT EXISTS departments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('admin', 'staff'))
);

CREATE TABLE IF NOT EXISTS staff (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    department_id INTEGER,
    designation TEXT,
    FOREIGN KEY (department_id) REFERENCES departments(id)
);

CREATE TABLE IF NOT EXISTS subjects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    department_id INTEGER NOT NULL,
    semester INTEGER NOT NULL,
    subject_name TEXT NOT NULL,
    subject_type TEXT NOT NULL CHECK (subject_type IN ('theory', 'lab')),
    hours_per_week INTEGER NOT NULL,
    UNIQUE (department_id, semester, subject_name),
    FOREIGN KEY (department_id) REFERENCES departments(id)
);

CREATE TABLE IF NOT EXISTS timetable (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    department_id INTEGER NOT NULL,
    semester INTEGER NOT NULL,
    day TEXT NOT NULL,
    period INTEGER NOT NULL,
    subject_id INTEGER NOT NULL,
    staff_id INTEGER,
    UNIQUE (department_id, semester, day, period),
    FOREIGN KEY (department_id) REFERENCES departments(id),
    FOREIGN KEY (subject_id) REFERENCES subjects(id),
    FOREIGN KEY (staff_id) REFERENCES staff(id)
);
