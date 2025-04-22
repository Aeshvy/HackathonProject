import json
import sqlite3
import os

JSON_PATH = 'data/results.json'
DB_PATH = 'data/scores.db'

def save_result_file(player, word, won):
    result = {
        'player': player.name,
        'score': player.scoore,
        'word': word,
        'won': won
    }

    if os.path.exists(JSON_PATH):
        with open(JSON_PATH, 'r+') as file:
            data = json.load(file)
            data.append(result)
            file.seek(0)
            json.dump(data, file, indent=2)

    else:
        with open(JSON_PATH, 'w') as file:
            json.dump([result], file, indent=2)

def save_result_db(player, word, won):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player TEXT,
            word TEXT,
            won BOOLEAN,
            score INTEGER
        )
    ''')
    c.execute('''
        INSERT INTO scores (player, word, won, score) VALUES (?, ?, ?, ?)
    ''', (player.name, word, won, player.score))
    conn.commit()
    conn.close()
