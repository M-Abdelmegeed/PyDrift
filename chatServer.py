import socket
import threading

#creating another server for the chat room different to the game server for operations
#to be decenteralized and to run smoothly and be more reliable


#setting TCP connection for chat
# host = "127.0.0.1"
host = "13.51.197.208"
port = 3250

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host,port))
server.listen()

#creating list of clients and their chosen names that will appear in chat
clients = []
names = []

#To broadcast messages to all clients
def broadcast(message):
    for client in clients:
        client.send(message)


#handling each client when they connect and disconnect
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            print(f"{names[clients.index(client)]} says {message}")
            broadcast(message)

        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            name = names[index]
            broadcast(f'{name} left the chat!'.encode('utf-8'))
            names.remove(name)
            break



def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        #first thing is receive client's name and append it to this game's names list
        client.send('NAME'.encode('utf-8'))
        name = client.recv(1024).decode('utf-8')
        names.append(name)
        clients.append(client)

        print(f'name of the client is {name}!')
        broadcast(f'{name} joined the chat'.encode('utf-8'))
        client.send('Connected to the server!'.encode('utf-8'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()



print("Server is listening...")
receive()

