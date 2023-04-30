import socket
from _thread import *
from player import Player
import pickle

size = width , height = (600,600)
road_width=int(width/1.5)
server = "192.168.1.21"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(3)
print("Waiting for a connection, Server Started")


players = [Player(width/2 - road_width/6 -75 ,height*0.8,50,50,(255,0,0),"lambo"),
           Player(width/2 -25,height*0.8, 50,50, (0,255,0),"mclaren"),
           Player(width/2 +road_width/6 +25 ,height*0.8, 50,50, (0,255,255),"corvette")]

def threaded_client(conn, player):
    conn.send(pickle.dumps(players[player]))
    reply = ""
    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            players[player] = data

            if not data:
                print("Disconnected")
                break
            else:
                if player == 1:
                    reply = [players[0],players[2]]
                elif player == 0:
                    reply = [players[1],players[2]]
                else:
                    reply = [players[0],players[1]]

                print("Received: ", data)
                print("Sending : ", reply)

            conn.sendall(pickle.dumps(reply))
        except:
            break

    print("Lost connection")
    conn.close()

currentPlayer = 0
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1