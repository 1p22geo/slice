from enum import IntEnum
from datetime import datetime
import sys
from threading import Lock

from pymongo import MongoClient


class InvalidLog(ValueError):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.name = name

    def __str__(self) -> str:
        return f"{self.name} is not a valid log verbosity. Try values 1 (TRACE) through 7 (CRITICAL) or read the docs (if I made any)"


class Log(IntEnum):
    CRITICAL = 7
    ERROR = 6
    WARN = 5
    INFO = 4
    LOG = 3
    DEBUG = 2
    TRACE = 1


def get_verbosity(name: str | int) -> Log:
    if isinstance(name, str):
        # TODO: what in the name of the bodge
        if name in dir(Log) and not name.startswith("__"):
            return Log[name]
        else:
            raise InvalidLog(name)
    if isinstance(name, int):
        try:
            return Log(name)
        except ValueError:
            raise InvalidLog(str(name))


class Logger:
    """
    Safe for multithread use.

    Kinda.
    """

    def __init__(
        self, verbosity: Log, file: str | None, db_connection: MongoClient | None = None
    ) -> None:
        self.verbosity = verbosity
        self.path = file
        self.__mutex = Lock()

        if file:
            self.file = open(file, "a")
        else:
            self.file = None

        if db_connection:
            db_connection["slice"]["logs"].delete_many({})

        self.db_connection = db_connection
        self.log(Log.TRACE, "Log opened", "logger")

    def __del__(self):
        print("Please don't start spamming ctrl-c and wait for the database to close")
        self.log(Log.TRACE, "Log closed", "logger")
        if self.file:
            self.file.close()
        if self.db_connection:
            self.db_connection.close()

    def log(self, verbosity: Log, message: str, component: str | None = None) -> None:
        message = message.strip()
        _component = f"[{component}] " if component else ""
        if verbosity >= self.verbosity:
            if "\n" in message:
                text = f"[{datetime.now().isoformat()}] {_component}[{verbosity.name}]\n\n {message}\n\n\n"
            else:
                text = f"[{datetime.now().isoformat()}] {_component}[{verbosity.name}] {message}"

            with self.__mutex:
                if self.file:
                    self.file.write(text + "\n")

                if self.db_connection:
                    self.db_connection["slice"]["logs"].insert_one(
                        {
                            "date": datetime.now(),
                            "verbosity": int(verbosity),
                            "verbosity_str": verbosity.name,
                            "content": message,
                            "component": component,
                        }
                    )

                if verbosity >= Log.WARN:
                    print(text, file=sys.stderr)
                else:
                    print(text, file=sys.stdout)
