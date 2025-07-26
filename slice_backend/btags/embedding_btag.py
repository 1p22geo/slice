import numpy as np
from typing import List
from slice_backend.btags.btag import BTag
from slice_backend.model import Model
from slice_backend.walker import dirwalk


class EmbeddingBTag(BTag):
    def __init__(
        self,
        id: str,
        name: str,
        name_A: str,
        name_B: str,
        dir_A: str,
        dir_B: str,
        model: Model,
    ):
        super().__init__(id, name, name_A, name_B)
        self.__dir_A = dir_A
        self.__dir_B = dir_B
        self.__model = model

        self.__embedding_A = self.__get_average_embedding(self.__dir_A)
        self.__embedding_B = self.__get_average_embedding(self.__dir_B)

        self.__total = np.zeros(512)
        self.__count = 0

    def __get_average_embedding(self, dir: str):
        self.__total = np.zeros((512))
        self.__count = 0

        def add_embedding(path: str, _):
            self.__total += np.array(self.__model.embed_audio(path))
            self.__count += 1

        dirwalk(dir, add_embedding, True)
        return self.__total / self.__count

    def get_value(
        self, abs_path: str | None = None, embedding: List[float] | None = None
    ):
        # I am very proud of this algorythm.
        # I spent 30 minutes in Desmos cooking it up.
        # Please don't laugh when it inevitably breaks.

        P1 = self.__embedding_A
        P2 = self.__embedding_B

        X = np.array(self.__model.embed_audio(abs_path) if abs_path else embedding)

        delta = P2 - P1  # vector distance
        deltadiff = np.sqrt(delta.dot(delta))  # scalar distance between P1 and P2

        x_to_p1 = P1 - X
        x_to_p2 = P2 - X

        factor = np.sqrt(x_to_p1.dot(x_to_p1)) - np.sqrt(x_to_p2.dot(x_to_p2))
        factor /= deltadiff * 2
        factor += 0.5

        return factor
