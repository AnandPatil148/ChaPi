#client.py

import socket
import threading

HEADER = 64
PORT = 5050
SERVER = input('Target IP: ')
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!dc"
NAME = str(input('Name:'))

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def server_receive():
    while True:
        try:
            message = client.recv(HEADER).decode(FORMAT)
            print(message)
        except:
            print("error")
            client.close()
            break


def send():
    while True:
        MSG = input (f'{NAME}: ')
        
        Ename = NAME.encode(FORMAT)
        name_length = len(Ename)
        send_Nlength = str(name_length).encode(FORMAT)
        send_Nlength += b' ' * (HEADER - len(send_Nlength))

        message = MSG.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))

        client.send(send_Nlength)
        client.send(Ename)
        client.send(send_length)
        client.send(message)

        if MSG == DISCONNECT_MESSAGE:
            client.close()
            break

server_receive_thread = threading.Thread(target=server_receive)
server_receive_thread.start()

send_thread = threading.Thread(target=send)
send_thread.start()
        
