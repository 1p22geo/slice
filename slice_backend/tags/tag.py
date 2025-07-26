from typing import Callable


class Tag:
    def __init__(self, id: str, name: str, check: Callable[[str], bool]):
        self.id = id
        self.name = name
        self.check = check
