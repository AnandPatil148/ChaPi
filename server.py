#server.py

import socket 
import threading


HEADER = 64
PORT = 5050
SERVER = input('Server IP:')
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!dc"
CLIENTS = []
NAMES = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def broadcast(message):
    for conn in CLIENTS:
        conn.send(message.encode(FORMAT)) #3rd conn.send

def handle_client(conn, addr):
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
                       
        broadcast(msg)

        print(f"[{addr}] {msg}")
        if msg == DISCONNECT_MESSAGE:
            index = CLIENTS.index(conn)
            name = NAMES[index]
            broadcast(f'{name} has disconnected'.encode(FORMAT))
            print (f"[{addr}] DISCONNECTED")
            CLIENTS.remove(conn)
            NAMES.remove(name)
            connected = False

    conn.close()
        

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}:{PORT}")
    while True:
        conn, addr = server.accept()
        print(f"[NEW CONNECTION] {addr} connected.")
        
        name_lenght = conn.recv(HEADER).decode(FORMAT)
        if name_lenght:
            name_lenght = int(name_lenght)
            name = conn.recv(name_lenght).decode(FORMAT)

        broadcast(f'{name} has connected')
        print(f"Name of {addr} is {name}")

        CLIENTS.append(conn) 
        NAMES.append(name)
        
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


print("[STARTING] server is starting...")
start()