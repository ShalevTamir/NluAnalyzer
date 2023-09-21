from abc import ABC, abstractmethod
from enum import Enum
from typing import TypeVar, Generic, Callable
import numpy
from matplotlib import pyplot as plt
from sklearn.decomposition import PCA

from services.classification.regularization_models.I_regularization_model import IRegularizationModel

GroupEnum = TypeVar("GroupEnum", bound=Enum)


class ClassificationModel(ABC, Generic[GroupEnum]):
    def __init__(self,
                 embedded_group1: list[list[float]],
                 embedded_group2: list[list[float]],
                 group1_enum: GroupEnum,
                 group2_enum: GroupEnum,
                 train_method: Callable[[list[list[float]], list[any]], any]):
        self._group_enum_class = group1_enum.__class__
        concatenated_groups = embedded_group1 + embedded_group2
        group_ids = [group1_enum.value] * len(embedded_group1) + \
                    [group2_enum.value] * len(embedded_group2)

        train_method(concatenated_groups, group_ids)

    @abstractmethod
    def predict(self, value: list[float]) -> GroupEnum:
        pass
