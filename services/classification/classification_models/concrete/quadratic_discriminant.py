from matplotlib import pyplot as plt
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
import numpy
from services.classification.classification_models.classification_model import ClassificationModel, GroupEnum


class QuadraticDiscriminant(ClassificationModel):
    def __init__(self, embedded_group1: list[list[float]],
                 embedded_group2: list[list[float]],
                 group1_enum: GroupEnum,
                 group2_enum: GroupEnum):

        self.__model = QuadraticDiscriminantAnalysis()
        super().__init__(embedded_group1, embedded_group2, group1_enum, group2_enum, self.__model.fit)

    def predict(self, value: list[float]) -> GroupEnum:
        return self._group_enum_class(self.__model.predict([value]))
