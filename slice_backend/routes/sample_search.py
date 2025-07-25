from slice_backend.db_connection import create_connection
from slice_backend.logger import Log, Logger
from flask import Flask, jsonify, request

from slice_backend.index import Index
from slice_backend.search_query import SearchQuery


def route_sample_search(app: Flask, logger: Logger, index: Index, db_uri: str):
    @app.post("/api/samples/search")
    def _route_post_samples_search():
        data = request.get_json(force=True)

        query = SearchQuery()
        query.addQuery(data["query"])
        for tag in data["tags"]:
            query.addTag(tag["name"], tag["selected"])
        for btag in data["btags"]:
            query.addBTag(btag["name"], btag["value"])

        logger.log(
            Log.LOG, f'Request recieved, search "{query.query}"', "/api/samples/search"
        )

        db = create_connection(db_uri)

        start = int(data["start"]) if "start" in data else 0
        count = int(data["count"]) if "count" in data else 10

        res = index.searchSamples(db, query, start, count)

        logger.log(Log.LOG, "Results retrieved", "/api/samples/search")
        db.close()
        logger.log(Log.DEBUG, "Connection closed", "/api/samples/search")

        return jsonify(
            {
                "resultCount": len(res),
                "results": res,
            }
        )
