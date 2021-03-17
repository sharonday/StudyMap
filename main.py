from flask import Flask, render_template, session, redirect, request
from google.cloud import datastore

from user import UserMan

app = Flask(__name__)
app.secret_key = b"20072012f35b38f51c782e21b478395891bb6be23a61d70a"

datastore_client = datastore.Client("studymap-307201")

@app.route("/")
def home():
    print("Home")
    current_user = get_current_user()
    print(current_user)
    return render_template("index.html", user=current_user)

@app.route("/login")
def login_page():
    return render_template("login.html", error=[])

@app.route("/signup")
def signup_page():
    return render_template("signup.html", error=[])

# Gets the username of the current user if they are signed in
def get_current_user():
    return session.get("user", None)

@app.route("/login-user/", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    login_info = UserMan(username, password)
    user = login_info.verify_password(datastore_client)
    if not user:
        return render_template("login.html", error="Wrong Username or Password.")
    session["user"]=login_info.username
    return redirect("/")

@app.route("/create-user/", methods=["POST"])
def create_new_user():
    username = request.form.get("username")
    password = request.form.get("password")  
    #print(list(existing_users()))
    if username in existing_users():
        return render_template("signup.html", error="Username is already taken.")
    new_user = UserMan(username, password)
    new_user.store_user(datastore_client)
    session["user"]=new_user.username
    return redirect("/")    

def existing_users():
    query = datastore_client.query(kind="Login")
    users = query.fetch()
    return [u["username"] for u in users if "username" in u]

@app.route("/logout-user/")
def logout():
    session.clear()
    return("/")


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True) 

    #python3 main.py  to run it
    #ctr +c to end the session 
    
    # how html forms work 
    # get checkout alyssa to get files 