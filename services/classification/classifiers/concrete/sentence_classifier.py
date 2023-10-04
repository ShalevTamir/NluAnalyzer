import os
from definitions import ROOT_DIR, DOCUMENTS_DIRECTORY_NAME
from models.enums.sentence_group import SentenceGroup
from services.classification.adjective_handler import AdjectiveHandler
from services.classification.classification_models.classification_model import GroupEnum
from services.classification.classification_models.concrete.logistic_regression import LogisticRegression
from services.classification.classification_models.concrete.quadratic_discriminant import QuadraticDiscriminant
from services.classification.classifiers.linear_classifier import LinearClassifier
from services.classification.word_embedding.concrete.spacy_embedder import SpacyEmbedder
from services.utils.file_parser import parse_file
from services.classification.preprocessing.preprocessor import preprocess_sentence
from services.utils.nltk_utils import extract_word_pos_tags

RANGE_FILE_PATH = os.path.join(ROOT_DIR, DOCUMENTS_DIRECTORY_NAME,
                               "sentence_classification", "range_sentences.txt")
PARAMETER_FILE_PATH = os.path.join(ROOT_DIR, DOCUMENTS_DIRECTORY_NAME,
                                   "sentence_classification", "single_parameter_sentences.txt")


class SentenceClassifier(LinearClassifier):
    def __init__(self, spacy_embedder: SpacyEmbedder, adjective_handler: AdjectiveHandler):
        range_sentences = [preprocess_sentence(sentence) for sentence in parse_file(RANGE_FILE_PATH)]
        parameter_sentences = [preprocess_sentence(sentence) for sentence in parse_file(PARAMETER_FILE_PATH)]
        super().__init__(spacy_embedder,
                         LogisticRegression(
                             spacy_embedder.embed_collection(range_sentences),
                             spacy_embedder.embed_collection(parameter_sentences),
                             SentenceGroup.RANGE,
                             SentenceGroup.PARAMETER),
                         preprocess_sentence)
        self.__adjective_handler = adjective_handler

    def classify_item(self, item_to_classify: str) -> SentenceGroup:
        if self.__adjective_handler.extract_comparative_adjectives(extract_word_pos_tags(item_to_classify)):
            return SentenceGroup.RANGE
        return super().classify_item(item_to_classify)

