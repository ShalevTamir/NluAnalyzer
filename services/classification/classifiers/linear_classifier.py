from abc import abstractmethod, ABC
from enum import Enum
from typing import Generic, TypeVar

from services.classification.interfaces.I_classification_model import IClassificationModel
from services.classification.interfaces.I_word_embedder import IWordEmbedder
from services.classification.models.logistic_regression import LogisticRegression
from services.utils.file_parser import parse_file


class LinearClassifier(ABC):
    def __init__(self, classification_model: IClassificationModel, word_embedding_model: IWordEmbedder):
        self._word_embedding_model = word_embedding_model
        self._classification_model = classification_model

    def classify_item(self, item_to_classify: str) -> Enum:
        word_vector = self._word_embedding_model.embed_item(item_to_classify)
        return self._classification_model.predict(word_vector)
