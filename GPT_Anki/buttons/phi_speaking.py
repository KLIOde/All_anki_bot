import os
from telegram import Update
from telegram.ext import ContextTypes
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
)
from utils import send_voise
import logging
from neural_models import phi
from translate import translate
import telebot
from voice import download_file, recognize_speech

PHI_FILE = "phi_file"
logger = logging.getLogger(__name__)
TELEGRAM_TOKEN = "8134028537:AAEddvqQNy3ovVrxZ49h1LO7rt4CnWiz1FA"
bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(content_types=['voice']) #Бот реагирует на голос, поэтому пишем voice

def transcript(message):

    filename = download_file(bot, message.voice.file_id) #Скачиваем голосовуху

    text = recognize_speech(filename) #Преобразуем её в вав-файл + расшифровываем

    response = f"🎤 Вот расшифровка вашего голосового сообщения:\n\n{text}" #Форматируем, чтобы на выходе пользователь получил не пустую расшифровку, а хоть какую-то красоту

    bot.send_message(message.chat.id, response) #Отправляем ответ пользователю :)

''' bot.polling() '''
# Это будет entry_point (когда нажимают кнопку)
# async def phi_speaking_button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     query = update.callback_query
#     await query.answer()
#     await query.edit_message_text(text="⌨️ Пожалуйста, отправте голосовое сообщение на английском языке:")

#     # Переходим в состояние PHI_FILE
#     return PHI_FILE  # Это имя состояния, которое мы используем в ConversationHandler

# async def phi_speaking_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     pass