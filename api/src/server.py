from flask import Flask, request, jsonify
from flask_cors import CORS
import re
from dotenv import load_dotenv

from .summarizers.all import SUMMARIZERS
from .article import summarize_article
from .video import summarize_video
from .scraping.page import get_icon

load_dotenv(".env.local")

application = Flask(__name__)
CORS(application)


@application.route("/summarize")
def summarize():
    url = request.args.get("url", "")
    url = "https://" + url.removeprefix("http://").removeprefix("https://")
    algorithm_key = request.args.get("algorithm", "lsa")

    if algorithm_key not in SUMMARIZERS:
        return jsonify({"error": "Algorithm not found"})
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
