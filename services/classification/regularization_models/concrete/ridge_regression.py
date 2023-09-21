from sklearn.linear_model import Ridge

from services.classification.regularization_models.I_regularization_model import IRegularizationModel


class RidgeRegression(IRegularizationModel):

    def __init__(self):
        self.__model = Ridge()

    def regularize(self, embedded_group1: list[list[float]], embedded_group2: list[float]):
        self.__model.fit(embedded_group1,embedded_group2)
