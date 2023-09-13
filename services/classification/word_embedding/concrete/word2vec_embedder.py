import os

from gensim.models import KeyedVectors

from definitions import ROOT_DIR, DOCUMENTS_DIRECTORY_NAME
from services.classification.interfaces.I_word_embedder import IWordEmbedder
import gensim.downloader as GensimDownloader

EMBEDDING_MODEL_NAME = "word2vec-google-news-300"
EMBEDDING_MODEL_PATH = os.path.join(ROOT_DIR, DOCUMENTS_DIRECTORY_NAME, EMBEDDING_MODEL_NAME + ".kv")


class Word2VecEmbedder(IWordEmbedder):
    def __init__(self):
        if not os.path.isfile(EMBEDDING_MODEL_PATH) or not os.path.isfile(EMBEDDING_MODEL_PATH + ".vectors.npy"):
            embedding_model = GensimDownloader.load(EMBEDDING_MODEL_NAME)
            embedding_model.save(EMBEDDING_MODEL_NAME)
        self.word2vec_model = KeyedVectors.load(EMBEDDING_MODEL_PATH, mmap='r')

    def embedder_contains(self, item: str) -> bool:
        return item in self.word2vec_model

    def embed_item(self, item_to_embed: str) -> list[float]:
        return self.word2vec_model[item_to_embed]
