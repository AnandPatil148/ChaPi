#server.py

import threading
import socket


SERVER = input('Server IP: ')
PORT = 5050
ADDR = (SERVER, PORT)
DISCONNECT_MESSAGE = "!dc"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
server.listen()
print(f"[LISTENING] Server is listening on {SERVER}:{PORT}...")

CLIENTS = []
NAMES = []


def broadcast(message):
    for CLIENT in CLIENTS:
        send_msg = message.encode('utf-8')
        CLIENT.send(send_msg)

# Function to handle CLIENTS'connections


def handle_client(CLIENT):
    while True:
        try:
            message = CLIENT.recv(1024).decode('utf-8')
            broadcast(message)
            print (message)
        except:
            index = CLIENTS.index(CLIENT)
            CLIENTS.remove(CLIENT)
            NAME = NAMES[index]   
            broadcast(f'{NAME} has left the chat room!')  
            print (f'{NAME} has disconnected')      
            NAMES.remove(NAME)
            CLIENT.close()
            break

# Main function to receive the CLIENTS connection

def receive():
    while True:
        
        CLIENT, address = server.accept()
        print(f'Connection is established with {str(address)}')
        CLIENT.send('NAME?'.encode('utf-8'))
        NAME = CLIENT.recv(1024).decode('utf-8')
        NAMES.append(NAME)
        CLIENTS.append(CLIENT)
        print(f'The NAME of {str(address)} is {NAME}')
        broadcast(f'\n{NAME} has connected to the chat room. Press enter to chat with them')
        CLIENT.send('You are now connected!. Press enter to chat'.encode('utf-8'))
        thread = threading.Thread(target=handle_client, args=(CLIENT,))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

if __name__ == "__main__":
    receive()
