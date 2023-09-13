import os
from typing import List

from definitions import ROOT_DIR, DOCUMENTS_DIRECTORY_NAME
from services.classification.comparative_adjectives_classification.word2vec_embedder import Word2VecEmbedder
from services.classification.linear_classifier import LinearClassifier
from gensim.models import KeyedVectors
from models.enums.adjective_group import AdjectiveGroup
from services.classification.models.logistic_regression import LogisticRegression

DECREASED_FILE_PATH = os.path.join(ROOT_DIR, DOCUMENTS_DIRECTORY_NAME, "comparative_adjectives",
                                   "decreased.txt")
INCREASED_FILE_PATH = os.path.join(ROOT_DIR, DOCUMENTS_DIRECTORY_NAME, "comparative_adjectives",
                                   "increased.txt")


class AdjectiveClassifier(LinearClassifier):

    def __init__(self, word2vec_embedder: Word2VecEmbedder):
        
        super().__init__(LogisticRegression(),word2vec_embedder)

    def _embed_item(self, adjective_to_embed) -> list[float]:
        return self.__word_embedding_model[adjective_to_embed]


