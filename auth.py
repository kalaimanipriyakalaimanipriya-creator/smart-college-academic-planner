from flask import render_template, request, redirect, session, url_for, flash
from db import query_db
from utils.security import verify_password

def auth_routes(app):

    # @app.route("/academic-planner/v1/login", methods=["GET", "POST"])
    # def login_v1():
    #     user = request.form["username"];
    #     pwd  = request.form["password"];
        
    #     if request.method == "POST":
    #         user = query_db(
    #             "SELECT role, password FROM users WHERE username=?",
    #             (request.form["username"],),
    #             one=True
    #         )

    #     if user and verify_password(user[1], request.form["password"]):
    #         session["username"] = request.form["username"]
    #         session["role"] = user[0]

    #         return redirect("/staff" if user[0] == "staff" else "/student")

    #     # ❌ login failed
    #     return render_template(
    #         "staff/staff_login.html",
    #         error="Invalid username or password"
    #     )

    #     # GET request
    #     return render_template("staff/staff_login.html")

    @app.route("/academic-planner/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            username = request.form["username"].lower()
            password = request.form["password"]

            # user = query_db(
            #     "SELECT role, password FROM users WHERE username=?",
            #     (username,),
            #     one=True
            # )
            
            user = query_db("SELECT * FROM staff WHERE username = ?", (username,), one=True)

            
            print("USER:", user)
            print("PASSWORD CHECK:", verify_password(user["password"], password))

            if user and verify_password(user["password"], password):
                session.clear()         
                print("SESSION l-50 LOGIN:", dict(session))
       
                session["username"] = username
                # session["role"] = user["role"]     # optional but good
                
                print("SESSION AFTER LOGIN:", dict(session))
                # return redirect("/staff" if user["role"] == "staff" else "/student")
                return redirect(url_for('staff_dashboard'))
            else:
                flash("Invalid username or password", "error")

        return render_template("staff/staff_login.html")
    
    @app.route("/logout")
    def logout():
        session.clear()
        return redirect(url_for("home"))
