import logging
import os
from telegram.ext import (
    ContextTypes,
    ConversationHandler,

)
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from utils import button
from neural_models import gpt
# Импорт функций из других модулей
from utils import prepare_dictionary
from buttons import state


logger = logging.getLogger(__name__)

async def handle_gpt_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.document:
        await update.message.reply_text("Пожалуйста, отправьте файл как документ.")
        return state.State.GPT_FILE

    file_name = update.message.document.file_name
    if not file_name.endswith(".apkg"):
        await update.message.reply_text("❌ Файл должен быть в формате `.apkg`.")
        return state.State.GPT_FILE

    file = await update.message.document.get_file()
    input_path = "downloads/latest.apkg"
    await file.download_to_drive(input_path)

    try:
        res = prepare_dictionary.read(apkg_path=input_path)
        if not res:
            await update.message.reply_text("❌ Колода пуста.")
            return ConversationHandler.END

        import numpy as np
        keys = list(res.keys())
        k = np.random.randint(0, len(keys))
        pick_word = res[keys[k]]
        
        prompt, old, trans = gpt.model(prompt=pick_word)
        await update.message.reply_text(f"Выбранное слово: \n{prompt}")
        await update.message.reply_text(f"Сгенерированный текст: \n{old}")
        await update.message.reply_text(f"Перевод: \n{trans}")

    except Exception as e:
        logger.exception("Ошибка в GPT обработке")
        await update.message.reply_text("❌ Ошибка при обработке файла.")
    finally:
        if os.path.exists(input_path):
            os.remove(input_path)

    await update.message.reply_text("Чем ещё могу помочь?", reply_markup=button.get_main_menu())
    return ConversationHandler.END

async def gpt_button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # Обязательно подтверждаем нажатие
    
    # Создаём две новые кнопки
    keyboard = [
        [
            InlineKeyboardButton("📤 Файл", callback_data="phi_py"),
            InlineKeyboardButton("📤 Слово", callback_data="phi_js"),
            InlineKeyboardButton("📤 Перевод", callback_data="phi_dialogue"),
        ],
        [
            InlineKeyboardButton("⬅️ Назад", callback_data="main_menu")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        text="Выберите тип обработки:",
        reply_markup=reply_markup
    )

# async def gpt_button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     query = update.callback_query
#     await query.answer()
#     await query.edit_message_text(
#         text="📤 Отправьте файл в формате `.apkg` для обработки в Py.",
#         parse_mode="Markdown",
#         reply_markup=None
#     )
#     return GPT_FILE
