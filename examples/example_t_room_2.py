from chai_py import ChaiBot, Update
from chai_py.t_room import TRoom


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


t_room = TRoom([ExampleBot2("DEV")])
t_room.start()


#
# ExampleBot2.package(
#     Metadata(
#         dev_uid="123"
#     )
# )
# ExampleBot2.predeploy_check()
# ExampleBot2.deploy()
