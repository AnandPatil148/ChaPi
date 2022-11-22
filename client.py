import threading
import socket
import time

IP = input('TARGET_IP:PORT -> ')
IP_LIST  = IP.split(':')
SERVER = IP_LIST[0]
PORT = int(IP_LIST[1])
ADDR = (SERVER, PORT)
DISCONNECT_MESSAGE = "!dc"
NAME = input('Choose your name >>> ')

try:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
except:
    print('Please retry with correct IP:PORT.')
else:
    pass

def client_receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == "NAME?":
                client.send(NAME.encode('utf-8'))
            else:
                print(message)
        except:
            client.close()
            break
    return


def client_send():
    while True:
        message = (input (''))
        send_msg = (f'{NAME}: {message}')
        client.send(send_msg.encode('utf-8'))
        if message == '!dc':
            client.close()
            break
    return

receive_thread = threading.Thread(target=client_receive)
receive_thread.start()

send_thread = threading.Thread(target=client_send)
send_thread.start()