import server
import threading

receiveThread = threading.Thread(target=server.receive, daemon=True)
receiveThread.start()

server.commands()