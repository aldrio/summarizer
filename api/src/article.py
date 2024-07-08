from functools import lru_cache
import re

from .summarizers.summarizer import Summarizer
from .scraping.page import fetch_page, get_page_title


@lru_cache(maxsize=128)
def summarize_article(url, summarizer: Summarizer):
    page = fetch_page(url)

    image = None
    og_image = page.find(name="meta", property="og:image")
    if og_image is not None:
        image = og_image.get("content")

    # Parse body of page

    # Group paragraphs by parent, use the largest one as the main text
    paragraphs = page.find_all(["p"])
    containers = {}
    for paragraph in paragraphs:
        parent = paragraph.parent
        if parent in containers:
            containers[parent].append(paragraph)
        else:
            containers[parent] = [paragraph]

    main_text = None
    for paragraphs in containers.values():
        if main_text is None or len(main_text) < len(paragraphs):
            main_text = paragraphs
    main_text = main_text[0].parent

    # Organize content in paragraphs, where headers are in caps at beginning
    last_header = False
    paragraphs = []
    for paragraph in main_text.find_all(["p", "h1", "h2", "h3"]):

        p = paragraph.get_text().strip()
        # collapse all multiple whitespaces to a single space
        p = re.sub(r"\s\s+", r" ", p, flags=re.M)

        # ensure the line ends with a punctuation
        m = re.search(r"\w$", p)
        if m is not None:
            p += "."

        if paragraph.name == "p":
            if last_header:
                paragraphs[-1] += "\n" + p
            else:
                paragraphs.append(p)
            last_header = False
        else:
            paragraphs.append(p.upper())
            last_header = True

    # Summarize
    summary = summarizer.summarize(paragraphs)

    return {
        "title": get_page_title(page),
        "summary": summary,
        "image": image,
        "reductionRatio": len(" ".join(" ".join(s) for s in paragraphs))
        / len(" ".join(" ".join(s) for s in summary)),
    }
