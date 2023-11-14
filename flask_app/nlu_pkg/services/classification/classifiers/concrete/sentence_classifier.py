import os

from flask_app.nlu_pkg.models.definitions.file_def import ROOT_DIR, DOCUMENTS_DIRECTORY_NAME
from flask_app.nlu_pkg.models.enums.sentence_group import SentenceGroup
from flask_app.nlu_pkg.services.classification.classification_models.concrete.quadratic_discriminant import \
    QuadraticDiscriminant
from flask_app.nlu_pkg.services.classification.classifiers.linear_classifier import LinearClassifier
from flask_app.nlu_pkg.services.classification.preprocessing.preprocessor import preprocess_sentence
from flask_app.nlu_pkg.services.classification.word_embedding.concrete.spacy_embedder import SpacyEmbedder
from flask_app.nlu_pkg.services.utils.file_parser import parse_file

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