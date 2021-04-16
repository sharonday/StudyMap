from flask import Flask, render_template, session, redirect, request
from google.cloud import datastore

from user import User
from course import Course, Assignment
from schedule import Schedule, generateScheduleID
from split_schedule import AssignmentSplitter

app = Flask(__name__)
app.secret_key = b"20072012f35b38f51c782e21b478395891bb6be23a61d70a"

datastore_client = datastore.Client("studymap-307201")
free_hours = Schedule(7, 24) #True = busy hours & False = free hours

# Route to Home Page
@app.route("/")
def home():
    print("Home")
    current_user = get_current_user()
    free_hours = get_free_hours()
    s_hours = list()
    m_hours = list()
    t_hours = list()
    w_hours = list()
    th_hours = list()
    f_hours = list()
    sat_hours = list()
    for days in free_hours:
        if days["day"] == "SUN":
            s_hours = days["hours"]
        if days["day"] == "MON":
            m_hours = days["hours"]
        if days["day"] == "TUES":
            t_hours = days["hours"]
        if days["day"] == "WED":
            w_hours = days["hours"]
        if days["day"] == "THURS":
            th_hours = days["hours"]
        if days["day"] == "FRI":
            f_hours = days["hours"]
        if days["day"] == "SAT":
            sat_hours = days["hours"]
    print("CURRENT USER: " + str(current_user))
    return render_template("index.html", user=current_user, sun=s_hours, mon=m_hours,tues=t_hours,wed=s_hours,thurs=th_hours,fri=f_hours,sat=sat_hours)

# Route to Login Page
@app.route("/login")
def login_page():
    return render_template("login.html", error=[])

# Route to Sign up Page
@app.route("/signup")
def signup_page():
    return render_template("signup.html", error=[])

# Route to How To Page
@app.route("/info")
def info_page():
    return render_template("info.html", error=[])

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
    session['logged_in'] = True
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
    session['logged_in'] = True
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
    user = get_current_user()
    new_course = Course(course_name, course_colors, user)
    new_course.store_course(datastore_client)
    return redirect("/")

# Processes Assignment Info
@app.route("/add-assignment/", methods=["POST"])
def enter_assignments():
    #add assignment to database
    assign_name = request.form.get("hwname")
    assign_date = request.form.get("hwdate")
    assign_course = request.form.get("hwcourse")
    assign_hours = request.form.get("hours")
    user = get_current_user()
    new_assign = Assignment(assign_name, assign_date, assign_course, assign_hours, user)
    new_assign.store_assignment(datastore_client)

    #split assignments
    splitter = AssignmentSplitter(get_assignments(), get_days_off(), get_free_hours())
    date_dict = splitter.split_assignments()
    print(date_dict)
    return redirect("/")

# get the current user's courses
def get_courses():
    q = datastore_client.query(kind="Course")
    user = get_current_user()
    q.add_filter("user", "=", user)
    courses = q.fetch()
    return courses

# get the current user's assignments
def get_assignments():
    q = datastore_client.query(kind="Assign")
    user = get_current_user()
    q.add_filter("user", "=", user)
    assign = q.fetch()
    return assign

# Logs the user out
@app.route("/logout-user/")
def logout():
    # clears session
    session.clear()
    # redirects to Home Page
    return redirect("/")

# deletes schedule in db if they enter another
def delete_old_schedule():
    user = get_current_user()
    q = datastore_client.query(kind="Free Hours")
    q.add_filter("user", "=", user)
    q.keys_only()
    old_f_hours = q.fetch()
    for o in old_f_hours:
        datastore_client.delete(o)

#gets the busy hours for a user
@app.route("/add-schedule/", methods=["POST"])
def enter_schedule():
        delete_old_schedule()
        sun_hours = generateScheduleID("SUN", 0, 24)
        sun_off = parseDayCheckboxes(sun_hours, 0)
        mon_hours = generateScheduleID("MON", 0, 24)
        mon_off = parseDayCheckboxes(mon_hours, 1)
        tue_hours = generateScheduleID("TUES", 0, 24)
        tue_off = parseDayCheckboxes(tue_hours, 2)
        wed_hours = generateScheduleID("WED", 0, 24)
        wed_off = parseDayCheckboxes(wed_hours, 3)
        thu_hours = generateScheduleID("THURS", 0, 24)
        thu_off = parseDayCheckboxes(thu_hours, 4)
        fri_hours = generateScheduleID("FRI", 0, 24)
        fri_off = parseDayCheckboxes(fri_hours, 5)
        sat_hours = generateScheduleID("SAT", 0, 24)
        sat_off = parseDayCheckboxes(sat_hours, 6)
        print(free_hours.returnSchedule())

        # store off days to the db
        user = get_current_user()
        off_days_key = datastore_client.key("Off Days", user)
        off_days = datastore.Entity(key=off_days_key)
        off_days["user"] = user
        off_days["sun"] = sun_off
        off_days["mon"] = mon_off
        off_days["tue"] = tue_off
        off_days["wed"] = wed_off
        off_days["thu"] = thu_off
        off_days["fri"] = fri_off
        off_days["sat"] = sat_off
        datastore_client.put(off_days)
        return redirect("/")

# gets the days the user is off
def get_days_off():
    q = datastore_client.query(kind="Off Days")
    user = get_current_user()
    q.add_filter("user", "=", user)
    days_off = q.fetch()
    # @Nayana and @Caroline
    # Should get 1 item
    # To access days off and use in function (put this code in whatever
    # function you are using but don't uncomment here)
    # for d in days_off:
        #if d["sun"] == True:
            # sunday is off day
        #if d['mon'] == True:
             # monday is off day
    return days_off

def parseDayCheckboxes(checkbox_names, col_num):
    # day originally set as "working day"
    off = False
    bh = 0
    hours =[]
    for checkbox_name in checkbox_names:
        if request.form.get(checkbox_name):
            row_num = int(checkbox_name.split("_")[1])
            free_hours.addBusyHour(row_num, col_num)
            bh = bh + 1
        else:
            # if they have available work time, 
            # it adds the time to the free hours list for that day
            hours.append(checkbox_name.split("_")[1] + ":00 - " + checkbox_name.split("_")[2]+ ":00")

    if bh == 24:
        # day originally set as "off day"
        print(checkbox_name.split("_")[0])
        off = True
    # after all the free hours for a day are determined,
    # it is stored to the db
    user = get_current_user()
    day = checkbox_name.split("_")[0]
    f_hours_key = datastore_client.key("Free Hours")
    f_hours = datastore.Entity(key=f_hours_key)
    f_hours["user"] = user
    f_hours["day"] = day
    f_hours["hours"] = hours
    datastore_client.put(f_hours)
    return off

# gets user's free_hours
def get_free_hours():
    q = datastore_client.query(kind="Free Hours")
    user = get_current_user()
    q.add_filter("user", "=", user)
    free_hours = q.fetch()
    # @Nick
    # Should get 7 items, one for each day of the week
    # To access and send free hours to webpage (put this code in whatever
    # function you are using but don't uncomment here)
    # for w in free_hours:
        #if w["day"] == "SUN":
            #sun_hours = w["hours"]
        #elif w["day"] == "MON":
            #mon_hours = w["hours"]
        #etc
    # the values stored in mon_hours will be an array/list
    # of free time slots for that day
    return free_hours

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)

    # python3 main.py  to run it
    # ctr +c to end the session
