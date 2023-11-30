from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis

from ..classification_model import ClassificationModel, GroupEnum


class QuadraticDiscriminant(ClassificationModel[GroupEnum]):
    def __init__(self, embedded_group1: list[list[float]],
                 embedded_group2: list[list[float]],
                 group1_enum: GroupEnum,
                 group2_enum: GroupEnum):

        self._model = QuadraticDiscriminantAnalysis()
        super().__init__(embedded_group1,
                         embedded_group2,
                         group1_enum,
                         group2_enum,
                         self._model.fit,
                         self._model.predict)
