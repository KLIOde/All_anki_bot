from deep_translator import GoogleTranslator
from utils import text
def trans(word):   
    translated = GoogleTranslator(source='auto', target='ru').translate(word)
    return translated

def trans_ru(word):   
    translated = GoogleTranslator(source='auto', target='en').translate(word)
    return translated


def trans_res(generated_words):
    eng_py = " ".join(generated_words)
    rus_py = trans(eng_py)
    rus_tg = text.escape_markdown_v2(rus_py)
    eng_tg = text.escape_markdown_v2(eng_py)
    return eng_tg, rus_tg, eng_py, rus_py

if __name__ == "__main__":
    trans('cat')