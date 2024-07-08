from functools import lru_cache
from yt_dlp import YoutubeDL
import uuid
import tempfile
import json
import os


@lru_cache(maxsize=128)
def scrape_video(url) -> tuple[str, str]:
    """
    Fetches video subtitles and title from a given URL.
    """

    path = f"{tempfile.gettempdir()}/{uuid.uuid4()}"
    subs_path = f"{path}.en.srt"
    info_path = f"{path}.info.json"

    # Download subs and video info
    ydl_opts = {
        "skip_download": True,
        "writesubtitles": True,
        "writeautomaticsub": True,
        "writeinfojson": True,
        "postprocessors": [
            {"format": "srt", "key": "FFmpegSubtitlesConvertor", "when": "before_dl"}
        ],
        "outtmpl": path,
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    # Parse subtitles
    with open(subs_path, "r", encoding="utf8") as file:
        raw_subs = file.read()

    # Get video info
    with open(info_path, "r") as f:
        video = json.load(f)
        title = video["title"]

    # Delete youtube-dl files
    os.remove(info_path)
    os.remove(subs_path)

    return title, raw_subs
