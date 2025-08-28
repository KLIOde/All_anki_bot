import logging
from telegram import Update
from telegram.ext import (
    ContextTypes
)
from buttons import state

command_name = 'listening'

logger = logging.getLogger(__name__)
async def start_listening_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(text="⌨️ Пожалуйста введите слово:")
    return state.State.PHI_L_FILE