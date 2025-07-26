from slice_backend.logger import Log, Logger


def initTags(logger: Logger):
    logger.log(Log.LOG, "Loading tags", "tags")
    from .drums import tags as drums
    from .fx import tags as fx
    from .instrum import tags as instrum
    from .loops import tags as loops

    logger.log(Log.TRACE, "Loaded tags", "tags")

    tags = [*drums, *fx, *instrum, *loops]
    return tags
