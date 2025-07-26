from slice_backend.logger import Logger
from flask_cors import cross_origin
from flask import Flask, jsonify
from slice_backend.index import Index


def route_tags(app: Flask, logger: Logger, index: Index):
    @app.route("/api/tags/tags", methods=["GET"])
    @cross_origin()
    def _route_get_tags():
        tags = index.tags

        return jsonify(
            {
                "resultCount": len(tags),
                "results": [{"id": tag.id, "name": tag.name} for tag in tags],
            }
        )
