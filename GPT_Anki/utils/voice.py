#Обработка полученного голосового сообщения. 
import os
import telebot
import speech_recognition # Преобразование голоса в текст (базаримся на готовенькое от Гугла)
from pydub import AudioSegment # Обработка аудиофайла, который присылает пользователь

from pydub import AudioSegment
import os

def ogg2wav(filename):
    # Проверка существования файла
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Файл не найден: {filename}")

    # Разделяем имя и расширение
    base, ext = os.path.splitext(filename)
    if ext.lower() != '.ogg':
        raise ValueError("Ожидается файл с расширением .ogg")

    new_filename = base + '.wav'

    # Загрузка и конвертация
    try:
        audio = AudioSegment.from_file(filename, format='ogg')
        audio.export(new_filename, format='wav')
    except Exception as e:
        raise RuntimeError(f"Ошибка при конвертации: {e}")

    return new_filename

def recognize_speech(ogg_filename):

    wav_filename = ogg2wav(ogg_filename)

    recognizer = speech_recognition.Recognizer()

    with speech_recognition.WavFile(wav_filename) as source:

        wav_audio = recognizer.record(source)

    text = recognizer.recognize_google(wav_audio, language='en')

    if os.path.exists(ogg_filename):

        os.remove(ogg_filename)

    if os.path.exists(wav_filename):

        os.remove(wav_filename)

    return text 

from telegram import Update
from telegram.ext import ContextTypes

async def download_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Проверяем, есть ли голосовое сообщение
    if not update.message.voice:
        await update.message.reply_text("❌ Пожалуйста, отправьте голосовое сообщение.")
        return

    # Получаем объект голосового сообщения
    voice = update.message.voice

    # Опционально: можно проверить длительность или формат
    file_name = f"voice_{voice.file_id}.ogg"  # Telegram использует .ogg для голосовых
    input_path = f"downloads/{file_name}"

    # Создаём папку, если её нет
    import os
    os.makedirs("downloads", exist_ok=True)

    # Получаем файл и скачиваем
    file = await voice.get_file()
    await file.download_to_drive(input_path)

    await update.message.reply_text(f"✅ Голосовое сообщение сохранено как: {input_path}")
    return input_path