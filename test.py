import datetime
import hashlib
import json
from uuid import uuid4
from flask import Flask, jsonify, request


t = datetime.datetime.now()
t.strftime('%y-%m-%d %H:%M:%S')  # '2024-02-14 01:13:15

print(t)

l = []

data = {
    'Time': t,  #TimeStamp of the message
    'Roomname': 'lobby',  # Room name from which the client chats from
    'UserID': '1',  # User ID for tracking user activity
    'Name': 'Test', # UserName for the user who is chatting
    'Message': 'HEHE', # Message to be sent by the user
}

passwd = 'test'

print(hashlib.sha256(passwd.encode('utf-8')).hexdigest())

print(len(hashlib.sha256(passwd.encode('utf-8')).hexdigest()))


#dataString = json.dumps(data)
#print(dataString)

#ataString2 = '{"Time": "02-02-24 15:43:41", "Roomname": "lobby", "UserID": "1", "Name": "Test", "Message": "HEHE"}'


'''
# Instantiate the Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

@app.route('/', methods=['GET'])
def index():
    return "Hello World"

app.run(host='0.0.0.0',port=8080)

BlockChainSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
BlockChainSocket.connect('127.0.0.1', 6969)
'''