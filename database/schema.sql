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
    hours_per_week INTEGER
);

CREATE TABLE IF NOT EXISTS timetable (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    department TEXT,
    semester INTEGER,
    day TEXT,
    period INTEGER,
    subject_name TEXT
);
