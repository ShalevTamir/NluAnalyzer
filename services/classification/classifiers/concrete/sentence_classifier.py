import os
from enum import Enum
from definitions import ROOT_DIR, DOCUMENTS_DIRECTORY_NAME
from models.enums.sentence_group import SentenceGroup
from services.classification.classification_models.I_classification_model import GroupEnum
from services.classification.classifiers.linear_classifier import LinearClassifier
from services.classification.classification_models.concrete.logistic_regression import LogisticRegression
from services.classification.word_embedding.concrete.spacy_embedder import SpacyEmbedder
from services.utils.file_parser import parse_file

RANGE_FILE_PATH = os.path.join(ROOT_DIR, DOCUMENTS_DIRECTORY_NAME,
                               "sentence_classification", "range_sentences.txt")
PARAMETER_FILE_PATH = os.path.join(ROOT_DIR, DOCUMENTS_DIRECTORY_NAME,
                                   "sentence_classification", "single_parameter_sentences.txt")


class SentenceClassifier(LinearClassifier):
    def __init__(self, spacy_embedder: SpacyEmbedder):
        range_sentences = parse_file(RANGE_FILE_PATH)
        parameter_sentences = parse_file(PARAMETER_FILE_PATH)
        super().__init__(LogisticRegression(
                            spacy_embedder.embed_collection(range_sentences),
                            spacy_embedder.embed_collection(parameter_sentences),
                            SentenceGroup.RANGE,
                            SentenceGroup.PARAMETER),
                         spacy_embedder)


