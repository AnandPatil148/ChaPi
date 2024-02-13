import mysql.connector
import threading
import datetime
import hashlib
import secrets
import socket
import time
import json

host = '172.27.224.1'
user = 'login'
password = 'login'

encodeFormat = 'utf-8'
SERVER = ('127.0.0.1')
PORT = 5050

ADDR = (SERVER, PORT)

DISCONNECT_MESSAGE = "!dc"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
server.listen()
print(f"[LISTENING] Server is listening on {SERVER}:{PORT}...") 

CLIENTS = []
NAMES = []
ROOMS = {'Lobby': []}

def commands():
    print("[COMMANDS] Commands Initiated")
    while True:
        cmd = input('')
        if cmd == '!clients':
            print(f"[ACTIVE CONNECTIONS]: {len(CLIENTS)} ")
        elif cmd == '!stop':
            broadcast("Server Stopping in 2 Sec", 'Lobby')  # Broadcast to all clients in the Lobby
            print("Server Stopping in 2 Sec")
            time.sleep(2)
            for CLIENT in CLIENTS:
                CLIENT.close()
            break

#BroadCasts to Clients in a specific Room
def broadcast(message: str, roomname: str):
    try:
        for CLIENT in ROOMS.get(roomname, []):
            CLIENT.send(message.encode(encodeFormat))
    except socket.error:
        return

#Join a room. If Room not present Makes one
def join_room(CLIENT, NAME, roomToJoin: str, roomToLeave: str):
    if roomToJoin not in ROOMS:
        ROOMS[roomToJoin] = []
    ROOMS[roomToLeave].remove(CLIENT)
    ROOMS[roomToJoin].append(CLIENT)
    broadcast(f'[{NAME}] has joined the room {roomToJoin}', roomToJoin)
    print(f'[{NAME}] has joined the room {roomToJoin}')

#Leaves a room and Joins Lobby
def leave_room(CLIENT, NAME, roomname: str):
    ROOMS[roomname].remove(CLIENT)
    ROOMS['Lobby'].append(CLIENT)
    broadcast(f"{NAME} left the room {roomname}", roomname)

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
    generated_password = hash_password(passwordToCheck, storedSalt)[0]
    return generated_password == storedHashOfPassword

#Creates Block On BlockChain
def create_block(t, roomname, userID, NAME , message, BlockChainSocket):
    #Collect data in the form of Dictionary
    data = {
        'Time': t,  #TimeStamp of the message
        'Roomname': roomname,  # Room name from which the client chats from
        'UserID': userID,  # User ID for tracking user activity
        'Name': NAME, # UserName for the user who is chatting
        'Message': message, # Message to be sent by the user
    }
    
    
    dataString = json.dumps(data) #convert to json string
    
    BlockChainSocket.send(dataString.encode(encodeFormat)) #send json string to blockchain server

#Handles all client connections
def HandleClient(CLIENT: socket.socket, NAME: str, userID:str, roomname: str):
    
    try:
        #Connects To The BlockChain Node
        BlockChainSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        BlockChainSocket.connect(('127.0.0.1', 6969))
        print("[CONNECTED] Successfully connected to Blockchain Node")
        connectedToBlockChain = True
    except:
        print("[FAILED] Couldn't connect to Blockchain Node. Running Offline mode")
        connectedToBlockChain = False
        
    
    while True:
        try:
            message = CLIENT.recv(1024).decode(encodeFormat)
            
            t = datetime.datetime.now().strftime('%m-%d-%y %H:%M:%S') #Time at which Message was recceived by server
            
            if not message:
                raise socket.error()

            if message.startswith('!join'):
                new_room = message.split(" ")[1]
                join_room(CLIENT, NAME, new_room, roomname)
                roomname = new_room  # Update the current room of the client

            elif message.startswith('!leave'):
                leave_room(CLIENT, NAME, roomname)
                roomname = 'Lobby'  # Update the current room of the client

            else:
                broadcast(f'{NAME}: {message}', roomname)
                print(f'[MSG] {roomname} - {NAME}: {message}')
                
                if connectedToBlockChain:
                    create_block(t, roomname, userID, NAME, message, BlockChainSocket)
                
                

        except socket.error as msg:
            broadcast(f'{NAME} has left the chat room!', roomname)
            print(f'[DISCONNECTED] {NAME} has disconnected with Error Message {msg}')
            CLIENTS.remove(CLIENT)
            NAMES.remove(NAME)
            ROOMS[roomname].remove(CLIENT)
            CLIENT.close()
            break

