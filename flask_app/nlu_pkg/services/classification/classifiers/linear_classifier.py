from abc import ABC
from typing import Callable

from flask_app.nlu_pkg.services.classification.classification_models.classification_model import ClassificationModel, \
    GroupEnum
from flask_app.nlu_pkg.services.classification.word_embedding.word_embedder import WordEmbedder


class LinearClassifier(ABC):
    def __init__(self,
                 word_embedding_model: WordEmbedder,
                 classification_model: ClassificationModel,
                 preprocessing_method: Callable[[any], str] = None):
        self._word_embedding_model = word_embedding_model
        self._classification_model = classification_model
        self._preprocessing_method = preprocessing_method

    def classify_item(self, item_to_classify: any) -> GroupEnum:
        if self._preprocessing_method:
            item_to_classify: str = self._preprocessing_method(item_to_classify)
        word_vector = self._word_embedding_model.embed_item(item_to_classify)
        return self._classification_model.predict(word_vector)
