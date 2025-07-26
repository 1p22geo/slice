from typing import List


class BTag:
    def __init__(
        self,
        id: str,
        name: str,
        name_A: str,
        name_B: str,
    ):
        self.id = id
        self.name = name
        self.name_A = name_A
        self.name_B = name_B

    def get_value(
        self, abs_path: str | None = None, embedding: List[float] | None = None
    ) -> float:
        raise NotImplementedError()
