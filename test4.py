from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import numpy as np
import laion_clap
import fnmatch
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

audio_embed = model.get_audio_embedding_from_filelist(
    x=[
        "./data/SAMPLES/ACTUAL_LIBRARY/DRUMS/SNARE/PITCHED/snare break remake.wav",
    ],
    use_tensor=False,
)[0].tolist()

res = audiosamples.aggregate(
    [
        {
            "$vectorSearch": {
                "queryVector": audio_embed,
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
