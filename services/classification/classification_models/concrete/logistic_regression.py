from enum import Enum
from typing import TypeVar

from sklearn.linear_model import LogisticRegression as LogisticRegressionModel

from models.enums.adjective_group import AdjectiveGroup
from models.enums.sentence_group import SentenceGroup
from services.classification.classification_models.I_classification_model import IClassificationModel, GroupEnum


class LogisticRegression(IClassificationModel[GroupEnum]):

    def __init__(self,
                 embedded_group1: list[list[float]],
                 embedded_group2: list[list[float]],
                 group1_enum: GroupEnum,
                 group2_enum: GroupEnum):
        self.group_enum_class = group1_enum.__class__
        concatenated_groups = embedded_group1 + embedded_group2
        group_ids = [group1_enum.value] * len(embedded_group1) + \
                    [group2_enum.value] * len(embedded_group2)

        self._model = LogisticRegressionModel(solver='liblinear', random_state=0).fit(concatenated_groups, group_ids)

    def predict(self, value: list[float]) -> GroupEnum:
        return self.group_enum_class(self._model.predict([value]))


