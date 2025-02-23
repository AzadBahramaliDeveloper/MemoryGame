import tkinter as tk
import random
import pymongo

# MongoDB connection
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["memory_game_db"]
collection = db["game_results"]

# Global variables
sequence = []
shuffled_sequence = []
difficulty = 5  # Default difficulty


def start_game():
    global sequence, shuffled_sequence, difficulty
    difficulty = difficulty_var.get()
    sequence = [random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789") for _ in range(difficulty)]
    sequence_label.config(text=" ".join(sequence), fg="blue")
    root.after(3000, shuffle_sequence)


def shuffle_sequence():
    global shuffled_sequence
    shuffled_sequence = sequence[:]
    random.shuffle(shuffled_sequence)
    sequence_label.config(text=" ".join(shuffled_sequence), fg="black")


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
    collection.insert_one(game_result)

    if is_correct:
        result_label.config(text="✔ Correct!", fg="green")
    else:
        result_label.config(text="✖ Wrong! Try again.", fg="red")
    display_results()


def restart_game():
    user_input.delete(0, tk.END)
    result_label.config(text="")
    sequence_label.config(text="")


def display_results():
    results_label.config(text="Last 5 Attempts:")
    recent_attempts = collection.find().sort("_id", -1).limit(5)
    result_text = "\n".join(
        [f"{entry['original_sequence']} - {'✔' if entry['correct'] else '✖'}" for entry in recent_attempts])
    past_results.config(text=result_text)


# GUI Setup
root = tk.Tk()
root.title("Memory Game")
root.geometry("600x700")
root.configure(bg="#f0f0f0")

frame = tk.Frame(root, bg="#ffffff", padx=20, pady=20, relief="solid", borderwidth=2)
frame.pack(pady=30, padx=30)

label = tk.Label(frame, text="Memorize this sequence:", font=("Arial", 16, "bold"), bg="#ffffff")
label.pack(pady=10)

sequence_label = tk.Label(frame, text="", font=("Arial", 20, "bold"), bg="#e9ecef", width=30, height=2, relief="solid")
sequence_label.pack(pady=10)

difficulty_label = tk.Label(frame, text="Select Difficulty:", font=("Arial", 14), bg="#ffffff")
difficulty_label.pack(pady=5)

difficulty_var = tk.IntVar(value=5)
difficulty_menu = tk.OptionMenu(frame, difficulty_var, 3, 5, 7, 10)
difficulty_menu.config(font=("Arial", 12))
difficulty_menu.pack(pady=5)

start_button = tk.Button(frame, text="Start Game", command=start_game, bg="#28a745", fg="white",
                         font=("Arial", 14, "bold"), padx=30, pady=10, relief="raised")
start_button.pack(pady=15)

input_label = tk.Label(frame, text="Enter the original sequence:", font=("Arial", 16), bg="#ffffff")
input_label.pack(pady=10)

user_input = tk.Entry(frame, font=("Arial", 16), width=25, relief="solid", borderwidth=2)
user_input.pack(pady=10)

submit_button = tk.Button(frame, text="Submit", command=check_answer, bg="#007bff", fg="white",
                          font=("Arial", 14, "bold"), padx=30, pady=10, relief="raised")
submit_button.pack(pady=10)

restart_button = tk.Button(frame, text="Restart", command=restart_game, bg="#dc3545", fg="white",
                           font=("Arial", 14, "bold"), padx=30, pady=10, relief="raised")
restart_button.pack(pady=10)

result_label = tk.Label(frame, text="", font=("Arial", 16, "bold"), bg="#ffffff")
result_label.pack(pady=15)

results_label = tk.Label(frame, text="", font=("Arial", 14, "bold"), bg="#ffffff")
results_label.pack(pady=10)

past_results = tk.Label(frame, text="", font=("Arial", 12), bg="#e9ecef", width=45, height=6, relief="solid",
                        borderwidth=2)
past_results.pack(pady=10)

root.mainloop()
