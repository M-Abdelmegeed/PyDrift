from dotenv import load_dotenv
from pymongo import MongoClient
from datetime import datetime
import os
import random


load_dotenv()
mongodb_connection_string = os.getenv("MONGODB_CONNECTION_STRING")
client = MongoClient(mongodb_connection_string, maxPoolSize=6)
db = client["DB1"]
scores_collection = db["Scores"]
sessions_collection = db["Sessions"]


def insertSession(players):
    sessions_collection.insert_one(
        {
            "sessionID": random.randint(1000, 9999),
            "player1": players[0],
            "player2": players[1],
            "player3": players[2],
        }
    )


def updateHighScore(documentID, playerName, score):
    new_data = {
        "$set": {
            "name": playerName,
            "score": score,
        }
    }
    scores_collection.update_one({"_id": documentID}, new_data)
