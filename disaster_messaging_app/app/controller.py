from flask import Blueprint, request, jsonify
from disaster_messaging_classification_model.models.predict import make_prediction
from disaster_messaging_classification_model import __version__ as _version
import os
from werkzeug.utils import secure_filename

from app.config import get_logger, UPLOAD_FOLDER
from app.validation import validate_inputs
from app import __version__ as app_version
import json
import plotly

_logger = get_logger(logger_name=__name__)


classification_app = Blueprint("classification_app", __name__)


@classification_app.route("/", methods=["GET"])
def default_page():
    if request.method == "GET":
        _logger.info("health status OK")
        return "Your Beijing House Price Predictions Model app is Starting"


@classification_app.route("/health", methods=["GET"])
def health():
    if request.method == "GET":
        _logger.info("health status OK")
        return "ok"


@classification_app.route("/version", methods=["GET"])
def version():
    if request.method == "GET":
        return jsonify({"model_version": _version, "app_version": app_version})


@classification_app.route("/go")
def go():
    # save user input in query
    query = request.args.get("query", "")

    # use model to predict classification for query
    response = make_prediction(input_data=query)
    _logger.debug(f"Outputs: {response}")

    # This will render the go.html Please see that file.
    return render_template(
        "go.html", query=query, classification_result=response["predictions"]
    )
