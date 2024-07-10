import math
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.nlp.stemmers import Stemmer
from sumy.models.dom import ObjectDocumentModel, Sentence, Paragraph

from .summarizer import Summarizer

LANGUAGE = "english"


class SumySummarizer(Summarizer):

    def __init__(self, target_ratio=0.1):
        self.target_ratio = target_ratio

    def summarize(self, paragraphs):
        """Summarize content with the sumy library"""

        tokenizer = Tokenizer(LANGUAGE)
        paragraphs = [
            Paragraph([Sentence(s, tokenizer) for s in p]) for p in paragraphs
        ]
        document = ObjectDocumentModel(paragraphs)

        stemmer = Stemmer(LANGUAGE)
        summarizer = LsaSummarizer(stemmer)

        summarized_paragraphs = [[] for _ in paragraphs]
        for sentence in summarizer(document, f"{math.ceil(self.target_ratio * 100)}%"):
            paragraph_index = next(
                i for i, p in enumerate(paragraphs) if sentence in p.sentences
            )
            summarized_paragraphs[paragraph_index].append(str(sentence))

        # remove empty paragraphs
        summarized_paragraphs = [p for p in summarized_paragraphs if p]

        return summarized_paragraphs

    def algorithm_name(self):
        return "LSA"
