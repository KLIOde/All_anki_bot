import enum

class State(enum.Enum):
    WAITING_FOR_FILENAME = 1 
    WAITING_FOR_FILE = 2
    PHI_L_FILE = "phi_l_file"
    ASKING_FILE = "anki_file"
    GPT_FILE = "gpt_file"
    PHI_D_FILE = "phi_d_file"
    PHI_FILE = "phi_file"
    PHI_S_FILE = "phi_s_file"
class version_anki:
    old = 1
    new = 2