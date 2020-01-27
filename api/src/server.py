from flask import Flask, escape, request, jsonify
from flask_cors import CORS
from bs4 import BeautifulSoup
import requests
import re
import favicon

from .summarizers import tf_idf
from .summarizers import sumy


application = Flask(__name__)
CORS(application)


@application.route('/summarize')
def summarize():
    url = request.args.get('url', '')
    url = 'https://' + url.strip('http://').strip('https://')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
    }
    # Download page
    res = requests.get(url, timeout=5, stream=True, headers=headers)

    if res.status_code != 200:
        raise Exception(f'bad response from website {res.status_code}')
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
    main_text = main_text[0].parent

    # Organize content in paragraphs, where headers are in caps at beginning
    last_header = False
    paragraphs = []
    for paragraph in main_text.find_all(['p', 'h1', 'h2', 'h3']):

        p = paragraph.get_text().strip()
        # collapse all multiple whitespaces to a single space
        p = re.sub(r'\s\s+', r' ', p, flags=re.M)

        # ensure the line ends with a punctuation
        m = re.search(r'\w$', p)
        if m is not None:
            p += '.'
        
        if paragraph.name == 'p':
            if last_header:
                paragraphs[-1] += '\n' + p
            else:
                paragraphs.append(p)
            last_header = False
        else:
            paragraphs.append(p.upper())
            last_header = True

    # Create summarizer
    # summarizer = tf_idf.TfIdfSummarizer()
    summarizer = sumy.SumySummarizer()
    summary = summarizer.summarize(paragraphs)

    # Get favicon
    icons = favicon.get(url)

    return jsonify(
        summary=summary,
        url=url,
        title=title,
        image=image,
        icon=icons[0].url
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
