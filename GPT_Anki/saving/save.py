import genanki
import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
import numpy as np
from utils import text
from utils import parsing_file

def open_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
                res = {}
                for line in f:
                    line = line.strip()
                    if line != '':
                        try:
                            eng, rus = text.split_en_ru(line)
                            res[eng] = rus
                        except (ValueError, TypeError):
                            print(line)
                            continue
        return res
    except Exception as e:
        print(f"Ошибка чтения файла: {e}")
        raise

def create_csv(res):
    output_path = "downloads/COOOOOOOL.csv"
    with open(output_path, "w", encoding="utf-8") as f:
        for eng, rus in res.items():
            f.write(f"{eng},{rus}\n")
    return output_path

def model_anki(res_name):
    MODEL_ID = 1607492319  
    my_model = genanki.Model(
        MODEL_ID,
        res_name,
        fields=[
            {"name": "English"},
            {"name": "Russian"},
        ],
        templates=[
            {
                "name": "Простая+",
                "qfmt": "{{Russian}}",
                "afmt": "{{English}}",
            },
        ],
        css="""
        .card {
            font-family: Arial;
            font-size: 30px;
            text-align: center;
            color: black;
            background-color: white;
        }
        """
    )
    return my_model

def append_word_to_anki(res_name, my_model, res):
    DECK_ID = 2057488654
    my_deck = genanki.Deck(DECK_ID, res_name)
    for eng, rus in res.items():
            note = genanki.Note(
                model=my_model,
                fields=[eng, rus],
            )
            my_deck.add_note(note)
    return my_deck

def save_in_anki(my_deck):
    output_path = "downloads/Vocabulary.apkg"
    genanki.Package(my_deck, media_files=['SSS.mp3']).write_to_file(output_path)
    print('OK')
    print(f"Файл Anki создан: {output_path}")
    return output_path

def create_anki(res_name, res):
    
    my_model = model_anki(res_name)
    
    my_deck = append_word_to_anki(res_name, my_model, res)

    # Сохраняем в папку downloads
    output_path = save_in_anki(my_deck)
    return output_path  # Возвращаем полный путь

def create_anki_parsing(res_name, res):
    
    MODEL_ID = np.random.randint(1, 2147483646)  
    DECK_ID = 2057488654
    
    my_model = genanki.Model(
            MODEL_ID,
            res_name,
            fields=[
                {"name": "English"},
                {"name": "Russian"},
                {"name": "Example"},
                {"name": "Audio"},
                {"name": "Definition"},
                {"name": "partOfSpeech"},
                {"name": "synonyms"},
                {"name": "antonyms"},
                {"name": "Transcript"},
            ],
            templates=[
                {
                    "name": "Простая+",
                    "qfmt": "{{Russian}}",
                    "afmt": """
                        {{FrontSide}}
                        <hr id="answer">
                        <div class ="english_transcrip_center">
                            <div class="english">{{English}}</div>
                            <div class="transcript">{{Transcript}}</div>
                        </div>
                        <div class="definition">
                            <span class="label">Definition:</span> <span class="value">{{Definition}}</span>
                        </div>

                        <div class="partofspeech">
                            <span class="label">Part of Speech:</span> <span class="value">{{partOfSpeech}}</span>
                        </div>

                        <div class="example">
                            <span class="label">Example:</span> <span class="value">{{Example}}</span>
                        </div>
                        <div class = "syn-ant">
                            <div class="synonyms">
                                <span class="label">Synonyms:</span> <span class="value">{{synonyms}}</span>
                            </div>

                            <div class="antonyms">
                                <span class="label">Antonyms:</span> <span class="value">{{antonyms}}</span>
                            </div>
                        </div>
                        <div class="audio">{{Audio}}</div>
                    """,
                },
            ],
            css="""
            .card {
                font-family: Arial;
                font-size: 30px;
                text-align: center;
                color: black;
                background-color: white;
            }
            
            .english_transcrip_center {
                text-align: center;
                margin: 20px 0;
            }
            
            .definition {
                font-size: 34px;
                color: #2f11f5;
                margin-top: 10px;
                margin-right: 0;
                margin-bottom: 10px;
                margin-left: 0;
                line-height: 1.4;
            }
            .partofspeech {
                font-size: 34px;
                color: #34f522;
                margin-top: 10px;
                margin-right: 0;
                margin-bottom: 10px;
                margin-left: 0;
                line-height: 1.4;
            }
            .example {
                font-size: 34px;
                color: #f51111;
                margin-top: 10px;
                margin-right: 0;
                margin-bottom: 10px;
                margin-left: 0;
                line-height: 1.4;
            }
            .audio {
                font-size: 34px;
                color: #2f11f5;
                margin-top: 10px;
                margin-right: 0;
                margin-bottom: 10px;
                margin-left: 0;
                line-height: 1.4;
            }
            .syn-ant {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin: 20px 0;
                font-size: 24px;  /* общий размер текста в блоке */
            }
            .synonyms {
                color: #19fa05;
                font-weight: bold;
            }
            .antonyms {
                color: #f70c0c;
                font-weight: bold;
            }
            .partofspeech .value {
                color: #4CAF50;  /* зелёный */
            }

            .definition .value {
                color: #2196F3;  /* синий */
            }

            .example .value {
                color: #FF5722;  /* оранжево-красный */
            }

            .synonyms .value {
                color: #8BC34A;  /* светло-зелёный */
            }

            .antonyms .value {
                color: #F44336;  /* красный */
            }
            """
        )
    media_files_list = []
    my_deck = genanki.Deck(DECK_ID, res_name)
    
    for eng, rus in res.items():
        example, definition, partOfSpeesh,synonyms, antonyms, text, sound_tag = parsing_file.parsing_word_from_dictionary(eng, media_files_list)
        note = genanki.Note(
            model=my_model,
            fields=[eng, rus, example.get(eng, ""), sound_tag, definition, partOfSpeesh,synonyms, antonyms, text],
        )
        my_deck.add_note(note)

    # Сохраняем в папку downloads
    output_path = "downloads/Vocabulary.apkg"
    genanki.Package(my_deck, media_files=media_files_list).write_to_file(output_path)
    
    print('OK')
    print(f"Файл Anki создан: {output_path}")
    
    for i in media_files_list:
        if os.path.exists(i):
            os.remove(i)
    return output_path  # Возвращаем полный путь

def saving(how='anki', file='GG.txt', res_name="Vocabulary MIPT"):
    res = open_file(file)
    print(res)
    if how == 'csv':
        return create_csv(res)

    elif how == 'anki':
        return create_anki(res_name, res)

if __name__ == "__main__":
    create_anki_parsing(res_name="Vocabulary MIPT", res = {'water': 'вода', 'find': 'найти'})