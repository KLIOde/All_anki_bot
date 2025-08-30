import requests
import os

def download_sound(url_sound, file_name_douwnload):
    response = requests.get(url_sound)
    response.raise_for_status()
    with open(file_name_douwnload, 'wb') as f:
        f.write(response.content)
        print('Скачано')

def parsing_word_from_dictionary(word, media_files_list):
    
    filename = f"downloads/{word.lower()}-us.mp3"
    sound_tag = f"[sound:{os.path.basename(filename)}]"
    if filename and os.path.exists(filename):
        media_files_list.append(filename)
    print(media_files_list)
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(url)
    if response:
        x = response.json()
        #print(x) # словарь: word:,  phonetic:, phonetics: text, audio, sourceUrl, lince  (ссылка)
        res_phonetics = []
        text = x[0]['phonetic']
        for dict in  x[0]['phonetics']:
                if 'text' in dict and 'audio' in dict and 'sourceUrl' in dict:
                    audio = dict['audio']
                    sourceUrl = dict['sourceUrl']
                    res_phonetics.append(dict)
                    download_sound(audio, f"downloads/{word.lower()}-us.mp3")
        # print(res_phonetics)
        
        res_meanings = []
        partOfSpeech = ''
        examples = {}
        synonyms = antonyms = ''
        defenition = ''
        for mean in x[0]['meanings']:
            if 'partOfSpeech' in mean and 'definitions' in mean:
                partOfSpeech = mean['partOfSpeech']
                antonyms = mean['antonyms']
                synonyms = mean['synonyms']
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
        print(synonyms, antonyms)
        return examples, defenition, partOfSpeech, synonyms, antonyms, text, sound_tag

if __name__ == "__main__":
    parsing_word_from_dictionary('hi')