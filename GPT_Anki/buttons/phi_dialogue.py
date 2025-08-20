from telegram import Update
from telegram.ext import (
    ContextTypes,
)
import logging
from neural_models import phi
from utils import text
from print import typing
from neural_models import phi

PHI_D_FILE = "phi_d_file"
logger = logging.getLogger(__name__)

async def phi_dialogue_button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(text="⌨️ Пожалуйста, введите слово для обработки в JS:")
        return PHI_D_FILE
    

async def phi_dialogue_state_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    
    await context.bot.send_chat_action(update.effective_chat.id, "typing")
    generated_words = []
    
    wait_msg = await update.message.reply_text("⏳ Подождите немного...")
    await context.bot.send_chat_action(update.effective_chat.id, "typing")
    # Начинаем печатать — удаляем предыдущее сообщение
    await context.bot.delete_message(
        chat_id=update.effective_chat.id,
        message_id=wait_msg.message_id
    )
    streamer = typing.WordStreamer(context, update.effective_chat.id)

    async def combined_callback(word):
        await streamer.send_word(word)
        generated_words.append(word)

    await phi.phi(combined_callback, user_text, prompt = 'Keep the conversation going if the following was said: ')
    await context.bot.send_chat_action(update.effective_chat.id, "cancel")

    await text.print_text(generated_words, update, context)
        
    return PHI_D_FILE