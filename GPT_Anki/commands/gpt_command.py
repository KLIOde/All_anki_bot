import logging
from telegram import Update
from telegram.ext import (
    ContextTypes
)
from buttons import state

command_name = 'gpt'

logger = logging.getLogger(__name__)
async def start_gpt_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(text="⌨️ Скиньте файл в формате .apkg:")
    return state.State.GPT_FILE