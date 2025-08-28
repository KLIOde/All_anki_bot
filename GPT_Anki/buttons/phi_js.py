from telegram import Update
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
)
import logging
from neural_models import phi
from utils import text, button
from print import typing
from neural_models import phi
from buttons import state

logger = logging.getLogger(__name__)

# Это будет state-обработчик внутри ConversationHandler
async def phi_js_state_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    
    await context.bot.send_chat_action(update.effective_chat.id, "typing")
    generated_words = []
    
    await update.message.reply_text("Подождите немного...")

    streamer = typing.WordStreamer(context, update.effective_chat.id)

    async def combined_callback(word):
        await streamer.send_word(word)
        generated_words.append(word)

    await phi.phi(combined_callback, user_text)
    await context.bot.send_chat_action(update.effective_chat.id, "cancel")

    await text.print_text(generated_words, update, context)
        
    await update.message.reply_text("Чем ещё могу помочь?", reply_markup=button.get_main_menu())

    # Завершаем диалог
    return ConversationHandler.END


# Это будет entry_point (когда нажимают кнопку)
async def phi_js_button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="⌨️ Пожалуйста, введите слово для обработки в JS:")

    # Переходим в состояние PHI_FILE
    return state.State.PHI_FILE  # Это имя состояния, которое мы используем в ConversationHandler