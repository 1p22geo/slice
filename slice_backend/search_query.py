class SearchQuery:
    def __init__(self) -> None:
        self.query = ""
        self.tags = {}
        self.btags = {}

    def addQuery(self, query: str) -> None:
        self.query = query

    def addTag(self, tag: str, selected: bool) -> None:
        self.tags[tag] = selected

    def addBTag(self, tag: str, value: float) -> None:
        self.btags[tag] = value
