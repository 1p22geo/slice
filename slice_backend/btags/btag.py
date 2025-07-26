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

    def get_value(self, sample: str) -> float:
        raise NotImplementedError()
