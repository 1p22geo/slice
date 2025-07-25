from flask import Flask
import os
from slice_backend.config import Config
from slice_backend.db_connection import create_connection
from slice_backend.indexer import Indexer
from slice_backend.logger import Log, Logger
from slice_backend.model import Model
from slice_backend.routes.sample_search import route_sample_search
from slice_backend.routes.sample_similar import route_sample_similar


def create_app(test_config=None):
    app = Flask(os.getenv("FLASK_NAME", ""))
    config = Config.from_dotenv()
    print("Connecting DB for logs")
    db = create_connection(config.get_DB_URI())
    logger = Logger(config.get_VERBOSITY(), config.get_LOG_FILE(), db)
    model = Model(logger, 1)
    index = Indexer.create_index(db, logger, config.get_SAMPLE_DIR(), model)

    route_sample_search(app, logger, index, config.get_DB_URI())
    route_sample_similar(
        app, logger, index, config.get_DB_URI(), config.get_SAMPLE_DIR()
    )

    @app.route("/test")
    def hello():
        logger.log(Log.INFO, "Request recieved")
        return "Hello, World!"

    return app
