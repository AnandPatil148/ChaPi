#A Flask Based Web Client for Blockchain server
from flask import Flask, redirect, url_for, jsonify, request, render_template, session, flash
from flask_socketio import SocketIO
from datetime import timedelta
import mysql.connector
import datetime
import secrets
import socket
import hashlib
import json


app = Flask(__name__)
#socketIO = SocketIO(app)

# Set up the database connection
#host = 'localhost' 
#port = 3306
host = '19.ip.gl.ply.gg' 
port = 6882
username = 'server'
password = 'server'
loginDatabase = 'login'
roomDatabase = 'roomdata'

#Connect to mysql server 
conn = mysql.connector.connect(host=host, port=port, user=username, passwd=password, )

cursor = conn.cursor(buffered=True)

#BCN params
BCN_ip = '180.ip.ply.gg'
BCN_port = 12378

# Setup the secret key for sessions
app.config.from_pyfile('config.py')
app.permanent_session_lifetime = timedelta(days=5)

#Hashes Password
def hash_password(passwordToHash, salt=None):
    if salt is None:
        salt = secrets.token_bytes(16)  # Generate a random 16-byte salt
    
    # Combine the password and salt, then hash
    hashed_password = hashlib.sha256(passwordToHash.encode() + salt).hexdigest()
    
    return hashed_password, salt

# Verifies password
def check_password(passwordToCheck, storedHashOfPassword, storedSalt):
    # Use the same process to hash the given password,
    # and compare it with the stored password
    generated_new_hash = hash_password(passwordToCheck, storedSalt)[0]
    return generated_new_hash == storedHashOfPassword


@app.route("/")
def index():
    if "USERID" in session: #Checks if user is logged in
        return render_template("index.html"  , ROOMS = session["ROOMS"])
    
    else:
        return redirect(url_for("login"))
    
@app.route("/signup/", methods = ["POST", "GET"])
def signup():
    
    if request.method == "POST":
        
        NAME = request.form["NAME"]
        EMAIL = request.form['EMAIL']
        PASSWD = request.form['PASSWD']
        CPASSWD = request.form['CPASSWD']
        
        # Checks that passwords match
        if PASSWD != CPASSWD:
            flash('Passwords do not match!')
            
        elif NAME == "" or EMAIL == "" or PASSWD == '':
            flash('Please Fill All Fields')
                
        else:
            # Generates a unique salt and hashed pass for this PASSWD
            hashed_PASSWD, saltOf_PASSWD = hash_password(PASSWD)
            
            try:
                
                query = "INSERT INTO login.info (NAME,EMAIL,PASSWD,SALT)  VALUES(%s,%s,%s,%s)"
                data = (NAME, EMAIL, hashed_PASSWD, saltOf_PASSWD)
                cursor.execute(query,data)
                conn.commit()
                flash('Sign Up Successful! Please Log In Now')
                return redirect(url_for('login'))
            except Exception as e:
                print(e)
                flash('Username Already Taken! Try Again With A Different Username')
                return render_template("signup.html")
    
    else: #If Method is GET       
        return render_template('signup.html')  
    
@app.route("/login/", methods = ["POST", "GET"])
def login():
    
    if request.method == "POST":
        session.permanent = True
                
        NAME = request.form.get("NAME", "")
        #login thru email rather than username
        
        PASSWD = request.form.get("PASSWD", "")
        
        try:
            
            query = f"SELECT * FROM login.info WHERE NAME='{NAME}';"  
            cursor.execute(query)
            
            data = cursor.fetchone()
            
            if not data:
                raise Exception ("Account Not Found. Please Signup")
            
            if not check_password(PASSWD, data[3], data[4]):
                raise Exception ("Incorrect username or password.")
                            
            session["USERID"] = data[0]
            session["NAME"] = data[1]
            session["EMAIL"] = data[2]       
            session["ROOMS"] = data[5]       
            flash('Logged In!')
                        
        except Exception as e:
            print(e)
            flash("An error occurred while trying to log in.")
            flash(f"Error Message - {e}")
            
        return redirect(url_for("index"))      
     
    else: #If Method is GET
        if "USERID" in session:
            return redirect(url_for("user"))

        else:
            return render_template("login.html")

