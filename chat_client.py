import socket
import threading
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog

nickname = input("Choose a nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 55555))

#Receiving messages from server
def receive():
    while True:
        #when receiving 'NICK', client knows to send nickname to server to show in chat
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'NICK':
                client.send(nickname.encode('utf-8'))
            else:
                print (message)
        except:
            print("An Error occurred!")
            client.close()
            break

#Client can either send message or close connection
def write():
    while True:
        message = f'{nickname}: {input("")}'
        client.send(message.encode('utf-8'))

#Setting the two threads running simultaneously
receive_thread = threading.Thread(target = receive)
receive_thread.start()

write_thread = threading.Thread(target = write)
write_thread.start()




