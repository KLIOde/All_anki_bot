import os
from telegram import Update
from telegram.ext import ContextTypes
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
)
from utils import send_voise
import logging
from neural_models import phi
from translate import translate
from buttons import state

logger = logging.getLogger(__name__)

async def phi_listening_button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(text="⌨️ Пожалуйста введите слово:")
        return state.State.PHI_L_FILE

async def phi_listening(update: Update, context: ContextTypes.DEFAULT_TYPE):
    generated_words = []
    user_text = update.message.text
    async def combined_callback(word):
            generated_words.append(word)
    await phi.phi(combined_callback, user_text)
    await context.bot.send_chat_action(update.effective_chat.id, "cancel")
    
    return translate.trans_res(generated_words)


async def handle_text_for_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.reply_text("🔊 Генерирую голосовое сообщение...")
        #Нейронка
        eng_tg, rus_tg, eng_py, rus_py = await phi_listening(update, context)
    
        try:
            audio_file, voice_file = await send_voise.result(eng_py, update, context)
            
            await update.message.reply_text(f"🔥 Полный текст: ||{eng_tg}||", parse_mode="MarkdownV2")
            await update.message.reply_text(f"💎 Перевод: ||{rus_tg}||", parse_mode="MarkdownV2")
            
        except Exception as e:
            logger.error(f"Ошибка при генерации или отправке: {e}", exc_info=True)
            await update.message.reply_text("❌ Ошибка: " + str(e))
        finally:
            # Удаляем временные файлы
            for f in [audio_file, voice_file]:
                try:
                    if os.path.exists(f):
                        os.remove(f)
                except Exception as clean_error:
                    logger.error(f"Ошибка при удалении файла {f}: {clean_error}")

    except Exception as e:
        logger.error(f"Критическая ошибка: {e}", exc_info=True)
        await update.message.reply_text("❌ Произошла ошибка.")

    return ConversationHandler.END