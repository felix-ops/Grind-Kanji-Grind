import csv
import time
import requests
import os

def get_kanji_meaning_jisho(kanji):
    url = f'https://jisho.org/api/v1/search/words?keyword={kanji}'
    response = requests.get(url)
    data = response.json()
    if 'data' in data and data['data']:
        return data['data'][0]['senses'][0]['english_definitions'][0]
    else:
        return 'Meaning not found'
    
def get_kanji_meaning_wanikani(kanji):
    url = f'https://api.wanikani.com/v2/subjects?types=kanji&slugs={kanji}'
    headers = {'Authorization': f'Bearer {wani_kani_api}'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        if 'data' in data and data['data']:
            return data['data'][0]['data']['meanings'][0]['meaning']
    
    return 'Meaning not found'

def get_kanji_meaning_kanjiapi(kanji):
    url = 'https://kanjiapi.dev/v1/kanji/' + str(kanji)

    for _ in range(5):
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if 'meanings' in data:
                return ', '.join(data['meanings'])
            
        time.sleep(3) 
        

    return 'Meaning not found'


def fetch_and_write_meaning(input_file_path, output_file_path):
    global kanji_counter
    with open(input_file_path, 'r', newline='', encoding='utf-8-sig') as infile, \
            open(output_file_path, 'w', newline='', encoding='utf-8') as outfile:

        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        
        for row in reader:
            kanji = row[0]
   
            meaning = get_kanji_meaning_kanjiapi(kanji)

            meaning = '' if meaning == 'Meaning not found' else meaning

            row_with_meaning = row + [meaning]  
            writer.writerow(row_with_meaning)


            print(f"Kanji: {kanji}, Meaning: {meaning}" + ".......... " + "(" + str(kanji_counter) + "/" + str(total_kanji) + ")")
            kanji_counter += 1



file_count = 5
kanji_counter = 0
total_kanji = 1973


script_dir = os.path.dirname(os.path.abspath(__file__))
filePaths = [[] for _ in range(file_count)]
output_names = [[] for _ in range(file_count)]

wani_kani_api = "0e4738a0-75ca-428c-8329-4d2577519524"

# print(get_kanji_meaning_kanjiapi("壌"))

for i in range(file_count):
    filePaths[i] = os.path.join(script_dir, "n"+ str(i+1) + "Kanji.csv")
    output_names[i] = "JLPT_N" + str(i+1) + ".csv"


for i in range(file_count):
    fetch_and_write_meaning(filePaths[i], output_names[i])