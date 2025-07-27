from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


class DatabaseError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


def create_connection(uri: str):
    client = MongoClient(
        uri,
        server_api=ServerApi("1"),
        maxPoolSize=50,
        socketTimeoutMS=60000,
        connectTimeoutMS=60000,
        minPoolSize=3,
    )

    try:
        client.admin.command("ping")
    except Exception as e:
        print(e)
        print("DB dead")
        raise DatabaseError(e)

    return client
