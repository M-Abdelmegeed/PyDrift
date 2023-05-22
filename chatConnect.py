import socket
import threading


class ChatClient:
    def __init__(self):
        PORT = 55555
        SERVER = "127.0.0.1"
        ADDRESS = (SERVER, PORT)
        
        # Create a new client socket
        # and connect to the server
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(ADDRESS)
    
 