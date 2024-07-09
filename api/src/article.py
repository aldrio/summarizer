from functools import lru_cache
import re
import nltk

from .errors import PublicError
from .summarizers.summarizer import Summarizer
from .scraping.page import fetch_page, get_page_title


@lru_cache(maxsize=128)
def summarize_article(url, summarizer: Summarizer):
    try:
        page = fetch_page(url)
    except Exception as e:
        raise PublicError("Failed to download the article", e)

    image = None
    og_image = page.find(name="meta", property="og:image")
    if og_image is not None:
        image = og_image.get("content")

    # Parse body of page
    page = page.find("body")

    # remove scripts and styles
    for script in page(["script", "style"]):
        script.decompose()

    # Find content
    content = page.find_all(["h1", "h2", "h3", "h4", "h5", "h6", "h7", "p"])

    paragraphs = []
    for content in content:
        text = content.get_text()
        # collapse white space
        text = re.sub(r"\s+", " ", text)
        text = text.strip()

        if not text:
            continue
        # Split into sentences
        sentences = nltk.tokenize.sent_tokenize(text)
        paragraphs.append(sentences)

    # Summarize
    summarized_paragraphs = summarizer.summarize_article(paragraphs)

    # Calculate reduction ratio
    full_content = [sentence for paragraph in paragraphs for sentence in paragraph]
    full_content_len = sum(len(sentence) for sentence in full_content)

    summarized_content = [
        sentence for paragraph in summarized_paragraphs for sentence in paragraph
    ]
    summarized_content_len = sum(len(sentence) for sentence in summarized_content)

    return {
        "title": get_page_title(page),
        "summary": summarized_paragraphs,
        "image": image,
        "reductionRatio": full_content_len / summarized_content_len,
    }
