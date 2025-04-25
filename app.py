import tkinter as tk
import json
import random
from tkinter import messagebox
from game.hangman import HangmanGame
from game.player import Player
from game.game_dictionary import get_definition
from game.datamuse_api import get_synonyms, get_antonyms
from game.utils import save_result_file, save_result_db
from game.hangmanpics import HANGMAN_PICS
from game.main_menu import build_main_menu

WORDLIST_PATH = "data/word_categories.json"

def load_words_from_category(category=None):
    """
    Loads the word list from the JSON file.
    If a category is specified, returns only words in that category.
    Otherwise, returns the entire dictionary.
    """
    with open(WORDLIST_PATH, "r") as file:
        data = json.load(file)
        return data if category is None else data.get(category, [])


class HangmanApp:
    def __init__(self, root):
        """
        Initializes the Hangman application with root window, player,
        and loads categorized words. Starts at the main menu.
        """
        self.root = root
        self.root.geometry("1280x720")
        self.root.title("Hangman")
        self.player = Player()
        self.words_by_category = load_words_from_category()
        self.selected_category = None

        build_main_menu(self)

    def start_game(self):
        """
        Starts the game by displaying the category selection screen.
        """
        self.show_category_selection()

    def show_category_selection(self):
        """
        Displays buttons for each category that the player can choose from.
        """
        self.clear_window()
        tk.Label(self.root, text="Choose a Category", font=("Helvetica", 20)).pack(pady=20)

        for category in self.words_by_category.keys():
            tk.Button(self.root, text=category, font=("Helvetica", 16),
                      command=lambda c=category: self.begin_game_with_category(c)).pack(pady=10)

        tk.Button(self.root, text="Back to Menu", command=lambda: build_main_menu(self),
                  font=("Helvetica", 14)).pack(pady=20)

    def begin_game_with_category(self, category):
        """
        Starts a new HangmanGame using a random word from the chosen category.
        Initializes game state and UI components.
        """
        self.selected_category = category
        words = self.words_by_category.get(category, [])
        if not words:
            messagebox.showerror("Error", f"No words found for category: {category}")
            return

        self.game = HangmanGame(random.choice(words).lower())
        self.word_var = tk.StringVar()
        self.status_var = tk.StringVar()
        self.hint_var = tk.StringVar()
        self.hangman_var = tk.StringVar()
        self.build_game_ui()
        self.update_display()

    def build_game_ui(self):
        """
        Constructs the UI for the active game view: word display, input,
        guess button, hangman drawing, hints, and navigation.
        """
        self.clear_window()
        tk.Label(self.root, text=f"Category: {self.selected_category}", font=("Helvetica", 16)).pack(pady=10)
        tk.Label(self.root, text=f"Player: {self.player.name}", font=("Helvetica", 14)).pack()

        self.word_label = tk.Label(self.root, textvariable=self.word_var, font=("Courier", 24))
        self.word_label.pack(pady=10)

        self.hangman_label = tk.Label(self.root, textvariable=self.hangman_var, font=("Courier", 14), justify="left")
        self.hangman_label.pack()

        self.entry = tk.Entry(self.root)
        self.entry.pack(pady=5)

        self.guess_button = tk.Button(self.root, text="Guess", command=self.make_guess)
        self.guess_button.pack(pady=5)

        self.status_label = tk.Label(self.root, textvariable=self.status_var)
        self.status_label.pack(pady=5)

        tk.Button(self.root, text="Hint", command=self.show_hint).pack(pady=5)
        self.hint_label = tk.Label(self.root, textvariable=self.hint_var, wraplength=400, justify="left")
        self.hint_label.pack(pady=10)

        tk.Button(self.root, text="Back to Menu", command=lambda: build_main_menu(self), font=("Helvetica", 14)).pack(pady=10)

    def update_display(self):
        """
        Updates the word display and hangman drawing based on current game state.
        """
        self.word_var.set(self.game.display_word())
        self.hangman_var.set(HANGMAN_PICS[6 - self.game.attempts_left])

    def make_guess(self):
        """
        Handles player's letter guess, updates game status, checks for win/loss,
        and saves results if the game ends.
        """
        guess = self.entry.get().strip().lower()
        self.entry.delete(0, tk.END)

        if not guess.isalpha() or len(guess) != 1:
            self.status_var.set("Please enter a single letter (A-Z).")
            return

        result = self.game.guess(guess)
        self.status_var.set(f"{result} | Attempts Left: {self.game.attempts_left}")
        self.update_display()

        if self.game.winner():
            messagebox.showinfo("Hangman", f"🎉 Congratulations, you won!")
            self.player.increment_score()
            save_result_file(self.player, self.game.word, True, self.selected_category)
            save_result_db(self.player, self.game.word, True)
            build_main_menu(self)
        elif self.game.loser():
            messagebox.showinfo("Hangman", f"💀 You lost. The word was: {self.game.word}")
            save_result_file(self.player, self.game.word, True, self.selected_category)
            save_result_db(self.player, self.game.word, False)
            build_main_menu(self)
            
    def show_hint(self):
        """
        Fetches and displays a hint for the current word, including
        its definition, synonyms, and antonyms.
        """
        definition = get_definition(self.game.word)
        synonyms = get_synonyms(self.game.word)
        if isinstance(synonyms, str):
            synonyms = [synonyms]
        antonyms = get_antonyms(self.game.word)
        if isinstance(antonyms, str):
            antonyms = [antonyms]
        hint = f"Definition: {definition}\nSynonyms: {', '.join(synonyms)}\nAntonyms: {', '.join(antonyms)}"
        self.hint_var.set(hint)

    def show_rules(self):
        """
        Displays a static view showing the rules of the game.
        """
        self.clear_window()
        tk.Label(self.root, text="Game Rules", font=("Helvetica", 24)).pack(pady=20)
        rules_text = """
        1. Guess the word by entering letters.
        2. You have 6 attempts to guess the word correctly.
        3. Each incorrect guess will result in part of the hangman being drawn.
        4. If you guess the word before running out of attempts, you win.
        5. If you run out of attempts, you lose.
        """
        tk.Label(self.root, text=rules_text, font=("Helvetica", 16), justify="left").pack(pady=10)
        tk.Button(self.root, text="Back to Menu", command=lambda: build_main_menu(self), font=("Helvetica", 14)).pack(pady=10)

    def clear_window(self):
        """
        Clears all widgets from the root window to prepare for a new screen.
        """
        for widget in self.root.winfo_children():
            widget.destroy()
