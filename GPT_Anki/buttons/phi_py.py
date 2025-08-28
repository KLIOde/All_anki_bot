import logging
from telegram import Update
from telegram.ext import (
    ContextTypes,
)
from buttons import state
logger = logging.getLogger(__name__)

async def phi_py_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        text="📤 Отправьте файл в формате `.apkg` для обработки в Py.",
        parse_mode="Markdown"
    )
    #context.user_data['awaiting_input'] = 'phi_py'
    return state.State.PHI_FILE  # ✅ Переход в состояние ожидания файла
