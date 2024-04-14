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
FIELD_NAME = config['FIELD_NAME']
CSV_FILE_NAME = config['CSV_FILE_NAME']
ANKI_CONNECT_URL = config['ANKI_CONNECT_URL']
ANKI_CONNECT_VERSION = config['ANKI_CONNECT_VERSION']

newKanjiCount = 0

def get_new_notes():
    data = {
        "action": "findNotes",
        "version": ANKI_CONNECT_VERSION,
        "params": {
            "query": f"deck:{DECK_NAME}"
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
    return [note_info["fields"][FIELD_NAME]["value"] for note_info in note_infos]



def extract_kanji(texts):
    kanji_dict = OrderedDict()
    for text in texts:
        for kanji in re.findall(r'[\u4e00-\u9fff]', text):
            kanji_dict[kanji] = None
    return list(kanji_dict.keys())

def fetch_kanji_meaning(kanji):
    print(f"Fetching meaning for {kanji}")
    url = 'https://kanjiapi.dev/v1/kanji/' + str(kanji)

    for _ in range(5):
        response = requests.get(url)
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
    print(f"Extracting kanjis from | Deck: {DECK_NAME} | Field: {FIELD_NAME} |")
    new_note_ids = get_new_notes()
    expressions = get_note_fields(new_note_ids)
    kanji_list = extract_kanji(expressions)
    save_to_csv(kanji_list)

    print(f"{newKanjiCount} new kanjis updated on {CSV_FILE_NAME}")
    input("Press Any Key to Exit...")

if __name__ == "__main__":
    main()