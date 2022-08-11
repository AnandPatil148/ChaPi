import threading
import socket

SERVER = input('Target IP: ')
PORT = 5050
ADDR = (SERVER, PORT)
DISCONNECT_MESSAGE = "!dc"
NAME = input('Choose your name >>> ')

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def client_receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == "NAME?":
                client.send(NAME.encode('utf-8'))
            else:
                print(message)
        except:
            print('Error!')
            client.close()
            break


def client_send():
    while True:
        message = (input (f'msg>>> '))
        send_msg = (f'{NAME}: {message}')
        client.send(send_msg.encode('utf-8'))
        if message == DISCONNECT_MESSAGE:
            client.close()
            break


receive_thread = threading.Thread(target=client_receive)
receive_thread.start()

send_thread = threading.Thread(target=client_send)
send_thread.start()
