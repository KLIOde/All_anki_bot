import logging
from telegram import Update
from telegram.ext import (
    ContextTypes
)
from buttons import state

command_name = 'speaking'

logger = logging.getLogger(__name__)
async def start_speaking_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        text="⌨️ Пожалуйста введите голосовуху:",
        parse_mode="Markdown"
    )
    return state.State.PHI_S_FILE