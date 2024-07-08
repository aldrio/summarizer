from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.nlp.stemmers import Stemmer

from .summarizer import Summarizer

LANGUAGE = "english"


class SumySummarizer(Summarizer):

    def summarize(self, paragraphs):
        """Summarize content with the sumy library"""

        content = "\n\n".join(paragraphs)

        stemmer = Stemmer(LANGUAGE)
        summarizer = LsaSummarizer(stemmer)

        tokenizer = Tokenizer(LANGUAGE)
        parser = PlaintextParser.from_string(content, tokenizer)

        sentences = []
        for sentence in summarizer(parser.document, "10%"):
            sentences.append([str(sentence)])
        return sentences

    def algorithm_name(self):
        return "LSA"
