from telegram import Update
from telegram.ext import ContextTypes
from telegram.ext import (
    ContextTypes,
)

import logging
from neural_models import phi
from utils.voice import download_voice, recognize_speech
from buttons import state

logger = logging.getLogger(__name__)
TELEGRAM_TOKEN = "8134028537:AAEddvqQNy3ovVrxZ49h1LO7rt4CnWiz1FA"

async def phi_speaking_button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(text="⌨️ Пожалуйста введите голосовуху:")
        return state.State.PHI_S_FILE

async def phi_speaking_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    filename = await download_voice(update, context) #Скачиваем голосовуху
    text = recognize_speech(filename) #Преобразуем её в вав-файл + расшифровываем
    response = f"🎤 Вот расшифровка вашего голосового сообщения:\n\n{text}" #Форматируем, чтобы на выходе пользователь получил не пустую расшифровку, а хоть какую-то красоту
    await update.message.reply_text(response)