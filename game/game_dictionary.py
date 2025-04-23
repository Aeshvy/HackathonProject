import requests

def get_definition(word):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        meanings = data[0].get("meanings", [])
        if meanings:
            definition = meanings[0]["definitions"][0]["definition"]
            return f"{definition}"
        else:
            return "No definition found."
    except requests.exceptions.RequestException:
        return "Failed to fetch definition."