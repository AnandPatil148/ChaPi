from BlockChain import *
import mysql.connector 
import json
import secrets
import socket
import threading
import datetime
from uuid import uuid4

# Server Related Variables
encodeFormat = 'utf-8'
SERVER = ('127.0.0.1')
PORT = 6969

ADDR = (SERVER, PORT)

#Can be changed later
Node_User = 'Anand'

# Set up the database connection
host = 'localhost' 
port = 3306
username = 'server'
password = 'server'
loginDatabase = 'login'
roomDatabase = 'roomdata'

#Connect to mysql server 
conn = mysql.connector.connect(host=host, port=port, user=username, passwd=password)

cursor = conn.cursor(buffered=True)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
server.listen()
print(f"[LISTENING] BlockChain Server is listening on {SERVER}:{PORT}...")

SERVERS = []
NODES = []

Orbit = Blockchain()
Orbit.create_room_genesis_block("Test", Node_User)
Orbit.load_wallets("wallets.json")
Orbit.load_chain("chain.json")



def commands():
    print("Commands Initiated")
    while True:
        cmd = input('')
        if cmd == '!VC':
            print( json.dumps(Orbit.to_dict(), indent= 4) )
        elif cmd == '!stop':
            for server in SERVERS:
                server.close()
            quit()

#Hashes Password
def hash_password(passwordToHash:str, salt=None):
    if salt is None:
        salt = secrets.token_bytes(16)  # Generate a random 16-byte salt
    
    # Combine the password and salt, then hash
    hashed_password = hashlib.sha256(passwordToHash.encode() + salt).hexdigest()
    
    return hashed_password, salt

# Verifies password
def check_password(passwordToCheck, storedHashOfPassword, storedSalt):
    # Use the same process to hash the given password,
    # and compare it with the stored password
    generated_new_hash = hash_password(passwordToCheck, storedSalt)[0]
    return generated_new_hash == storedHashOfPassword

# Function to handle SERVERS' connection
def HandleServer(SERVER: socket.socket, addr):
    while True:
        try:
            dataString = SERVER.recv(1024).decode()
            print(f"{addr} : {dataString}")
            
            # Sends message back to client
            
            if not dataString:
                raise socket.error("Disconnected")
            
            # Splitting Data String into Command & Arguments
            
            # GET Block from BlockChain 
            if dataString.startswith("GET"):
                blocktoget = dataString.split(" ")[1]
                roomname = dataString.split(" ")[3]
                
                data = Orbit.get_block(int(blocktoget), roomname) #Data of one Block in form of dict
                
                    
                # Send back the Data in JSON Formated string
                dataString = json.dumps(data) #convert to JSON Formated string
                SERVER.send(dataString.encode(encodeFormat)) #sends the data to the SERVER
                print(f"Data Sent To SERVER {addr}")
                continue
            
            elif dataString.startswith("AUTH"):
                sub_command = dataString.split(" ")[1]
                
                if sub_command == "LOGIN":
                    
                    # User tries to login with username and password
                    auth_data = json.loads(dataString.split("!")[1]) #Getting the user credentials from message
                    NAME = auth_data["NAME"]
                    PASSWD = auth_data["PASSWD"]
                    
                    try:
            
                        query = f"SELECT * FROM login.info WHERE NAME='{NAME}';"  
                        cursor.execute(query)

                        data = cursor.fetchone()

                        if not data:
                            raise Exception ("Account Not Found. Please Signup")

                        if not check_password(PASSWD, data[3], data[4]):
                            raise Exception ("Incorrect username or password.")
                        
                        response_data = json.dumps({
                            "USERID": data[0],
                            "NAME": data[1],
                            "EMAIL": data[2],
                            "ROOMS": data[5],
                            })
                        
                        SERVER.send(f"AUTH OK !{response_data}".encode())
                        
                    except Exception as e:
                        print(e)
                        eD = json.dumps({
                            "ERROR": str(e),
                            }) 
                        SERVER.send(f"AUTH ERROR !{eD}".encode())
                        continue
                    
                elif sub_command == "REGISTER":
                    
                    auth_data = json.loads(dataString.split("!")[1]) #Getting the user credentials from message
                    
                    NAME = auth_data["NAME"]
                    EMAIL = auth_data["EMAIL"]
                    PASSWD = auth_data["PASSWD"]
                    hashed_PASSWD, saltOf_PASSWD = hash_password(PASSWD)
                    
                    # Create new User
                    try:
                        # Check if Username already exists
                        query = "INSERT INTO login.info (NAME,EMAIL,PASSWD,SALT)  VALUES(%s,%s,%s,%s)"
                        data = (NAME, EMAIL, hashed_PASSWD, saltOf_PASSWD)
                        cursor.execute(query,data)
                        conn.commit()
                        
                        response_data = json.dumps({
                            "ERROR": None
                        })
                        
                        SERVER.send(f"AUTH OK !{response_data}".encode())
                        
                    except mysql.connector.Error as err:
                        #
                        print("Failed to insert into MySQL table {}".format(err))
                        
                        response_data = {"ERROR":"User with this username or email already exists."}
                        SERVER.send(f"AUTH ERROR !{json.dumps(response_data)}".encode())
                        
                        continue
                
                elif sub_command == "EMAIL_UPDATE":
                    
                    # User tries to login with username and password
                    auth_data = json.loads(dataString.split("!")[1]) #Getting the new EMAIL credential from message
                    EMAIL = auth_data["EMAIL"]
                    USERID = auth_data["USERID"]
                    
                    try:
                        
                        query = "UPDATE login.info SET EMAIL=%s WHERE ID=%s"
                        params = (EMAIL, USERID)
                        cursor.execute(query,params)
                        conn.commit()
                        
                        response_data = json.dumps({
                            "ERROR": None
                        })
                        SERVER.send(f"AUTH OK !{response_data}".encode())
                        
                    except Exception as e:
                        response_data = json.dumps({
                            "ERROR": str(e)
                        })
                        SERVER.send(f"AUTH ERROR !{response_data}".encode())
                
                else:
                    response_data = {
                        'ERROR': 'Unknown command'
                    }
                    SERVER.send(f"AUTH ERROR !{json.dumps(response_data)}".encode())
            
            else:
                #print(dataString)
                data = json.loads(dataString) #data is a disctionary here

                block = Block(len(Orbit.chain), data.get("TimeStamp"), data, Node_User)
                Orbit.add_block(block, roomBlockOrNot=False)
            '''
            # Mintes a block on the Blockchain
            elif dataString.startswith("MINT"):
                block_data = dataString.split(" ")[1]
                data = json.loads(block_data) #data is a disctionary here

                block = Block(len(Orbit.chain), data.get("TimeStamp"), data)
                Orbit.add_block(block, roomBlockOrNot=False)
            '''
            
        except socket.error as msg:
            print (f'{SERVER.getpeername()} has disconnected ')      
            SERVERS.remove(SERVER)
            SERVER.close()
            break
    return

# Main function to receive the SERVER connections
def receive():
    while True:
        
        SERVER, address = server.accept()
        print(f'Connection is established with {str(address)}')
        try:
            
            SERVERS.append(SERVER)
            
            thread = threading.Thread(target=HandleServer, args=(SERVER, address), daemon=True)
            thread.start()
            
        except socket.error:
            print(f"{str(address)} DISCONNECTED WITH {address} WITH ERROR : {socket.error}")



def startservers():
    cmd_thread = threading.Thread(target=commands)
    cmd_thread.start()
    
    receive_thread = threading.Thread(target=receive)
    receive_thread.start()
    
startservers()


