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
JSON_FILE_NAME = config['ANKI_MEDIACOLLECTION_PATH']
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
    meaning = get_meaning_from_files(kanji)
    if meaning is None:
        meaning = fetch_meaning_from_api(kanji)
    return meaning

def get_meaning_from_files(kanji):
    # Check CSV file
    csv_meaning = get_meaning_from_csv(kanji)
    # Check JSON file
    json_meaning = get_meaning_from_json(kanji)


    if csv_meaning is not None:
        if json_meaning == None:        
            print(f"Syncing meaning from CSV => JSON: {kanji}")
        return csv_meaning

    if json_meaning is not None:
        if csv_meaning == None:
            print(f"Syncing meaning from JSON => CSV: {kanji}")
        return json_meaning

    return None

def get_meaning_from_csv(kanji):
    if os.path.isfile(CSV_FILE_NAME):
        with open(CSV_FILE_NAME, "r", newline="", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[0] == kanji:
                    return row[1]
    return None

def get_meaning_from_json(kanji):
    if os.path.isfile(JSON_FILE_NAME):
        with open(JSON_FILE_NAME, "r", encoding="utf-8") as jsonfile:
            data = json.load(jsonfile)
            if kanji in data:
                return data[kanji]
    return None

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

def save_to_json(kanji_list):
    data = {}
    for kanji in kanji_list:
        meaning = fetch_kanji_meaning(kanji)
        data[kanji] = meaning

    with open(JSON_FILE_NAME, "w", encoding="utf-8") as jsonfile:
        json.dump(data, jsonfile, ensure_ascii=False, indent=4)

def main():
    print(f"Extracting kanjis from | Deck: {DECK_NAME} | Fields: {', '.join(FIELD_NAMES)} |")
    try:
        new_note_ids = get_new_notes()
        expressions = get_note_fields(new_note_ids)
        kanji_list = extract_kanji(expressions)
        save_to_csv(kanji_list)
        save_to_json(kanji_list)
        print(f"{newKanjiCount} new kanjis updated from web")
        print(f"Kanji meanings synced between {CSV_FILE_NAME} and {JSON_FILE_NAME}")
    except requests.exceptions.RequestException as e:
        print("Error connecting to Anki Connect:", e)
    input("Press Any Key to Exit...")


if __name__ == "__main__":
    main()