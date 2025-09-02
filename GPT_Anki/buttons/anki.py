import logging
import os
from telegram import Update
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
)
from utils import button
from saving import save
from buttons import state

logger = logging.getLogger(__name__)


# Anki Conversation
async def anki_button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Проверяем, откуда пришёл запрос: кнопка или команда
    if update.callback_query:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(
            text="📝 Введите НАЗВАНИЕ файла для Anki:",
            parse_mode="Markdown",
            reply_markup=None
        )
    return state.State.WAITING_FOR_FILENAME

async def anki_handle_filename(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Сохраняем название файла в контексте
    context.user_data['anki_filename'] = update.message.text
    
    # Затем запрашиваем сам файл
    await update.message.reply_text(
        text="📤 Теперь отправьте файл в формате `.txt` для обработки в Anki:",
        parse_mode="Markdown"
    )
    
    # Переходим в состояние ожидания файла
    return state.State.WAITING_FOR_FILE

# Парсинг
async def parsing(update: Update, context: ContextTypes.DEFAULT_TYPE):
    return  update.message.document.file_name

#Скачивание
async def load(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = await update.message.document.get_file()
    input_path = "downloads/latest.txt"
    await file.download_to_drive(input_path)
    logger.info(f"Файл сохранён как {input_path}")
    return input_path

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! Упрости

async def send(res_name, output_file_path, update: Update, context: ContextTypes.DEFAULT_TYPE):
    with open(output_file_path, 'rb') as f:
            await update.message.reply_document(
                document=f,
                filename=f"{res_name}.apkg",
                caption="✅ Вот ваша колода Anki!"
            )

#Ошибки
async def error_parsing(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.document:
        await update.message.reply_text("Пожалуйста, отправьте файл как документ.")
        return state.State.ASKING_FILE

async def error_load(file_name, update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not file_name.endswith(".txt"):
        await update.message.reply_text("❌ Файл должен быть в формате `.txt`.")
        return state.State.ASKING_FILE

async def error_create_file(output_file_path, update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not os.path.exists(output_file_path):
        await update.message.reply_text("❌ Ошибка: файл колоды не был создан.")
        return ConversationHandler.END

async def handle_anki_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    await error_parsing(update, context)
    #Название, которое хочет пользователь
    
    Voc = context.user_data['anki_filename']
    
    #Загрузка
    file_name = await parsing(update, context)
    
    await error_load(file_name, update, context)

    # Скачиваем
    input_path = await load(update, context)    
    print(input_path)
    try:
        # Вызываем saving
        S = save.save2apkg(how='anki_lms', res_name=Voc, file=input_path, id = 'new_advanced')
        output_file_path = S.saving()
        print('OK', output_file_path)
        # Проверяем, что файл создан
        await error_create_file(output_file_path, update, context)

        # Отправляем
        await send(Voc, output_file_path, update, context)        

        # Очистка (опционально)
        os.remove(input_path)
        # os.remove(output_file_path)  # если не хочешь хранить

    except FileNotFoundError:
        await update.message.reply_text("❌ Ошибка: не удалось найти загруженный файл.")
    except ValueError as e:
        await update.message.reply_text(f"❌ Ошибка обработки файла:\n{e}")
    except Exception as e:
        logger.exception("Неизвестная ошибка в saving()")
        await update.message.reply_text(
            "❌ Произошла ошибка при создании колоды.\n"
            "Возможно, файл имеет неправильный формат.\n"
            "Пример правильной строки:\n`hello – привет`"
        )
        return ConversationHandler.END

    await update.message.reply_text("Чем ещё могу помочь?", reply_markup=button.get_main_menu())
    return ConversationHandler.END
