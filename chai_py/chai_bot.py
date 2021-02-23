import logging
import sys
from typing import List

from .logger import ColoredFormatter
from .types import Update, Message


class ChaiBot:
    def __init__(self, uid: str):
        self.uid = uid
        self.logger = logging.getLogger(self.__class__.__name__)

        self.setup_logger()

    async def on_message(self, update: Update) -> str:
        """Event called when the bot receives a message.

        @param update:
        @return:
            String containing the reply.
        """
        raise NotImplementedError

    async def get_messages(self, conversation_id: str) -> List[Message]:
        """Fetches a list of messages for the specified conversation.

        @param conversation_id:
        @return:
            List of messages in the conversation, sorted by increasing timestamp (i.e. oldest first).
        """
        raise NotImplemented

    def setup_logger(self):
        formatter = ColoredFormatter.default_chai_formatter()
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
