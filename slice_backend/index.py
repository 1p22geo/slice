from typing import Collection
from pymongo import MongoClient
from slice_backend.btags.btag import BTag
from slice_backend.logger import Log, Logger
from slice_backend.model import Model
from slice_backend.search_query import SearchQuery
from slice_backend.tags.tag import Tag


class Index:
    def __init__(
        self,
        logger: Logger,
        sample_dir: str,
        model: Model,
        tags: Collection[Tag],
        btags: Collection[BTag],
    ) -> None:
        self.logger = logger
        self.sample_dir = sample_dir
        self.model = model
        self.tags = tags
        self.btags = btags

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
                        "path": "index.embedding",
                        # This could become a problem.
                        "numCandidates": 1000 + start + count,
                        "index": "vector_index",
                        "limit": start + count,
                        "exact": False,
                        "filter": {
                            "$and": [
                                {"index.tags": {"$eq": "SLICE:SAMPLE"}},
                                *[{"index.tags": {"$eq": tag}} for tag in query.tags],
                                *[
                                    {f"index.btags.{k}": {"$gt": BTag.get_bounds(v)[0]}}
                                    for k, v in query.btags.items()
                                ],
                                *[
                                    {f"index.btags.{k}": {"$lt": BTag.get_bounds(v)[1]}}
                                    for k, v in query.btags.items()
                                ],
                            ]
                        },
                    }
                },
                {
                    "$project": {
                        "_id": 1,
                        "path": 1,
                        "display": 1,
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
                        "path": "index.embedding",
                        # This could become a problem.
                        "numCandidates": 1000 + start + count,
                        "index": "vector_index",
                        "limit": start + count,
                        "exact": False,
                    }
                },
                {
                    "$project": {
                        "_id": 1,
                        "path": 1,
                        "display": 1,
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
