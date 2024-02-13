from BlockChain import *
import json
import socket
import threading
import datetime
from uuid import uuid4
from flask import Flask, jsonify, request

# Server Related Variables
encodeFormat = 'utf-8'
SERVER = ('127.0.0.1')
PORT = 6969

ADDR = (SERVER, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
server.listen()
print(f"[LISTENING] BlockChain Server is listening on {SERVER}:{PORT}...")

SERVERS = []
NODES = []

Orbit = Blockchain()


def commands():
    print("Commands Initiated")
    while True:
        cmd = input('')
        if cmd == '!VC':
            print( json.dumps(Orbit.toDict(), indent= 4) )


# Function to handle SERVERS' connection
def HandleServer(CLIENT: socket.socket):
    while True:
        try:
            dataString = CLIENT.recv(1024).decode('utf-8')
            
            if not dataString:
                raise socket.error("Disconnected")
            
            #print(dataString)
            data = json.loads(dataString)

            block = Block(len(Orbit.chain), data.get("Time"), data)
            Orbit.addBlock(block)
            
            
        except socket.error as msg:
            print (f'{CLIENT.getpeername()} has disconnected with msg {msg}')      
            SERVERS.remove(CLIENT)
            CLIENT.close()
            break
    return

# Main function to receive the SERVER connections
def receive():
    while True:
        
        CLIENT, address = server.accept()
        print(f'Connection is established with {str(address)}')
        try:
            
            SERVERS.append(CLIENT)
            
            thread = threading.Thread(target=HandleServer, args=(CLIENT,), daemon=True)
            thread.start()
            
        except socket.error:
            print(f"{str(address)} DISCONNECTED WITH {address} WITH ERROR : {socket.error}")


'''
Flask to view the chain on web browser
'''
# Instantiate the Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

@app.route('/', methods=['GET'])
def index():
    response = {
        'chain': Orbit.toDict(),
        'length': len(Orbit.chain),
    }
    return jsonify(response), 200


def startservers():
    cmd_thread = threading.Thread(target=commands)
    cmd_thread.start()
    
    receive_thread = threading.Thread(target=receive)
    receive_thread.start()

    app.run(host='0.0.0.0', port=8080)
    
startservers()


