"""
Proof-of-concept for searching samples by string search query.

Queries the database for samples similar to a text embedding.
Does not go through sample files, only through metadata in a MongoDB cluster.

More optimised search than Splice.
At least, should be.
"""

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import laion_clap
import os

load_dotenv()

uri = os.getenv("MONGODB_URI")

client = MongoClient(uri, server_api=ServerApi("1"))

try:
    client.admin.command("ping")
    print("DB connected")
except Exception as e:
    print(e)
    print("DB dead")
    os._exit(1)

audiosamples = client["slice"]["audiosamples"]

model = laion_clap.CLAP_Module(enable_fusion=False)
model.load_ckpt(model_id=1)
print("Model connected")

text_embed = model.get_text_embedding(
    x=[
        "Pitched future bass snare",
    ],
    use_tensor=False,
)[0].tolist()

res = audiosamples.aggregate(
    [
        {
            "$vectorSearch": {
                "queryVector": text_embed,
                "path": "embedding",
                "numCandidates": 30,
                "index": "vector_index",
                "limit": 10,
            }
        },
        {"$project": {"path": 1, "name": 1, "score": {"$meta": "vectorSearchScore"}}},
    ]
).to_list()

print(res)
