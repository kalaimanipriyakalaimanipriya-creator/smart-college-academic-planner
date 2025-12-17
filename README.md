# Smart College Timetable Generator

A web-based application to automatically generate college timetables.  
The system is currently designed for **BSc Information Technology** and is **fully extendible** to support multiple departments and Engineering colleges in the future.

---

## 📌 Features

### Current Features (Phase 1)
- Role-based access: **Staff** and **Student**
- Department-based timetable (BSc IT)
- Semester-wise support (1 to 6)
- Automatic timetable generation
- Rule-based scheduling
- Timetable storage using SQLite
- Simple, clean UI
- Extendible architecture

### Planned Enhancements (Phase 2)
- Multiple departments (Arts & Science + Engineering)
- Staff availability constraints
- Clash detection
- Lab & room allocation
- Electives and credit-based system
- Export timetable to PDF / Excel
- Multi-college support

---

## 🏗️ Tech Stack

| Layer      | Technology |
|-----------|------------|
| Backend   | Python (Flask) |
| Frontend | HTML, CSS, JavaScript |
| Database | SQLite |
| Version Control | Git |

---

## 👥 User Roles

### Staff
- Login
- Add subjects
- Generate timetable
- View timetable

### Student
- View timetable by selecting department & semester



#### AI PROMPT

Act as a senior full-stack developer.

Build a Smart College Timetable Generator application with the following details:

Tech Stack

Backend: Python (Flask)

Frontend: HTML, CSS, JavaScript

Database: SQLite

Functional Requirements

User roles: Staff, Student

Department: BSc IT (extendible)

Semesters: 1 to 6

Staff can:

Login

Add subjects (theory/lab, hours per week)

Generate timetable

Students can:

Select department & semester

View timetable

Timetable Rules

Monday to Friday

5 periods per day

Subjects distributed based on weekly hours

No empty periods if possible

Output

Full project structure

app.py with Flask routes

SQLite database schema

HTML templates (login, dashboard, timetable view)

Separate CSS file

JavaScript for form handling

Comments in code

Additional Notes

Code should be clean, modular, and extendible for multiple departments and engineering colleges

Use SQLite initially but design should support migration

Generate the complete working application code.

If you want, next I can:

🔹 Convert this into SRS document

🔹 Give ER diagram

🔹 Provide final year project report format

🔹 Generate complete working code step-by-step
---

## 🗂️ Project Structure

