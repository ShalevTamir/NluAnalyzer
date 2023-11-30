import os
from gensim.models import KeyedVectors

import gensim.downloader as gensim_downloader

from flask_app.nlu_pkg.models.definitions.file_def import DOCUMENTS_DIRECTORY_NAME, ROOT_DIR
from flask_app.nlu_pkg.services.classification.word_embedding.word_embedder import WordEmbedder

EMBEDDING_MODEL_NAME = "word2vec-google-news-300"
EMBEDDING_MODEL_PATH = os.path.join(ROOT_DIR, DOCUMENTS_DIRECTORY_NAME, EMBEDDING_MODEL_NAME + ".kv")


class Word2VecEmbedder(WordEmbedder):
    def __init__(self):
        print("INITIALIZING WORD2VEC CLASS")
        if not os.path.isfile(EMBEDDING_MODEL_PATH) or not os.path.isfile(EMBEDDING_MODEL_PATH + ".vectors.npy"):
            print("LOADING EMBEDDING MODEL FROM WEB")
            embedding_model = gensim_downloader.load(EMBEDDING_MODEL_NAME)
            embedding_model.save(EMBEDDING_MODEL_PATH)
        print("LOADING EMBEDDING MODEL")
        self._word2vec_model = KeyedVectors.load(EMBEDDING_MODEL_PATH, mmap='r')

    def embed_item(self, item_to_embed: str) -> list[float]:
        return self._word2vec_model[item_to_embed]


