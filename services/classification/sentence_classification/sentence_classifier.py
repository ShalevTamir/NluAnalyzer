import os

import spacy

from definitions import ROOT_DIR, DOCUMENTS_DIRECTORY_NAME
from models.enums.sentence_group import SentenceGroup
from services.classification.linear_classifier import LinearClassifier

RANGE_FILE_PATH = os.path.join(ROOT_DIR, DOCUMENTS_DIRECTORY_NAME,
                               "sentence_classification", "range_sentences.txt")
PARAMETER_FILE_PATH = os.path.join(ROOT_DIR, DOCUMENTS_DIRECTORY_NAME,
                                   "sentence_classification", "parameter_sentences.txt")


class SentenceClassifier(LinearClassifier):

    def __init__(self):
        self.model = spacy.load('en_core_web_sm')
        super().__init__(RANGE_FILE_PATH, PARAMETER_FILE_PATH, SentenceGroup.RANGE, SentenceGroup.PARAMETER)

    def _embed_item(self, sentence_to_embed) -> list[float]:
        return self.model(sentence_to_embed).vector

