import threading
import socket
import time

DISCONNECT_MESSAGE = "!dc"
encodeFormat = 'utf-8'
Authenticated = [False,True]

SERVER = ('127.0.0.1')
PORT = 5050
ADDR = (SERVER, PORT)

#regORlog = input("Register Or Login (r/l): ")
regORlog = ("l")

if  regORlog == 'r':
    NAME = input("Enter Username :")
    EMAIL = input("Enter Email: ")
    PASSWD = input("Enter Password: ")
elif regORlog == 'l':
    '''
    EMAIL = input("Enter Email: ")
    PASSWD = input("Enter Password: ")
    '''
    EMAIL = ("test@test.com")
    PASSWD = ("test")
else:
    print("Invalid Option.")
    exit()


try:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    print("Connection Successfull. Authenticating...")
    Authenticated[1] = True
except:
    print('Please retry with correct IP:PORT.')
else:
    pass

def client_receive():
    while True:
        try:
            message = client.recv(1024).decode(encodeFormat)
            
            if not message:
                raise socket.error("Lost Connection")
            
            elif message == "regORlog":
                client.send(regORlog.encode(encodeFormat))
            
            elif message == "NAME?":
                client.send(NAME.encode(encodeFormat))
                
            elif message == "EMAIL?":
                client.send(EMAIL.encode(encodeFormat))
                
            elif message == "PASSWD?":
                client.send(PASSWD.encode(encodeFormat))
                
            elif message == "AuthSuccessfull":
                Authenticated[0] = True
                print("You have successfully Authenticated. Getting you into the Lobby.")
                
                time.sleep(1)
                
                print("You have entered the Lobby!. Press enter to chat")
                
            else:
                print(message)
                
        except socket.error as msg:
            print(f"EXITED WITH ERROR: {msg} ")
            Authenticated[1] = False
            client.close()
            break
    return


def client_send():
    while Authenticated[1]:
        if Authenticated[0]:
            message = (input (''))
            
            try:
                client.send(message.encode(encodeFormat))
                if message == '!dc':
                    client.close()
                    break
                
            except socket.error as msg:
                print(f'Error Sending Message : {msg} ')
                break
    exit()

receive_thread = threading.Thread(target=client_receive, daemon=True)
receive_thread.start()

client_send()
