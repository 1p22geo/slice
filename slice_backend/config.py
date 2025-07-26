from __future__ import annotations
import os
from typing import TypeVar
from dotenv import load_dotenv

from slice_backend.logger import Log, get_verbosity


def ensure_env(name: str) -> str:
    """
    Returns the environment variable and throws if it's not found or empty.
    """
    var = os.getenv(name)
    if not var:
        raise InsufficientDataException(name)

    return var


# ts is so cool
T = TypeVar("T")

# ts could mean both this shi or typescript, where I learned generic types
# you will never know


def default_env(name: str, default: T) -> str | T:
    """
    Returns the environment variable and returns default if it's not found or empty.

    Basically os.getenv()
    """
    var = os.getenv(name)
    if not var:
        return default

    return var


class InsufficientDataException(Exception):
    def __init__(self, missing_field: str) -> None:
        super().__init__(missing_field)
        self.missing_field = missing_field

    def __str__(self) -> str:
        return f"The environment variable {self.missing_field} was not provided."


class Config:
    def __init__(
        self,
        DB_URI: str,
        SAMPLE_DIR: str,
        BTAGS_DIR: str,
        VERBOSITY: str,
        LOG_FILE: str | None,
        ORIGIN_URL: str,
    ) -> None:
        self.__DB_URI = DB_URI
        self.__SAMPLE_DIR = SAMPLE_DIR
        self.__BTAGS_DIR = BTAGS_DIR
        self.__VERBOSITY = get_verbosity(VERBOSITY)
        self.__LOG_FILE = LOG_FILE
        self.__ORIGIN_URL = ORIGIN_URL

    def get_DB_URI(self) -> str:
        return self.__DB_URI

    def get_SAMPLE_DIR(self) -> str:
        return self.__SAMPLE_DIR

    def get_BTAGS_DIR(self) -> str:
        return self.__BTAGS_DIR

    def get_LOG_FILE(self) -> str | None:
        return self.__LOG_FILE

    def get_VERBOSITY(self) -> Log:
        return self.__VERBOSITY

    def get_ORIGIN_URL(self) -> str:
        return self.__ORIGIN_URL

    @staticmethod
    def from_dotenv() -> Config:
        load_dotenv()

        c = Config(
            ensure_env("MONGODB_URI"),
            ensure_env("SAMPLES_DIR").rstrip("/"),
            ensure_env("BTAGS_DIR").rstrip("/"),
            default_env("VERBOSITY", "INFO"),
            default_env("LOG_FILE", None),
            default_env("ORIGIN_URL", "http://127.0.0.1:5000"),
        )

        return c
