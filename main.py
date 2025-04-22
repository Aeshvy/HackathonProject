import json
import os
from game.hangman import HangmanGame
from game.player import Player
from game.utils import save_result_file, save_result_db

WORDLIST_PATH = 'data/words.json'

def load_words():
    with open(WORDLIST_PATH, 'r') as file:
        return json.load(file)
    
def main():
    words = load_words()
    player = Player()
    word = random.choice(words)
    game = HangmanGame(word)

    print(f'Welcome {Player.name} to Hangman!')
    while not game.winner and not game.loser():
        print(f'\Word: {game.display_word()}')
        print(f'LIVES: {game.attempts_left()}')
        guess = input('Guess a letter: ').strip()
        result = game.guess(guess)
        print(result)

    if game.winner():
        print(f'\nCongratulations, {player.name}!')
        player.increment_score()
    else:
        print(f'\nBetter luck next time, {player.name} The word was: {game.word}')

if __name__ == '__main__':
    main()