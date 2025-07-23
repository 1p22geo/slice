from pymongo.mongo_client import MongoClient


from slice_backend.logger import Log, Logger
from slice_backend.model import Model
from slice_backend.walker import dirwalk


class Indexer:
    @staticmethod
    def check_index(
        db: MongoClient, logger: Logger, sample_dir: str, model: Model
    ) -> None:
        logger.log(Log.TRACE, "Checking for sample index database", "indexer")

        if "audiosamples" not in db["slice"].list_collection_names():
            logger.log(Log.WARN, "Sample collection not found", "indexer")
            Indexer.create_index(db, logger, sample_dir, model)
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
                Indexer.create_index(db, logger, sample_dir, model)

    @staticmethod
    def create_index(
        db: MongoClient, logger: Logger, sample_dir: str, model: Model
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

        def process_sample(absolute_path: str, name: str):
            logger.log(Log.TRACE, f"Processing {absolute_path}", "indexer")

            embedding = model.embed_audio(absolute_path)
            db["slice"]["audiosamples"].insert_one(
                {"path": absolute_path, "name": name, "embedding": embedding}
            )

            logger.log(Log.LOG, f"Saved {absolute_path}", "indexer")

        dirwalk(sample_dir, process_sample)
