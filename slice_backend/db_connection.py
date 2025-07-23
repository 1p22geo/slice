from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


class DatabaseError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


def create_connection(uri: str):
    client = MongoClient(uri, server_api=ServerApi("1"))

    try:
        client.admin.command("ping")
        print("DB connected")
    except Exception as e:
        print(e)
        print("DB dead")
        raise DatabaseError(e)

    return client
