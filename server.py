import socket
from _thread import *
from player import Player
from dotenv import load_dotenv
from pymongo import MongoClient
import pickle
import random
import time
import math
import os

# Load connection string and connect to the database
load_dotenv()
mongodb_connection_string = os.getenv("MONGODB_CONNECTION_STRING")
client = MongoClient(mongodb_connection_string)
db = client["DB1"]
scores_collection = "Scores"
sessions_collection = "Sessions"


size = width, height = (600, 600)
road_width = int(width / 1.5)
roadmark_width = int(width / 90)
server = "192.168.1.21"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(3)
print("Waiting for a connection, Server Started")

gameID = 0
games = []
idCount = 0

players = [
    Player(width / 2 - road_width / 6 - 75, height * 0.8, 50, 50, (255, 0, 0), "lambo"),
    Player(width / 2 - 25, height * 0.8, 50, 50, (0, 255, 0), "mclaren"),
    Player(
        width / 2 + road_width / 6 + 25, height * 0.8, 50, 50, (0, 255, 255), "corvette"
    ),
]


def threaded_client(conn, player, gameID, games):
    global game_connections
    global idCount
    global no_of_connections
    global game_time
    conn.send(pickle.dumps({"gameID": gameID, "player": games[gameID][player]}))
    reply = ""
    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            random_int = random.randint(
                width / 2 - road_width / 2 + roadmark_width * 2 - 6,
                width / 2 + road_width / 2 - roadmark_width * 2 - 25,
            )
            # print("Data:", data)
            games[gameID][player] = data[gameID]["loc"]
            if data[gameID]["crashed"]:
                games[gameID][player] = ""
            if not data:
                print("Disconnected")
                break
            else:
                if player == 1:
                    if (games[gameID][0] == "") and (games[gameID][2] == ""):
                        reply = {
                            gameID: {
                                "Opponent 1": games[gameID][0],
                                "Opponent 2": games[gameID][2],
                                "Connections": game_connections[gameID],
                                "Game Time": game_time,
                                "won": True,
                                "Obstacle Center": (random_int, 0),
                            }
                        }
                    else:
                        reply = {
                            gameID: {
                                "Opponent 1": games[gameID][0],
                                "Opponent 2": games[gameID][2],
                                "Connections": game_connections[gameID],
                                "Game Time": game_time,
                                "won": False,
                                "Obstacle Center": (random_int, 0),
                            }
                        }
                elif player == 0:
                    if (games[gameID][1] == "") and (games[gameID][2] == ""):
                        reply = {
                            gameID: {
                                "Opponent 1": games[gameID][1],
                                "Opponent 2": games[gameID][2],
                                "Connections": game_connections[gameID],
                                "Game Time": game_time,
                                "won": True,
                                "Obstacle Center": (random_int, 0),
                            }
                        }
                    else:
                        reply = {
                            gameID: {
                                "Opponent 1": games[gameID][1],
                                "Opponent 2": games[gameID][2],
                                "Connections": game_connections[gameID],
                                "Game Time": game_time,
                                "won": False,
                                "Obstacle Center": (random_int, 0),
                            }
                        }
                else:
                    if (games[gameID][0] == "") and (games[gameID][1] == ""):
                        reply = {
                            gameID: {
                                "Opponent 1": games[gameID][0],
                                "Opponent 2": games[gameID][1],
                                "Connections": game_connections[gameID],
                                "Game Time": game_time,
                                "won": True,
                                "Obstacle Center": (random_int, 0),
                            }
                        }
                    else:
                        reply = {
                            gameID: {
                                "Opponent 1": games[gameID][0],
                                "Opponent 2": games[gameID][1],
                                "Connections": game_connections[gameID],
                                "Game Time": game_time,
                                "won": False,
                                "Obstacle Center": (random_int, 0),
                            }
                        }

            conn.sendall(pickle.dumps(reply))
        except:
            break

    print("Lost connection")
    try:
        no_of_connections -= 1
        del game_connections[gameID]
        del games[gameID]
        print("Games:", games)
        print("Closing Game", gameID)
    except:
        pass
    conn.close()


def timer():
    while True:
        global game_time
        game_time += 1
        time.sleep(1)


no_of_connections = 0
currentPlayer = 0
game_time = 0
total_connections = 0
game_connections = []

while True:
    conn, addr = s.accept()
    print("Connected to:", addr)
    total_connections += 1
    no_of_connections += 1
    if (no_of_connections % 3) == 1:
        games.append(players[:])
        print("Games list", games)
        gameID += 1
        print("Game connections", game_connections)
        print("Current game id:", gameID)
        start_new_thread(timer, ())
        game_connections.append(0)
        print("Current Connections:", total_connections)
    game_connections[math.ceil(no_of_connections / 3) - 1] += 1

    start_new_thread(
        threaded_client,
        (conn, currentPlayer % 3, math.ceil(no_of_connections / 3) - 1, games),
    )
    currentPlayer += 1
