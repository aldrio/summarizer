import math
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from .summarizer import Summarizer

model = SentenceTransformer("./data/models/sentence_transformer")


class SentenceEmbeddingsSummarizer(Summarizer):

    def algorithm_name(self):
        return "Sentence Embeddings"

    def summarize(self, paragraphs):
        """Summarize content with sentence embeddings"""
        sentences = [sentence for paragraph in paragraphs for sentence in paragraph]

        embeddings = model.encode(sentences)
        content_embedding = embeddings.mean(axis=0)

        similarities = cosine_similarity([content_embedding], embeddings).flatten()

        reduction_ratio = 0.1
        target_sentence_count = min(25, math.ceil(len(sentences) * reduction_ratio))
        top_sentence_indices = similarities.argsort()[-target_sentence_count:][::-1]

        # reorganize back into paragraphs
        summarized_paragraphs = [[] for _ in paragraphs]
        for i in top_sentence_indices:
            sentence = sentences[i]

            pi = i
            for paragraph_index, ps in enumerate(paragraphs):
                assert pi >= 0
                if pi < len(ps):
                    summarized_paragraphs[paragraph_index].append(sentence)
                    break
                pi -= len(ps)

        return summarized_paragraphs
