import os

from gensim.models import KeyedVectors

from definitions import ROOT_DIR, DOCUMENTS_DIRECTORY_NAME
from services.classification.word_embedding.word_embedder import WordEmbedder
import gensim.downloader as GensimDownloader

EMBEDDING_MODEL_NAME = "word2vec-google-news-300"
EMBEDDING_MODEL_PATH = os.path.join(ROOT_DIR, DOCUMENTS_DIRECTORY_NAME, EMBEDDING_MODEL_NAME + ".kv")


class Word2VecEmbedder(WordEmbedder):
    def __init__(self):
        if not os.path.isfile(EMBEDDING_MODEL_PATH) or not os.path.isfile(EMBEDDING_MODEL_PATH + ".vectors.npy"):
            embedding_model = GensimDownloader.load(EMBEDDING_MODEL_NAME)
            embedding_model.save(EMBEDDING_MODEL_NAME)
        self.__word2vec_model = KeyedVectors.load(EMBEDDING_MODEL_PATH, mmap='r')

    def embedder_contains(self, item: str) -> bool:
        return item in self.__word2vec_model

    def embed_item(self, item_to_embed: str) -> list[float]:
        return self.__word2vec_model[item_to_embed]


