#A Flask Based Web Client for server
from flask import Flask, redirect, url_for, jsonify, request, render_template, session, flash
from flask_socketio import SocketIO
from datetime import timedelta

app = Flask(__name__)
socketIO = SocketIO(app)

app.secret_key = "yomamagey"
app.permanent_session_lifetime = timedelta(minutes=5)


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login/", methods = ["POST", "GET"])
def login():
    
    if request.method == "POST":
        session.permanent = True
                
        NAME = request.form.get("NAME", "")
        session["NAME"] = NAME
        
        '''
        #Get NAME from Database and store in SESSION
        try:
            NAME = "GET FROM DATABASE"            
            session["NAME"] = NAME
            
            flash('Logged In!')
            return redirect(url_for("home"))
        except Exception as e:
            print(e)
            flash('Failed to Login')
        '''

        return redirect(url_for("user"))
        
    else:
        if "NAME" in session:
            return redirect(url_for("user"))

        else:
            return render_template("login.html")

@app.route("/user/",methods = ["POST", "GET"])
def user():
    EMAIL = None
    
    if "NAME" in session:
        NAME = session["NAME"]
        
        if request.method == "POST":
            EMAIL = request.form["EMAIL"]
            session["EMAIL"] = EMAIL
            flash(f"Email Successfully Saved", "info")
        else:
            if "EMAIL" in session:
               EMAIL = session["EMAIL"]
                        
        return render_template("user.html", NAME = NAME, EMAIL = EMAIL)
    
    else:
        return redirect(url_for("login"))
    
@app.route("/logout/")
def logout():
    if "NAME" in session:
        NAME = session["NAME"]
        flash(f"{NAME} Successfully Logged Out", "info")
        
    session.pop("NAME", None)
    session.pop("EMAIL", None)
    return redirect(url_for("login"))


socketIO.run(app=app, host='0.0.0.0', port=8080, debug=True)

