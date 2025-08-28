import logging
import os
from telegram import Update
from telegram.ext import (
    ContextTypes
)
from utils import text, button
from translate import translate

logger = logging.getLogger(__name__)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        secret = 'Привет, Меня зовут Клим, Спасибо, что решили воспользоваться моим ботом!'
        secret1 = 'I appreciate your choise'
        await update.message.reply_text(f"{secret}")
        await update.message.reply_text(f"||{secret1}||", parse_mode="MarkdownV2")
        await update.message.reply_text('Выберите 1 из команд:')