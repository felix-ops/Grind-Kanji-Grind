import csv
import time
import requests
import re
import os
import json
from collections import OrderedDict

# Load the configuration from the JSON file
config_file = 'anki_sync_config.json'
if os.path.exists(config_file):
    with open(config_file, 'r', encoding='utf-8') as f:
        config = json.load(f)
else:
    raise FileNotFoundError(f"Configuration file '{config_file}' not found.")

# Set the configuration variables
DECK_NAME = config['DECK_NAME']
FIELD_NAMES = config['FIELD_NAMES']
CSV_FILE_NAME = config['CSV_FILE_PATH']
ANKI_CONNECT_URL = config['ANKI_CONNECT_URL']
ANKI_CONNECT_VERSION = config['ANKI_CONNECT_VERSION']

newKanjiCount = 0

def get_new_notes():
    deck_name_encoded = DECK_NAME.encode('utf-8')  # Encode the deck name as UTF-8
    data = {
        "action": "findNotes",
        "version": ANKI_CONNECT_VERSION,
        "params": {
             "query": f'deck:"{deck_name_encoded.decode("utf-8")}"' 
        }
    }
    response = requests.post(ANKI_CONNECT_URL, json=data)
    response.raise_for_status()

    return response.json()["result"]

def get_note_fields(note_ids):
    data = {
        "action": "notesInfo",
        "version": ANKI_CONNECT_VERSION,
        "params": {
            "notes": note_ids
        }
    }
    response = requests.post(ANKI_CONNECT_URL, json=data)
    response.raise_for_status()
    note_infos = response.json()["result"]
    all_expressions = []
    for note_info in note_infos:
        note_expressions = []
        for field_name in FIELD_NAMES:
            note_expressions.append(note_info["fields"][field_name]["value"])
        all_expressions.append(note_expressions)
    return all_expressions

def extract_kanji(texts):
    kanji_dict = OrderedDict()
    for text_list in texts:
        for text in text_list:
            for kanji in re.findall(r'[\u4e00-\u9fff]', text):
                kanji_dict[kanji] = None
    return list(kanji_dict.keys())

def fetch_kanji_meaning(kanji):
    meaning = fetch_meaning_from_api(kanji)
    return meaning

def fetch_meaning_from_api(kanji):
    print(f"Fetching meaning from web: {kanji}")
    for _ in range(5):
        response = requests.get(f'https://kanjiapi.dev/v1/kanji/{kanji}')
        if response.status_code == 200:
            data = response.json()
            if 'meanings' in data:
                meaning = ', '.join(data['meanings'])
                print(f"Meaning founded: {meaning}")
                return meaning
        print('Meaning not found retrying...')
        time.sleep(3)
    return 'Meaning not found'

def save_to_csv(kanji_list):
    global newKanjiCount
    file_exists = os.path.isfile(CSV_FILE_NAME)
    existing_kanji = set()
    if file_exists:
        with open(CSV_FILE_NAME, "r", newline="", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            existing_kanji = {row[0] for row in reader}

    new_kanji = [kanji for kanji in kanji_list if kanji not in existing_kanji]
    newKanjiCount = len(new_kanji)
    print(f"{newKanjiCount} new kanjis found")

    with open(CSV_FILE_NAME, "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        for kanji in new_kanji:
            meaning = fetch_kanji_meaning(kanji)
            writer.writerow([kanji, meaning])


def main():
    print(f"Extracting kanjis from | Deck: {DECK_NAME} | Fields: {', '.join(FIELD_NAMES)} |")
    try:
        new_note_ids = get_new_notes()
        expressions = get_note_fields(new_note_ids)
        kanji_list = extract_kanji(expressions)
        save_to_csv(kanji_list)
        print(f"{newKanjiCount} new kanjis updated on {CSV_FILE_NAME}")
    except requests.exceptions.RequestException as e:
        print("Error connecting to Anki Connect:", e)
    input("Press Any Key to Exit...")


if __name__ == "__main__":
    main()