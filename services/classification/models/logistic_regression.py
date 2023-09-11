from sklearn.linear_model import LogisticRegression as LogisticRegressionModel
from models.interfaces.I_classification_model import IClassificationModel


class LogisticRegression(IClassificationModel):

    def __init__(self, words: list[list[float]], group_results: list[any]):
        self._model = LogisticRegressionModel(solver='liblinear', random_state=0).fit(words, group_results)

    def predict(self, value: list[float]):
        return self._model.predict([value])

