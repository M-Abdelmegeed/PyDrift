import socket
from _thread import *
from player import Player
import pickle
import time

size = width, height = (600, 600)
road_width = int(width / 1.5)
server = "192.168.70.192"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(3)
print("Waiting for a connection, Server Started")


players = [
    Player(width / 2 - road_width / 6 - 75, height * 0.8, 50, 50, (255, 0, 0), "lambo"),
    Player(width / 2 - 25, height * 0.8, 50, 50, (0, 255, 0), "mclaren"),
    Player(
        width / 2 + road_width / 6 + 25, height * 0.8, 50, 50, (0, 255, 255), "corvette"
    ),
]


def threaded_client(conn, player):
    global no_of_connections
    global game_time
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
                    reply = {
                        "Opponent 1": players[0],
                        "Opponent 2": players[2],
                        "Connections": no_of_connections,
                        "Game Time": game_time,
                    }
                elif player == 0:
                    reply = {
                        "Opponent 1": players[1],
                        "Opponent 2": players[2],
                        "Connections": no_of_connections,
                        "Game Time": game_time,
                    }
                else:
                    reply = {
                        "Opponent 1": players[0],
                        "Opponent 2": players[1],
                        "Connections": no_of_connections,
                        "Game Time": game_time,
                    }

                print("Received: ", data)
                print("Sending : ", reply)

            conn.sendall(pickle.dumps(reply))
        except:
            break

    print("Lost connection")
    conn.close()


def timer():
    while True:
        global game_time
        game_time += 1
        time.sleep(1)


no_of_connections = 0
currentPlayer = 0
game_time = 0

while True:
    conn, addr = s.accept()
    print("Connected to:", addr)
    no_of_connections += 1
    if no_of_connections == 3:
        start_new_thread(timer, ())
    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1
