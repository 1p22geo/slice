"""
Proof-of-concept for sample indexing

DROPS THE COLLECTION ON RUN

Finds all samples, calculates embeddings and saves into collection.

Slow as hell, but only needs to be done once.
"""

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
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
audiosamples.delete_many({})

model = laion_clap.CLAP_Module(enable_fusion=False)
model.load_ckpt(model_id=1)
print("Model connected")

for root, dirnames, filenames in os.walk("./data/SAMPLES/SAMLEFOKUS", followlinks=True):
    for filename in fnmatch.filter(filenames, "*.wav"):
        file = str(os.path.join(root, filename))
        audio_embed = model.get_audio_embedding_from_filelist(
            x=[
                file,
            ],
            use_tensor=False,
        )[0].tolist()

        audiosamples.insert_one(
            {"path": file, "name": filename, "embedding": audio_embed}
        )
