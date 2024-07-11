import os

from dotenv import load_dotenv

load_dotenv(".env.local")
os.environ["NLTK_DATA"] = "./nltk_data"

from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import re

from .errors import PublicError
from .summarizers.all import SUMMARIZERS
from .article import summarize_article
from .video import summarize_video
from .scraping.page import get_icon


application = Flask(__name__)
CORS(application)


@cross_origin()
@application.errorhandler(PublicError)
def public_error(error):
    return jsonify({"error": error.message}), 500


@cross_origin()
@application.errorhandler(500)
def generic_error(_e):
    return jsonify({"error": "Internal server error"}), 500


@application.route("/healthz")
def healthz():
    return "OK"


@application.route("/summarize")
def summarize():
    url = request.args.get("url", "")
    url = "https://" + url.removeprefix("http://").removeprefix("https://")
    algorithm_key = request.args.get("algorithm", "lsa").lower()

    if algorithm_key not in SUMMARIZERS:
        raise PublicError("Invalid summarization algorithm")
    summarizer = SUMMARIZERS[algorithm_key]

    if re.match(r"^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+$", url):
        data = summarize_video(url, summarizer)
        data["type"] = "video"
    else:
        data = summarize_article(url, summarizer)
        data["type"] = "article"

    if "icon" not in data:
        data.setdefault("icon", get_icon(url))

    data.setdefault("algorithm", summarizer.algorithm_name())
    data.setdefault("url", url)
    data.setdefault("title", url)

    return jsonify(data)
