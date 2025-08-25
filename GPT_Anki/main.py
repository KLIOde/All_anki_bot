import logging
import os
from telegram.ext import (
    Application,
    CommandHandler,

)
from buttons import state, anki, gpt, phi, phi_js, phi_py, phi_dialogue, phi_listening, phi_speaking
from utils import button, text
from commands import start

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)
TELEGRAM_TOKEN = "8134028537:AAEddvqQNy3ovVrxZ49h1LO7rt4CnWiz1FA"
os.makedirs("downloads", exist_ok=True)

callback_anki="anki_menu"
callback_gpt="gpt_menu"
callback_gpt="gpt_gp_menu"
callback_phi="phi_menu"
callback_phi_py="phi_py"
callback_phi_js="phi_js"
callback_phi_dialogue="phi_dialogue"
callback_phi_listening="phi_listening"
callback_phi_speaking="phi_speaking"


patter_phi = "^" + callback_phi + "$"
patter_phi_py = "^" + callback_phi_py + "$"
patter_phi_js = "^" + callback_phi_js + "$"
patter_phi_dialogue = "^" + callback_phi_dialogue + "$"
patter_phi_listening = "^" + callback_phi_listening + "$"
patter_phi_speaking = "^" + callback_phi_speaking + "$"

def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("start", start.start))
    button.create_read_anki(
        WAITING_FOR_FILENAME = state.State_anki.WAITING_FOR_FILENAME,
        WAITING_FOR_FILE = state.State_anki.WAITING_FOR_FILE,
        pattern = text.pattern(callback_anki),
        button_handler  =anki.anki_button_handler,
        handle_name_file = anki.anki_handle_filename,
        handle_get_file = anki.handle_anki_file,
        app = application
        )
    
    button.create_read_file(
        name_file = gpt.GPT_FILE,
        pattern = text.pattern(callback_gpt),
        button_handler  =gpt.gpt_button_handler,
        handle_file = gpt.handle_gpt_file,
        apli = application
        )

    button.create_read_file(
        name_file = phi.PHI_FILE,
        pattern = patter_phi,
        button_handler  =phi.phi_button_handler,
        handle_file = phi.handle_phi_file,
        apli = application
        )

    button.create_read_file(
        name_file = phi_py.PHI_FILE,
        pattern= patter_phi_py,
        button_handler = phi_py.phi_py_handler,
        handle_file=phi.handle_phi_file,
        apli = application
    )

    button.create_read_text(
        name_file = phi_py.PHI_FILE,
        pattern= patter_phi_js,
        button_handler = phi_js.phi_js_button_handler,
        handle_file=phi_js.phi_js_state_handler,
        app = application
    )

    button.create_read_text(
        name_file = phi_dialogue.PHI_D_FILE,
        pattern= patter_phi_dialogue,
        button_handler = phi_dialogue.phi_dialogue_button_handler,
        handle_file=phi_dialogue.phi_dialogue_state_handler,
        app = application
    )
    
    button.create_read_return_voice(
        name_file=phi_listening.PHI_L_FILE,
        pattern= patter_phi_listening,
        button_handler = phi_listening.phi_listening_button_handler,
        handle_file=phi_listening.handle_text_for_voice,
        apli = application
    )

    # button.create_read_send_voice(
    #     name_file = phi_py.PHI_FILE,
    #     pattern= patter_phi_speaking,
    #     button_handler = phi_speaking.phi_speaking_button_handler,
    #     handle_file=phi_speaking.phi_speaking_handler,
    #     apli = application
    # )
    print("Бот запущен... Ожидание сообщений.")
    application.run_polling()

if __name__ == '__main__':
    main()