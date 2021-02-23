import asyncio
import time
import uuid
from typing import Sequence

from chai_py import ChaiBot, Update, LatestMessage, Message, MessageKind


class TRoom:
    def __init__(self, bots: Sequence[ChaiBot]):
        self.bots = bots
        self.conversation_id = str(uuid.uuid4())
        self.messages = []

    def start(self):
        print("Starting TRoom. Press ctrl-c to escape.")
        self.setup_bots()
        asyncio.run(self._loop())

    async def _loop(self):
        while True:
            message = input("Enter your message: ")
            await self.send_message(message)

    def setup_bots(self):
        async def get_messages_local(conversation_id: str):
            return self.messages

        for bot in self.bots:
            bot.get_messages = get_messages_local

    async def send_message(self, message: str):
        timestamp = int(time.time() * 1000)
        print(f"<<< {message}")
        self.messages.append(
            Message(
                sender_name='local_dev',
                timestamp=timestamp,
                message_kind=MessageKind.TEXT,
                content=message,
            )
        )
        update = Update(
            conversation_id=self.conversation_id,
            latest_message=LatestMessage(
                text=message,
                timestamp=timestamp
            )
        )

        for coro in asyncio.as_completed([self._bot_on_message(bot, update) for bot in self.bots]):
            bot, result = await coro
            print(f">>> {result}")
            self.messages.append(
                Message(
                    sender_name=bot.__class__.__name__,
                    timestamp=timestamp,
                    message_kind=MessageKind.TEXT,
                    content=result,
                )
            )

    @staticmethod
    async def _bot_on_message(bot: ChaiBot, update: Update):
        result = await bot.on_message(update)
        return bot, result
