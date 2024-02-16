#A Flask Based Web Client for server
from flask import Flask, redirect, url_for, jsonify, request, render_template, session, flash
from datetime import timedelta


app = Flask(__name__)

app.secret_key = "yomamagey"
app.permanent_session_lifetime = timedelta(days=30)


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login/", methods = ["POST", "GET"])
def login():
    
    if request.method == "POST":
        session.permanent = True
        
        NAME = request.form.get("NAME", "")
        
        session["username"] = NAME
        return redirect(url_for("user"))
        
    else:
        if "username" in session:
            return redirect(url_for("user"))

        else:
            return render_template("login.html")

@app.route("/user/",methods = ["POST", "GET"])
def user():
    
    if "username" in session:
        
        NAME = session["username"]
        return render_template("user.html", NAME = NAME)
    
    else:
        return redirect(url_for("login"))
    
@app.route("/logout/")
def logout():
    if "username" in session:
        NAME = session["username"]
        flash(f"{NAME} Successfully Logged Out", "info")
        
    session.pop("username", None)
    return redirect(url_for("login"))


app.run(host='0.0.0.0', port=8080, debug=True)

