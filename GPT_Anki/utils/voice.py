#Обработка полученного голосового сообщения. 
import os
import telebot
import speech_recognition # Преобразование голоса в текст (базаримся на готовенькое от Гугла)
from pydub import AudioSegment # Обработка аудиофайла, который присылает пользователь

def ogg2wav(filename):

    new_filename = filename.replace('.ogg', '.wav')

    audio = AudioSegment.from_file(filename)

    audio.export(new_filename, format='wav')

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

def download_file(bot, file_id):

    file_info = bot.get_file(file_id)

    downloaded_file = bot.download_file(file_info.file_path)

    filename = file_id + file_info.file_path

    filename = filename.replace('/','_') #Чтобы ошибок с косой чертой не было бллин

    with open(filename, 'wb') as f:

        f.write(downloaded_file)

    return filename