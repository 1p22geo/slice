from bson import ObjectId
from slice_backend.db_connection import create_connection
from slice_backend.logger import Log, Logger
from flask_cors import cross_origin
from flask import Flask, jsonify, request
from slice_backend.index import Index


def route_sample_similar(
    app: Flask, logger: Logger, index: Index, db_uri: str, sample_dir: str
):
    @app.route("/api/samples/similar", methods=["POST"])
    @cross_origin()
    def _route_post_samples_similar():
        data = request.get_json(force=True)

        logger.log(Log.DEBUG, "Creating connection for request", "/api/samples/similar")
        db = create_connection(db_uri)
        logger.log(Log.DEBUG, "DB connected", "/api/samples/similar")
        samples = db["slice"]["audiosamples"]

        globalpath = ""

        if "id" in data and data["id"]:
            logger.log(
                Log.LOG,
                f"Request recieved, correlate id {data['id']}",
                "/api/samples/similar",
            )
            sample = samples.find_one({"_id": ObjectId(data["id"])})
            if not sample:
                raise FileNotFoundError(data["id"])
            globalpath = sample["path"]

        elif "path" in data and data["path"]:
            logger.log(
                Log.LOG,
                f"Request recieved, correlate path {data['path']}",
                "/api/samples/similar",
            )
            globalpath = sample_dir + data["path"]

        else:
            raise ValueError("no sample file")

        start = int(data["start"]) if "start" in data else 0
        count = int(data["count"]) if "count" in data else 10

        res = index.findSimilar(db, globalpath, start, count)

        logger.log(Log.LOG, "Results retrieved", "/api/samples/similar")
        db.close()
        logger.log(Log.DEBUG, "Connection closed", "/api/samples/similar")
        return jsonify(
            {
                "resultCount": len(res),
                "results": res,
            }
        )
