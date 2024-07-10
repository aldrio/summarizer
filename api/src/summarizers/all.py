from . import tf_idf
from . import sumy
from . import sentence_embeddings

SUMMARIZERS = {
    "tf_idf": tf_idf.TfIdfSummarizer(),
    "lsa": sumy.SumySummarizer(),
    "sentence_embeddings": sentence_embeddings.SentenceEmbeddingsSummarizer(),
}
