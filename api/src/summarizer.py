import math
import re
import nltk

stop_words = set(nltk.corpus.stopwords.words('english'))
ps = nltk.stem.PorterStemmer()


def _tokenize_document(doc):
    words = nltk.tokenize.word_tokenize(doc)
    twords = []

    for word in words:
        word = word.lower()
        if word in stop_words:
            continue
        if bool(re.search(r'\W', word)):
            continue
        word = ps.stem(word)
        twords.append(word)
    return twords


def _create_tf_matrix(doc):
    tf_matrix = {}

    for word in doc:
        if word in tf_matrix:
            tf_matrix[word] += 1
        else:
            tf_matrix[word] = 1

    for word, count in tf_matrix.items():
        tf_matrix[word] = count / len(tf_matrix)

    return tf_matrix


def _create_idf_matrix(tf_matrices):
    idf_matrix = {}

    # Collect set of all words
    vocabs = [tuple(tfm.keys()) for tfm in tf_matrices]
    vocab = set([word for vocab in vocabs for word in vocab])

    for word in vocab:
        docs_with_word = 0
        for tf_matrix in tf_matrices:
            if word in tf_matrix:
                docs_with_word += 1
        idf_matrix[word] = math.log2(len(tf_matrices) / docs_with_word)

    return idf_matrix


def _word_tf_idf(word, tf_matrix, idf_matrix):
    if word not in tf_matrix:
        return 0.0
    return tf_matrix[word] * idf_matrix[word]


def _score_doc(doc, tf_matrix, idf_matrix):
    score = 0

    if len(doc) < 3:
        return score

    for word in doc:
        score += _word_tf_idf(word, tf_matrix, idf_matrix)

    return score


def summarize(text):
    sentences = nltk.tokenize.sent_tokenize(text)
    docs = [_tokenize_document(sentence) for sentence in sentences]

    tf_matrices = [_create_tf_matrix(doc) for doc in docs]
    idf_matrix = _create_idf_matrix(tf_matrices)

    scores = [
        _score_doc(
            doc,
            tf_matrix,
            idf_matrix
        ) for (
            doc,
            tf_matrix
        ) in zip(
            docs,
            tf_matrices
        )]

    sorted_scores = sorted(scores, reverse=True)
    threshold = sorted_scores[max(2, min(6, math.floor(len(scores) / 4)))]

    summary = ''
    for (i, sentence) in enumerate(sentences):
        if scores[i] >= threshold:
            summary += sentence + ' '

    return summary
