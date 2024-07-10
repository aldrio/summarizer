import nltk
from sentence_transformers import SentenceTransformer

nltk.download("punkt", download_dir="./data/nltk_data")
nltk.download("stopwords", download_dir="./data/nltk_data")

model = SentenceTransformer("paraphrase-albert-small-v2")
model.save("./data/models/sentence_transformer")
