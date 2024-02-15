#A Flask Based Web Client for server

from flask import Flask, redirect, url_for, jsonify, request, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login/", methods = ["POST", "GET"])
def login():
    
    if request.method == "POST":
        
        NAME = request.form.get("NAME", "")
        return redirect(url_for("user", NAME = NAME))
        
    else:
        return render_template("login.html")

@app.route("/<NAME>/")
def user(NAME):
    return render_template("user.html", NAME = NAME)


app.run(host='0.0.0.0', port=8080, debug=True)

