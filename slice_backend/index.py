from slice_backend.logger import Log, Logger
from slice_backend.model import Model


class Index:
    def __init__(self, logger: Logger, sample_dir: str, model: Model) -> None:
        self.logger = logger
        self.sample_dir = sample_dir
        self.model = model

    # TODO: create this thing
