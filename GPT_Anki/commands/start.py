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
        secret = text.escape_markdown_v2(secret)
        secret1 = translate.trans('I appreciate your choise')
        await update.message.reply_text(f"||{secret}||", parse_mode="MarkdownV2")
        await update.message.reply_text(f"||{secret1}||", parse_mode="MarkdownV2")
        await update.message.reply_text(
            "Привет! Выберите действие:",
            reply_markup=button.get_main_menu()
        )
    elif update.callback_query:
        query = update.callback_query
        await query.edit_message_text(
            "Привет! Выберите действие:",
            reply_markup=button.get_main_menu()
        )