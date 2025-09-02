import requests
import os
import time

def download_sound(url_sound, file_name_douwnload):
    response = requests.get(url_sound)
    response.raise_for_status()
    with open(file_name_douwnload, 'wb') as f:
        f.write(response.content)
        print(f'Скачано: {file_name_douwnload}')

def preapre_dounload_sound(word, media_files_list):
    filename = f"downloads/{word.lower()}-us.mp3"
    sound_tag = f"[sound:{os.path.basename(filename)}]"
    if filename and os.path.exists(filename):
        media_files_list.append(filename)
    return sound_tag, media_files_list

def get_request(url, word):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(url)
    while True:  # Цикл повтора
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            time.sleep(1)  # Задержка между успешными запросами
            return data
        
        elif response.status_code == 429:
            print(f"Too many requests for '{word}'. Waiting 10 seconds...")
            time.sleep(10)  # Подождать и повторить
            continue  # ← Теперь continue работает, потому что мы в while
        
        else:
            time.sleep(1)
            return None  # Или можно повторять? Зависит от логики

def json_progressing_phonetics(word, x):
    res_phonetics = []
    audio = ''
    for dict in  x[0]['phonetics']:
            if 'text' in dict and 'audio' in dict and 'sourceUrl' in dict:
                if audio == '':
                    audio = dict['audio']
                    res_phonetics.append(dict)
                    download_sound(audio, f"downloads/{word.lower()}-us.mp3")
                
def json_progressing_meaning(word, x):
    partOfSpeech = ''
    examples = {}
    synonyms = antonyms = ''
    defenition = ''
    for mean in x[0]['meanings']:
        if 'partOfSpeech' in mean and 'definitions' in mean:
            partOfSpeech = mean['partOfSpeech']
            antonyms = mean['antonyms']
            synonyms = mean['synonyms']
            if defenition == '':
                defenition = mean['definitions'][0]['definition']
            if 'example' in mean['definitions'][0]:
                examples[word] = (mean['definitions'][0]['example'])  
                
    if len(synonyms) >= 1:
        synonyms = synonyms[0]
    else:
        synonyms = ''
    if len(antonyms) >= 1:
        antonyms = antonyms[0]
    else:
        antonyms =''
    return defenition, partOfSpeech, examples, synonyms, antonyms
  
def parsing_word_from_dictionary(word, media_files_list):
    sound_tag, media_files_list = preapre_dounload_sound(word, media_files_list)
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    
    x = get_request(url, word)
    text = ''
    if 'phonetic' in x[0]:
        text = x[0]['phonetic']
    
    json_progressing_phonetics(word, x)
    
    defenition, partOfSpeech, examples, synonyms, antonyms = json_progressing_meaning(word, x)
    
    return examples, defenition, partOfSpeech, synonyms, antonyms, text, media_files_list, sound_tag

if __name__ == "__main__":
    parsing_word_from_dictionary('hi')