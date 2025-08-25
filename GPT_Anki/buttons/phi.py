import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
)
from print import typing
from utils import text, button, prepare_dictionary
from translate import translate
from neural_models import phi
PHI_FILE = "phi_file"
logger = logging.getLogger(__name__)

async def phi_button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # Обязательно подтверждаем нажатие
    
    # Создаём две новые кнопки
    keyboard = [
        [
            InlineKeyboardButton("📤 Файл", callback_data="phi_py"),
            InlineKeyboardButton("📤 Слово", callback_data="phi_js"),
            InlineKeyboardButton("📤 Диалог", callback_data="phi_dialogue"),
            InlineKeyboardButton("📤 Слух", callback_data="phi_listening"),
            InlineKeyboardButton("📤 Говорение", callback_data="phi_speaking"),
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

async def handle_phi_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("✅ handle_phi_file вызван!")  # Лог
    if not update.message.document:
        await update.message.reply_text("Пожалуйста, отправьте файл как документ.")
        return PHI_FILE
    await update.message.reply_text("Все заебись")
    file_name = update.message.document.file_name
    if not file_name.endswith(".apkg"):
        await update.message.reply_text("❌ Файл должен быть в формате `.apkg`.")
        return PHI_FILE

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

        print('========================================')
        print(f"Выбрано слово: {pick_word}")
        trans_pick_word = translate.trans_ru(pick_word)
        #Исправить
        generated_words = []
        await update.message.reply_text(f"Выбранное слово: {trans_pick_word}, ||{pick_word}||", parse_mode="MarkdownV2")
        await update.message.reply_text("Подождите немного...")

        streamer = typing.WordStreamer(context, update.effective_chat.id)

        async def combined_callback(word):
            await streamer.send_word(word)
            generated_words.append(word)

        await phi.phi(combined_callback, trans_pick_word)
        await context.bot.send_chat_action(update.effective_chat.id, "cancel")

        #Печать текста:
        
        await text.print_text(generated_words, update, context)
        
        await update.message.reply_text("Чем ещё могу помочь?", reply_markup=button.get_main_menu())

        # Завершаем диалог
        return ConversationHandler.END
    except Exception as e:
        logger.exception("Ошибка в PHI обработке")
        await update.message.reply_text("❌ Ошибка при обработки файла.")
    finally:
        if os.path.exists(input_path):
            os.remove(input_path)

    await update.message.reply_text("Чем ещё могу помочь?", reply_markup=button.get_main_menu())
    return ConversationHandler.END