@app.route("/user/",methods = ["POST", "GET"])
def user():
    EMAIL = None
    
    if "USERID" in session:
        USERID = session["USERID"]
        NAME = session["NAME"]
        
        if request.method == "POST":
            EMAIL = request.form["EMAIL"]
            session["EMAIL"] = EMAIL
            flash(f"Email Successfully Saved", "info") #Update email in db
            
            query = "UPDATE login.info SET EMAIL=%s WHERE USERID=%s"
            params = (EMAIL, USERID)
            cursor.execute(query,params)
            conn.commit()             
            
        else:
            if "EMAIL" in session:
               EMAIL = session["EMAIL"]
                        
        return render_template("user.html", NAME = NAME, EMAIL = EMAIL, ROOMS = session["ROOMS"])
    
    else:
        return redirect(url_for("login"))
    
    
@app.route("/room/<roomname>/")
def room(roomname):
    #check if user has logged in
    if "USERID" not in session:  
        return redirect(url_for('login'))  
    
    else:
        #Check if User can access room
        ROOMS = session["ROOMS"]
        if roomname not in ROOMS: 
            flash("You don't have permission to view this page.")
            return redirect(url_for("index"))
      
        else:
            
            BCN = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP Conn to Blockchain Nodes
            BCN.connect((BCN_ip, BCN_port))    # Connecting with local BCS Server (localhost:6969)
            
            BCNquery = f"GET 1 FROM {roomname}" # Query for getting data from the blockchain
            BCN.send(BCNquery.encode('utf-8')) # Sends the Query
            dataString = BCN.recv(4096).decode('utf-8') # Receive Data from BCS server and decode it into utf-8 format
            Block = json.loads(dataString)       # Loads into Dictionary form
            
            if Block != None:
                BlockData = Block["Data"]
            else:
                BlockData = []
            
            BCN.close()
            return render_template("room.html", roomname = roomname, ROOMS = session["ROOMS"], dataDict = BlockData)


@app.route("/room/<roomname>/newpost/" , methods=["GET", "POST"])
def newpost(roomname):
    
    #check if user has logged in
    if request.method == "POST":
        
        message = request.form.get("POSTMSG", "")
        
        #check if message if null or not 
        if message == "":
            flash("Message cannot be empty!","danger")
            return redirect(url_for("room", roomname = roomname))
            
        
        #Time at which Message was recceived by server
        t = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # '2024-02-14 01:13:15'
        NAME = session["NAME"]
        UserID = session["USERID"]
        
        #Collect data in the form of Dictionary
        data = {
            'TimeStamp': t,  #TimeStamp of the message
            'RoomName': roomname,  # Room name from which the client chats from
            'UserID': UserID,  # User ID for tracking user activity
            'Name': NAME, # UserName for the user who is chatting
            'Message': message, # Message to be sent by the user
        }


        dataString = json.dumps(data) #convert to json string

        print(dataString)
        
        BCN = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP Conn to Blockchain servers
        BCN.connect((BCN_ip, BCN_port))    # Connecting with local BCS Server (localhost:6969)
        
        BCN.send(dataString.encode("utf-8")) #send json string to blockchain server
        
        #print(f"{t}:{roomname} - {NAME}: {message}")
        
        BCN.close()
        
        return redirect(url_for("room", roomname = roomname))
        
    else:
       return render_template("newpost.html", ROOMS = session["ROOMS"])
    
@app.route("/logout/")
def logout():
    if "NAME" in session:
        NAME = session["NAME"]
        flash(f"{NAME} Successfully Logged Out", "info")
        
    session.pop("USERID", None)
    session.pop("NAME", None)
    session.pop("EMAIL", None)
    session.pop("ROOMS", None)
    return redirect(url_for("login"))


#socketIO.run(app=app, host='0.0.0.0', port=8080, debug=True)
#app.run(host = '0.0.0.0', port = 8080, debug = True)

