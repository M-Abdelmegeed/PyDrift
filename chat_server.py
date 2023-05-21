import socket
import threading

#creating another server for the chat room different to the game server for operations
#to be decenteralized and to run smoothly and be more reliable


#setting TCP connection for chat
host = "127.0.0.1"
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host,port))
server.listen()

#creating list of clients and their chosen nicknames that will appear in chat
clients = []
nicknames = []

#To broadcast messages to all clients
def broadcast(message):
    for client in clients:
        client.send(message)


#handling each client when they connect and disconnect
def handle(client):
    while True:

        try:
            message = client.recv(1024)
            broadcast(message)

        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} left the chat!'.encode('utf-8'))
            nicknames.remove(nickname)
            break



def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        #first thing is receive client's nickname and append it to this game's nicknames list
        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)

        print(f'Nickname of the client is {nickname}!')
        broadcast(f'{nickname} joined the chat'.encode('utf-8'))
        client.send('Connected to the server!'.encode('utf-8'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()



print("Server is listening...")
receive()

