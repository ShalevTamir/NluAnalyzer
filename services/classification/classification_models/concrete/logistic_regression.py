from enum import Enum
from typing import TypeVar

from sklearn.linear_model import LogisticRegression as LogisticRegressionModel

from models.enums.adjective_group import AdjectiveGroup
from models.enums.sentence_group import SentenceGroup
from services.classification.classification_models.classification_model import ClassificationModel, GroupEnum


class LogisticRegression(ClassificationModel[GroupEnum]):

    def __init__(self,
                 embedded_group1: list[list[float]],
                 embedded_group2: list[list[float]],
                 group1_enum: GroupEnum,
                 group2_enum: GroupEnum):
        self.__model = LogisticRegressionModel(solver='liblinear', random_state=0)
        super().__init__(embedded_group1, embedded_group2, group1_enum, group2_enum, self.__model.fit)

    def predict(self, value: list[float]) -> GroupEnum:
        return self._group_enum_class(self.__model.predict([value]))
