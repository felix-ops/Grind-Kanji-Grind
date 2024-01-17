import csv
import requests
import os

def get_kanji_meaning(kanji):
    url = f'https://jisho.org/api/v1/search/words?keyword={kanji}'
    response = requests.get(url)
    data = response.json()
    if 'data' in data and data['data']:
        return data['data'][0]['senses'][0]['english_definitions'][0]
    else:
        return 'Meaning not found'

def fetch_and_write_meaning(input_file_path, output_file_path):
    global kanji_counter
    with open(input_file_path, 'r', newline='', encoding='utf-8') as infile, \
            open(output_file_path, 'w', newline='', encoding='utf-8') as outfile:

        reader = csv.reader(infile)
        header = next(reader)

        header_with_meaning = header + ['Meaning']
        writer = csv.writer(outfile)
        writer.writerow(header_with_meaning)

        for row in reader:
            kanji = row[0]
            meaning = get_kanji_meaning(kanji)
            row_with_meaning = row + [meaning]
            writer.writerow(row_with_meaning)

            # Uncomment the next line to print for verification
            print(f"Kanji: {kanji}, Meaning: {meaning}" + ".......... " + "(" + str(kanji_counter) + "/" + str(total_kanji) + ")")
            kanji_counter+=1



file_count = 5
kanji_counter = 0
total_kanji = 1973

script_dir = os.path.dirname(os.path.abspath(__file__))
filePaths = [[] for _ in range(file_count)]
output_names = [[] for _ in range(file_count)]

for i in range(file_count):
    filePaths[i] = os.path.join(script_dir, "n"+ str(i+1) + "Kanji.csv")
    output_names[i] = "n" + str(i+1) + "KanjiWithMeaning.csv"


for i in range(file_count):
    fetch_and_write_meaning(filePaths[i], output_names[i])