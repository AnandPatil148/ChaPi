#server.py

import socket 
import threading

HEADER = 64
PORT = 5050
SERVER = input('Server IP:')
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!dc"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        name_lenght = conn.recv(HEADER).decode(FORMAT)
        if name_lenght:
                name_lenght = int(name_lenght)
                name = conn.recv(name_lenght).decode(FORMAT)

        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
                
        print(f"[{addr}{name}] {msg}")
        if msg == DISCONNECT_MESSAGE:
            print (f"[{name}] DISCONNECTED")
            connected = False

    conn.close()
        

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}:{PORT}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


print("[STARTING] server is starting...")
start()