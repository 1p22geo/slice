from typing import Collection
import laion_clap

from slice_backend.logger import Log, Logger


class Model:
    def __init__(self, logger: Logger, model_id: int = 1) -> None:
        self.model_id = model_id
        self.logger = logger

        logger.log(Log.DEBUG, "Loading model started. This can take a while.", "model")

        self.model = laion_clap.CLAP_Module(enable_fusion=False)
        self.model.load_ckpt(model_id=model_id)

        logger.log(Log.INFO, "Loading model finished.", "model")

    def embed_audio(self, src: str | Collection[str]):
        return self.model.get_audio_embedding_from_filelist(
            x=([src]) if isinstance(src, str) else src,
            use_tensor=False,
        )[0].tolist()

    def embed_text(self, src: str | Collection[str]):
        return self.model.get_text_embedding(
            x=([src]) if isinstance(src, str) else src,
            use_tensor=False,
        )[0].tolist()
