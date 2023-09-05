from sklearn.linear_model import LogisticRegression as LogisticRegressionModel
from typing import List
from Services.DiffrentiateAdjectives.Interfaces.IClassificationModel import IClassificationModel


class LogisticRegression(IClassificationModel):

    def __init__(self, words: List[List[float]], group_results: List[float]):
        self.model = LogisticRegressionModel(solver='liblinear', random_state=0).fit(words,group_results)

    def predict(self, value: float):
        return self.model.predict([value])
