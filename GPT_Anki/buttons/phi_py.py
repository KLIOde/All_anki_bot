import logging
from telegram import Update
from buttons import state
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
)
from utils import  prepare_dictionary, button
import os
from saving import save

logger = logging.getLogger(__name__)


async def phi_py_1_button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Проверяем, откуда пришёл запрос: кнопка или команда
    if update.callback_query:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(
            text="📝 Введите НАЗВАНИЕ файла для Anki:",
            parse_mode="Markdown",
            reply_markup=None
        )
    return state.State.PHI_PY_1_FILE

async def phi_py_2_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['phi_py_filename'] = update.message.text
    
    await update.message.reply_text(
        text="📤 Теперь отправьте файл в формате `.apkg` для обработки",
        parse_mode="Markdown"
    )
    return state.State.PHI_PY_FILE 

async def send(res_name, output_file_path, update: Update, context: ContextTypes.DEFAULT_TYPE):
    with open(output_file_path, 'rb') as f:
            await update.message.reply_document(
                document=f,
                filename=f"{res_name}.apkg",
                caption="✅ Вот ваша колода Anki!"
            )

async def handle_phi_py_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("✅ handle_phi_file вызван!")  # Лог
    Voc = context.user_data['phi_py_filename']
    if not update.message.document:
        await update.message.reply_text("Пожалуйста, отправьте файл как документ.")
        return state.State.PHI_PY_FILE
    
    await update.message.reply_text("Все заебись")
    
    file_name = update.message.document.file_name
    if not file_name.endswith(".apkg"):
        await update.message.reply_text("❌ Файл должен быть в формате `.apkg`.")
        return state.State.PHI_PY_FILE

    file = await update.message.document.get_file()
    input_path = "downloads/latest.apkg"
    await file.download_to_drive(input_path)
    print('OK')
    try:
        res = prepare_dictionary.read(apkg_path=input_path)
        if not res:
            await update.message.reply_text("❌ Колода пуста.")
            return ConversationHandler.END
        S = save.save2apkg(res_name=Voc,  how = 'anki_parsing', id = 'advanced', res = res)     
        out_path = S.create_anki_parsing()
        print(out_path)
        # Отправляем
        await send(Voc, out_path, update, context)      
        
    except Exception as e:
        logger.exception("Ошибка в PHI обработке")
        await update.message.reply_text("❌ Ошибка при обработки файла.")
    finally:
        if os.path.exists(input_path):
            os.remove(input_path)

    await update.message.reply_text("Чем ещё могу помочь?", reply_markup=button.get_main_menu())
    return ConversationHandler.END
