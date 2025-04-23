LIVES = 6
class HangmanGame:
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
    
    def display_word(self):
        return " ".join([letter if letter in self.guessed_letters else "_" for letter in self.word])
    
    def winner(self):
        return all(letter in self.guessed_letters for letter in self.word)
    
    def loser(self):
        return self.attempts_left <= 0