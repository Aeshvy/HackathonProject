import requests

def get_synonyms(word):
    url = f"https://api.datamuse.com/words?rel_syn={word}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        if data:
            synonyms = [item['word'] for item in data[:5]]
            return f"Synonyms: {', '.join(synonyms)}"
        else:
            return "No synonyms found."
    except requests.exceptions.RequestException:
        return "Failed to fetch synonyms."

def get_antonyms(word):
    url = f"https://api.datamuse.com/words?rel_ant={word}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        if data:
            antonyms = [item['word'] for item in data[:5]]
            return f"Antonyms: {', '.join(antonyms)}"
        else:
            return "No antonyms found."
    except requests.exceptions.RequestException:
        return "Failed to fetch antonyms."