import genanki
import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
import numpy as np
from utils import text
from utils import parsing_file
class save2apkg:
    def __init__(self, res_name, file, how, id, res = {}):
        self.res_name = res_name
        self.file = file
        self.how = how
        self.id = id
        self._res = res
        self._output_path = None
        
    def saving(self):
        self.__open_file()
        print(self._res)
        if self.how == 'csv':
            return self.__create_csv()

        elif self.how == 'anki':
            return self.__create_anki()
        
        elif self.how == 'anki_parsing':
            return self.create_anki_parsing()
        
    def __open_file(self):
        try:
            with open(self.file, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line != '':
                            try:
                                eng, rus = text.split_en_ru(line)
                                self._res[eng] = rus
                            except (ValueError, TypeError):
                                print(line)
                                continue
        except Exception as e:
            print(f"Ошибка чтения файла: {e}")
            raise
        
    def __create_anki(self):
    
        my_model = self.__model_anki()
        
        my_deck = self.__append_word_to_anki(my_model)

        # Сохраняем в папку downloads
        self._output_path = self.__save_in_anki(my_deck, [])
        return self._output_path
    
    def __model_anki(self):
        MODEL_ID = np.random.randint(1, 2147483646)  
        if self.id == 'simple': 
            my_model = genanki.Model(
                MODEL_ID,
                self.res_name,
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
        elif self.id == 'advanced':
            my_model = genanki.Model(
                MODEL_ID,
                self.res_name,
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
            return my_model
    
    def __append_word_to_anki(self, my_model):
        if self.id == 'simple':
            DECK_ID = 2057488654
            my_deck = genanki.Deck(DECK_ID, self.res_name)
            for eng, rus in self._res.items():
                    note = genanki.Note(
                        model=my_model,
                        fields=[eng, rus],
                    )
                    my_deck.add_note(note)
            return my_deck
        elif self.id == 'advanced':
            DECK_ID = 2057488654
            media_files_list = []
            my_deck = genanki.Deck(DECK_ID, self.res_name)
            
            for eng, rus in self._res.items():
                try:
                    example, definition, partOfSpeesh,synonyms, antonyms, text, media_files_list, sound_tag = parsing_file.parsing_word_from_dictionary(eng, media_files_list)
                except:
                    example, definition, partOfSpeesh,synonyms, antonyms, text, sound_tag = {}, '', '', '', '' , '', ''
                finally:
                    print(sound_tag)
                    note = genanki.Note(
                        model=my_model,
                        fields=[eng, rus, example.get(eng, ""), sound_tag, definition, partOfSpeesh,synonyms, antonyms, text],
                    )
                    my_deck.add_note(note)
            return my_deck, media_files_list
    
    def __save_in_anki(self, my_deck, media_files_list):
        if self.id == 'simple':
            self._output_path = "downloads/Vocabulary.apkg"
            genanki.Package(my_deck).write_to_file(self._output_path)
            print('OK')
            print(f"Файл Anki создан: {self._output_path}")
        elif self.id == 'advanced':
            self._output_path = "downloads/Vocabulary.apkg"
            genanki.Package(my_deck, media_files=media_files_list).write_to_file(self._output_path)
            
            print('OK')
            print(f"Файл Anki создан: {self._output_path}")
        return self._output_path
    
    def __create_csv(self):
        self._output_path = "downloads/COOOOOOOL.csv"
        with open(self._output_path, "w", encoding="utf-8") as f:
            for eng, rus in self._res.items():
                f.write(f"{eng},{rus}\n")
        return self._output_path
    
    def create_anki_parsing(self):
    
        my_model = self.__model_anki()
        
        my_deck, media_files_list = self.__append_word_to_anki(my_model)

        self._output_path = self.__save_in_anki(my_deck, media_files_list)
        
        # for i in media_files_list:
        #     if os.path.exists(i):
        #         os.remove(i)
        return self._output_path
    
if __name__ == "__main__":
    s = save2apkg(how='anki', file='GG.txt', res_name="Vocabulary MIPT", id = 'advanced', res = {'water': 'вода', 'find': 'найти', 'when': 'когда', 'how are you': 'как ты'})
    s.create_anki_parsing()
