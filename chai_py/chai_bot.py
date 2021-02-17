from .types import Update


class ChaiBot:
    def __init__(self, uid: str):
        self.uid = uid

    async def on_message(self, update: Update) -> str:
        """
        Event called when the bot receives a message.
        @param update:
        @return:
            String containing the reply.
        """
        raise NotImplementedError

    async def get_state(self) -> dict:
        """
        Fetches bot state.
        :return:
            State [dict]
        """
        # TODO: Implement getting state from Firebase
        raise NotImplemented

    async def set_state(self, state: dict):
        """
        Sets bot's state. State has to be JSON-serializable.
        :param state:
        :return:
        """
        # TODO: Implement setting state in Firebase
        raise NotImplemented
