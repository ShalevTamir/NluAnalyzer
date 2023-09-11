import os
from typing import List

from definitions import ROOT_DIR, DOCUMENTS_DIRECTORY_NAME
from services.classification.linear_classifier import LinearClassifier
from services.classification.models.logistic_regression import LogisticRegression
from services.utils.file_parser import parse_file
from gensim.models import KeyedVectors
from models.enums.adjective_group import AdjectiveGroup
import gensim.downloader as GensimDownloader

DECREASED_FILE_PATH = os.path.join(ROOT_DIR, DOCUMENTS_DIRECTORY_NAME, "comparative_adjectives",
                                   "decreased.txt")
INCREASED_FILE_PATH = os.path.join(ROOT_DIR, DOCUMENTS_DIRECTORY_NAME, "comparative_adjectives",
                                   "increased.txt")
EMBEDDING_MODEL_NAME = "word2vec-google-news-300"
EMBEDDING_MODEL_PATH = os.path.join(ROOT_DIR, DOCUMENTS_DIRECTORY_NAME, EMBEDDING_MODEL_NAME + ".kv")


class AdjectiveClassifier(LinearClassifier):

    def __init__(self):
        self.__word_embedding_model = self.__retrieve_embedding_model()
        super().__init__(DECREASED_FILE_PATH, INCREASED_FILE_PATH, AdjectiveGroup.DECREASED, AdjectiveGroup.INCREASED)

    def _embed_item(self, adjective_to_embed) -> list[float]:
        return self.__word_embedding_model[adjective_to_embed]

    def __retrieve_embedding_model(self):
        if not os.path.isfile(EMBEDDING_MODEL_PATH) or not os.path.isfile(EMBEDDING_MODEL_PATH + ".vectors.npy"):
            embedding_model = GensimDownloader.load(EMBEDDING_MODEL_NAME)
            embedding_model.save(EMBEDDING_MODEL_NAME)
        return KeyedVectors.load(EMBEDDING_MODEL_PATH, mmap='r')

