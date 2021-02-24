from chai_py import package, Metadata
from bot.example_bot import ExampleBot

package(
    Metadata(
        name="Example Bot",
        image_url="http://picsum.photos/seed/example_bot/256/256",
        color="f1abab",
        developer_uid="__dev_anon",
        description="I am an example bot.",
        input_class=ExampleBot,
    )
)
