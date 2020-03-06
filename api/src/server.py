from flask import Flask, escape, request, jsonify
from flask_cors import CORS
from bs4 import BeautifulSoup
import requests
import re
import favicon
import pysubs2
import youtube_dl
import uuid
import tempfile
import json
import os

from .summarizers import tf_idf
from .summarizers import sumy


application = Flask(__name__)
CORS(application)


@application.route('/summarize')
def summarize():
    url = request.args.get('url', '')
    url = 'https://' + url.strip('http://').strip('https://')
    
    if re.match(r'^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+$', url):
        return summarize_video(url)
    else:
        return summarize_article(url)


def summarize_video(url):
    path = f'{tempfile.gettempdir()}/{uuid.uuid4()}'
    subs_path = f'{path}.en.vtt'
    info_path = f'{path}.info.json'

    # Download subs and video info
    ydl_opts = {
        'writesubtitles': True,
        'writeautomaticsub': True,
        'subtitlesformat': 'vtt',
        'subtitleslangs': ['en'],
        'skip_download': True,
        'writeinfojson': True,
        'outtmpl': path,
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    # Parse subtitles
    subs = pysubs2.load(f'{path}.en.vtt')

    # clean subtitles
    cleaned = []
    for sub in subs:
        start = sub.start
        end = sub.end
        text = sub.text.strip()
        # remove all [Music] type markers
        text = re.sub(r"\[.+\]", "", text)
        text = re.sub(r"\(.+\)", "", text)
        # remove random time codes
        text = re.sub(r"<\d{2}:\d{2}:\d{2}.\d{3}>", "", text)
        # convert the vtt encoded newlines to real newlines
        text = re.sub(r"\\N", "\n", text)
        
        # Split newlines and add each as it's own sentence
        texts = text.split('\n')
        for text in texts:
            if len(text) == 0:
                continue

            if len(cleaned) > 0 and cleaned[-1]['text'] == text:
                # autogenerated subs duplicate lines for a scrolling effect
                # we'll update the 'end' value here
                cleaned[-1]['end'] = end
            else:
                cleaned.append({
                    'start': start,
                    'end': end,
                    'text': text
                })

    # Guess if the sentences are already punctuated by count of periods
    content = ' '.join([c['text'] for c in cleaned])
    periods = content.count('.')
    
    well_formatted = False
    if periods / len(content) > 0.005:
        well_formatted = True

    if not well_formatted:
        # It's not well formed, the auto generated subtitles don't seperate by sentence so instead
        # we'll just blindly group up content by time
        normalized = []
        for clean in cleaned:
            if len(normalized) != 0 and clean['end'] - normalized[-1]['start'] < 6000:
                normalized[-1]['end'] = clean['end']
                normalized[-1]['text'] += ' ' + clean['text']
            else:
                normalized.append({
                    'start': clean['start'], 
                    'end': clean['end'], 
                    'text': clean['text']
                })
        cleaned = normalized
        content = '. '.join([s['text'] for s in cleaned])

    # Create summarizer
    # summarizer = tf_idf.TfIdfSummarizer()
    summarizer = sumy.SumySummarizer()
    summary = summarizer.summarize([content])
    
    # Find corresponding timestamped subtitles
    sum_subs = []
    for sentence in summary:
        sentence = sentence[0].strip()
        start_index = content.index(sentence)
        end_index = start_index + len(sentence)
        si = 0

        ss = []
        for c in cleaned:
            # add one or two extra to account for the space inserted between cleaned lines when
            # joined for the summarizer
            if well_formatted:
                si += len(c['text']) + 1
            else:
                si += len(c['text']) + 2
            
            if si > start_index:
                ss.append(c)
            if si > end_index:
                break
        sum_subs.append({
            'start': ss[0]['start'],
            'end': ss[-1]['end'],
            'text': ' '.join([s['text'] for s in ss]),
        })

    # Get video info
    with open(info_path, 'r') as f:
        video = json.load(f)
    title = video['title']

    # Delete youtube-dl files
    os.remove(info_path)
    os.remove(subs_path)

    # Get favicon
    icons = favicon.get(url)

    return jsonify(
        type='video',
        summary=sum_subs,
        url=url,
        title=title,
        icon=icons[0].url,
        goodSubtitles=well_formatted,
    )

def summarize_article(url):
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
        type='article',
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
