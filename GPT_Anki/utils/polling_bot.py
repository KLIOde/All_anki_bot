import logging
import os
from telegram.ext import (
    Application,
    CommandHandler,

)
from commands import anki_command
from buttons import state, anki, gpt, phi, phi_js, phi_py, phi_dialogue, phi_listening, phi_speaking
from utils import button, text
from commands import anki_command, speaking_command, listening_command, gpt_command, phi_command, phi_py_command
from saving import save

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

def Start():
    
    S = save.save2apkg()
    text.delete_all_old_mp3(S.folder)
    
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    button.comands(application)
    
    button.create_read_File(
        WAITING_FOR_FILENAME = state.State.WAITING_FOR_FILENAME,
        WAITING_FOR_FILE = state.State.WAITING_FOR_FILE,
        pattern = text.pattern(callback_anki),
        button_handler  =anki.anki_button_handler,
        handle_name_file = anki.anki_handle_filename,
        handle_get_file = anki.handle_anki_file,
        command_name = anki_command.command_name,
        command_func= anki_command.start_anki_conversation,
        app = application
        )

    button.create_read_file(
        name_file = state.State.GPT_FILE,
        pattern = text.pattern(callback_gpt),
        button_handler  =gpt.gpt_button_handler,
        handle_file = gpt.handle_gpt_file,
        command_name= gpt_command.command_name,
        command_func= gpt_command.start_gpt_command,
        apli = application
        )

    button.create_read_file(
        name_file = state.State.PHI_FILE,
        pattern = patter_phi,
        button_handler  =phi.phi_button_handler,
        handle_file = phi.handle_phi_file,
        command_name= phi_command.command_name,
        command_func= phi_command.start_phi_command,
        apli = application
        )

    button.create_read_File_py(
        WAITING_FOR_FILENAME = state.State.PHI_PY_1_FILE,
        WAITING_FOR_FILE = state.State.PHI_PY_FILE,
        pattern = text.pattern(callback_phi_py),
        button_handler  =phi_py.phi_py_1_button_handler,
        handle_name_file = phi_py.phi_py_2_handler,
        handle_get_file = phi_py.handle_phi_py_file,
        command_name = phi_py_command.command_name,
        command_func= phi_py_command.start_phi_py_command,
        app = application
        )

    button.create_read_text(
        name_file = state.State.PHI_FILE,
        pattern= patter_phi_js,
        button_handler = phi_js.phi_js_button_handler,
        handle_file=phi_js.phi_js_state_handler,
        app = application
    )

    button.create_read_text(
        name_file = state.State.PHI_D_FILE,
        pattern= patter_phi_dialogue,
        button_handler = phi_dialogue.phi_dialogue_button_handler,
        handle_file=phi_dialogue.phi_dialogue_state_handler,
        app = application
    )

    button.create_read_return_voice(
        name_file=state.State.PHI_L_FILE,
        pattern= patter_phi_listening,
        button_handler = phi_listening.phi_listening_button_handler,
        handle_file=phi_listening.handle_text_for_voice,
        command_name=listening_command.command_name,
        command_func=listening_command.start_listening_command,
        apli = application
    )

    button.create_read_send_voice(
        name_file = state.State.PHI_S_FILE,
        pattern= patter_phi_speaking,
        button_handler = phi_speaking.phi_speaking_button_handler,
        handle_file=phi_speaking.phi_speaking_handler,
        command_name=speaking_command.command_name,
        command_func=speaking_command.start_speaking_command,
        apli = application
    )
    print("Бот запущен... Ожидание сообщений.")
    application.run_polling()