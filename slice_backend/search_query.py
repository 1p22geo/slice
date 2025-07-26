from typing import Dict, List


class SearchQuery:
    def __init__(self) -> None:
        self.query = ""
        self.tags: List[str] = []
        self.btags: Dict[str, float] = {}

    def addQuery(self, query: str) -> None:
        self.query = query

    def addTag(self, id: str) -> None:
        self.tags.append(id)

    def addBTag(self, id: str, value: float) -> None:
        self.btags[id] = value
