from chai_py import ChaiBot, Update


class ExampleBot2(ChaiBot):
    STRING = 'hi'

    def setup(self):
        self.logger.info("Hello, world!")
        self.logger.info("Pretending to setup: nltk.download('punkt')")
        self.logger.info(f"Listening for '{self.STRING}'.")

    async def on_message(self, update: Update) -> str:
        messages = await self.get_messages(update.conversation_id)
        self.logger.info(f"Received {len(messages)} messages.")
        string_count = sum(1 for message in messages if self.STRING in message.content)
        return f"The string has been said {string_count} times."
