from flask import Flask, render_template, session, g
from db import init_db
from auth import auth_routes
from staff import staff_routes
from student import student_routes
from timetable import timetable_routes
from mapping import mapping

app = Flask(__name__)
app.secret_key = "smart_timetable_secret"

print("app.url_map#################" , app.url_map)

@app.teardown_appcontext
def close_db(error):
    db = g.pop('db', None)
    if db is not None:
        db.close()
        
# Home
@app.route("/academic-planner/home")
def home():
    return render_template("home.html")

@app.context_processor
def inject_user():
    return dict(current_user_role = session.get("role"))

# Register routes
auth_routes(app)
staff_routes(app)
student_routes(app)
timetable_routes(app)
mapping(app)

if __name__ == "__main__":
    # run once, then comment / uncomment - next 2 lines
    with app.app_context():
        init_db()
    app.run(debug=True)