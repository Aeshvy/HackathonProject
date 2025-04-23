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

    def update_display(self):
        self.word_var.set(self.game.display_word())
        self.status_var.set(f"Attempts Left: {self.game.attempts_left}")

    def make_guess(self, event):
        guess = self.entry.get().strip()
        self.entry.delete(0, tk.END)

        if guess:
            result = self.game.guess(guess)
            self.status_var.set(result)
            self.update_display()

            if self.game.is_won():
                messagebox.showinfo("Hangman", f"You won! The word was: {self.game.word}")
                self.root.quit()
            elif self.game.is_lost():
                messagebox.showinfo("Hangman", f"You lost. The word was: {self.game.word}")
                self.root.quit()

    def show_hint(self):
        definition = get_definition(self.word)
        synonyms = get_synonyms(self.word)
        antonyms = get_antonyms(self.word)
        hint = f"{definition}\n{synonyms}\n{antonyms}"
        messagebox.showinfo("Hint", hint)

if __name__ == "__main__":
    root = tk.Tk()
    app = HangmanApp(root)
    root.mainloop()