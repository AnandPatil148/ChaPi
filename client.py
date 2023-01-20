import PySimpleGUI as sg
import os, sys
import threading
import socket
import time

sg.theme('DarkAmber')

MsgList = []
connected = False
recieveThreadStart = False
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


serverNotFoundError = 'Could Not connect to server. \n Please Try again with proper server IP'
recieverCouldNotStart = 'The reciever thread already present, cant start another one'
connectedTrue = 'Already connected'
connectedFalse = 'Not connected to any server'



def connectToServer(ADDR):
        try:
            client.connect(ADDR)
        except socket.error:
            return
        #return self.client

def client_receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == "NAME?":
                client.send(NAME.encode('utf-8'))
            else:
                MsgList.append(message)
                window['-ML-'].update(MsgList)
        except:
            client.close()
            break



file_list_column = [[sg.Text('Name : '), sg.In(size = (25, 1), key = '-ID-')],
                    [sg.Text('Server IP (ip_address:port) : '), sg.In(size = (25, 1), key = '-IP-')],
                    [sg.Button('Connect')],
                    [sg.Text('Msg -> '), sg.In(size = (25, 1), do_not_clear=False, key = '-MSG-')],
                    [sg.Button('Send')],
                    [sg.Listbox(MsgList, size = (100, 10), key = '-ML-',)],
                    [sg.Button('Close')]]

layout = [[sg.Column(file_list_column)],]

window = sg.Window('Client', layout, resizable=True, finalize=True)

while True:
    
    event, values = window.read()
    
    
    if event == 'Close' or event == sg.WIN_CLOSED or event == 'Exit':
        if connected:
            client.close()
        break
        
    if event == 'Connect':
        
        
        if connected == False:
            try:
                NAME = str(values['-ID-']) 
                IP_LIST = values['-IP-'].split(':')
                SERVER = IP_LIST[0]
                PORT = int(IP_LIST[1])
                ADDR = (SERVER, PORT)

                connectToServer(ADDR)
                connected = True
                recieveThreadStart = True

            except:
                MsgList.append(serverNotFoundError)
                window['-ML-'].update(MsgList)
                recieveThreadStart = False
                connected = False
                
        else:
            MsgList.append(connectedTrue)
            window['-ML-'].update(MsgList)
            
        if recieveThreadStart:
            try:
                recieve_thread = threading.Thread(target=client_receive)
                recieve_thread.start()
                recieveThreadStart = False
            except:
                MsgList.append(recieverCouldNotStart)
                window['-ML-'].update(MsgList)
                recieveThreadStart = False
        
               
    if event == 'Send':
        if connected == True:
            
            msg = str(values['-MSG-'])
            
            if msg != '':
                send_msg = (f'{NAME}: {msg}')
                client.send(send_msg.encode('utf-8'))
                if msg == "!dc":
                    time.sleep(1)
                    client.close()
                    connected = False
            else:
                pass
        
        else:
            MsgList.append(connectedFalse)
            window['-ML-'].update(MsgList)
    
    window['-ML-'].update(MsgList)
    
window.close()