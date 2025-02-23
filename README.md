# Memory-Game
This is a memory game built with Python, Tkinter, and MongoDB. The game challenges players to memorize a randomly generated sequence and recall it correctly. The last 5 attempts are stored in a MongoDB database.

# Features
Select a difficulty level: 3, 5, 7, or 10 characters
Display a random sequence for 3 seconds
Shuffle the sequence for a challenge
Enter the correct sequence to win
Stores the last 5 attempts in MongoDB
# Requirements
To run this game, you need:

Python 3.x
Tkinter (for the GUI)
pymongo (for MongoDB connection)
MongoDB (running locally or remotely)

# Installation & Setup
1- Clone the Repository
sh
git clone https://github.com/AzadBahramaliDeveloper/Memory-Game.git
cd memory-game

2- Install Dependencies
sh
pip install pymongo

3- Start MongoDB
- If using a local MongoDB, start it with:
sh
mongod

- If using MongoDB Atlas, update the MongoDB URI in memory_game.py:

python
client = pymongo.MongoClient("your-mongodb-connection-uri")

4- Run the Game

sh
python memory_game.py