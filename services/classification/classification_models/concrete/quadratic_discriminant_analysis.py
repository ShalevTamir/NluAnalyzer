from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis

from services.classification.classification_models.I_classification_model import IClassificationModel, GroupEnum


class QuadDiscAnalysis(IClassificationModel):

    def __init__(self,
                 embedded_group1: list[list[float]],
                 embedded_group2: list[list[float]],
                 group1_enum: GroupEnum,
                 group2_enum: GroupEnum):
        self.__group_enum_class = group1_enum.__class__
        concatenated_groups = embedded_group1 + embedded_group2
        group_ids = [group1_enum.value] * len(embedded_group1) + \
                    [group2_enum.value] * len(embedded_group2)

        self.__model = QuadraticDiscriminantAnalysis()
        self.__model.fit(concatenated_groups, group_ids)

    def predict(self, value: list[float]) -> GroupEnum:
        return self.__group_enum_class(self.__model.predict([value]))
