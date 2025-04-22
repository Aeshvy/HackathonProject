import random

LIVES = 6

class hangmanGame:
    def __init__(self, word):
        self.word = word.upper()
        self.guessed_letters = set()
        self.attempts_left = LIVES

    def guess(self, letter):
        letter = letter.upper()
        if letter in self.guessed_letters:
            return "Already guessed."
        self.guessed_letters.add(letter)

        if letter in self.word:
            return "Correct!"
        else:
            self.attempts_left -= 1
            return "Wrong!"
    
    def