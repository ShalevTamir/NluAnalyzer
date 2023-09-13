import os
from enum import Enum

from definitions import ROOT_DIR, DOCUMENTS_DIRECTORY_NAME
from models.enums.adjective_group import AdjectiveGroup
from services.classification.classification_models.I_classification_model import GroupEnum
from services.classification.word_embedding.concrete.word2vec_embedder import Word2VecEmbedder
from services.classification.classifiers.linear_classifier import LinearClassifier
from services.classification.classification_models.concrete.logistic_regression import LogisticRegression
from services.utils.file_parser import parse_file

DECREASED_FILE_PATH = os.path.join(ROOT_DIR, DOCUMENTS_DIRECTORY_NAME, "comparative_adjectives",
                                   "decreased.txt")
INCREASED_FILE_PATH = os.path.join(ROOT_DIR, DOCUMENTS_DIRECTORY_NAME, "comparative_adjectives",
                                   "increased.txt")


class AdjectiveClassifier(LinearClassifier):

    def __init__(self, word2vec_embedder: Word2VecEmbedder):
        decreased_group = parse_file(DECREASED_FILE_PATH)
        increased_group = parse_file(INCREASED_FILE_PATH)
        super().__init__(LogisticRegression(
                            word2vec_embedder.embed_collection(decreased_group),
                            word2vec_embedder.embed_collection(increased_group),
                            AdjectiveGroup.DECREASED,
                            AdjectiveGroup.INCREASED),
                         word2vec_embedder)



