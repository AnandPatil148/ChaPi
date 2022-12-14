#server.py

import threading
import socket
import time

IP = input('SERVER_IP:PORT -> ')
IP_LIST  = IP.split(':')
SERVER = IP_LIST[0]
PORT = int(IP_LIST[1])
ADDR = (SERVER, PORT)
DISCONNECT_MESSAGE = "!dc"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
print(f"[LISTENING] Server is listening on {SERVER}:{PORT}...")

CLIENTS = []
NAMES = []


def broadcast(message):
    for CLIENT in CLIENTS:
        send_msg = message.encode('utf-8')
        CLIENT.send(send_msg)

# Function to handle CLIENTS'connections


def handle_client(CLIENT, NAME):
    while True:
        try:
            message = CLIENT.recv(1024).decode('utf-8')
            broadcast(message)
            print (message)
        except:
            CLIENTS.remove(CLIENT)
            broadcast(f'{NAME} has left the chat room!')  
            print (f'{NAME} has disconnected')      
            NAMES.remove(NAME)
            CLIENT.close()
            break
    return

# Main function to receive the CLIENTS connection

def receive():
    server.listen()
    while True:
        
        CLIENT, address = server.accept()
        print(f'Connection is established with {str(address)}')
        CLIENT.send('Your have successfully connected. Getting you into the chating channel.'.encode('utf-8'))
        
        time.sleep(1)
        
        CLIENT.send('NAME?'.encode('utf-8'))
        NAME = CLIENT.recv(1024).decode('utf-8')
        NAMES.append(NAME)
        CLIENTS.append(CLIENT)
        
        time.sleep(3)
        
        print(f'The NAME of {str(address)} is {NAME}')
        
        CLIENT.send('\nYou have entered chat room!. Press enter to chat'.encode('utf-8'))
        broadcast(f'\n{NAME} has connected to the chat room. Welcome them!! :)\n')
        
        thread = threading.Thread(target=handle_client, args=(CLIENT, NAME))
        thread.daemon = True
        thread.start()
        print(f"[ACTIVE CONNECTIONS]: {threading.active_count()} (including main thread)")


receive()