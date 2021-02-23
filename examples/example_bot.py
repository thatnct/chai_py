from chai_py import ChaiBot, Update


class ExampleBot(ChaiBot):
    def __init__(self, uid: str):
        super().__init__(uid)
        self.logger.info("Hello, world!")
        self.logger.info("Pretending to setup: nltk.download('punkt')")

    async def on_message(self, update: Update):
        return "Hi I'm ExampleBot"
