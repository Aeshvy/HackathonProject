import json
import sqlite3
import os

JSON_PATH = 'data/results.json'
DB_PATH = 'data/scores.db'

def save_result_file(player, word, won, category):
    result = {
        'player': player.name,
        'score': player.score,
        'word': word,
        'won': won,
        'category': category,
        'word_length': len(word)
    }

    if os.path.exists(JSON_PATH):
        with open(JSON_PATH, 'r+') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = []
            data.append(result)
            file.seek(0)
            json.dump(data, file, indent=2)
    else:
        with open(JSON_PATH, 'w') as file:
            json.dump([result], file, indent=2)

#-------------------------------------------------------------------------------------------------------------------------------------------          

def save_result_db(player, word, won, category):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS game_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player TEXT,
            score INTEGER,
            word TEXT,
            won BOOLEAN,
            category TEXT,
            word_length INTEGER
        )
    ''')

    c.execute('''
        INSERT INTO game_results (player, score, word, won, category, word_length)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (player.name, player.score, word, won, category, len(word)))

    conn.commit()
    conn.close()
