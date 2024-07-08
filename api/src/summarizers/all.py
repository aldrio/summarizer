from . import tf_idf
from . import sumy

SUMMARIZERS = {
    "tf_idf": tf_idf.TfIdfSummarizer(),
    "lsa": sumy.SumySummarizer(),
}
