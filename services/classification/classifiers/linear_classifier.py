from abc import ABC
from enum import Enum

from services.classification.classification_models.I_classification_model import IClassificationModel
from services.classification.word_embedding.base_word_embedder import IWordEmbedder


class LinearClassifier(ABC):
    def __init__(self, classification_model: IClassificationModel, word_embedding_model: IWordEmbedder):
        self._word_embedding_model = word_embedding_model
        self._classification_model = classification_model

    def classify_item(self, item_to_classify: str) -> Enum:
        word_vector = self._word_embedding_model.embed_item(item_to_classify)
        return self._classification_model.predict(word_vector)