def Authenticator(CLIENT: socket.socket, address):
    conn = mysql.connector.connect(host=host, user=user, passwd=password)
    cursor = conn.cursor()

    try:
        CLIENT.send('regORlog'.encode(encodeFormat))
        regORlog = CLIENT.recv(1024).decode(encodeFormat)

        if regORlog == 'r':
            CLIENT.send('NAME?'.encode(encodeFormat))
            NAME = CLIENT.recv(1024).decode(encodeFormat)

            CLIENT.send('EMAIL?'.encode(encodeFormat))
            EMAIL = CLIENT.recv(1024).decode(encodeFormat)

            CLIENT.send('PASSWD?'.encode(encodeFormat))
            PASSWD = CLIENT.recv(1024).decode(encodeFormat)
            HashedPASSWD, salt  = hash_password(PASSWD)

            #Insert Data into Database
            query = f"INSERT INTO info (NAME,EMAIL, PASSWD, SALT) VALUES ('{NAME}', '{EMAIL}', '{HashedPASSWD}', %s);" 
            cursor.execute(query, (salt))
            conn.commit()

        elif regORlog == 'l':
            CLIENT.send('EMAIL?'.encode(encodeFormat))
            EMAIL = CLIENT.recv(1024).decode(encodeFormat)

            CLIENT.send('PASSWD?'.encode(encodeFormat))
            PASSWD = CLIENT.recv(1024).decode(encodeFormat)

        query = f"SELECT PASSWD,SALT FROM login.info WHERE EMAIL = '{EMAIL}';"
        cursor.execute(query)
        result = cursor.fetchone()
        
        if result == []: #Check if account is present or not
            CLIENT.send("Authentication Failed. Account Not Found. Please Create One".encode(encodeFormat))
            print(f'[DISCONNECTED] Connection with {str(address)} Closed Due to Failed Authentication')
            CLIENT.close()
        

        elif check_password(PASSWD, result[0], result[1]):
            query = f"SELECT ID,NAME FROM login.info WHERE EMAIL = '{EMAIL}'"
            cursor.execute(query)
            NAME = cursor.fetchone()[0] # Gets Client Name from database 
            userID = cursor.fetchone()[1] # Gets Client userID from database
            
            CLIENTS.append(CLIENT)
            NAMES.append(NAME)
            ROOMS['Lobby'].append(CLIENT)

            CLIENT.send('AuthSuccessfull'.encode(encodeFormat))
            print(f'[USER] User with Address {str(address)}, Name "{NAME} and UserID {userID}" joined Lobby')

            time.sleep(1)

            broadcast(f'\n{NAME} has connected to the Lobby. Welcome them!! :)\n', 'Lobby')

            thread = threading.Thread(target=HandleClient, args=(CLIENT, NAME, userID, 'Lobby'), daemon=True)
            thread.start()

        else:
            CLIENT.send("Authentication Failed. Retry with Correct Email and Password".encode(encodeFormat))
            print(f'[DISCONNECTED] Connection with {str(address)} Closed Due to Failed Authentication')
            CLIENT.close()

    except socket.error as msg:
        print(f"[DISCONNECTED] {str(address)} DISCONNECTED ABRUPTLY WITH ERROR : {msg}")

def receive():
    while True:
        CLIENT, address = server.accept()
        print(f'[CONNECTED] Connection is established with {str(address)}')

        authThread = threading.Thread(target=Authenticator, args=(CLIENT, address), daemon=True)
        authThread.start()

receiveThread = threading.Thread(target=receive, daemon=True)
receiveThread.start()

commands()
