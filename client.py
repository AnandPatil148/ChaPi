import threading
import socket
import time

DISCONNECT_MESSAGE = "!dc"
Authenticated = [False]

INPUT = input('TARGET_IP:PORT -> ')
SERVER = INPUT.split(':')[0]
PORT = int(INPUT.split(':')[1])
ADDR = (SERVER, PORT)
EMAIL = input("Enter Email: ")
PASSWD = input("Enter Password: ")

try:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    print("Connection Successfull. Authentication...")
except:
    print('Please retry with correct IP:PORT.')
else:
    pass

def client_receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            
            if message == "EMAIL?":
                client.send(EMAIL.encode('utf-8'))
                
            elif message == "PASSWD?":
                client.send(PASSWD.encode('utf-8'))
                
            elif message == "AuthSuccessfull":
                Authenticated[0] = True
                print("You have successfully Authenticated. Getting you into the Lobby.")
                
                time.sleep(1)
                
                print("You have entered the Lobby!. Press enter to chat")
                
            else:
                print(message)
        except socket.error as msg:
            print(f"EXITED WITH ERROR: {msg} ")
            Authenticated[0] = False
            client.close()
            break
    return


def client_send():
    while True:
        
        if Authenticated[0]:
            message = (input (''))
            try:
                client.send(message.encode('utf-8'))
                if message == '!dc':
                    client.close()
                    break
            except socket.error as msg:
                print(f'Error Sending Message : {msg} ')
                break
    return

receive_thread = threading.Thread(target=client_receive, daemon=True)
receive_thread.start()

client_send()

#send_thread = threading.Thread(target=client_send)
#send_thread.start()