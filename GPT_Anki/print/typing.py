class WordStreamer:
    def __init__(self, context, chat_id):
        self.context = context
        self.chat_id = chat_id
        self.partial_message = ""
        self.message_id = None

    async def send_word(self, word):
        """Функция-коллбэк: вызывается для каждого слова"""
        self.partial_message += word + " "

        # Показываем индикатор печати
        await self.context.bot.send_chat_action(self.chat_id, "typing")

        # Удаляем старое сообщение или редактируем
        if self.message_id:
            try:
                await self.context.bot.edit_message_text(
                    chat_id=self.chat_id,
                    message_id=self.message_id,
                    text=self.partial_message.strip()
                )
            except Exception as e:
                print(f"Ошибка редактирования: {e}")
        else:
            # Первое сообщение
            sent = await self.context.bot.send_message(
                chat_id=self.chat_id,
                text=self.partial_message.strip()
            )
            self.message_id = sent.message_id

