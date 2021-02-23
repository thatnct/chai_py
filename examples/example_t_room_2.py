from chai_py.t_room import TRoom
from examples.example_bot_2.example_bot_2 import ExampleBot2

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
