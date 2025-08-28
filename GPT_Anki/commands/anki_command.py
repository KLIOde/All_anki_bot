import logging
from telegram import Update
from telegram.ext import (
    ContextTypes
)
from buttons import state

command_name = 'anki'

logger = logging.getLogger(__name__)
async def start_anki_conversation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        text="📝 Введите НАЗВАНИЕ файла для Anki:",
        parse_mode="Markdown"
    )
    return state.State.WAITING_FOR_FILENAME