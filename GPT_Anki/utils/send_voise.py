import tempfile
import os
from gtts import gTTS
from pydub import AudioSegment
from telegram import Update, InputFile
from telegram.ext import ContextTypes
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
)
from utils import send_voise
import logging
import time

logger = logging.getLogger(__name__)

# Обработка голосового сообщения
#Временные файлы
def timeout_file():
    temp_dir = tempfile.gettempdir()
    timestamp = str(int(time.time()))
    audio_file = os.path.join(temp_dir, f"tts_output_{timestamp}.mp3")
    voice_file = os.path.join(temp_dir, f"voice_message_{timestamp}.ogg")
    return audio_file, voice_file

# Генерация TTS с обработкой возможных ошибок
async def generate_tts(audio_file, eng_py, update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        tts = gTTS(text=eng_py, lang='en', slow=False)
        tts.save(audio_file)
    except Exception as tts_error:
        logger.error(f"Ошибка gTTS: {tts_error}")
        await update.message.reply_text("❌ Ошибка при генерации речи.")
        return ConversationHandler.END

async def convector_MP3_OGG(audio_file, voice_file, update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        sound = AudioSegment.from_mp3(audio_file)
        sound.export(voice_file, format="ogg", codec="libopus")
    except Exception as conv_error:
        logger.error(f"Ошибка конвертации: {conv_error}")
        await update.message.reply_text("❌ Ошибка конвертации аудио. Убедитесь, что установлен ffmpeg.")
        return ConversationHandler.END
    
async def examination(voice_file, update: Update, context: ContextTypes.DEFAULT_TYPE):
       if not os.path.exists(voice_file) or os.path.getsize(voice_file) == 0:
            logger.error(f"Файл {voice_file} не был создан или пустой!")
            await update.message.reply_text("❌ Не удалось конвертировать аудио.")
            return ConversationHandler.END

async def send_voised(voice_file, update: Update, context: ContextTypes.DEFAULT_TYPE):
    with open(voice_file, 'rb') as voice:
        await context.bot.send_voice(
            chat_id=update.effective_chat.id,
            voice=InputFile(voice),
            caption="🎙️ HI!"
        )

async def exam1(audio_file, update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not os.path.exists(audio_file) or os.path.getsize(audio_file) == 0:
        logger.error(f"Файл {audio_file} не был создан или пустой!")
        await update.message.reply_text("❌ Не удалось создать аудиофайл.")
        return ConversationHandler.END


async def result(eng_py, update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Создаем временные файлы с уникальными именами
            
    audio_file, voice_file = send_voise.timeout_file()
    # Генерация TTS с обработкой возможных ошибок
    await generate_tts(audio_file, eng_py, update, context)
    
    # Проверка файла
    await exam1(audio_file, update, context)

    # Конвертация MP3 → OGG
    
    await convector_MP3_OGG(audio_file, voice_file, update, context)
    
    # Проверка OGG файла
    
    await examination(voice_file, update, context)

    # Отправка голосового
    await send_voised(voice_file, update, context)
    return audio_file, voice_file