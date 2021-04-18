from flask import Flask, render_template, session, redirect, request, flash
from google.cloud import datastore
from datetime import datetime, date, timedelta
from pytz import timezone

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

    work0 = list()
    work1 = list()
    work2 = list()
    work3 = list()
    work4 = list()
    work5 = list()
    work6 = list()
    work_dict = split()

    curr_date = get_current_week()

    for d in range(7):
        if d == 0:
            day0 = get_work_for_day(curr_date.weekday())
            hours0 = hours_for_day(curr_date.weekday(), s_hours, m_hours, t_hours, w_hours, th_hours, f_hours, sat_hours)
            date0 = curr_date.strftime("%m-%d")
        if d == 1:
            date = curr_date + timedelta(days=d)            
            day1 = get_work_for_day(date.weekday())
            hours1 = hours_for_day(date.weekday(), s_hours, m_hours, t_hours, w_hours, th_hours, f_hours, sat_hours)
            date1 = date.strftime("%m-%d")
        if d == 2:
            date = curr_date + timedelta(days=d)
            day2 = get_work_for_day(date.weekday())
            hours2 = hours_for_day(date.weekday(), s_hours, m_hours, t_hours, w_hours, th_hours, f_hours, sat_hours)
            date2 = date.strftime("%m-%d")
        if d == 3:
            date = curr_date + timedelta(days=d)
            day3 = get_work_for_day(date.weekday())
            hours3 = hours_for_day(date.weekday(), s_hours, m_hours, t_hours, w_hours, th_hours, f_hours, sat_hours)
            date3 = date.strftime("%m-%d")        
        if d == 4:
            date = curr_date + timedelta(days=d)
            day4 = get_work_for_day(date.weekday())
            hours4 = hours_for_day(date.weekday(), s_hours, m_hours, t_hours, w_hours, th_hours, f_hours, sat_hours)
            date4 = date.strftime("%m-%d")
        if d == 5:
            date = curr_date + timedelta(days=d)
            day5 = get_work_for_day(date.weekday())
            hours5 = hours_for_day(date.weekday(), s_hours, m_hours, t_hours, w_hours, th_hours, f_hours, sat_hours)
            date5 = date.strftime("%m-%d")
        if d == 6:
            date = curr_date + timedelta(days=d)
            day6 = get_work_for_day(date.weekday())
            hours6 = hours_for_day(date.weekday(), s_hours, m_hours, t_hours, w_hours, th_hours, f_hours, sat_hours)
            date6 = date.strftime("%m-%d")

    if current_user == None: 
        return render_template("index.html", user=None,day0=day0, day1=day1, day2=day2, day3=day3, day4=day4, day5=day5, day6=day6,
            date0=date0, date1=date1, date2=date2, date3=date3, date4=date4, date5=date5, date6=date6)

    if(work_dict == None):
        return render_template("index.html", user=current_user)
    isWeek = False
    for key in work_dict:
        #if(list(work_dict.keys())[0].weekday() == key.weekday() and isWeek ):
           # break
        #isWeek = True
        if(isWeek):
           break
        for item in work_dict[key]:
            assign = list()
            num = item[0]
            book = item[1][0]
            course = item[1][1]
            assign.append(num)
            assign.append(book)
            assign.append(course)
            

            if(str(key) == curr_date.strftime("%Y-%m-%d")):
                work0.append(assign)       
            if (str(key) == (curr_date + timedelta(days=1)).strftime("%Y-%m-%d")):
                work1.append(assign)
            if (str(key) == (curr_date + timedelta(days=2)).strftime("%Y-%m-%d")):
                work2.append(assign)
            if (str(key) == (curr_date + timedelta(days=3)).strftime("%Y-%m-%d")):
                work3.append(assign)
            if (str(key) == (curr_date + timedelta(days=4)).strftime("%Y-%m-%d")):
                work4.append(assign)
            if (str(key) == (curr_date + timedelta(days=5)).strftime("%Y-%m-%d")):
                work5.append(assign)
            if (str(key) == (curr_date + timedelta(days=6)).strftime("%Y-%m-%d")):
                work6.append(assign)
                isWeek = True
                
    print("CURRENT USER: " + str(current_user))
    #m_date=m_date, t_date=t_date, w_date=w_date, th_date=th_date, 
    #f_date=f_date, s_date=s_date    
    return render_template("index.html", user=current_user, day0=day0, day1=day1, day2=day2, day3=day3, day4=day4, day5=day5, day6=day6,
     hours0=hours0, hours1=hours1, hours2=hours2, hours3=hours3, hours4=hours4, hours5=hours5, hours6=hours6,
     date0=date0, date1=date1, date2=date2, date3=date3, date4=date4, date5=date5, date6=date6,
     work0=work0, work1=work1, work2=work2, work3=work3, work4=work4, work5=work5, work6=work6)

def get_work_for_day(w_day):
    if(w_day == 0):
        day = "Monday"
    if(w_day == 1):
        day = "Tuesday"
    if(w_day == 2):
        day = "Wednesday"
    if(w_day == 3):
        day = "Thursday"
    if(w_day == 4):
        day = "Friday"
    if(w_day == 5):
        day = "Saturday"
    if(w_day == 6): 
        day = "Sunday"              
    return day

def hours_for_day(w_day, s_hours, m_hours, t_hours, w_hours, th_hours, f_hours, sat_hours):
    if(w_day == 0):
        hours = m_hours
    if(w_day == 1):
        hours = t_hours
    if(w_day == 2):
        hours = w_hours
    if(w_day == 3):
        hours = th_hours
    if(w_day == 4):
        hours = f_hours
    if(w_day == 5):
        hours = sat_hours
    if(w_day == 6): 
        hours = s_hours
    
    return hours

def get_current_week():
    curr_date = datetime.now()  
    eastern = timezone('US/Eastern')  
    curr_date = curr_date.astimezone(eastern)
    return curr_date

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

    return redirect("/")

# get the current user's courses
def get_courses():
    q = datastore_client.query(kind="Course")
    user = get_current_user()
    q.add_filter("user", "=", user)
    courses = q.fetch()
    return courses

def split():
    splitter = AssignmentSplitter(get_assignments(), get_days_off(), get_free_hours())
    date_dict = splitter.split_assignments()
    if date_dict == None:
        flash("You have overscheduled. Please update your schedule to add more free hours", "error")
        print("OVERSCHEDULED")
    else:
        print("DATE DICT: " + str(date_dict))
    return date_dict

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

        #split assignments
        splitter = AssignmentSplitter(get_assignments(), get_days_off(), get_free_hours())
        date_dict = splitter.split_assignments()
        if date_dict == None:
            print("OVERSCHEDULED")
            flash("You have overscheduled. Please update your schedule to add more free hours", "error")
        else:
            print("DATE DICT: " + str(date_dict))

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
