from flask import Flask, render_template, session, redirect, request
from google.cloud import datastore

from user import User
from course import Course, Assignment
from schedule import Schedule, generateScheduleID

app = Flask(__name__)
app.secret_key = b"20072012f35b38f51c782e21b478395891bb6be23a61d70a"

datastore_client = datastore.Client("studymap-307201")
free_hours = Schedule(7, 24) #True = busy hours & False = free hours

# Route to Home Page
@app.route("/")
def home():
    print("Home")
    current_user = get_current_user()
    print("CURRENT USER: " + str(current_user))
    return render_template("index.html", user=current_user)

# Route to Login Page
@app.route("/login")
def login_page():
    return render_template("login.html", error=[])

# Route to Sign up Page
@app.route("/signup")
def signup_page():
    return render_template("signup.html", error=[])

# Route to Enter Schedule Page
@app.route("/free_hours")
def hours_page():
    return render_template("free_hours.html", error=[])

# Route to Add Courses Page
@app.route("/course")
def course_page():
    return render_template("course.html", error=[])

# Route to Add Assignments Page
@app.route("/assignment")
def assignment_page():
    output = get_courses()       
    course_names = [ x["name"] for x in output]
    print(course_names)
    return render_template("assignment.html", courses=course_names, error=[])

# Route to Workspace Page
@app.route("/workspace")
def workspace_page():
    return render_template("workspace.html", error=[])

# Gets the username of the current user if they are signed in
def get_current_user():
    return session.get("user", None)

# Processes Login
@app.route("/login-user/", methods=["POST"])
def login():
    # Gets information from form
    username = request.form.get("username")
    password = request.form.get("password")
    login_info = User(username, password)
    # Creates to see if username exists and if password matches
    user = login_info.verify_password(datastore_client)
    if not user:
        return render_template("login.html", error="Wrong Username or Password.")
    # Makes session with username
    session["user"]=login_info.username
    # Redirects user to Home Page if Login is successful
    return redirect("/")

# Processes Sign Up
@app.route("/create-user/", methods=["POST"])
def create_new_user():
    # Gets information from form
    username = request.form.get("username")
    password = request.form.get("password")  
    #print(list(existing_users()))
    # Checks to see if username is already taken
    if username in existing_users():
        return render_template("signup.html", error="Username is already taken.")
    # Create new user, stores in database, and then makes session with username
    new_user = User(username, password)
    new_user.store_user(datastore_client)
    session["user"]=new_user.username
    # Redirects user to Home Page if Sign up is successful
    return redirect("/")    

# Gets list of all users from database
def existing_users():
    query = datastore_client.query(kind="Login")
    users = query.fetch()
    return [u["username"] for u in users if "username" in u]

# Processes Course Info
@app.route("/add-course/", methods=["POST"])
def enter_courses():
    course_name = request.form.get("course1")
    course_colors = request.form.get("course_colors")
    user = session.get("user", None)
    new_course = Course(course_name, course_colors, user)
    new_course.store_course(datastore_client)
    return redirect("/")    

# Processes Assignment Info
@app.route("/add-assignment/", methods=["POST"])
def enter_assignments():
    assign_name = request.form.get("hwname")
    assign_date = request.form.get("hwdate")
    assign_course = request.form.get("hwcourse")
    assign_hours = request.form.get("hours")
    user = session.get("user", None)
    new_assign = Assignment(assign_name, assign_date, assign_course, assign_hours, user)
    new_assign.store_assignment(datastore_client)
    return redirect("/")

# get the current user's courses
def get_courses():
    q = datastore_client.query(kind="Course")
    user = session.get("user", None)
    q.add_filter("user", "=", user)
    courses = q.fetch()
    return courses

# get the current user's assignments
def get_assignments():
    q = datastore_client.query(kind="Assign")
    user = session.get("user", None)
    q.add_filter("user", "=", user)
    assign = q.fetch()
    results = list(assign)
    #print(list(assign))
    return assign

# Logs the user out
@app.route("/logout-user/")
def logout():
    # clears session
    session.clear()
    # redirects to Home Page
    return("/")

#gets the busy hours for a user
@app.route("/add-schedule/", methods=["POST"])
def get_busy_hours():
        sun_hours = generateScheduleID("SUN", 0, 24)
        parseDayCheckboxes(sun_hours, 0)
        mon_hours = generateScheduleID("MON", 0, 24)
        parseDayCheckboxes(mon_hours, 1)
        tue_hours = generateScheduleID("TUES", 0, 24)
        parseDayCheckboxes(tue_hours, 2)
        wed_hours = generateScheduleID("WED", 0, 24)
        parseDayCheckboxes(wed_hours, 3)
        thu_hours = generateScheduleID("THURS", 0, 24)
        parseDayCheckboxes(thu_hours, 4)
        fri_hours = generateScheduleID("FRI", 0, 24)
        parseDayCheckboxes(fri_hours, 5)
        sat_hours = generateScheduleID("SAT", 0, 24)
        parseDayCheckboxes(sat_hours, 6)
        print(free_hours.returnSchedule())
        return redirect("/")    
        
def parseDayCheckboxes(checkbox_names, col_num):
    for checkbox_name in checkbox_names:
        if request.form.get(checkbox_name):
            row_num = int(checkbox_name.split("_")[1])
            free_hours.addBusyHour(row_num, col_num)

if __name__ == "__main__":
    
    app.run(host='127.0.0.1', port=5000, debug=True) 

    # python3 main.py  to run it
    # ctr +c to end the session 