from chai_py import ChaiBot, Update


class ExampleBot2(ChaiBot):
    STRING = 'hi'

    def __init__(self, uid: str):
        super().__init__(uid)
        self.logger.info("Hello, world!")
        self.logger.info(f"Listening for '{self.STRING}'.")

    async def on_message(self, update: Update):
        messages = await self.get_messages(update.conversation_id)
        string_count = sum(1 for message in messages if self.STRING in message.content)
        return f"The string has been said {string_count} times."
