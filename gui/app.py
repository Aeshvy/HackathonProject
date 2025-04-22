import tkinter as tk
from tkinter import messagebox
from game.hangman import HangmanGame
from game.player import Player
from game.game_dictionary import get_definition
from game.datamuse_api import get_synonyms, get_antonyms
import json
import random

WORDLIST_PATH = "data/words.json"

def load_words():
    with open(WORDLIST_PATH, "r") as file:
        return json.load(file)
    
class HangmanApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hangman")
        self.player = Player()
        self.words = load_words()
        self.word = random.choice(self.words)
        self.game = HangmanGame(self.word)
        self.word_var = tk.StringVar()
        self.status_var = tk.StringVar()

        self.update_display()
        self.build_ui()

    def build_ui(self):
        tk.Label(self.root, text=f"Welcome, {self.player.name}!", font=("Helvetica", 16)).pack(pady=10)

        self.word_label = tk.Label(self.root, textvariable=self.word_var, font=("Courier", 24))
        self.word_label.pack(pady=10)

        self.entry = tk.Entry(self.root)
        self.entry.pack()
        self.entry.bind("<Return>", self.make_guess)

        self.status_label = tk.Label(self.root, textvariable=self.status_var)
        self.status_label.pack(pady=5)

        tk.Button(self.root, text="Hint", command=self.show_hint).pack(pady=5)