from chai_py import ChaiBot, Update
from collections import Counter


class StatefulBot(ChaiBot):

    def setup(self):
        self.counter = Counter()

    async def on_message(self, update: Update) -> str:

        if update.latest_message.text == self.FIRST_MESSAGE_STRING:
            return "Enter text to see the letter count: " 

        self.counter += Counter(c for c in update.latest_message.text)

        return self.counter.__str__()

