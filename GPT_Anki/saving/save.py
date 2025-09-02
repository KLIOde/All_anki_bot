import genanki
import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
import numpy as np
from utils import text
from utils import parsing_file
import re
import time
class save2apkg:
    folder = "downloads"
    def __init__(self, res_name = 'V', file = 'GG.txt', how = 'anki_lms', id = 'new_advanced', res = {}):
        self.res_name = res_name
        self.file = file
        self.how = how
        self.id = id
        self._res = res
        self._output_path = None
        text.delete_all_old_mp3(self.folder)
        
        
    def saving(self):
        
        self.__open_file_txt_lms()
        print(self._res)
        if self.how == 'csv':
            return self.__create_csv()

        elif self.how == 'anki':
            return self.__create_anki()
        
        elif self.how == 'anki_parsing':
            return self.create_anki_parsing()
        
        elif self.how == 'anki_lms':
            return self.create_anki_lms()
        
    def __open_file_txt_lms(self):
        self._res = text.open_file_txt(self.file)
    
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
        elif self.id == 'new_advanced':
            my_model = genanki.Model(
                MODEL_ID,
                self.res_name,
                fields=[
                    {"name": "English"},
                    {"name": "Example"},
                    {"name": "Definition"},
                    {"name": "Transcript"},
                    {"name": "partOfSpeech"},  # ✅ Добавлено!
                ],
                templates=[
                    {
                        "name": "Простая+",
                        "qfmt": "{{English}}",
                        "afmt": """
                            {{FrontSide}}
                            <hr id="answer">
                            <div class ="english_transcrip_center">
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
                .partofspeech .value {
                    color: #4CAF50;  /* зелёный */
                }

                .definition .value {
                    color: #2196F3;  /* синий */
                }

                .example .value {
                    color: #FF5722;  /* оранжево-красный */
                }
                """
            )
            return my_model
    
    def __append_word_to_anki(self, my_model):
        DECK_ID = np.random.randint(1, 2147483646)
        my_deck = genanki.Deck(DECK_ID, self.res_name)
        media_files_list = []
        if self.id == 'simple':
            for eng, rus in self._res.items():
                note = genanki.Note(model=my_model, fields=[eng, rus])
                my_deck.add_note(note)
        elif self.id == 'advanced':
            for eng, rus in self._res.items():
                example, definition, partOfSpeesh, synonyms, antonyms, text, sound_tag = {}, '', '', '', '', '', ''
                try:
                    time.sleep(0.1)
                    words = re.split(r'[,/]', eng)
                    result = parsing_file.parsing_word_from_dictionary(words[0], media_files_list)
                    example, definition, partOfSpeesh, synonyms, antonyms, text, media_files_list, sound_tag = result
                except Exception as e:
                    print(f"Ошибка при парсинге {eng}: {e}")
                
                note = genanki.Note(
                    model=my_model,
                    fields=[
                        eng, rus,
                        example.get(eng, ""),
                        sound_tag,
                        definition,
                        partOfSpeesh,
                        synonyms,
                        antonyms,
                        text
                    ],
                )
                my_deck.add_note(note)
        
        elif self.id == 'new_advanced':
            for entry in self._res:
                if not isinstance(entry, dict):
                    continue

                eng = entry.get('word', '')
                example = entry.get('example', '')
                definition = entry.get('definition', '')
                trans = entry.get('trans', '') or ""
                partOfSpeesh = entry.get('pos', '')

                note = genanki.Note(
                    model=my_model,
                    fields=[
                        eng,           # English
                        example,       # Example
                        definition,    # Definition
                        trans,         # Transcript
                        partOfSpeesh,  # partOfSpeech
                    ],
                )
                my_deck.add_note(note)
        return my_deck, media_files_list  # всегда возвращаем кортеж
    
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
        elif self.id == 'new_advanced':
            self._output_path = "downloads/Vocabulary.apkg"
            genanki.Package(my_deck).write_to_file(self._output_path)
            
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
        

        return self._output_path
    
    def create_anki_lms(self):
        my_model = self.__model_anki()
        
        my_deck, media_files_list = self.__append_word_to_anki(my_model)

        self._output_path = self.__save_in_anki(my_deck, media_files_list)

        return self._output_path
if __name__ == "__main__":
    res  = {'trifles': 'пустяки', 'chord': 'аккорд', 'sober': 'трезвый', 'drunk': 'нетрезвый', 'decisive': 'решительный', 'frank': 'откровенный', 
'fussy': 'суетливый', 'active': 'активный', 'ambitious': 'амбициозный', 'high flying': 'целеустремленный', 'reckless': 'безумный', 'light hearted, easygoing': 'беспечный', 'furious': 'бешенный', 'strong willed': 'волевой', 'grumbling': 'ворчливый', 'proud': 'гордый', 'humane': 'гуманный', 'kind': 'добрый', 'greedy': 'жадный', 'acrimonious': 'желчный', 'cruel': 'жестокий', 'envious': 'завистливый', 'unsociable': 'замкнутый', 'arrogant': 'заносчивый, высокомерный', 'angry': 'злой', 'ideal, perfect': 'идеальный', 'capricious,': 'капризный', 'sly': 'коварный, хитрый', 'lazy': 'ленивый', 'lying,': 'лживый', 'personality': 'личность', 'curious': 'любопытный', 'disgusting': 'мерзкий', 'impertinent': 'наглый', 'reliable': 'надежный, верный', 'importunate': 'назойливый', 'naive': 'наивный', 'naughty': 'непослушный, капризный (о ребенке)', 'touchy': 'обидчивый', 'he is a man of (strong) character': 'он человек с характером', 'optimist': 'оптимист', 'witty': 'остроумный', 'courageous': 'отважный', 'responsible': 'ответственный', 'responsive': 'отзывчивый', 'passive': 'пассивный', 'pessimist': 'пессимист', 'positive': 'позитивный', 'indifferent': 'равнодушный', 'smart': 'разумный, сообразительный', 'uninhibited': 'раскованный', 'sober minded, reasonable': 'рассудительный', 'realist': 'реалист', 'harsh': 'резкий', 'self critical': 'самокритичный', 'selfish': 'самолюбивый', 'serious': 'серьезный', 'attitude of mind, mentality': 'склад ума', 'modest': 'скромный', 'brave': 'смелый', 'fair': 'справедливый', 'talented': 'талантливый', 'patient': 'терпеливый', 'calm, quiet': 'тихий', 'tolerant': 'толерантный', 'stupid': 'тупой', 'clever': 'умный', 'intelligent': 'умный, разумный', 'stubborn': 'упрямый', 'cynical': 'циничный', 'character trait': 'черта характера', 'sensitive': 'чувствительный', 'generous': 'щедрый'}
    s = save2apkg(how='anki_parsing', file='GG.txt', res_name="Vocabulary MIPT", id = 'advanced', res = res)
    s.create_anki_parsing()
    # s.delete_all_old_mp3()