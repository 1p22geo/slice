from typing import Collection
from slice_backend.btags.btag import BTag
from slice_backend.btags.embedding_btag import EmbeddingBTag
from slice_backend.logger import Logger, Log
from slice_backend.model import Model


def initBTags(logger: Logger, model: Model, btags_dir: str) -> Collection[BTag]:
    logger.log(Log.LOG, "Loading Btags", "tags")

    dark_bright = EmbeddingBTag(
        "SLICE:BTAGS:DARK_BRIGHT",
        "Brightness",
        "Dark",
        "Bright",
        f"{btags_dir}/DARK/",
        f"{btags_dir}/BRIGHT/",
        model,
    )

    logger.log(Log.TRACE, "Loaded Btags", "tags")

    return [dark_bright]
