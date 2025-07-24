import uuid
from pymongo import MongoClient
from slice_backend.logger import Log, Logger


class Tag:
    def __init__(self, id: uuid.UUID, name: str, btag: bool) -> None:
        self.id = id
        self.name = name
        self.btag = btag

    def __eq__(self, value: object, /) -> bool:
        if isinstance(value, Tag):
            return self.id == value.id
        if isinstance(value, uuid.UUID):
            return self.id == value
        if isinstance(value, str):
            return self.id == uuid.UUID(value)
        if isinstance(value, bytes):
            return self.id == uuid.UUID(bytes=value)

        raise TypeError("this is not a tag")

    @staticmethod
    def getTagList(db: MongoClient, logger: Logger):
        # TODO: create this thing
        logger.log(Log.DEBUG, "Retrieving tag list", "tag")
        return [Tag(uuid.uuid4(), "test tag", False)]
