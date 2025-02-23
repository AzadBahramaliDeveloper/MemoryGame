import tkinter as tk
import random
#import pymongo

# MongoDB connection
"""client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["memory_game_db"]
collection = db["game_results"]"""

# Global variables
sequence = []
shuffled_sequence = []
difficulty = 5  # Default difficulty


def start_game():
    global sequence, shuffled_sequence, difficulty
    difficulty = difficulty_var.get()
    sequence = [random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789") for _ in range(difficulty)]
    sequence_label.config(text=" ".join(sequence))
    root.after(3000, shuffle_sequence)


def shuffle_sequence():
    global shuffled_sequence
    shuffled_sequence = sequence[:]
    random.shuffle(shuffled_sequence)
    sequence_label.config(text=" ".join(shuffled_sequence))


def check_answer():
    user_answer = user_input.get().strip().upper().replace(" ", "")
    correct_answer = "".join(sequence)
    is_correct = user_answer == correct_answer

    # Save result to MongoDB
    game_result = {
        "original_sequence": " ".join(sequence),
        "user_attempt": " ".join(user_answer),
        "correct": is_correct
    }
    #collection.insert_one(game_result)

    if is_correct:
        result_label.config(text="Correct!", fg="green")
    else:
        result_label.config(text="Wrong! Try again.", fg="red")


# GUI Setup
root = tk.Tk()
root.title("Memory Game")

label = tk.Label(root, text="Memorize this sequence:", font=("Arial", 14))
label.pack()

sequence_label = tk.Label(root, text="", font=("Arial", 16, "bold"))
sequence_label.pack()

difficulty_label = tk.Label(root, text="Select Difficulty:", font=("Arial", 12))
difficulty_label.pack()

difficulty_var = tk.IntVar(value=5)
difficulty_menu = tk.OptionMenu(root, difficulty_var, 3, 5, 7, 10)
difficulty_menu.pack()

start_button = tk.Button(root, text="Start Game", command=start_game)
start_button.pack()

input_label = tk.Label(root, text="Enter the original sequence:", font=("Arial", 14))
input_label.pack()

user_input = tk.Entry(root, font=("Arial", 14))
user_input.pack()

submit_button = tk.Button(root, text="Submit", command=check_answer)
submit_button.pack()

result_label = tk.Label(root, text="", font=("Arial", 14))
result_label.pack()

root.mainloop()
