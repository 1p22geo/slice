from slice_backend.logger import Logger
from flask_cors import cross_origin
from flask import Flask, jsonify
from slice_backend.index import Index


def route_btags(app: Flask, logger: Logger, index: Index):
    @app.route("/api/tags/btags", methods=["GET"])
    @cross_origin()
    def _route_get_btags():
        btags = index.btags

        return jsonify(
            {
                "resultCount": len(btags),
                "results": [
                    {
                        "id": tag.id,
                        "name": tag.name,
                        "name_A": tag.name_A,
                        "name_B": tag.name_B,
                    }
                    for tag in btags
                ],
            }
        )
