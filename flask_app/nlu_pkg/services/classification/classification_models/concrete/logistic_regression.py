from sklearn.linear_model import LogisticRegression as LogisticRegressionModel

from flask_app.nlu_pkg.services.classification.classification_models.classification_model import ClassificationModel, \
    GroupEnum


class LogisticRegression(ClassificationModel[GroupEnum]):

    def __init__(self,
                 embedded_group1: list[list[float]],
                 embedded_group2: list[list[float]],
                 group1_enum: GroupEnum,
                 group2_enum: GroupEnum):
        self._model = LogisticRegressionModel(solver='liblinear', random_state=0)
        super().__init__(embedded_group1,
                         embedded_group2,
                         group1_enum,
                         group2_enum,
                         self._model.fit,
                         self._model.predict)

