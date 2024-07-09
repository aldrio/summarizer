from functools import lru_cache
from difflib import SequenceMatcher
import re
from nltk.tokenize import PunktSentenceTokenizer

from .errors import PublicError
from .summarizers.summarizer import Summarizer
from .scraping.video import scrape_video
from .scraping.simplesrt import SimpleSrt, dedupe_yt_srt


@lru_cache(maxsize=128)
def summarize_video(url, summarizer: Summarizer):
    try:
        title, url, raw_subs = scrape_video(url)
    except Exception as e:
        raise PublicError("Failed to download the video", e)

    srt = SimpleSrt(raw_subs)
    subs = list(dedupe_yt_srt(srt.subs))

    # clean subtitles
    for sub in subs:
        # remove all [Music] type markers
        sub.text = re.sub(r"\[.+\]", "", sub.text)
        sub.text = re.sub(r"\(.+\)", "", sub.text)

        # remove all non-space whitespace (run twice to collapse double spaces)
        sub.text = re.sub(r"\s+", " ", sub.text)
        sub.text = re.sub(r"\s+", " ", sub.text)

        sub.text = sub.text.strip()

    subs = [sub for sub in subs if sub.text != ""]

    # Determine if the subtitles are well formatted
    well_formatted = is_well_formatted(subs)

    # Prepare content for summarization
    indexed_sentences = []
    if well_formatted:
        indexed_sentences = split_sentences([sub.text for sub in subs])
    else:
        if summarizer.supports_malformed():
            # the summarizer supports malformed inputs, so we'll just pass the raw text
            indexed_sentences = [(sub.text, (i, i)) for i, sub in enumerate(subs)]
        else:
            # non well formatted subtitles need punctuation to separate sentences
            # we have to guess where to put the punctuation
            # just a random idea, let's combine them in groups of 3
            # and add a period at the end of each group
            for i in range(0, len(subs), 3):
                group = " ".join(s.text for s in subs[i : i + 3])
                indexed_sentences.append((group, (i, i + 3)))

    # Summarize
    summarized_sentences = summarizer.summarize_video(
        [sentence for sentence, _ in indexed_sentences]
    )

    # Find corresponding timestamped subtitles
    sum_subs = []
    for summarized_sentence in summarized_sentences:
        summarized_sentence = summarized_sentence.strip().lower()

        # search for the span that most closely matches the summarized sentence
        match = None
        match_similarity = -1000000
        for i, (sentence, _) in enumerate(indexed_sentences):
            similarity = SequenceMatcher(
                None,
                summarized_sentence,
                sentence,
            ).quick_ratio()
            if similarity > match_similarity:
                match_similarity = similarity
                match = i

        if match is None:
            continue

        indexed_sentence, (start, end) = indexed_sentences[match]
        start_sub = subs[start]
        end_sub = subs[end]

        start_time = start_sub.start.total_seconds()
        end_time = end_sub.end.total_seconds()

        # concat with previous subtitle if they overlap
        prev_sum_sub = sum_subs[-1] if len(sum_subs) > 0 else None
        if (
            prev_sum_sub
            and prev_sum_sub["end"] >= (start_time - 2)
            and prev_sum_sub["start"] < start_time
        ):
            prev_sum_sub["text"] += " " + indexed_sentence
            prev_sum_sub["end"] = end_time
        else:
            sum_subs.append(
                {
                    "start": start_time,
                    "end": end_time,
                    "text": indexed_sentence,
                }
            )

    # Calculate reduction ratio
    full_content_len = sum(len(sentence) for sentence, _ in indexed_sentences)
    summarized_content_len = sum(len(sentence) for sentence in summarized_sentences)

    return {
        "title": title,
        "url": url,
        "summary": sum_subs,
        "goodSubtitles": well_formatted,
        "reductionRatio": full_content_len / summarized_content_len,
    }


def is_well_formatted(subs):
    """
    Determines if the subtitles already seem to be punctuated correcly
    """
    content = " ".join([s.text for s in subs])
    periods = content.count(".")
    return periods / len(content) > 0.005


def split_sentences(texts) -> list[tuple[str, tuple[int, int]]]:
    """
    Tokenizes a list of subtitles into sentences and keeps track of the index range that
    they span
    """
    tokenizer = PunktSentenceTokenizer()

    sentences = []

    current_start_sub_index = None
    current_sentence = None
    for i, text in enumerate(texts):
        if current_sentence is not None:
            text = current_sentence + " " + text

        split_sentences = tokenizer.span_tokenize(text)
        for start, end in split_sentences:
            sentence = text[start:end]
            # if the span ends at the end of the subtitle, we'll need to check
            # it on the next iteration in case it's a part of a larger sentence
            if end == len(text):
                if current_start_sub_index is None:
                    current_start_sub_index = i
                current_sentence = sentence
                break

            # it is possible that the last iteration (if we carried over a current_sentence)
            # actually was not part of a larger sentence, so we need to check that
            if (
                start == 0
                and current_sentence is not None
                and end == len(current_sentence.strip())
            ):
                sentences.append((sentence, (current_start_sub_index, i - 1)))
                current_start_sub_index = None
                current_sentence = None
                continue

            start_sub_index = (
                i if current_start_sub_index is None else current_start_sub_index
            )
            end_sub_index = i
            sentences.append((sentence, (start_sub_index, end_sub_index)))

            current_start_sub_index = None
            current_sentence = None

    if current_sentence:
        sentences.append((current_sentence, (current_start_sub_index, len(texts) - 1)))

    return sentences
