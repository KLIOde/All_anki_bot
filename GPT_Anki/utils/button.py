from telegram.ext import (
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes,
    ConversationHandler,
    Application,
)

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
#from buttons import anki
def get_main_menu():
    keyboard = [
        [InlineKeyboardButton("Anki", callback_data="anki_menu")],  # ✅
        [InlineKeyboardButton("GPT", callback_data="gpt_menu")],
        [InlineKeyboardButton("PHI3", callback_data="phi_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Операция отменена.",
        reply_markup=get_main_menu()
    )
    return ConversationHandler.END
def create_read_file(name_file, pattern, button_handler, handle_file, apli):
    buton = ConversationHandler(
        entry_points=[CallbackQueryHandler(button_handler, pattern=pattern)],
        states={name_file: [MessageHandler(filters.Document.ALL, handle_file)]},
        fallbacks=[CommandHandler("cancel", cancel)],
        per_user=True,
    )
    apli.add_handler(buton)
def create_read_text(name_file, pattern, button_handler, handle_file, app):
    buton = ConversationHandler(
        entry_points=[CallbackQueryHandler(button_handler, pattern=pattern)],
        states={name_file: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_file)]},
        fallbacks=[CommandHandler("cancel", cancel)],
        per_user=True,
    )
    app.add_handler(buton)
    
def create_read_return_voice(name_file, pattern, button_handler, handle_file, apli):
    buton = ConversationHandler(
        entry_points=[CallbackQueryHandler(button_handler, pattern=pattern)],
        states={name_file: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_file)]},
        fallbacks=[CommandHandler("cancel", cancel)],
        per_user=True,
    )
    apli.add_handler(buton)
    
    
    
def create_read_anki(WAITING_FOR_FILENAME, WAITING_FOR_FILE, pattern, button_handler, handle_name_file, handle_get_file, app):
    buton = ConversationHandler(
        entry_points=[CallbackQueryHandler(button_handler, pattern=pattern)],
        states={
        WAITING_FOR_FILENAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_name_file)],
        WAITING_FOR_FILE: [MessageHandler(filters.Document.TXT, handle_get_file)],
    },
        fallbacks=[CommandHandler("cancel", cancel)],
        per_user=True,
    )
    app.add_handler(buton)
    
def create_read_send_voice(name_file, pattern, button_handler, handle_file, apli):
    buton = ConversationHandler(
        entry_points=[CallbackQueryHandler(button_handler, pattern=pattern)],
        states={name_file: [MessageHandler(filters.VOICE & ~filters.COMMAND, handle_file)]},
        fallbacks=[CommandHandler("cancel", cancel)],
        per_user=True,
    )
    apli.add_handler(buton)