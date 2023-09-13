from enum import Enum
from typing import TypeVar

from sklearn.linear_model import LogisticRegression as LogisticRegressionModel
from services.classification.interfaces.I_classification_model import IClassificationModel

GroupEnum = TypeVar("GroupEnum",bound=type(Enum))


class LogisticRegression(IClassificationModel[GroupEnum]):

    def __init__(self,
                 embedded_group1: list[list[float]],
                 embedded_group2: list[list[float]],
                 group1_enum: GroupEnum,
                 group2_enum: GroupEnum):
        concatenated_groups = embedded_group1 + embedded_group2
        group_ids = [group1_enum.value] * len(embedded_group1) + \
                    [group2_enum.value] * len(embedded_group2)

        self._model = LogisticRegressionModel(solver='liblinear', random_state=0).fit(concatenated_groups, group_ids)

    def predict(self, value: list[float]) -> GroupEnum:
        return GroupEnum(self._model.predict([value]))



