import sqlite3
import zipfile
import os

def unpack_zip_file(apkg_path, extract_dir):
    try:
        with zipfile.ZipFile(apkg_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
        print("✅ Файл .apkg успешно распакован.")
    except Exception as e:
        raise RuntimeError(f"Ошибка при распаковке .apkg: {e}")
    
def selection(db_path):
    res = {}
    try:
        conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
        cursor = conn.cursor()
        cursor.execute("SELECT flds FROM notes")
        notes = cursor.fetchall()

        for row in notes:
            fields = row[0]
            field_list = fields.split('\x1f')  # \x1f — разделитель полей в Anki

            if len(field_list) >= 2:
                russian = field_list[0].strip()
                english = field_list[1].strip()
                res[russian] = english
            else:
                print(f"⚠️ Пропущена запись с некорректным количеством полей: {field_list}") 
        conn.close()
        return res
    except Exception as e:
        raise RuntimeError(f"Ошибка при чтении базы данных: {e}")
    finally:
        # Опционально: удалить временную папку после чтения
        # Но пока оставим, чтобы не пересоздавать при каждом запуске
        pass
def read(apkg_path="Anki2.apkg"):
    """
    Читает .apkg файл Anki и возвращает список карточек в формате:
    [{"front": "английское", "back": "русское"}, ...]
    Или словарь: {"русское": "английское"} — как у тебя сейчас.
    """
    if not os.path.exists(apkg_path):
        raise FileNotFoundError(f"Файл не найден: {apkg_path}")

    extract_dir = "temp_apkg"
    os.makedirs(extract_dir, exist_ok=True)

    # Распаковка .apkg (это ZIP)
    unpack_zip_file(apkg_path, extract_dir)

    db_path = os.path.join(extract_dir, "collection.anki2")
    
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Не найден файл базы данных: {db_path}")

    res = selection(db_path)
    print(f"📚 Загружено {len(res)} карточек.")
    return res

if __name__ == "__main__":
    data = read()
    for k, v in list(data.items())[:5]:
        print(f"{k} → {v}")