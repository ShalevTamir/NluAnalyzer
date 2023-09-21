from abc import ABC
from enum import Enum
from typing import Callable

from services.classification.classification_models.classification_model import ClassificationModel, GroupEnum
from services.classification.word_embedding.word_embedder import WordEmbedder


class LinearClassifier(ABC):
    def __init__(self,
                 word_embedding_model: WordEmbedder,
                 classification_model: ClassificationModel,
                 preprocessing_method: Callable[[str], str]):
        self._word_embedding_model = word_embedding_model
        self._classification_model = classification_model
        self.__preprocessing_method = preprocessing_method

    def classify_item(self, item_to_classify: str) -> GroupEnum:
        item_to_classify = self.__preprocessing_method(item_to_classify)
        word_vector = self._word_embedding_model.embed_item(item_to_classify)
        return self._classification_model.predict(word_vector)
