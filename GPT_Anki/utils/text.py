import re
import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
)
from print import typing
from utils import text, button, prepare_dictionary
from translate import translate
from neural_models import phi
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