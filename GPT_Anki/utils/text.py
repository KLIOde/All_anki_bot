import re
import logging
from telegram import Update
from telegram.ext import (
    ContextTypes,
)
import os
from translate import translate

logger = logging.getLogger(__name__)

def escape_markdown_v2(text: str) -> str:
    """
    Экранирует специальные символы для Telegram MarkdownV2.
    """
    # Список символов, которые нужно экранировать
    escape_chars = r'_*[]()~`>#+-=|{}.!'
    # Экранируем каждый из них через \
    return re.sub(f'([{re.escape(escape_chars)}])', r'\\\1', text)

def split_en_ru(text):
    # Удаляем возможные разделители
    cleaned = re.sub(r'[-—]', ' ', text).strip()
    parts = cleaned.split()
    # Разделяем на английские и русские части
    eng_parts = []
    rus_parts = []
    
    for part in parts:
        if re.search(r'[a-zA-Z]', part):
            eng_parts.append(part)
        elif re.search(r'[а-яёА-ЯЁ]', part):
            rus_parts.append(part)
    
    a = ' '.join(eng_parts)
    b = ' '.join(rus_parts)
    
    return a, b

async def print_text(generated_words, update: Update, context: ContextTypes.DEFAULT_TYPE):
    eng_tg, rus_tg, eng_py, rus_py = translate.trans_res(generated_words)
    await update.message.reply_text(f"🔥 Полный текст: ||{eng_tg}||", parse_mode="MarkdownV2")
    await update.message.reply_text(f"💎 Перевод: ||{rus_tg}||", parse_mode="MarkdownV2")

def pattern(word):
    return "^" + word + "$"

def ecran(line):
    result = ''
    for i in line:
        if i not in '()\{\}[]':
            result += i
        else:
            result+= '\\' + i
    return result

def delete_all_old_mp3(folder):
        for filename in os.listdir(folder):
            filepath = os.path.join(folder, filename)
            if os.path.isfile(filepath) and filename.endswith(".mp3"):
                print(f"Удаляю: {filepath}")
                os.remove(filepath)
                print("Готово!")
                
def split_en_en(line):
    text = re.split(r"[-]", line)
    eng = re.split(r"[\s]", text[0])
    # Список для хранения результатов
    entries = []

    # Шаблон регулярного выражения
    # Объясню ниже
    pattern = r'''
        ^\s*                            # Пробелы в начале
        ([\w\s/()-]+?)                  # Группа 1: основное слово/фраза (лениво)
        (?:\s+(/\S+/))?                 # Группа 2: опциональная транскрипция
        \s*                             # Пробелы
        (\([\w\s/]+\))                  # Группа 3: часть речи (в скобках)
        \s*                             # Пробелы
    '''

    regex = re.compile(pattern, re.VERBOSE | re.DOTALL)

    def clean_text(text):
        """Убирает лишние пробелы и объединяет части"""
        return re.sub(r'\s+', ' ', text.strip())

    full_line = line
    full_line = clean_text(full_line)

    match = regex.search(full_line)
    phrase = match.group(1).strip()
    trans = match.group(2)  # Может быть None
    pos = match.group(3).strip('()')  # Убираем скобки
    
    notes = text[1]
    definition = re.split(r"[:]", notes)
    example = definition[1]
    clean_phrase = phrase
    if trans:
        clean_phrase = clean_phrase.replace(trans, '').strip()
    clean_phrase = re.sub(r'\s*\([\w\s/]+\)$', '', clean_phrase).strip()  # удаляем (n), (v) и т.п. в конце

    entries = ({
        'word': clean_phrase,
        'trans': trans,
        'pos': pos,
        'definition': definition[0],
        'example': example
    })
    return entries
def open_file_txt(file):
    try:
        res = []
        with open(file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line != '':
                        try:
                            res.append(split_en_en(line))
                        except (ValueError, TypeError):
                            print(line)
                            continue
        print('OKk')
        return res
    except Exception as e:
            print(f"Ошибка чтения файла: {e}")
            raise
if __name__ == '__main__':
    open_file_txt(file = 'GG.txt')