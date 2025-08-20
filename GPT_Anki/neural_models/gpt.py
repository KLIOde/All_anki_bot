import numpy as np
from transformers import pipeline
from deep_translator import GoogleTranslator
from utils import prepare_dictionary 

def model(prompt="Cat", mo="gpt2"):
    if mo == 'gpt2':
    # Загрузка модели (например, gpt2-medium)
        generator = pipeline(
            "text-generation",
            model=mo,  # или любая другая
            pad_token_id=50256  # важно для GPT-2
        )

        # Получение ID токена для точки "."
        tokenizer = generator.tokenizer
        model = generator.model

        dot_token_id = tokenizer.encode(".", add_special_tokens=False)[0]  # ID токена точки
        eos_token_id = tokenizer.eos_token_id  # стандартный конец последовательности

        # Генерация текста
        output = generator(
            prompt,
            max_new_tokens=30,
            eos_token_id=[dot_token_id, eos_token_id],  # завершать на точке или EOS
            early_stopping=True,       # остановиться, как только встретится один из eos
            do_sample=True,
            temperature=0.7,
            top_k=50,
            top_p=0.9,
        )

        generated_sentences = [out['generated_text'] for out in output]
        result = []
        # Выводим результат
        for i, sentence in enumerate(generated_sentences, 1):
            result.append(sentence)
        #print(f"Выбранное слово\n{prompt}")
        # Перевод первого варианта на русский язык
        translated = GoogleTranslator(source='auto', target='ru').translate(result[0])
        res  = GoogleTranslator(source='auto', target='en').translate(translated)
        return prompt, res, translated
if __name__ == "__main__":


    res = prepare_dictionary.read('Anki2.apkg') # Чтение данных из Anki-коллекции

    if not res:
        print("Коллекция Anki пуста.")   # Проверка, что коллекция не пуста
        exit()
    k = np.random.randint(len(res.keys()))    # Выбор случайного слова из Anki-коллекции
    random_word = list(res.keys())[k]
    print(f"Хуйня: {random_word}")

    prompt, generated_texts, translated_text = model(prompt=random_word)  # Генерация текста с использованием выбранного слова
    print('Сгенерированный текст:', generated_texts)
    print('Перевод:', translated_text)
