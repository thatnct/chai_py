from unittest import TestCase
from collections import Counter

from chai_py import  ChaiBot, TRoom

from stateful_bot import StatefulBot

class TestStatefulBot(TestCase):

    def test_initial_message(self):

        bot = StatefulBot()
        chat_room = TRoom([bot])
        messages = []
        chat_room.test_chat(messages)
        first_message = "Enter text to see the letter count: "
        self.assertEqual(first_message, chat_room.messages[-1].content)

    def test_count_one_message(self):

        bot = StatefulBot()
        chat_room = TRoom([bot])
        messages = ["one"]
        chat_room.test_chat(messages)
        self.assertEqual(Counter(['o', 'n', 'e']), bot.counter)

    def test_multiple_messages(self):

        bot = StatefulBot()
        chat_room = TRoom([bot])
        messages = ["one", "two"]
        chat_room.test_chat(messages)
        self.assertEqual(Counter([ 'o', 'n', 'e', 't', 'w', 'o']), bot.counter)

