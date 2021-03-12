from flask import Flask, render_template
from google.cloud import datastore

app = Flask(__name__)

datastore_client = datastore.Client("studymap-307201")

@app.route("/")
def home():
    print("Home")
    user_key = datastore_client.key("Login", "test3")
    user = datastore.Entity(key=user_key)
    user["username"] = "test3"
    user["password"] = "pass"
    datastore_client.put(user)
    #query = datastore_client.query(kind="Login")
    #users = query.fetch()
    #print(u["username"] for u in users if "username" in u)
    print("Done")
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True) 