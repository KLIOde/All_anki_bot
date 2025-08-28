import logging
from telegram import Update
from telegram.ext import (
    ContextTypes
)
from utils import button

logger = logging.getLogger(__name__)
async def button_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        secret = 'Привет, Выбери 1 из 3 кнопок: 1 - Если хочешь получить Anki, 2 - Луше не трогай), 3 - Phi, если хочешь выучить язык!'
        await update.message.reply_text(f"{secret}")
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