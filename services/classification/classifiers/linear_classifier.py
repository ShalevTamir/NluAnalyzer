from abc import ABC
from enum import Enum

from services.classification.classification_models.classification_model import ClassificationModel, GroupEnum
from services.classification.word_embedding.word_embedder import WordEmbedder


class LinearClassifier(ABC):
    def __init__(self,
                 word_embedding_model: WordEmbedder,
                 classification_model: ClassificationModel):
        self._word_embedding_model = word_embedding_model
        self._classification_model = classification_model

    def classify_item(self, item_to_classify: str) -> GroupEnum:
        word_vector = self._word_embedding_model.embed_item(item_to_classify)

        return self._classification_model.predict(word_vector)
