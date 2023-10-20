import os

from definitions import ROOT_DIR, DOCUMENTS_DIRECTORY_NAME
from models.enums.sentence_group import SentenceGroup
from services.classification.classification_models.concrete.logistic_regression import LogisticRegression
from services.classification.classifiers.linear_classifier import LinearClassifier
from services.classification.preprocessing.preprocessor import preprocess_sentence
from services.classification.relational_handler import RelationalHandler
from services.classification.word_embedding.concrete.spacy_embedder import SpacyEmbedder
from services.utils.file_parser import parse_file

_RANGE_FILE_PATH = os.path.join(ROOT_DIR, DOCUMENTS_DIRECTORY_NAME,
                                "sentence_classification", "range_sentences.txt")
_PARAMETER_FILE_PATH = os.path.join(ROOT_DIR, DOCUMENTS_DIRECTORY_NAME,
                                    "sentence_classification", "single_parameter_sentences.txt")


class SentenceClassifier(LinearClassifier):
    def __init__(self, spacy_embedder: SpacyEmbedder, relational_handler: RelationalHandler):
        range_sentences = [preprocess_sentence(sentence) for sentence in parse_file(_RANGE_FILE_PATH)]
        parameter_sentences = [preprocess_sentence(sentence) for sentence in parse_file(_PARAMETER_FILE_PATH)]
        super().__init__(spacy_embedder,
                         LogisticRegression(
                             spacy_embedder.embed_collection(range_sentences),
                             spacy_embedder.embed_collection(parameter_sentences),
                             SentenceGroup.RANGE,
                             SentenceGroup.PARAMETER),
                         preprocess_sentence)
        self._relational_handler = relational_handler

    def classify_item(self, item_to_classify: str) -> SentenceGroup:
        if list(self._relational_handler.extract_relational_bounds(item_to_classify)):
            return SentenceGroup.RANGE
        return super().classify_item(item_to_classify)
