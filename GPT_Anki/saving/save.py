import genanki
import re
from utils import text

def open_file(file_path):
    try:
        file_path = file_path
        with open(file_path, 'r', encoding='utf-8') as f:
                res = {}
                for line in f:
                    line = line.strip()
                    if not line or '-' not in line and '–' not in line:
                        continue
                    # Поддержка разных тире: - или –
                    print(line)
                    eng, rus = text.split_en_ru(line)
                    res[eng] = rus
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

def create_anki(res_name, res):
    MODEL_ID = 1607492319  
    DECK_ID = 2057488654
    
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
                    "afmt": '{{FrontSide}}<hr id="answer">{{English}}',
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

    my_deck = genanki.Deck(DECK_ID, res_name)
    for eng, rus in res.items():
        note = genanki.Note(
            model=my_model,
            fields=[eng, rus],
        )
        my_deck.add_note(note)

    # Сохраняем в папку downloads
    output_path = "downloads/Vocabulary.apkg"
    genanki.Package(my_deck).write_to_file(output_path)
    
    print(f"Файл Anki создан: {output_path}")
    return output_path  # Возвращаем полный путь

def saving(how='anki', file='GG.txt', res_name="Vocabulary MIPT"):
    res = open_file(file)
    print(res)
    if how == 'csv':
        return create_csv(res)

    elif how == 'anki':
        return create_anki(res_name, res)

if __name__ == "__main__":
    saving()