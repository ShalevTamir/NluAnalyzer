import os

from models.definitions.file_def import ROOT_DIR, DOCUMENTS_DIRECTORY_NAME
from models.enums.relation_group import RelationGroup
from services.classification.classification_models.concrete.logistic_regression import LogisticRegression
from services.classification.classifiers.linear_classifier import LinearClassifier
from services.classification.preprocessing.preprocessor import preprocess_token
from services.classification.word_embedding.concrete.word2vec_embedder import Word2VecEmbedder
from services.utils.file_parser import parse_file

DECREASED_FILE_PATH = os.path.join(ROOT_DIR, DOCUMENTS_DIRECTORY_NAME, "relational_words",
                                   "decreased.txt")
INCREASED_FILE_PATH = os.path.join(ROOT_DIR, DOCUMENTS_DIRECTORY_NAME, "relational_words",
                                   "increased.txt")


class RelationalWordsClassifier(LinearClassifier):
    def __init__(self, word2vec_embedder: Word2VecEmbedder):
        decreased_group = parse_file(DECREASED_FILE_PATH)
        increased_group = parse_file(INCREASED_FILE_PATH)
        super().__init__(word2vec_embedder,
                         LogisticRegression(
                             word2vec_embedder.embed_collection(decreased_group),
                             word2vec_embedder.embed_collection(increased_group),
                             RelationGroup.DECREASED,
                             RelationGroup.INCREASED),
                         preprocess_token)
