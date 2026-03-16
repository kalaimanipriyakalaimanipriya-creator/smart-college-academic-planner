import os
from werkzeug.utils import secure_filename
from flask import render_template, request, redirect, session, url_for, flash, jsonify,current_app
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
        role = data.get("role")

        sqlResult = None
        if role == 'staff':
            # Ensure your frontend sends 'userName' for staff
            print('I am here at staff')
            userName = data.get("userName")
            sqlResult = query_db("SELECT * FROM staff WHERE username = ?", (userName,), one=True)
        elif role == 'student':
            # Ensure your frontend sends 'regNo' for students
            print('I am here at student')
            regNo = data.get("regNo")
            print('regNo---->', regNo)
            sqlResult = query_db("SELECT * FROM student WHERE regNo = ?", (regNo,), one=True)
        elif role == 'admin':
            print('I am here at admin')
            userName = data.get("userName")
            sqlResult = query_db("SELECT * FROM admin WHERE username = ?",(userName,),one=True)

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
            session["userFullName"] = user_dict.get("name")
            session["userType"] = userType # Essential for access control
            session["role"] = role

            # Dynamic Redirect based on userType

            # redirect_url = url_for("dashboard")
            # if role == 'staff':
            redirect_url = url_for('staff_dashboard')
            # elif role == 'student':
            #     redirect_url = url_for('student_dashboard')
            # elif role == 'admin':
            #     redirect_url = url_for('admin_dashboard')
            # redirect_url = url_for('staff_dashboard') if role == 'staff' elif role ==  url_for('student_dashboard')
            
            return jsonify({
                "success": True,
                "redirect": redirect_url
            })
        
        # Fail case
        return jsonify({
            "success": False, 
            "message": "Invalid username or password"
        }), 401 # Return 401 Unauthorized



    UPLOAD_FOLDER = os.path.join("static", "uploads")
    @app.route("/register", methods=["POST"])
    def register():

        print("request.form--------------------------------->")
        print(request.form)

        fullName    = request.form.get("fullName")
        hashed_password = request.form.get("password")
        print('password------------>', hashed_password)

        password = hash_password(hashed_password)
        print('hashed_password------------>', password)

        email       = request.form.get("email")
        department  = request.form.get("department")
        designation = request.form.get("designation")
        regNo = request.form.get("regNo")
        username = None
        userType    = request.form.get("userType")   # staff OR regNo (for student)

        print('userType------------------>', userType)

        os.makedirs(UPLOAD_FOLDER, exist_ok=True)

        image_file = request.files.get("image")
        image_path = None

        if image_file and image_file.filename != "":
            ext = os.path.splitext(image_file.filename)[1]

            if userType == "staff":
                username    = request.form.get("userName")
                filename = secure_filename(f"{username}{ext}")
            else:
                regNo = userType
                filename = secure_filename(f"{regNo}{ext}")

            save_path = os.path.join(UPLOAD_FOLDER, filename)
            image_file.save(save_path)
            image_path = f"uploads/{filename}"

        try:
            if userType == "staff":
                query_db("""
                    INSERT INTO staff
                    (name, email, username, password, department, designation, image)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (fullName, email, username, password, department, designation, image_path))

            else:
                regNo = userType

                query_db("""
                    INSERT INTO student
                    (name, email, password, department, regNo, image)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (fullName, email, password, department, regNo, image_path))

            return jsonify(success=True, redirect=url_for('home'))

        except Exception as e:
            print("Error:", e)
            return jsonify(success=False, message="Internal error"), 500


    # @app.route("/register", methods=["GET", "POST"])
    # def register():

        fullName    = request.form.get("fullName")
        password    = request.form.get("password")
        email       = request.form.get("email")
        department  = request.form.get("department")
        username    = request.form.get("userName")
        designation = request.form.get("designation")
        userType    = request.form.get("userType")

        image_file  = request.files.get("image")

        if image_file:
            image_data = image_file.read()   # 👈 This is BLOB data
        else:
            image_data = None
        
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
                (name, email, username, password, department, designation,image)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (fullName, email, username, password, department, designation, image_data))
            else:
                query_db("""
                INSERT INTO student
                (name, email, username, password, department, regNo)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (fullName, email, username, password, department, userType, image_data))

                return jsonify(success=True, redirect=url_for('home'))
        except Exception as e:
            print(f"Error: {e}")
            return jsonify(success=False, message="An internal error occurred."), 500

    # @app.route("/register", methods=["GET", "POST"])
    # def register():
    #     data = request.get_json(silent=True)
    #     if not data:
    #         return jsonify(success=False, message="Invalid JSON data received"), 400

    #     result = {}

    #     fullName    = data.get("fullName")
        
    #     print('password ', data.get('password'))
    #     password    = hash_password(data.get('password'))
        
    #     print('password after hashing: ', password)
          
    #     email       = data.get("email")
        
    #     department  = data.get("department")
    #     username    = data.get("userName")
    #     designation = data.get("designation")
    #     userType    = data.get("userType")
        
    #     print(userType)
    #     # Check for duplicate email or username
    #     existing_user = query_db(
    #         "SELECT id FROM staff WHERE email = ? OR username = ?",
    #         (email, username),
    #         one=True
    #     )

    #     if existing_user:
    #         # flash("Email or Username already exists. Please use a different one.", "error")
    #         # return redirect(url_for('staff_register'))
    #         # Instead of flash/redirect, return JSON error to the AJAX call
    #         return jsonify(success=False, message="Email or Username already exists.")


    #     try:

    #         # check the usertype as staff or student and insert the table appropriately
    #         if userType == 'staff':
    #             query_db("""
    #             INSERT INTO staff
    #             (name, email, username, password, department, designation)
    #             VALUES (?, ?, ?, ?, ?, ?)
    #             """, (fullName, email, username, password, department, designation))
    #         else:
    #             query_db("""
    #             INSERT INTO student
    #             (name, email, username, password, department, regNo)
    #             VALUES (?, ?, ?, ?, ?, ?)
    #             """, (fullName, email, username, password, department, userType))

    #         # # print('prior to insert users table...................')
    #         # query_db("""
    #         #     INSERT INTO users
    #         #     (username, password, role)
    #         #     VALUES (?, ?, ?)
    #         # """, (username, password, userData.userType))
    #         # # print('inserted users table...................')

    #         # # print('prior to insert staff table...................')
    #         # query_db("""
    #         #     INSERT INTO staff
    #         #     (name, email, username, password, department, designation)
    #         #     VALUES (?, ?, ?, ?, ?, ?)
    #         # """, (fullName, email, username, password, department, designation))
    #         # # print('inserted staff table...................')

            
    #         return jsonify(success=True, redirect=url_for('home'))

    #     except Exception as e:
    #         print(f"Error: {e}")
    #         return jsonify(success=False, message="An internal error occurred."), 500

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
