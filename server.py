#server.py

import threading
import socket
import time
import mysql.connector
#from RoomManager import RoomManager


# Databaes Related Variables
host = 'localhost'
user = 'Anand'
password = 'anand'

conn = mysql.connector.connect(host = host,
                               user = user,
                               passwd = password,
                               database = 'login')

print("[DATABASE] Connection to Database was Successfull")

cursor = conn.cursor()

# Server Related Variables

INPUT = input('SERVER_IP:PORT -> ')
SERVER = INPUT.split(':')[0]
PORT = int(INPUT.split(':')[1])

ADDR = (SERVER, PORT)

#roomManager = RoomManager()
DISCONNECT_MESSAGE = "!dc"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
server.listen()
print(f"[LISTENING] Server is listening on {SERVER}:{PORT}...")

CLIENTS = []
NAMES = []

def commands():
    print("[COMMANDS] Commands Initiated")
    while True:
        cmd = input('')
        if cmd == '!clients':
            print(f"[ACTIVE CONNECTIONS]: {len(CLIENTS)} ")
                
        elif cmd == '!stop':
            broadcast("Server Stopping in 2 Sec")
            time.sleep(2)
            
            for CLIENT in CLIENTS:
                CLIENT.close()
                    
            break
    return
        


def broadcast(message):
    try:
        for CLIENT in CLIENTS:
            send_msg = message.encode('utf-8')
            CLIENT.send(send_msg)
    except socket.error:
        return
        


# Function to handle CLIENTS'connections

def handle_client(CLIENT, NAME):
    while True:
        try:
            message = CLIENT.recv(1024).decode('utf-8')
            if not message:
                raise socket.error()
                broadcast(f'{NAME} has left the chat room!')  
                print (f'[DISCONNECTED] {NAME} has disconnected')      
                CLIENTS.remove(CLIENT)
                NAMES.remove(NAME)
                CLIENT.close()
                break
            
            broadcast(f'{NAME}: {message}')
            print (f'[MSG] {NAME}: {message}')
               
        except socket.error as msg:
            broadcast(f'{NAME} has left the chat room!')  
            print (f'[DISCONNECTED] {NAME} has disconnected with Error Message {msg}')      
            CLIENTS.remove(CLIENT)
            NAMES.remove(NAME)
            CLIENT.close()
            break
    return

# Performs Authentication of Clients

def Authenticator(CLIENT:socket.socket, address):
    try:
        # Get Clients Email      
        CLIENT.send('EMAIL?'.encode('utf-8'))
        EMAIL = CLIENT.recv(1024).decode('utf-8')
        
        # Get Clients Password
        CLIENT.send('PASSWD?'.encode('utf-8'))
        PASSWD = CLIENT.recv(1024).decode('utf-8')
        
        query = f"SELECT PASSWD FROM info WHERE EMAIL = '{EMAIL}';"
        cursor.execute(query)
        
        resultPASSWD = cursor.fetchall()[0][0]
        
        if(PASSWD == resultPASSWD):
            
            query = f"SELECT NAME FROM info WHERE EMAIL = '{EMAIL}'"
            cursor.execute(query)
            NAME = cursor.fetchall()[0][0]
            
            CLIENTS.append(CLIENT)
            NAMES.append(NAME)
            
            CLIENT.send('AuthSuccessfull'.encode('utf-8'))          
            print(f'[USER] User with Address {str(address)} and Name "{NAME}" joined Lobby')
                    
            time.sleep(1)
        
            #roomManager.ROOMS[0].InitiateClient(CLIENT, NAME)
        
            broadcast(f'\n{NAME} has connected to the Lobby. Welcome them!! :)\n')
            
            thread = threading.Thread(target=handle_client, args=(CLIENT, NAME), daemon=True)
            thread.start()
                        
        else:
            
            CLIENT.send("Authentication Failed. Retry with Correct Email and Password".encode('utf-8'))
            print(f'[DISCONNECTED] Connection with {str(address)} Closed Due to Failed Authentication')
            CLIENT.close()
                       
    except socket.error as msg:
        print(f"[DISCONNECTED] {str(address)} DISCONNECTED WITH ERROR : {msg}")
        
    finally:
        return


# Main function to receive the CLIENTS connection

def receive():
    while True:
        
        CLIENT, address = server.accept()
        print(f'[CONNECTED] Connection is established with {str(address)}')
        
        authThread = threading.Thread(target=Authenticator, args=(CLIENT,address), daemon=True)
        authThread.start()
    return
            

receiveThread = threading.Thread(target=receive, daemon=True)
receiveThread.start()

commands()