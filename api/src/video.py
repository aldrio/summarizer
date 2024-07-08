from functools import lru_cache
from difflib import SequenceMatcher
import re

from .errors import PublicError
from .summarizers.summarizer import Summarizer
from .scraping.video import scrape_video
from .scraping.simplesrt import SimpleSrt, dedupe_yt_srt


@lru_cache(maxsize=128)
def summarize_video(url, summarizer: Summarizer):
    try:
        title, raw_subs = scrape_video(url)
    except Exception as e:
        raise PublicError("Failed to download the video", e)

    srt = SimpleSrt(raw_subs)
    subs = list(dedupe_yt_srt(srt.subs))

    # clean subtitles
    for sub in subs:
        # remove all [Music] type markers
        sub.text = re.sub(r"\[.+\]", "", sub.text)
        sub.text = re.sub(r"\(.+\)", "", sub.text)

    subs = [sub for sub in subs if sub.text != ""]

    # Determine if the subtitles are well formatted
    well_formatted = is_well_formatted(subs)

    # Join all subtitles into one big string to summarize
    if well_formatted or summarizer.supports_malformed():
        content = " ".join([s.text for s in subs])
    else:
        # non well formatted subtitles need punctuation to separate sentences
        # we have to guess where to put the punctuation
        # just a random idea, let's combine them in groups of 3
        # and add a period at the end of each group
        content = ""
        for i in range(0, len(subs), 3):
            group = " ".join(s.text for s in subs[i : i + 3])
            content += group + ". "

    # Summarize
    summary = summarizer.summarize([content])

    # Find corresponding timestamped subtitles
    content = content.lower()
    sum_subs = []
    for sentence in summary:
        sentence = sentence[0].strip().lower()

        start_index = None
        start_index_similarity = -1000000
        for i in range(len(content)):
            similarity = SequenceMatcher(
                None, sentence, content[i : i + len(sentence)]
            ).quick_ratio()
            if similarity > start_index_similarity:
                start_index_similarity = similarity
                start_index = i

        if start_index is None:
            continue

        end_index = start_index + len(sentence)
        si = 0

        ss = []
        for s in subs:
            # add one or two extra to account for the space inserted between cleaned lines when
            # joined for the summarizer
            if well_formatted:
                si += len(s.text) + 1
            else:
                si += len(s.text) + 2

            if si > start_index:
                ss.append(s)
            if si > end_index:
                break

        sum_subs.append(
            {
                "start": ss[0].start.total_seconds(),
                "end": ss[-1].end.total_seconds(),
                "text": " ".join([s.text for s in ss]),
            }
        )

    return {
        "title": title,
        "summary": sum_subs,
        "goodSubtitles": well_formatted,
        "reductionRatio": len(content) / len(" ".join([s["text"] for s in sum_subs])),
    }


def is_well_formatted(subs):
    content = " ".join([s.text for s in subs])
    periods = content.count(".")
    return periods / len(content) > 0.005
