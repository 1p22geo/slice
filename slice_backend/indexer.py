import datetime
from typing import Collection
from pymongo.errors import OperationFailure
from pymongo.mongo_client import MongoClient
from pymongo.operations import SearchIndexModel
from slice_backend.btags import assignBTags
from slice_backend.btags.btag import BTag
from slice_backend.index import Index
from slice_backend.logger import Log, Logger
from slice_backend.model import Model
from slice_backend.tags import assignTags
from slice_backend.tags.tag import Tag
from slice_backend.walker import countfiles, dirwalk
import time
import os


class Indexer:
    @staticmethod
    def create_index(
        db: MongoClient,
        logger: Logger,
        sample_dir: str,
        model: Model,
        tags: Collection[Tag],
        btags: Collection[BTag],
    ) -> Index:
        """
        Can only be called in the master thread, does not work multithreaded
        """

        logger.log(Log.TRACE, "Checking for sample index database", "indexer")

        def rethink_your_life_choices():
            # both the indexer should, and you, if you're redading this
            Indexer.new_index(db, logger, sample_dir, model, tags, btags)

        if not os.path.exists(sample_dir):
            logger.log(
                Log.CRITICAL, f"Sample path {sample_dir} DOES NOT EXIST", "indexer"
            )
            raise FileNotFoundError(sample_dir)

        if "audiosamples" not in db["slice"].list_collection_names():
            logger.log(Log.WARN, "Sample collection not found", "indexer")
            rethink_your_life_choices()
        else:
            estimate_count = db["slice"]["audiosamples"].estimated_document_count()

            if estimate_count > 0:
                logger.log(
                    Log.LOG,
                    f"Collection exists, {estimate_count} samples found",
                    "indexer",
                )
            else:
                logger.log(Log.WARN, "Sample collection exits but is empty", "indexer")
                rethink_your_life_choices()

        index_list = list(
            db["slice"]["audiosamples"].list_search_indexes("vector_index")
        )
        if not (len(index_list) and index_list[0].get("queryable") is True):
            logger.log(Log.WARN, "Vector search index does not exist", "indexer")
            rethink_your_life_choices()

        return Index(logger, sample_dir, model, tags, btags)

    @staticmethod
    def new_index(
        db: MongoClient,
        logger: Logger,
        sample_dir: str,
        model: Model,
        tags: Collection[Tag],
        btags: Collection[BTag],
    ) -> None:
        logger.log(
            Log.INFO,
            f"""
Creating new index.

Indexing ALL FILES in {sample_dir} now.
This will take A LONG TIME.
        """,
            "indexer",
        )

        logger.log(Log.LOG, "Dropping indexes", "indexer")
        db["slice"]["audiosamples"].drop_indexes()
        logger.log(Log.LOG, "Dropping search indexes", "indexer")
        try:
            db["slice"]["audiosamples"].drop_search_index("vector_index")
        except OperationFailure:
            logger.log(Log.LOG, "No indexes found", "indexer")
        logger.log(Log.LOG, "Dropping collection (if any exists)", "indexer")
        db["slice"]["audiosamples"].drop()

        logger.log(Log.LOG, "Inserting data", "indexer")

        start = datetime.datetime.now()
        total = countfiles(sample_dir, True)
        count = 0

        def process_sample(absolute_path: str, name: str):
            nonlocal count, total, start  # since when is that a thing wtf

            logger.log(Log.TRACE, f"Processing {absolute_path}", "indexer")

            embedding = model.embed_audio(absolute_path)

            active_tags = assignTags(absolute_path, sample_dir, tags)
            active_btags = assignBTags(btags, embedding=embedding)

            while True:
                try:
                    db["slice"]["audiosamples"].insert_one(
                        {
                            "path": absolute_path,
                            "display": {
                                "name": name,
                                "tags": [
                                    {"id": tag.id, "name": tag.name}
                                    for tag in active_tags
                                ],
                                "btags": [
                                    {
                                        "id": tag.id,
                                        "name": tag.name,
                                        "name_A": tag.name_A,
                                        "name_B": tag.name_B,
                                        "value": value,
                                    }
                                    for tag, value in active_btags.items()
                                ],
                            },
                            "index": {
                                "embedding": embedding,
                                "tags": [t.id for t in active_tags],
                                "btags": {k.id: v for k, v in active_btags.items()},
                            },
                        }
                    )
                    break
                except:
                    continue

            logger.log(Log.LOG, f"Saved {absolute_path}", "indexer")
            count += 1

            if count % 100 == 0:
                dt = (datetime.datetime.now() - start) / count
                done = start + dt * total
                done = done.isoformat()

                percentage = round((count / total) * 100)
                logger.log(Log.TRACE, f"{percentage}% done, {count}/{total}", "indexer")
                logger.log(Log.TRACE, f"Should be done by {done}", "indexer")

        dirwalk(sample_dir, process_sample)

        logger.log(Log.LOG, "Configuring vector search index", "indexer")

        search_index_model = SearchIndexModel(
            definition={
                "fields": [
                    {
                        "type": "vector",
                        "numDimensions": 512,
                        "path": "index.embedding",
                        "similarity": "dotProduct",
                    },
                    {"type": "filter", "path": "index.tags"},
                    *[
                        {"type": "filter", "path": f"index.btags.{bt.id}"}
                        for bt in btags
                    ],
                ]
            },
            name="vector_index",
            type="vectorSearch",
        )

        result = db["slice"]["audiosamples"].create_search_index(
            model=search_index_model
        )

        logger.log(Log.INFO, f'New index building: "{result}"', "indexer")

        logger.log(Log.LOG, "Polling new index", "indexer")

        while True:
            index_list = list(db["slice"]["audiosamples"].list_search_indexes(result))
            if len(index_list) and index_list[0].get("queryable") is True:
                break
            logger.log(Log.TRACE, "Still not ready", "indexer")
            time.sleep(5)

        logger.log(Log.INFO, f'Index ready: "{result}"', "indexer")
