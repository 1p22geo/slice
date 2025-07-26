from slice_backend.db_connection import create_connection
from slice_backend.logger import Log, Logger
from flask import Flask, jsonify, request
from flask_cors import cross_origin
from slice_backend.index import Index
from slice_backend.search_query import SearchQuery


def route_sample_search(app: Flask, logger: Logger, index: Index, db_uri: str):
    @app.route("/api/samples/search", methods=["POST"])
    @cross_origin()
    def _route_post_samples_search():
        data = request.get_json(force=True)

        if not data["query"]:
            response = jsonify({"error": "Please search for something."})
            response.status_code = 400
            return response

        query = SearchQuery()
        query.addQuery(data["query"])
        logger.log(
            Log.LOG, f'Request recieved, search "{query.query}"', "/api/samples/search"
        )
        for tag in data["tags"]:
            logger.log(Log.TRACE, f"Adding tag {tag['id']}", "/api/samples/search")
            query.addTag(tag["id"])
        for btag in data["btags"]:
            query.addBTag(btag["id"], btag["value"])

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
