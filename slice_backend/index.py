from typing import Collection
from pymongo import MongoClient
from slice_backend.logger import Log, Logger
from slice_backend.model import Model
from slice_backend.search_query import SearchQuery
from slice_backend.tags.tag import Tag


class Index:
    def __init__(
        self, logger: Logger, sample_dir: str, model: Model, tags: Collection[Tag]
    ) -> None:
        self.logger = logger
        self.sample_dir = sample_dir
        self.model = model
        self.tags = tags

    def searchSamples(
        self, db: MongoClient, query: SearchQuery, start: int = 0, count: int = 25
    ):
        samples = db["slice"]["audiosamples"]

        self.logger.log(Log.DEBUG, "Embedding query", "index")
        text_embed = self.model.embed_text(query.query)

        self.logger.log(Log.DEBUG, "Executing aggregation", "index")
        res = samples.aggregate(
            [
                {
                    "$vectorSearch": {
                        "queryVector": text_embed,
                        "path": "embedding",
                        # This could become a problem.
                        "numCandidates": 1000 + start + count,
                        "index": "vector_index",
                        "limit": start + count,
                        "exact": False,
                        "filter": {
                            "$and": [
                                *[{"tags": {"$eq": tag}} for tag in query.tags],
                                {"tags": {"$eq": "SLICE:SAMPLE"}},
                            ]
                        },
                    }
                },
                {
                    "$project": {
                        "path": 1,
                        "name": 1,
                        "score": {"$meta": "vectorSearchScore"},
                    }
                },
                {"$limit": start + count},
                {"$skip": start},
            ]
        ).to_list()

        for sample in res:
            sample["_id"] = str(sample["_id"])
            sample["path"] = sample["path"].replace(self.sample_dir, "")
            if not sample["path"].startswith("/"):
                sample["path"] = "/" + sample["path"]

        return res

    def findSimilar(
        self,
        db: MongoClient,
        globalpath: str,
        start: int = 0,
        count: int = 25,
    ):
        samples = db["slice"]["audiosamples"]

        audio_embed = self.model.embed_audio(globalpath)

        res = samples.aggregate(
            [
                {
                    "$vectorSearch": {
                        "queryVector": audio_embed,
                        "path": "embedding",
                        # This could become a problem.
                        "numCandidates": 1000 + start + count,
                        "index": "vector_index",
                        "limit": start + count,
                        "exact": False,
                    }
                },
                {
                    "$project": {
                        "path": 1,
                        "name": 1,
                        "score": {"$meta": "vectorSearchScore"},
                    }
                },
                {"$limit": start + count},
                {"$skip": start},
            ]
        ).to_list()

        for sample in res:
            sample["_id"] = str(sample["_id"])
            sample["path"] = sample["path"].replace(self.sample_dir, "")
            if not sample["path"].startswith("/"):
                sample["path"] = "/" + sample["path"]

        return res
