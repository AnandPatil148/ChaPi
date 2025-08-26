#server.py

import threading
import socket
import time


# Server Related Variables
encodeFormat = 'utf-8'
INPUT = input('SERVER_IP:PORT -> ')
SERVER = INPUT.split(':')[0]
PORT = int(INPUT.split(':')[1])

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
            # Add a feature to send to all clients in rooms
            broadcast("Server Stopping in 2 Sec", 'Lobby')  # Broadcast to all clients in the Lobby
            print("Server Stopping in 2 Sec")
            time.sleep(2)
            
            for CLIENT in CLIENTS:
                CLIENT.close()
                    
            break
    return
        


def broadcast(message:str,roomname:str):
    try:
        for CLIENT in ROOMS.get(roomname, []):
            CLIENT.send(message.encode(encodeFormat))
    except socket.error:
        return

def join_room(CLIENT, NAME, roomToJoin:str, roomToleave:str):
    if roomToJoin not in ROOMS:
        ROOMS[roomToJoin] = []  # If room doesn't exist, create it
        
    ROOMS[roomToleave].remove(CLIENT)
    ROOMS[roomToJoin].append(CLIENT)
    broadcast(f"{NAME} has joined the room '{roomToJoin}' ", roomToJoin)
    print(f"[JOINED] {NAME} has joined the room: '{roomToJoin}'")

def leave_room(CLIENT, NAME,roomname):
    broadcast(f"{NAME} left the room '{roomname}'", roomname)
    print(f"[LEFT] {NAME} left the room '{roomname}'")
    ROOMS[roomname].remove(CLIENT)
    ROOMS['Lobby'].append(CLIENT)


# Function to handle CLIENTS'connections

def handle_client(CLIENT:socket.socket, NAME:str, roomname:str):
    while True:
        try:
            message = CLIENT.recv(1024).decode(encodeFormat)
            if not message:
                raise socket.error()
            
            if message.startswith('!join'):
                newRoomname = message.split(" ")[1]
                join_room(CLIENT, NAME, newRoomname, roomname)
                roomname = newRoomname #Update current room of client
                
            elif message.startswith('!leave'):
                if roomname == 'Lobby':
                    CLIENT.send("ERROR: Cannot leave lobby.".encode(encodeFormat))
                
                else:                  
                    leave_room(CLIENT, NAME, roomname)
                    roomname = 'Lobby' #Update current room of client
                
            else:
                broadcast(f'{NAME}: {message}', roomname)
                print (f'[MSG] {roomname} - {NAME}: {message}')
            
               
        except socket.error as msg:
            broadcast(f'{NAME} has left the chat room!', roomname)  
            print (f'[DISCONNECTED] {NAME} has disconnected with Error Message {msg}')
            CLIENTS.remove(CLIENT)
            NAMES.remove(NAME)
            ROOMS[roomname].remove(CLIENT)
            CLIENT.close()
            break
    return
        

# Main function to receive the CLIENTS connection
def receive():
    while True:
        
        CLIENT, address = server.accept()
        print(f'[CONNECTED] Connection is established with {str(address)}')
        
        CLIENT.send('NAME?'.encode(encodeFormat))
        NAME = CLIENT.recv(1024).decode(encodeFormat)
        
        CLIENTS.append(CLIENT)
        NAMES.append(NAME)
        ROOMS['Lobby'].append(CLIENT)
            
        CLIENT.send('AuthSuccessfull'.encode(encodeFormat))
        print(f"[USER] User with Address {str(address)} and Name '{NAME}' joined Lobby")
                    
        time.sleep(1)
                
        broadcast(f'\n{NAME} has connected to the Lobby. Welcome them!! :)\n', 'Lobby')
        
        authThread = threading.Thread(target=handle_client, args=(CLIENT,NAME, "Lobby"), daemon=True)
        authThread.start()  

receiveThread = threading.Thread(target=receive, daemon=True)
receiveThread.start()

commands()