from pymongo import MongoClient
from slice_backend.logger import Log, Logger
from slice_backend.model import Model
from slice_backend.search_query import SearchQuery


class Index:
    def __init__(self, logger: Logger, sample_dir: str, model: Model) -> None:
        self.logger = logger
        self.sample_dir = sample_dir
        self.model = model

    # TODO: create this thing
    def searchSamples(
        self, db: MongoClient, query: SearchQuery, start: int = 0, count: int = 25
    ):
        self.logger.log(Log.DEBUG, "searching database", "index")
        samples = db["slice"]["audiosamples"]

        text_embed = self.model.embed_text(query.query)

        res = samples.samples.aggregate(
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
        ).to_list(count)

        return res
