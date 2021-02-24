from chai_py import ChaiBot, Update


class ExampleBot(ChaiBot):
    def setup(self):
        self.logger.info("Hello, world!")

    async def on_message(self, update: Update) -> str:
        return "Hi I'm ExampleBot"
