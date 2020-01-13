from flask import Flask, escape, request, jsonify
from flask_cors import CORS
from bs4 import BeautifulSoup
import requests
import re
from . import summarizer


application = Flask(__name__)
CORS(application)


@application.route('/summarize')
def summarize():
    url = request.args.get('url', '')
    url = 'http://' + url.strip('http://').strip('https://')

    # Download page
    res = requests.get(url, timeout=5, stream=True)

    if res.status_code != 200:
        raise Exception('bad response from website')
    if not res.headers['content-type'].startswith('text/html'):
        raise Exception('bad content-type')

    maxsize = 5000000  # 5mb
    content = ''
    for chunk in res.iter_content(chunk_size=2048, decode_unicode=True):
        content += chunk
        if len(content) > maxsize:
            res.close()
            raise Exception('response from website too large')

    # Parse relevant parts of page
    page = BeautifulSoup(content, 'html.parser')

    image = None
    og_image = page.find(name='meta', property='og:image')
    if og_image is not None:
        image = og_image.get('content')

    title = _get_page_title(page)
    if title is None:
        title = url

    # Parse body of page

    # Group paragraphs by parent, use the largest one as the main text
    paragraphs = page.find_all(['p'])
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

    paragraphs = []
    for paragraph in main_text:

        p = paragraph.get_text().strip()
        # collapse all multiple whitespaces to a single space
        p = re.sub(r'\s\s+', r' ', p, flags=re.M)

        # ensure the line ends with a punctuation
        m = re.search(r'\w$', p)
        if m is not None:
            p += '.'

        paragraphs.append(p)

    return jsonify(
        summary=summarizer.summarize(paragraphs),
        title=title,
        image=image,
    )


def _get_page_title(page):

    og_title = page.find(name='meta', property='og:title')
    if og_title is not None:
        return og_title.get('content')

    h1_title = page.find(name='h1')
    if h1_title is not None:
        return h1_title.get_text()

    title = page.find('title')
    if title is not None:
        return title.get_text()

    return None


if __name__ == '__main__':
    application.run(host='0.0.0.0')
