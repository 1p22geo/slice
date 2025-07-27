from typing import Collection, List
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

    comp_snap = EmbeddingBTag(
        "SLICE:BTAGS:COMP_SNAP",
        "Snap",
        "Compressed",
        "Snappy",
        f"{btags_dir}/COMPRESSED/",
        f"{btags_dir}/SNAPPY/",
        model,
    )

    thin_fat = EmbeddingBTag(
        "SLICE:BTAGS:THIN_FAT",
        "Fatness",
        "Thin",
        "Fat",
        f"{btags_dir}/THIN/",
        f"{btags_dir}/FAT/",
        model,
    )

    narrow_wide = EmbeddingBTag(
        "SLICE:BTAGS:NARROW_WIDE",
        "Stereo",
        "Narrow",
        "Wide",
        f"{btags_dir}/NARROW/",
        f"{btags_dir}/WIDE/",
        model,
    )

    logger.log(Log.TRACE, "Loaded Btags", "tags")

    return [dark_bright, comp_snap, thin_fat, narrow_wide]


def assignBTags(
    btags: Collection[BTag],
    abs_path: str | None = None,
    embedding: List[float] | None = None,
):
    return {t: t.get_value(abs_path=abs_path, embedding=embedding) for t in btags}
