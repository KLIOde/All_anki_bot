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

def split_en_ru(s):
    match = re.match(r'^\s*(.+?)\s*[-–]\s*([а-яА-ЯёЁ].*)$', s.strip())
    
    if match:
        eng = match.group(1).strip()  # Всё до тире
        rus = match.group(2).strip()  # Всё после тире, начиная с кириллицы
        return eng, rus

async def print_text(generated_words, update: Update, context: ContextTypes.DEFAULT_TYPE):
    eng_tg, rus_tg, eng_py, rus_py = translate.trans_res(generated_words)
    await update.message.reply_text(f"🔥 Полный текст: ||{eng_tg}||", parse_mode="MarkdownV2")
    await update.message.reply_text(f"💎 Перевод: ||{rus_tg}||", parse_mode="MarkdownV2")


def pattern(word):
    return "^" + word + "$"