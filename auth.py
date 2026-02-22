from flask import render_template, request, redirect, session, url_for, flash, jsonify
from db import query_db
from utils.security import hash_password, verify_password
# import hash_password, verify_password from utils/security

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
    
    @app.route("/login", methods=["GET", "POST"])
    def login():
        data = request.get_json()
        password = data.get("password")
        userType = data.get("userType")

        sqlResult = None
        if userType == 'staff':
            # Ensure your frontend sends 'userName' for staff
            print('I am here at staff')
            userName = data.get("userName")
            sqlResult = query_db("SELECT * FROM staff WHERE username = ?", (userName,), one=True)
        else:
            # Ensure your frontend sends 'regNo' for students
            print('I am here at student')
            regNo = data.get("regNo")
            sqlResult = query_db("SELECT * FROM student WHERE regNo = ?", (regNo,), one=True)

        print(f"Query Result: {sqlResult}")

        if sqlResult:
            print("USER:", dict(sqlResult))
        else:
            print("USER: No user found in database.")

        # Validate user and password
        if sqlResult and verify_password(sqlResult["password"], password):
            user_dict = dict(sqlResult)
            
            session.clear()
            session["user_id"] = user_dict.get("id")
            # Store common identifier
            session["userName"] = user_dict.get("username") or user_dict.get("regNo")
            session["userType"] = userType # Essential for access control

            # Dynamic Redirect based on userType
            redirect_url = url_for('staff_dashboard') if userType == 'staff' else url_for('student_dashboard')
            
            return jsonify({
                "success": True,
                "redirect": redirect_url
            })
        
        # Fail case
        return jsonify({
            "success": False, 
            "message": "Invalid username or password"
        }), 401 # Return 401 Unauthorized


    @app.route("/register", methods=["GET", "POST"])
    def register():
        data = request.get_json(silent=True)
        if not data:
            return jsonify(success=False, message="Invalid JSON data received"), 400

        result = {}

        fullName    = data.get("fullName")
        
        print('password ', data.get('password'))
        password    = hash_password(data.get('password'))
        
        print('password after hashing: ', password)
          
        email       = data.get("email")
        
        department  = data.get("department")
        username    = data.get("userName")
        designation = data.get("designation")
        userType    = data.get("userType")
        
        print(userType)
        # Check for duplicate email or username
        existing_user = query_db(
            "SELECT id FROM staff WHERE email = ? OR username = ?",
            (email, username),
            one=True
        )

        if existing_user:
            # flash("Email or Username already exists. Please use a different one.", "error")
            # return redirect(url_for('staff_register'))
            # Instead of flash/redirect, return JSON error to the AJAX call
            return jsonify(success=False, message="Email or Username already exists.")


        try:

# check the usertype as staff or student and insert the table appropriately
            if userType == 'staff':
                query_db("""
                INSERT INTO staff
                (name, email, username, password, department, designation)
                VALUES (?, ?, ?, ?, ?, ?)
                """, (fullName, email, username, password, department, designation))
            else:
                query_db("""
                INSERT INTO student
                (name, email, username, password, department, regNo)
                VALUES (?, ?, ?, ?, ?, ?)
                """, (fullName, email, username, password, department, userType))

            # # print('prior to insert users table...................')
            # query_db("""
            #     INSERT INTO users
            #     (username, password, role)
            #     VALUES (?, ?, ?)
            # """, (username, password, userData.userType))
            # # print('inserted users table...................')

            # # print('prior to insert staff table...................')
            # query_db("""
            #     INSERT INTO staff
            #     (name, email, username, password, department, designation)
            #     VALUES (?, ?, ?, ?, ?, ?)
            # """, (fullName, email, username, password, department, designation))
            # # print('inserted staff table...................')

            
            return jsonify(success=True, redirect=url_for('home'))

        except Exception as e:
            print(f"Error: {e}")
            return jsonify(success=False, message="An internal error occurred."), 500

    # @app.route("/academic-planner/login", methods=["GET", "POST"])
    @app.route("/login123", methods=["GET", "POST"])
    def login123():
        if request.method == "POST":
            data = request.get_json()
            
            username = data.get('userName').lower()
            password = data.get("password")

            # user = query_db(
            #     "SELECT role, password FROM users WHERE username=?",
            #     (username,),
            #     one=True
            # )
            
            user = query_db("SELECT * FROM staff WHERE username = ?", (username,), one=True)

            
            print("USER:", dict(user))
            
            print("PASSWORD CHECK:", verify_password(user["password"], password))

            if user and verify_password(user["password"], password):
                session.clear()         
                print("SESSION l-50 LOGIN:", dict(session))
       
                session["username"] = user[username]
                # session["role"] = user["role"]     # optional but good
                
                print("SESSION AFTER LOGIN:", dict(session))
                # return redirect("/staff" if user["role"] == "staff" else "/student")
                # return redirect(url_for('staff_dashboard'))
                return jsonify({"message": "success"})
            else:
                # flash("Invalid username or password", "error")
                return jsonify({"message": "Invalid username or password"})

        # return render_template("staff/staff_login.html")
    
    @app.route("/logout")
    def logout():
        session.clear()
        return redirect(url_for("home"))
