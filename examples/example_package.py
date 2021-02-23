from pathlib import Path

from chai_py.packaging import package, Metadata
from example_bot_1.example_bot import ExampleBot

base_dir = Path("example_bot_1")
package(
    base_dir,
    Metadata(
        name="Example Bot",
        image_url="http://picsum.photos/seed/example_bot/256/256",
        color="f1abab",
        developer_uid="__dev_anon",
        description="I am an example bot.",
        input_class=ExampleBot,
    )
)
