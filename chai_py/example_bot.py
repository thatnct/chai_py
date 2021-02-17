from .chai_bot import ChaiBot


class ExampleBot(ChaiBot):
    def __init__(self, uid: str):
        super().__init__(uid)
        print("Hello, world!")
        print("Pretending to setup: nltk.download('punkt')")

    async def on_message(self, *args):
        return "Hi I'm ExampleBot"
