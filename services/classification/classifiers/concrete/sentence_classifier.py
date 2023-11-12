import os

from models.definitions.file_def import ROOT_DIR, DOCUMENTS_DIRECTORY_NAME
from models.definitions.spacy_def import SPACY_MODEL
from models.enums.sentence_group import SentenceGroup
from services.classification.classification_models.concrete.logistic_regression import LogisticRegression
from services.classification.classification_models.concrete.quadratic_discriminant import QuadraticDiscriminant
from services.classification.classifiers.linear_classifier import LinearClassifier
from services.classification.preprocessing.preprocessor import preprocess_sentence
from services.classification.word_embedding.concrete.spacy_embedder import SpacyEmbedder
from services.utils.file_parser import parse_file

_RANGE_FILE_PATH = os.path.join(ROOT_DIR, DOCUMENTS_DIRECTORY_NAME,
                                "sentence_classification", "range_sentences.txt")
_PARAMETER_FILE_PATH = os.path.join(ROOT_DIR, DOCUMENTS_DIRECTORY_NAME,
                                    "sentence_classification", "single_parameter_sentences.txt")


class SentenceClassifier(LinearClassifier):
    def __init__(self, spacy_embedder: SpacyEmbedder):
        range_sentences = [preprocess_sentence(sentence) for sentence in parse_file(_RANGE_FILE_PATH)]
        parameter_sentences = [preprocess_sentence(sentence) for sentence in parse_file(_PARAMETER_FILE_PATH)]
        super().__init__(spacy_embedder,
                         QuadraticDiscriminant(
                             spacy_embedder.embed_collection(range_sentences),
                             spacy_embedder.embed_collection(parameter_sentences),
                             SentenceGroup.RANGE,
                             SentenceGroup.PARAMETER),
                         preprocess_sentence)

# classifier = SentenceClassifier(SpacyEmbedder())
# print(classifier.classify_item("maintain pressure at 35"))