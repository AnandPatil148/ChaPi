#client.py

import socket

HEADER = 64
PORT = 5050
SERVER = input('Target IP: ')
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!dc"
NAME = str(input('Name:'))

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg, name):
    Ename = name.encode(FORMAT)
    name_length = len(Ename)
    send_Nlength = str(name_length).encode(FORMAT)
    send_Nlength += b' ' * (HEADER - len(send_Nlength))

    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))

    client.send(send_Nlength)
    client.send(Ename)
    client.send(send_length)
    client.send(message)


while True:
    MSG = input ('%s: '%(NAME))
    if MSG == DISCONNECT_MESSAGE:
        connected = False
    send(MSG, NAME)

