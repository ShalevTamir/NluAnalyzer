from abc import abstractmethod, ABC
from enum import Enum
from typing import Generic, TypeVar

from services.classification.models.logistic_regression import LogisticRegression
from services.utils.file_parser import parse_file

GroupEnum = TypeVar("GroupEnum", bound=Enum)


class LinearClassifier(ABC):
    def __init__(self, group1_file_path: str, group2_file_path: str, group1_enum: GroupEnum, group2_enum: GroupEnum):
        self.__group_enum_class = group1_enum.__class__
        embedded_group1 = self.__embed_items(parse_file(group1_file_path))
        embedded_group2 = self.__embed_items(parse_file(group2_file_path))
        concatenated_groups = embedded_group1 + embedded_group2
        group_ids = [group1_enum.value] * len(embedded_group1) + \
                    [group2_enum.value] * len(embedded_group2)

        self._classification_model = LogisticRegression(concatenated_groups, group_ids)

    @abstractmethod
    def _embed_item(self, item_to_embed) -> list[float]:
        pass

    def __embed_items(self, items_to_embed) -> list[list[float]]:
        return [
            self._embed_item(item)
            for item in items_to_embed
            if self._embed_item(item) is not None
        ]

    def classify_item(self, item_to_classify: str) -> GroupEnum:
        word_vector = self._embed_item(item_to_classify)
        return self.__group_enum_class(self._classification_model.predict(word_vector))
