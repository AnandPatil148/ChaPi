from BlockChain import *
import json
import socket
import threading
import datetime
from uuid import uuid4

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
Orbit.load_data("wallets.json")


def commands():
    print("Commands Initiated")
    while True:
        cmd = input('')
        if cmd == '!VC':
            print( json.dumps(Orbit.toDict(), indent= 4) )
        elif cmd == '!stop':
            for server in SERVERS:
                server.close()
            quit()


# Function to handle SERVERS' connection
def HandleServer(SERVER: socket.socket, addr):
    while True:
        try:
            dataString = SERVER.recv(1024).decode('utf-8')
            
            if not dataString:
                raise socket.error("Disconnected")
            
            if dataString.startswith("GET"):
                blocktoget = dataString.split(" ")[1]
                roomname = dataString.split(" ")[3]
                
                data = Orbit.getBlock(int(blocktoget), roomname) #Data of one Block in form of dict
                
                    
                # Send back the Data in JSON Formated string
                dataString = json.dumps(data) #convert to JSON Formated string
                SERVER.send(dataString.encode(encodeFormat)) #sends the data to the SERVER
                print(f"Data Sent To SERVER {addr}")
                continue
            
            else:
                #print(dataString)
                data = json.loads(dataString) #data is a disctionary here

                block = Block(len(Orbit.chain), data.get("TimeStamp"), data)
                Orbit.addBlock(block)
            
            
        except socket.error as msg:
            print (f'{SERVER.getpeername()} has disconnected ')      
            SERVERS.remove(SERVER)
            SERVER.close()
            break
    return

# Main function to receive the SERVER connections
def receive():
    while True:
        
        SERVER, address = server.accept()
        print(f'Connection is established with {str(address)}')
        try:
            
            SERVERS.append(SERVER)
            
            thread = threading.Thread(target=HandleServer, args=(SERVER, address), daemon=True)
            thread.start()
            
        except socket.error:
            print(f"{str(address)} DISCONNECTED WITH {address} WITH ERROR : {socket.error}")



def startservers():
    cmd_thread = threading.Thread(target=commands)
    cmd_thread.start()
    
    receive_thread = threading.Thread(target=receive)
    receive_thread.start()
    
startservers()


