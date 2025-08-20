import requests
import asyncio
import json
import re
async def stream_words(callback):
    """
    Генерирует слова по одному и вызывает callback для каждого.
    """
    full_text = "Привет, я нейросеть. Я печатаю каждое слово постепенно, как живой человек."
    words = full_text.split()

    for word in words:
        await callback(word)  # Отправляем слово в бота
        await asyncio.sleep(0.4)  # Имитация "печати"


def respon(sentense, link, model, prompt, stream, timeout):
    return requests.post(
            link,
            json={
                'model': model,
                'prompt': prompt + sentense,
                'stream': stream
            },
            stream=True,
            timeout=timeout
        )
    
async def phi(callback, sentense, prompt = 'Tell me a one sentense with this word or sentense: '):
    """
    Запрашивает у Ollama потоковый ответ и отправляет полные слова в callback.
    """
    buffer = ""

    try:
        response = respon(
            sentense = sentense,
            link = 'http://localhost:11434/api/generate',
            model = 'phi3',
            prompt= prompt,
            stream=True,
            timeout=30
        )
        
        for line in response.iter_lines():
            if not line:
                continue

            try:
                chunk = line.decode('utf-8')
                data = json.loads(chunk)
                textt = data.get("response", "")
                if not textt:
                    continue

                buffer += textt
                parts = re.split(r'(\s+|[.,!?;:])', buffer)
                complete_parts = parts[:-1]
                buffer = parts[-1]
                for part in complete_parts:
                    part = part.strip()
                    if part:  # Исключаем пустые и чистые пробелы
                        await callback(part)
                
            except json.JSONDecodeError:
                continue
            except Exception as e:
                print(f"Ошибка в обработке чанка: {e}")

        # После завершения потока — отправляем остаток буфера (на случай, если что-то осталось)
        if buffer.strip():
            await callback(buffer.strip())

    except requests.exceptions.ConnectionError:
        error_msg = "❌ Не удалось подключиться к Ollama. Убедитесь, что Ollama запущен: `ollama run phi3`"
        await callback(error_msg)
    except requests.exceptions.Timeout:
        await callback("❌ Таймаут подключения к Ollama.")
    except Exception as e:
        await callback(f"❌ Ошибка: {str(e)}")