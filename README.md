# ChaiPy

A developer interface for creating chatbots for the Chai app.


## Requirements
Python 3.8 is required due to the usage of the `dirs_exist_ok` argument in [`shutil.copytree()`](https://docs.python.org/3.8/library/shutil.html#shutil.copytree)

Manual workarounds exist (see [here](https://stackoverflow.com/q/1868714)), enabling the potential support of earlier 
versions of Python. Other potential limiting factors include the use of `asyncio.run()`, and of `async` in general.

