from flask import render_template, request, redirect, session, url_for, flash
from db import query_db
from utils.security import hash_password
import sqlite3

def staff_routes(app):

    # @app.route("/staff/register", methods=['GET', 'POST'])
    # def staff_register():
    #     return render_template("staff/staff_register.html")

    @app.route("/staff", methods=["GET", "POST"])
    def staff_dashboard():
        if session.get("role") != "staff":
            return redirect(url_for("login"))

        if request.method == "POST":
            query_db("""
                INSERT INTO subjects
                (department, semester, subject_name, subject_type, hours_per_week)
                VALUES (?,?,?,?,?)
            """, (
                request.form["department"],
                request.form["semester"],
                request.form["subject"],
                request.form["type"],
                request.form["hours"]
            ))

        return render_template("staff_dashboard.html")


    @app.route("/staff/register", methods=['GET', 'POST'])
    def staff_register():
        if request.method == 'POST':
            try:
                query_db("""
                    INSERT INTO staff
                    (name, email, username, password, department, designation)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    request.form['name'],
                    request.form['email'],
                    request.form['username'],
                    hash_password(request.form['password']),
                    request.form['department'],
                    request.form['designation']
                ))

                flash("Staff profile created successfully!", "success")
                return redirect(url_for('home'))

            except Exception as e:
                flash("Username already exists. Please choose different username.", "error")
                return redirect(url_for('create_staff'))

        return render_template("staff/staff_register.html")

    

    # @app.route("/staff/generate/timetable", methods=['GET', 'POST'])
    # def generate_timetable():
    #     # validate DB prior to generating the timetable
    #     # show timetable that were already generated
        
    #     try:
    #         rows = query_db ("""
    #             SELECT * FROM timetable
    #             WHERE semester = ?
    #             OR department = ?
    #             """, (
    #                 request.form['semester'],
    #                 request.form['department']
    #             ))
            
    #         if rows.__len__ == 0:
    #             flash("No timetable generated yet", "error")
    #         else:
    #             print("rows:", rows.count)
    #             print("rows: ---> ", rows)
            
    #     except Exception as e:
    #         flash("Error in.", "error")
    #         return redirect(url_for('home'))

        
    #     return render_template(
    #         "generate_timetable.html",
    #         rows
    #     )


# TODO: can be deleted at later point

    # def staff_register_old():
    #     if request.method == 'POST':
    #         name = request.form['name']
    #         email = request.form['email']
    #         username = request.form['username']
    #         # Password is never stored as plain text
    #         password = hash_password(request.form['password']) # convert hashed password 
    #         department = request.form['department']
    #         designation = request.form['designation']

    #         try:
    #             conn = sqlite3.connect('database.db')
    #             cur = conn.cursor()

    #             cur.execute("""
    #                 INSERT INTO staff
    #                 (name, email, username, password, department, designation)
    #                 VALUES (?, ?, ?, ?, ?, ?)
    #             """, (name, email, username, password, department, designation))

    #             conn.commit()
    #             conn.close()

    #             # ✅ SUCCESS
    #             flash("Staff profile created successfully!", "success")
    #             return redirect(url_for('home'))

    #         except sqlite3.IntegrityError:
    #             # ❌ DUPLICATE USERNAME
    #             flash("Username already exists. Please choose a different username.", "error")
    #             return redirect(url_for('create_staff'))

    #     # return render_template('staff_profile.html')
    #     return render_template("staff/staff_register.html")

    
    # @app.route("/timetable/grid")
    # def timetable_grid():
    #     rows = query_db("""
    #     SELECT day, period, subject_name
    #     FROM timetable
    #     WHERE department=? AND semester=?
    # """, ("BSc CS", 3))

    #     days = ["DAY-1", "DAY-2", "DAY-3", "DAY-4", "DAY-5"]
    #     periods = [1, 2, 3, 4, 5]

    #     # Empty grid
    #     grid = {day: {p: "" for p in periods} for day in days}

    #     # Fill grid
    #     for day, period, subject in rows:
    #         grid[day][period] = subject

    #     return render_template(
    #         "timetable_grid.html",
    #         grid=grid,
    #         periods=periods
    #     )